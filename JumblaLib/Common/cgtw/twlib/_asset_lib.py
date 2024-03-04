# coding: utf-8
import os, sys, json, subprocess,six
from ._lib import _lib
import types
from ._compat import *
import ctlib

class _asset_lib:
    
    @staticmethod
    def download_asset(a_fun, a_http_ip, a_token, a_lib_sign, a_online_asset_path, a_local_asset_path, a_call_back=None):
        t_operation_files = _asset_lib_file(a_http_ip, a_token)
        return t_operation_files.download_asset(a_fun, a_lib_sign, a_online_asset_path, a_local_asset_path, a_call_back)

    @staticmethod
    def upload_asset(a_fun, a_http_ip,  a_token, a_lib_sign, a_local_asset_path, a_online_asset_path, a_call_back=None):
        t_operation_files = _asset_lib_file(a_http_ip, a_token)
        return t_operation_files.upload_asset(a_fun, a_lib_sign, a_local_asset_path, a_online_asset_path, a_call_back)

    @staticmethod
    def download_file(a_fun, a_http_ip, a_token, a_lib_sign, a_online_path, a_local_path, a_call_back=None):
        t_operation_files = _asset_lib_file(a_http_ip, a_token)
        return t_operation_files.download_file(a_fun, a_lib_sign, a_online_path, a_local_path, a_call_back)

    @staticmethod
    def upload_file(a_fun, a_http_ip, a_token, a_lib_sign, a_local_path, a_online_asset_path, a_call_back=None, argv_dict={}):
        t_operation_files = _asset_lib_file(a_http_ip, a_token)
        
        return t_operation_files.upload_file(a_fun, a_lib_sign, a_local_path, a_online_asset_path, a_call_back, argv_dict)
    
    @staticmethod
    def set_cover(a_fun, a_http_ip, a_token, a_lib_sign, a_online_asset_path, a_media_path):
        t_operation_files = _asset_lib_file(a_http_ip, a_token)
        
        return t_operation_files.set_cover(a_fun, a_lib_sign, a_online_asset_path, a_media_path)
 
    #------------------------------私有-----------------------------------


