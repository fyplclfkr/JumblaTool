# coding:utf-8

import os
import boto3
from botocore.client import Config
import types
from threading import Lock
from .utils import *
from .threadpool import ThreadPool


class S3Client(object):

    def __init__(self, accessKey, secretKey, endpoint, region, sessionToken=None, timeout=60, **kwargs):
        config = Config(connect_timeout=timeout, read_timeout=timeout)
        self._client = boto3.client(
            's3',
            region_name=region,
            aws_access_key_id=accessKey,
            aws_secret_access_key=secretKey,
            aws_session_token=sessionToken,
            endpoint_url=endpoint,
            config=config,
            **kwargs
        )
        self._threadPool = None
        self._stop = False
        self._lock = Lock()

    def __getattr__(self, name):
        if hasattr(self._client, name):
            method = getattr(self._client, name)
            if isinstance(method, types.MethodType):
                return method
        message = "'{}' object has no attribute '{}'".format(type(self).__name__, name)
        raise AttributeError(message)

    def stop(self):
        self._stop = True
        if self._threadPool:
            self._threadPool.stop()

    def upload_file(self, Bucket, Key, LocalFilePath, PartSize=10, MAXThread=5, Metadata={}, EnableMD5=False,
                    CallBack=None, **kwargs):
        """小于等于20MB的文件简单上传，大于20MB的文件使用分块上传

            :rtype: object
            :param Bucket(string): 存储桶名称.
            :param Key(string): 分块上传路径名.
            :param LocalFile(string): 本地文件路径名.
            :param PartSize(int): 分块的大小设置,单位为MB.
            :param MAXThread(int): 并发上传的最大线程数.
            :param MetaData(dict): 元数据.
            :param EnableMD5(dict): 是否打开MD5校验.
            :param CallBack(callable): 回调.
            :param kwargs(dict): 设置请求headers.
            :return(dict): 成功上传文件的元信息.

        """
        if not isinstance(CallBack, (types.MethodType, types.FunctionType)):
            CallBack = None
        file_size = os.path.getsize(LocalFilePath)
        if file_size < 1024 * 1024 * 20:
            with open(LocalFilePath, 'rb') as fp:
                if EnableMD5:
                    md5_str = get_content_md5(fp)
                    if md5_str:
                        kwargs['ContentMD5'] = md5_str
                result = self._client.put_object(Bucket=Bucket, Key=Key, Body=fp, Metadata=Metadata, **kwargs)
                if CallBack is not None:
                    CallBack(file_size, file_size, file_size)
                return result
        else:
            part_size = 1024 * 1024 * PartSize  # 默认按照1MB分块,最大支持10G的文件，超过10G的分块数固定为10000
            parts_num = file_size // part_size
            last_size = file_size % part_size

            if last_size != 0:
                parts_num += 1
            else:  # 如果刚好整除,最后一块的大小等于分块大小
                last_size = part_size
            if parts_num > 10000:
                parts_num = 10000
                part_size = file_size // parts_num
                last_size = file_size % parts_num
                last_size += part_size

            # 创建分块上传
            # 判断是否可以断点续传
            resumable_flag = False
            already_exist_parts = {}
            uploadid = self._get_resumable_uploadid(Bucket, Key)
            if uploadid is not None:
                # 校验服务端返回的每个块的信息是否和本地的每个块的信息相同,只有校验通过的情况下才可以进行断点续传
                resumable_flag = self._check_all_upload_parts(Bucket, Key, uploadid, LocalFilePath, parts_num,
                                                              part_size, last_size, already_exist_parts)
            # 如果不能断点续传,则创建一个新的分块上传
            if not resumable_flag:
                rt = self._client.create_multipart_upload(Bucket=Bucket, Key=Key, Metadata=Metadata, **kwargs)
                uploadid = rt['UploadId']

            self._file_size = file_size
            self._has_upload_size = 0  # 已经上传的大小
            # 计算已经上传的，already_exist_parts={1:"md5", 6:"md5"}
            exist_keys = already_exist_parts.keys()
            if len(exist_keys) > 0:
                # 判断最后一断是否已经上传了,有的话;已上传大小=其他段的个数*part_size+last_size
                if parts_num in exist_keys:
                    self._has_upload_size = last_size + (len(exist_keys) - 1) * part_size
                else:
                    # 没有的话;已上传大小=其他段的个数*part_size
                    self._has_upload_size = len(exist_keys) * part_size

            # 上传分块
            offset = 0  # 记录文件偏移量
            lst = list()  # 记录分块信息
            self._threadPool = ThreadPool(MAXThread)
            for i in range(1, parts_num + 1):
                if i == parts_num:  # 最后一块
                    self._threadPool.add_task(self._upload_part, Bucket, Key, LocalFilePath, offset, file_size - offset,
                                              i, uploadid, lst, resumable_flag, already_exist_parts, EnableMD5,
                                              Metadata, CallBack)
                else:
                    self._threadPool.add_task(self._upload_part, Bucket, Key, LocalFilePath, offset, part_size, i,
                                              uploadid, lst, resumable_flag, already_exist_parts, EnableMD5, Metadata,
                                              CallBack)
                    offset += part_size
            self._threadPool.start()
            self._threadPool.wait_completion()
            if self._stop:
                return True
            result = self._threadPool.get_result()
            self._threadPool = None
            if not result['success_all'] or len(lst) != parts_num:
                raise Exception('some upload_part fail after max_retry, please upload_file again')
            lst = sorted(lst, key=lambda x: x['PartNumber'])  # 按PartNumber升序排列

            # 完成分块上传
            rt = self._client.complete_multipart_upload(Bucket=Bucket, Key=Key, UploadId=uploadid,
                                                        MultipartUpload={'Parts': lst})
            return rt

    def _upload_part(self, bucket, key, local_path, offset, size, part_num, uploadid, md5_lst, resumable_flag,
                     already_exist_parts, enable_md5, meta_data, callback=None):
        """从本地文件中读取分块, 上传单个分块,将结果记录在md5——list中
        :param bucket(string): 存储桶名称.
        :param key(string): 分块上传路径名.
        :param local_path(string): 本地文件路径名.
        :param offset(int): 读取本地文件的分块偏移量.
        :param size(int): 读取本地文件的分块大小.
        :param part_num(int): 上传分块的序号.
        :param uploadid(string): 分块上传的uploadid.
        :param md5_lst(list): 保存上传成功分块的MD5和序号.
        :param resumable_flag(bool): 是否为断点续传.
        :param already_exist_parts(dict): 断点续传情况下,保存已经上传的块的序号和Etag.
        :param enable_md5(bool): 是否开启md5校验.
        :param callback(callable): 进度回调.
        :return: None.
        """
        # 如果是断点续传且该分块已经上传了则不用实际上传
        if resumable_flag and part_num in already_exist_parts:
            md5_lst.append({'PartNumber': part_num, 'ETag': already_exist_parts[part_num]})
        else:
            with open(local_path, 'rb') as fp:
                fp.seek(offset, 0)
                data = fp.read(size)
            kwargs = dict()
            if enable_md5:
                md5_str = get_content_md5(fp)
                if md5_str:
                    kwargs['ContentMD5'] = md5_str
            rt = self._client.upload_part(Bucket=bucket, Key=key, Body=data, PartNumber=part_num, UploadId=uploadid,
                                          **kwargs)
            md5_lst.append({'PartNumber': part_num, 'ETag': rt['ETag']})
            with self._lock:
                self._has_upload_size += size
                if callback is not None:
                    callback(self._has_upload_size, size, self._file_size)
        return None

    def _get_resumable_uploadid(self, bucket, key):
        """从服务端获取未完成的分块上传任务,获取断点续传的uploadid
        :param bucket(string): 存储桶名称.
        :param key(string): 分块上传路径名.
        :return(string): 断点续传的uploadid,如果不存在则返回None.
        """
        if key and key[0] == '/':
            key = key[1:]
        multipart_response = self._client.list_multipart_uploads(Bucket=bucket, Prefix=key)
        if 'Uploads' in multipart_response:
            # 取最后一个(最新的)uploadid
            index = len(multipart_response['Uploads']) - 1
            while index >= 0:
                if multipart_response['Uploads'][index]['Key'] == key:
                    return multipart_response['Uploads'][index]['UploadId']
                index -= 1
        return None

    def _check_single_upload_part(self, local_path, offset, local_part_size, remote_part_size, remote_etag):
        """从本地文件中读取分块, 校验本地分块和服务端的分块信息
        :param local_path(string): 本地文件路径名.
        :param offset(int): 读取本地文件的分块偏移量.
        :param local_part_size(int): 读取本地文件的分块大小.
        :param remote_part_size(int): 服务端的文件的分块大小.
        :param remote_etag(string): 服务端的文件Etag.
        :return(bool): 本地单个分块的信息是否和服务端的分块信息一致
        """
        if local_part_size != remote_part_size:
            return False
        with open(local_path, 'rb') as fp:
            fp.seek(offset, 0)
            local_etag = get_raw_md5(fp.read(local_part_size))
            if local_etag == remote_etag:
                return True
        return False

    def _check_all_upload_parts(self, bucket, key, uploadid, local_path, parts_num, part_size, last_size,
                                already_exist_parts):
        """获取所有已经上传的分块的信息,和本地的文件进行对比
        :param bucket(string): 存储桶名称.
        :param key(string): 分块上传路径名.
        :param uploadid(string): 分块上传的uploadid
        :param local_path(string): 本地文件的大小
        :param parts_num(int): 本地文件的分块数
        :param part_size(int): 本地文件的分块大小
        :param last_size(int): 本地文件的最后一块分块大小
        :param already_exist_parts(dict): 保存已经上传的分块的part_num和Etag
        :return(bool): 本地文件是否通过校验,True为可以进行断点续传,False为不能进行断点续传
        """
        parts_info = []
        part_number_marker = 0
        list_over_status = False
        while list_over_status is False:
            response = self._client.list_parts(
                Bucket=bucket,
                Key=key,
                UploadId=uploadid,
                PartNumberMarker=part_number_marker
            )
            # 已经存在的分块上传,有可能一个分块都没有上传,判断一下
            if 'Parts' in response:
                parts_info.extend(response['Parts'])
            if response['IsTruncated'] == False:
                list_over_status = True
            else:
                part_number_marker = int(response['NextPartNumberMarker'])
        for part in parts_info:
            part_num = int(part['PartNumber'])
            # 如果分块数量大于本地计算出的最大数量,校验失败
            if part_num > parts_num:
                return False
            offset = (part_num - 1) * part_size
            local_part_size = part_size
            if part_num == parts_num:
                local_part_size = last_size
            # 有任何一块没有通过校验，则校验失败
            if not self._check_single_upload_part(local_path, offset, local_part_size, int(part['Size']), part['ETag']):
                return False
            already_exist_parts[part_num] = part['ETag']
        return True
