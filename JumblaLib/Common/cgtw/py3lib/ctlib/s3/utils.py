# coding:utf-8

import base64
import hashlib
from six import text_type, binary_type

DEFAULT_CHUNK_SIZE = 1024 * 1024  # 计算MD5值时,文件单次读取的块大小为1MB


def to_str(s):
    """非字符串转换为字符串"""
    if isinstance(s, text_type) or isinstance(s, binary_type):
        return s
    return str(s)


def to_unicode(s):
    """将字符串转为unicode"""
    if isinstance(s, binary_type):
        try:
            return s.decode('utf-8')
        except UnicodeDecodeError as e:
            raise Exception('your bytes strings can not be decoded in utf8, utf8 support only!')
    return s


def to_bytes(s):
    """将字符串转为bytes"""
    if isinstance(s, text_type):
        try:
            return s.encode('utf-8')
        except UnicodeEncodeError as e:
            raise Exception('your unicode strings can not encoded in utf8, utf8 support only!')
    return s


def get_raw_md5(data):
    """计算md5 md5的输入必须为bytes"""
    data = to_bytes(data)
    m2 = hashlib.md5(data)
    etag = '"' + str(m2.hexdigest()) + '"'
    return etag


def get_md5(data):
    """计算 base64 md5 md5的输入必须为bytes"""
    data = to_bytes(data)
    m2 = hashlib.md5(data)
    MD5 = base64.standard_b64encode(m2.digest())
    return MD5


def get_content_md5(body):
    """计算任何输入流的md5值"""
    if isinstance(body, text_type) or isinstance(body, binary_type):
        return get_md5(body)
    elif hasattr(body, 'tell') and hasattr(body, 'seek') and hasattr(body, 'read'):
        file_position = body.tell()  # 记录文件当前位置
        # avoid OOM
        md5 = hashlib.md5()
        chunk = body.read(DEFAULT_CHUNK_SIZE)
        while chunk:
            md5.update(to_bytes(chunk))
            chunk = body.read(DEFAULT_CHUNK_SIZE)
        md5_str = base64.standard_b64encode(md5.digest())
        try:
            body.seek(file_position)  # 恢复初始的文件位置
        except Exception as e:
            raise Exception('seek unsupported to calculate md5!')
        return md5_str
    else:
        raise Exception('unsupported body type to calculate md5!')