class _asset_lib_file(object):
    m_total_size           = 0 #总大小
    m_already_perform_size = 0 #已执行大小
    m_current_name = '' #当前下载的文件名称
    def __init__(self, a_http_ip, a_token):
        super(_asset_lib_file, self).__init__()


        self.m_ct_file = ctlib.file()
        self.m_ct_mov  = ctlib.mov()
        self.m_http    = ctlib.asset_lib_http(a_http_ip, a_token)        
        self.m_os      = _lib.get_os()
    
    def download_asset(self, a_fun, a_lib_sign, a_online_asset_path, a_local_asset_path, a_call_back):
        self.m_call_back = a_call_back
        a_online_asset_path = to_unicode(a_online_asset_path).replace("\\", "/")
        a_online_asset_path="/"+a_online_asset_path.strip("/")
        a_local_asset_path = to_unicode(a_local_asset_path).replace("\\", "/")
        a_local_asset_path=a_local_asset_path.strip("/")
        
        #获取资产包的ID
        folder_id = a_fun('asset_lib', 'get_folder_id', {"lib_sign":a_lib_sign, 'path':a_online_asset_path})
        if folder_id=="null":
            raise Exception("_asset_lib.download_asset, online dir not exist")
        
        #设置下载次数
        a_fun('asset_lib', 'set_download_num', {"lib_sign":a_lib_sign, "folder_id_array":[folder_id]})
        
        #获取资产包下的所有数据
        t_local_path_list=[]
        t_online_data_list=[]
        t_temp_online_data_list = a_fun('asset_lib', 'bulk_download', {"lib_sign":a_lib_sign, 'current_folder_id':"", "folder_id_array":[folder_id]})
        
        for dic in t_temp_online_data_list:
            t_online_data_list.append({"id":dic["id"], "path":dic["path"], "size":dic["file_size"]})
            temp_path=dic["path"]
            t_child_path=to_unicode(temp_path).replace(a_online_asset_path+"/", "/")
            t_local_path_list.append(a_local_asset_path+t_child_path)
            
        return self.__download(a_fun, a_lib_sign, t_online_data_list, t_local_path_list, a_call_back)
    
    
    def upload_asset(self, a_fun, a_lib_sign, a_local_asset_path, a_online_asset_path, a_call_back):
        self.m_call_back = a_call_back
        local_path_list=self.m_ct_file.get_path_list(a_local_asset_path, ['*'])
        return self.__upload(a_fun, a_lib_sign, a_online_asset_path, local_path_list, a_call_back)
    
    def download_file(self, a_fun, a_lib_sign, a_online_path, a_local_path, a_call_back):
        self.m_call_back = a_call_back
        if not isinstance(a_online_path, type(a_local_path)):
            raise Exception("_asset_lib.download_file, type mismatch")
        t_online_path_list=a_online_path
        t_local_path_list=a_local_path
        if not isinstance(t_online_path_list, list):
            t_online_path_list=[t_online_path_list]
        
        if not isinstance(t_local_path_list, list):
            t_local_path_list=[t_local_path_list]
                
        #--获取在线文件对应信息
        t_online_data_list = a_fun('asset_lib', 'get_online_file_path_array', {"lib_sign":a_lib_sign, 'path_array':t_online_path_list})  
        return self.__download(a_fun, a_lib_sign, t_online_data_list, t_local_path_list, a_call_back)
        
    
    def upload_file(self, a_fun, a_lib_sign, a_local_path, a_online_asset_path, a_call_back, argv_dict):
        self.m_call_back = a_call_back
        t_local_path_list=a_local_path
        if not isinstance(t_local_path_list, list):
            t_local_path_list=[t_local_path_list]
        return self.__upload(a_fun, a_lib_sign, a_online_asset_path, t_local_path_list, a_call_back, a_argv_dict=argv_dict)
    
    def set_cover(self, a_fun, a_lib_sign, a_online_asset_path, a_media_path):
        #设置资产封面
        if not os.path.exists(a_media_path):
            raise Exception("_asset_lib.set_cover, the media path not exist")
        
        suffix = os.path.splitext(a_media_path)[1]
        suffix = to_unicode(suffix).strip(".").lower()  
        img_suff_list=["jpg", "jpeg", "png", "exr", "tiff", "tif", "tga", "dpx", "psd", "bmp", "gif"]
        mov_suff_list=[
        "3g2", "3gp", "3gp2", "3gpp", "amv", "asf", "avi", "bik", "divx", "drc", "dv",
        "f4v", "flv", "gvi", "gxf", "iso", "m1v", "m2v", "m2t", "m2ts", "m4v", "mkv",
        "mov", "mp2", "mp2v", "mp4", "mp4v", "mpe", "mpeg", "mpeg1", "mpeg2", "mpeg4",
        "mpg", "mpv2", "mts", "mtv", "mxf", "mxg", "nsv", "nuv", "ogg", "ogm", "ogv",
        "ogx", "ps", "rec", "rm", "rmvb", "rpl", "thp", "tod", "ts", "tts", "txd",
        "vob", "vro", "webm", "wm", "wmv", "wtv", "xesc"
    	]
        
        if suffix in img_suff_list:
            is_image=True
        elif suffix in mov_suff_list:
            is_image=False
        else:
            raise Exception("_asset_lib.set_cover, the media no support convert")
        
        #获取资产包的id
        t_asset_id = a_fun("asset_lib", "create_asset_and_get_id", {"lib_sign":a_lib_sign, "asset_path":a_online_asset_path})   
        #本地直接转中图
        t_w="480"
        t_h="270"
        if is_image:
            t_img_path=self.m_ct_mov.image_to_image(a_media_path, a_width=t_w, a_height=t_h)
        else:
            #视频转gif
            t_img_path = os.path.join(_lib.get_tmp_path(), "{}.gif".format(_lib.uuid()))
            t_output_dir = os.path.dirname(t_img_path)
            if not os.path.exists(t_output_dir):
                os.makedirs(t_output_dir)    
            ffmpeg = to_unicode(self.m_ct_mov.get_ffmpeg_path())
            if not os.path.exists(ffmpeg):
                raise Exception("_asset_lib.set_cover, Could't find ffmpeg")
            t_cmd = u'"{}" -ss 0 -t 2 -i "{}" -vf scale={}:{} -y "{}"'.format(ffmpeg, to_unicode(a_media_path), t_w, t_h, t_img_path)
            if six.PY2:
                t_cmd = to_syscode(t_cmd)
            
            convert_ps = subprocess.Popen(t_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            convert_ps.wait()
        
        if not os.path.exists(t_img_path) or os.path.getsize(t_img_path)==0:
            raise Exception("_asset_lib.set_cover, the media convert failed")        
        
        t_sou_dict         = self.m_ct_file.get_chuck_md5(t_img_path)
        t_md5              = t_sou_dict["md5"]
        t_chuck            = t_sou_dict["chuck"]       
        t_session_id = t_md5
        try:
            md5_path = self.m_http.upload(t_session_id, t_img_path, a_lib_sign, os.path.basename(a_media_path), t_md5, t_chuck)
        except Exception as e:
            raise Exception("_asset_lib.set_cover, {}".format(e))
        a_fun("asset_lib", "set_cover", {"lib_sign":a_lib_sign, "asset_id":t_asset_id, "image_md5_path":md5_path})
        return True


    def __call_back(self, a, b, c):
        func = self.m_call_back
        if func != None and (isinstance(func, types.FunctionType) or isinstance(func, types.MethodType) ): 
            t_argcount =  func.__code__.co_argcount
            t_varnames =  func.__code__.co_varnames   
            t_args =  list(t_varnames)[0:t_argcount]
            if 'self' not in t_args:
                t_args.append('self')
            if len(t_args) == 5: 
                func(self.m_already_perform_size+a, b, self.m_total_size, self.m_current_name)
            elif len(t_args) == 4:
                func(self.m_already_perform_size+a, b, self.m_total_size)


    #---私有
    def __download_backup_path(self, a_des, a_time):
        #a_name有可能是文件夹名称/或者文件的名称
        #a_time: 2018-01-01-22-11-22
        t_time_no_char=to_unicode(a_time).replace("-", "") #a_time: 20180101221122
        base_name=os.path.basename(a_des)        
        lis=os.path.splitext(base_name)
        if len(lis)==2:
            backup_path=t_back_dir=os.path.dirname(a_des)+"/history/backup/"+lis[0]+"."+t_time_no_char+lis[1]
        else:
            backup_path=t_back_dir=os.path.dirname(a_des)+"/history/backup/"+base_name+"."+t_time_no_char

        return backup_path        
    
    def __download(self, a_fun, a_lib_sign, a_online_data_list, a_local_path_list, a_call_back):
        t_fail_list = []
        if len(a_online_data_list) != len(a_local_path_list): #获取在线文数量不正确 
            raise Exception("_asset_lib.download Incorrect number of online files obtained,"+json.dumps(a_online_data_list))
        
        #--计算所有将下载文件的总大小
        for _online_file_dict in a_online_data_list:
            if isinstance(_online_file_dict, dict) and 'size' in _online_file_dict:
                self.m_total_size += int(_online_file_dict['size'])
        
        #--循环下载
        for index in range(len(a_online_data_list)):
            t_online_data   = a_online_data_list[index]
            t_id = t_online_data['id']
            t_sou           = t_online_data['path']
            t_size          = t_online_data['size']
            t_des           = a_local_path_list[index]

            try:
                if t_des.strip() == "" or t_id.strip() == "":
                    t_fail_list.append(t_sou)
                    self.m_already_perform_size += int(t_size)  #计算当前已经下载的所有大小 --->(成功的时候添加)  
                    continue
                
                t_name = os.path.basename(t_des)
                if t_sou[0] != '/':
                    self.m_current_name = '/'+t_sou
                else:
                    self.m_current_name = t_sou

                t_download_backup_path = self.__download_backup_path(t_des, _lib.now('%Y-%m-%d-%H-%M-%S'))

                if not self.m_http.download(a_lib_sign, t_id, t_des, self.__call_back, t_download_backup_path):
                    t_fail_list.append(t_sou)
                else:    
                    self.m_already_perform_size += int(t_size)  #计算当前已经下载的所有大小 --->(成功的时候添加)  
                
            except Exception as e:
                t_fail_list.append(t_sou)

        if len(t_fail_list) > 0:
            raise Exception("_asset_lib.download download fail,"+json.dumps(t_fail_list))
            
        return True

    
    def __upload(self, a_fun, a_lib_sign, a_online_asset_path, a_local_path_list, a_call_back, a_metadata={}, a_argv_dict={}):
        a_online_asset_path = to_unicode(a_online_asset_path).replace("\\", "/")
        self.m_call_back = a_call_back
        t_fail_list = []
        
        t_online_child_file_list = a_argv_dict.get("online_child", []) #online_child(str/unicode/list)为资产包下的路径,和local_path对应, 如本地上传路径为z:/aa/bb/1.txt, aa为资产包, online_child=/bb/1.txt
        if t_online_child_file_list != []:
            if not isinstance(t_online_child_file_list, list):
                t_online_child_file_list = [t_online_child_file_list]
            if len(a_local_path_list) != len(t_online_child_file_list):
                raise Exception("_asset_lib.upload, the number of local_path and online_child does not match)")
                

        #--计算总文件大小
        t_new_sou_path_list = [] #新的原文件列表{'size':'','md5':'','modify_time':'','sou':''}     
        for index in range(len(a_local_path_list)):
            _file = a_local_path_list[index]
            _file = to_unicode(_file).replace("\\", "/").rstrip('/')#20220927
            if  _file.strip() == "" or not os.path.exists(_file):
                t_fail_list.append(_file)
                continue
            
            t_online_child_path=""
            if len(t_online_child_file_list)>0:
                t_online_child_path = t_online_child_file_list[index]
                t_online_child_path=to_unicode(t_online_child_path).replace("\\", "/").strip("/")
                
            if os.path.isdir(_file):
                for i in self.m_ct_file.get_file_with_walk_folder(_file):
                    i=to_unicode(i).replace("\\", "/")
                    t_file_size        = self.m_ct_file.get_size(i)
                    t_sou_dict         = self.m_ct_file.get_chuck_md5(i)
                    t_md5              = t_sou_dict["md5"]
                    t_chuck            = t_sou_dict["chuck"]
                    t_file_modify_time = self.m_ct_file.get_modify_time(i)
                    self.m_total_size  += t_file_size
                    
                    if t_online_child_path != "": #说明外部有传资产包下的子目录下
                        _file=to_unicode(_file).rstrip("/")
                        t_child_online_path = to_unicode(i).replace(_file+"/", t_online_child_path+"/")  
                        t_online_child="/"+ os.path.dirname(t_child_online_path).strip("/")
                    
                    else:
                        temp_dir=to_unicode(os.path.dirname(_file)).replace("\\", "/")#如z:/aa      
                        child_dir=to_unicode(os.path.dirname(i)).replace("\\", "/")#如z:/aa/dd/cc                        
                        t_online_child="/"+to_unicode(child_dir).replace(temp_dir, "/").strip("/")#得到/dd/cc                        
                    
                    t_new_sou_path_list.append({'size':t_file_size,'md5':t_md5, "chuck":t_chuck ,'modify_time':t_file_modify_time,'sou':i, "online_child":t_online_child})
        
            else:
                t_file_size        = self.m_ct_file.get_size(_file)
                t_sou_dict         = self.m_ct_file.get_chuck_md5(_file)
                t_md5              = t_sou_dict["md5"]
                t_chuck            = t_sou_dict["chuck"]
                t_file_modify_time = self.m_ct_file.get_modify_time(_file)
                self.m_total_size  += t_file_size
                
                t_online_child = ""
                if t_online_child_path != "": #说明外部有传资产包下的子目录下
                    t_online_child = to_unicode(os.path.dirname(t_online_child_path)).replace("\\", "/")
                    if t_online_child != "":
                        t_online_child="/"+to_unicode(t_online_child).strip("/")
                        
                t_new_sou_path_list.append({'size':t_file_size,'md5':t_md5, "chuck":t_chuck ,'modify_time':t_file_modify_time,'sou':_file, "online_child":t_online_child})

        
        #--存在不是文件 或不存在 或空的 直接返回
        if len(t_fail_list) > 0:
            raise Exception("asset_lib.upload There are not file or not exists,please check,"+json.dumps(t_fail_list))
        
        #资产库生成资产包的路径并返回ID
        t_asset_id = a_fun("asset_lib", "create_asset_and_get_id", {"lib_sign":a_lib_sign, "asset_path":a_online_asset_path})
        
        child_dic={}
        for t_sou_data in t_new_sou_path_list:
            t_sou               = t_sou_data['sou']
            t_file_modify_time  = t_sou_data['modify_time']
            t_md5               = t_sou_data['md5']
            t_chuck             = t_sou_data['chuck']
            t_file_size         = t_sou_data['size']
            t_online_child         = t_sou_data['online_child']
            t_file_name=os.path.basename(t_sou)
            try:
                if t_online_child=="":
                    t_folder_id=t_asset_id
                else:
                    if t_online_child in child_dic:
                        t_folder_id=child_dic[t_online_child]#之前有查过一次
                    else:
                        t_folder_id=a_fun("asset_lib", "create_child_and_get_id", {"lib_sign":a_lib_sign, "asset_id":t_asset_id, "child_path":t_online_child})
                        child_dic[t_online_child]=t_folder_id
    
                exist_file_res = a_fun("asset_lib", "exist_file", {"lib_sign":a_lib_sign, "entity": t_file_name, "folder_id": t_folder_id, "md5": t_md5})
                exist_file_dic = dict(exist_file_res)

                if "md5_path" not in exist_file_dic and "is_exist_data" not in exist_file_dic and 'id' not in exist_file_dic:
                    t_fail_list.append(t_sou)
                    continue
                
                asset_lib_file_id         = exist_file_dic['id'].strip()
                is_exist_data   = to_unicode(exist_file_dic["is_exist_data"]).strip().lower()  # 数据库是否存在数据
                server_md5_path = to_unicode(exist_file_dic["md5_path"]).strip()
                new_server_md5_path = server_md5_path
                if server_md5_path == "":  # 服务器不存在这个文件
                    t_session_id = t_md5
                    new_server_md5_path = self.m_http.upload(t_session_id, t_sou, a_lib_sign, t_file_name, t_md5, t_chuck, self.__call_back)
                else:
                    self.__call_back(t_file_size,t_file_size,0)
                self.m_already_perform_size += t_file_size  #计入已下载大小
                # 文件已经在服务器上。这个时候则需要插入数据
                if is_exist_data != "y" or server_md5_path == "" or asset_lib_file_id == "":  # 不存在数据
                    #is_convert_format=self.m_ct_mov.is_convert_format(t_sou)
                    upload_res = a_fun("asset_lib", "upload", {
                                                                      "lib_sign":a_lib_sign, 
                                                                      "md5": t_md5,
                                                                      "md5_path": new_server_md5_path,
                                                                      "entity": t_file_name,
                                                                      "folder_id": t_folder_id,                  
                                                                      "modify_time": t_file_modify_time,                                                                      
                                                                      "size": to_unicode(t_file_size),
                                                                      "meta_data_array": a_metadata
                                                                      })
                else:
                    if asset_lib_file_id != "" and a_metadata != {}:
                        a_fun('asset_lib', 'set_metadata', {"lib_sign":a_lib_sign, 'id':asset_lib_file_id, 'meta_data_array':a_metadata})
 
                    update_modify_time_res = a_fun("asset_lib", "update_file_modify_time", {"lib_sign":a_lib_sign, "entity": t_file_name, "folder_id": t_folder_id, "md5": t_md5, "file_modify_time": t_file_modify_time})
    
            except Exception as e:
                t_fail_list.append(t_sou)
    
        if len(t_fail_list) > 0:
            raise Exception("_asset_lib.upload upload fail,"+json.dumps(t_fail_list))
    
        return True      