# coding: utf-8
import os, sys, six
from ._lib import _lib
from ._dom import _dom
from ._compat import *
import ctlib
class _module_e:
    
    _class="etask"
    _module_type="task"
    
                
    @staticmethod
    def get(a_fun, a_db, a_id_list, a_field_sign_list, a_limit="5000", a_order_sign_list=[]):
        return a_fun(_module_e._class, "get", {"db":a_db, "sign_array":a_field_sign_list, "id_array":a_id_list, "order_sign_array":a_order_sign_list, "limit":a_limit})
               
    @staticmethod
    def set(a_fun, a_db, a_id_list, a_sign_data_dict, a_exec_event_filter=True):
        return a_fun(_module_e._class, "set", {"db":a_db, "id_array":a_id_list, "sign_data_array":a_sign_data_dict, "exec_event_filter":a_exec_event_filter})
    
    @staticmethod
    def download_image(a_fun, a_http_ip, a_token, a_db, a_id_list, a_field_sign, a_is_small=True, a_local_dir=""):
       
        t_localpath=a_local_dir
        if t_localpath.strip()=="":
            t_localpath=_lib.get_tmp_path()
        if not os.path.exists(t_localpath):
            try:
                os.mkdir(t_localpath)
            except Exception as e:
                raise Exception(e)

        t_data_list=_module_e.get(a_fun, a_db, a_id_list, [a_field_sign])
        t_image_data=[]
        t_size="max"
        if a_is_small==True:
            t_size="min"
        t_http=ctlib.http(a_http_ip, a_token)
        for data in t_data_list:
            if not isinstance(data, dict) or a_field_sign not in data or to_unicode(data[a_field_sign]).strip() == '':
                continue
            t_download_list = []
            t_image_json=_lib.decode(data[a_field_sign])
            if not isinstance(t_image_json, list) or t_image_json == []:
                continue
            for _image in t_image_json:
                if not isinstance(_image, dict) or 'type' not in _image or _image['type'] != 'image' :
                    continue
                t_image = _image[t_size]
                #t_local_file=t_localpath+t_image
                t_local_file=to_unicode(t_localpath).rstrip("/").rstrip("\\")+"/"+os.path.basename(t_image)
                t_result=t_http.download(t_image, t_local_file)
                if t_result==False:
                    t_local_file=""
                t_download_list.append(t_local_file)
            t_image_data.append({"id":data["id"], a_field_sign:t_download_list})#.mp4
        return t_image_data    
    
    @staticmethod
    def set_image(a_fun, a_http_ip, a_token, a_db, a_id_list, a_field_sign, a_img_path, a_compress="1080", a_exec_event_filter=True):
        a_img_path_list = []
        if isinstance(a_img_path, basestring):
            if a_img_path.strip()=="":
                #清空
                return _module_e.set(a_fun, a_db, a_id_list, {a_field_sign:""}, a_exec_event_filter)
            a_img_path_list.append(a_img_path)
        else:
            a_img_path_list = a_img_path
            
        if not isinstance(a_img_path_list, (list)):
            raise Exception("_module.set_image argv error , a_img_path type in (list/str/unicode)")

        t_list = []
        t_http=ctlib.http(a_http_ip, a_token)

        for t_image_file in a_img_path_list:
            res=t_http.upload_project_img(t_image_file, a_db, {"type":"main"})
            if "max" in res and "min" in res or 'att_id' not in res:
                t_list.append({"min":res["min"], "max":res["max"], "type":"image",'att_id':res['att_id']})
        return _module_e.set(a_fun, a_db, a_id_list, {a_field_sign:t_list }, a_exec_event_filter)
    
        
    @staticmethod
    def get_makedirs(a_fun, a_db, a_id_list):
        if to_unicode(a_db).lower().strip()=="public":
            raise Exception("_module_e.get_makedirs , can not use to public database")
        
        if len(a_id_list)==0:
            return False
        
        t_os=_lib.get_os()
        #怕选择的要创建的目录太多的时候。进行分ID取数据
        t_page_num=100#每次的条数
        t_num= int(len(a_id_list)/t_page_num) #循环的次数
        t_module_num=len(a_id_list)%t_page_num #取模
        if t_module_num>0:
            t_num=t_num+1
        
        t_all_data_lis=[]                    
        for i in range(t_num):
            temp_id_lis=a_id_list[i*t_page_num: (i+1)*t_page_num]
            t_os=_lib.get_os()
            res=a_fun(_module_e._class, "get_makedirs", {"db":a_db, "id_array":temp_id_lis, "os":t_os})
            t_all_data_lis=t_all_data_lis+res
                
        return t_all_data_lis    
    
        
    @staticmethod
    def submit(a_fun, a_http_ip, a_token, a_db, a_id, a_filebox_sign, a_path_list, a_note=[],  a_version="", a_version_argv={}, a_note_argv={}, a_callback=None,a_argv_dict={}):

        if to_unicode(a_id).strip()=="":
            raise Exception("_module_e.submit id is empty")
        
        if len(a_path_list)==0:
            raise Exception("_module_e.submit path_list is empty")
        
        from ._publish import _publish
        t_publish=_publish(a_fun, a_http_ip, a_token, a_db, _module_e._class, _module_e._module_type, a_id, a_path_list, a_filebox_sign, a_version, a_version_argv, a_note, a_note_argv, a_callback=a_callback,a_argv_dict=a_argv_dict)
        return t_publish._exec()        

        
    
    @staticmethod
    def update_flow(a_fun, a_http_ip, a_token, a_db, a_id, a_field_sign, a_status, a_note=[], a_image_list=[], a_retake_pipeline_id_list=[], a_argv_dict={}):
        for _id in a_id:
            if to_unicode(_id).strip()=="":
                return False    

        t_dom_list=a_note
        if len(a_image_list)!=0:
            
            t_http=ctlib.http(a_http_ip, a_token)
                                          
            for t_image_file in a_image_list:
                res=t_http.upload_project_img(t_image_file, a_db, {"type":"note"})
                if "max" in res and "min" in res and 'att_id' in res:
                    t_dom_list.append({"type":"image", "min":res["min"], "max":res["max"],'att_id':res['att_id']})
        
        return  a_fun(_module_e._class, "update_flow", {"db":a_db, "field_sign":a_field_sign, "dom_array":t_dom_list, "status":a_status, "task_id_array":a_id, "retake_pipeline_id_array":a_retake_pipeline_id_list, "tag":a_argv_dict.get("tag", "")})
    
    @staticmethod
    def update_task_status(a_fun, a_http_ip, a_token, a_db, a_id_list, a_status, a_note=[], a_image_list=[], a_retake_pipeline_id_list=[]):
        if len(a_id_list)==0:
            return False   
        
        t_dom_list=a_note
        if len(a_image_list)!=0:
            t_http=ctlib.http(a_http_ip, a_token)                       
            for t_image_file in a_image_list:
                res=t_http.upload_project_img(t_image_file, a_db, {"type":"note"})
                if "max" in res and "min" in res and 'att_id' in res:
                    t_dom_list.append({"type":"image", "min":res["min"], "max":res["max"],'att_id':res['att_id']})
        
        return  a_fun(_module_e._class, "update_task_status", {"db":a_db,"dom_array":t_dom_list, "status":a_status, "task_id_array":a_id_list, "retake_pipeline_id_array":a_retake_pipeline_id_list})   
    
    @staticmethod
    def set_media(a_fun, a_http_ip, a_token, a_db, a_id_list, a_field_sign, a_data_list, a_exec_event_filter=True):
        #-清空
        if a_data_list == []:
            return _module_e.set(a_fun, a_db, a_id_list, {a_field_sign:""}, a_exec_event_filter)
        
        a_data_list = _dom.convert(a_data_list)
        a_data_list = _dom.to_list(a_http_ip, a_token, a_db, a_data_list, 'main')
        return _module_e.set(a_fun, a_db, a_id_list, {a_field_sign:a_data_list }, a_exec_event_filter)
    
    @staticmethod
    def download_media(a_fun, a_http_ip, a_token, a_db, a_id_list, a_field_sign, a_local_dir=''):   

        t_localpath=a_local_dir
        if t_localpath.strip()=="":
            t_localpath=_lib.get_tmp_path()
        if not os.path.exists(t_localpath):
            try:
                os.mkdir(t_localpath)
            except Exception as e:
                raise Exception(e)
                        
        t_data_list=_module_e.get(a_fun, a_db, a_id_list, [a_field_sign])
   
        t_http=ctlib.http(a_http_ip, a_token)
        
        t_download_data = []
        for data in t_data_list:
            t_download_list = []
            if not isinstance(data, dict) or to_unicode(data[a_field_sign]).strip() == "":
                continue
            
            t_file_list = _lib.decode(data[a_field_sign])

            if not isinstance(t_file_list, list) or t_file_list == []:
                continue
            for _dict in t_file_list:
                if not isinstance(_dict, dict) or 'type' not in _dict:
                    continue
                t_type = _dict['type']
                
                if t_type == 'image':
                    t_path = _dict['max']
                elif t_type == 'video':
                    t_path = _dict['video']
                else:#audio  attachment
                    t_path = _dict['content']
                
                #t_local_file=t_localpath+t_path
                t_local_file=to_unicode(t_localpath).rstrip("/").rstrip("\\")+"/"+os.path.basename(t_path)
                t_result=t_http.download(t_path, t_local_file)
                if t_result==False:
                    t_local_file=""
                t_download_list.append(t_local_file)
                
            t_download_data.append({"id":data["id"], a_field_sign:t_download_list})
        return t_download_data    
    #------------------------------------------------------------------------
    @staticmethod
    def publish(a_fun, a_http_ip, a_token, a_db, a_id, a_path_list, a_filebox_sign, a_version="", a_version_argv={}, a_note_list=[], a_note_argv={}, a_callback=None, a_argv_dict={}):
        from ._publish import _publish
        t_publish=_publish(a_fun, a_http_ip, a_token, a_db, _module_e._class, _module_e._module_type, a_id, a_path_list, a_filebox_sign, a_version, a_version_argv, a_note_list, a_note_argv,a_callback,a_argv_dict)
        return t_publish._exec()
        
    


   
