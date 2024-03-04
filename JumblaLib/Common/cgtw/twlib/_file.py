# coding: utf-8
import os
from ._lib import _lib
from ._compat import *
import ctlib
class _file:
    
    

    @staticmethod
    def create(a_fun, a_http_ip, a_token, a_db, a_module, a_module_type, a_link_id, a_version_id, a_path, a_is_upload_online=False, a_argv_dict={}):
        t_os=_lib.get_os()
        if not os.path.exists(a_path):
            raise Exception("_file.create, path not exist {}".format(repr(a_path)))
        
        if not os.path.isfile(a_path):
            raise Exception("_file.create, not a file {}".format(repr(a_path)))
        
        file_data_list=[{"path":a_path, "size":str(os.path.getsize(a_path)), "modify_time":_lib.get_modify_time(a_path)}]
                    
            
        t_sign_data_dict = {"db":a_db, "module":a_module,  "module_type":a_module_type, "link_id":a_link_id, "version_id":a_version_id,\
                            "file_data_array":file_data_list, "os": t_os, "meta_data_array":a_argv_dict}
        file_data_list=a_fun("file", "create", t_sign_data_dict)
        if not a_is_upload_online:
            return True
        else:
            sou_list=[a_path]
            online_path_list=[]
            file_log_dic={}
            for dic in file_data_list:
                if isinstance(dic, dict) and "path" in dic  and "online" in dic  and "id" in dic:
                    t_online=dic["online"]
                    file_log_dic[t_online]=dic["id"]
                    online_path_list.append(t_online)
            if len(sou_list) != len(online_path_list):
                raise Exception("_file.create, the number of sources and targets is inconsistent")
            
            from ._media_file import _media_file
            return _media_file.upload(a_fun, a_http_ip, a_token, a_db, sou_list, online_path_list, a_call_back=None, a_file_log_dict=file_log_dic)
         