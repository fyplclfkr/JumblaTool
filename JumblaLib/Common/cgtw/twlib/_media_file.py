# coding: utf-8
import os, sys, json
from ._lib import _lib
import types
from ._compat import *
import ctlib

class _media_file:
    @staticmethod    
    def download_filebox(a_fun, a_http_ip, a_token, a_db, a_module, a_module_type, a_task_id, a_filebox_id, a_is_download_all, a_is_show_exist, a_des_dir="", a_call_back=None, a_argv_dict={}): #--20190122 a_des_dir
        t_operation_files = operation_files(a_http_ip, a_token)
        return t_operation_files.download_filebox(a_fun, a_db, a_module, a_module_type, a_task_id, a_filebox_id, a_is_download_all, a_is_show_exist, a_des_dir,  a_call_back, a_argv_dict)
    
    @staticmethod    
    def upload_filebox(a_fun, a_http_ip, a_token, a_db, a_module, a_module_type, a_task_id, a_filebox_id, a_sou_path_list, a_call_back=None, a_argv_dict={}):
        t_operation_files = operation_files(a_http_ip, a_token)
        return t_operation_files.upload_filebox(a_fun, a_db, a_module, a_module_type, a_task_id, a_filebox_id, a_sou_path_list, a_call_back, a_argv_dict)
    
    @staticmethod
    def download(a_fun, a_http_ip, a_token, a_db, a_online_path_list, a_des_path_list, a_call_back=None, backup_dir=""):
        if len(a_online_path_list) != len(a_des_path_list):
            raise Exception("media_file.download, the number of source and destination paths does not match")  # --20190122 a_des_dir

        t_operation_files = operation_files(a_http_ip, a_token)
        return t_operation_files.download(a_fun, a_db, a_online_path_list, a_des_path_list, a_call_back, backup_dir)

    @staticmethod
    def upload(a_fun, a_http_ip, a_token, a_db, a_sou_path_list, a_online_path_list, a_call_back=None, a_metadata = {}, a_file_log_dict={}, a_folder_data={}):
        if len(a_sou_path_list) != len(a_online_path_list):
            raise Exception("media_file.upload, the number of source and destination paths does not match)")  # --20190122 a_des_dir

        t_operation_files = operation_files(a_http_ip, a_token)
        return t_operation_files.upload(a_fun, a_db, a_sou_path_list, a_online_path_list, a_metadata, a_call_back, a_file_log_dict, a_folder_data)

    @staticmethod
    def download_lastest(a_fun, a_http_ip, a_token, a_db,  a_online_dir, a_des_dir, a_time, a_call_back=None):
        t_operation_files = operation_files(a_http_ip, a_token)
        return t_operation_files.download_lastest(a_fun, a_db, a_online_dir, a_des_dir, a_time, a_call_back)    
    
    @staticmethod
    def upload_and_convert_image(a_fun, a_http_ip, a_token, a_db, a_sou_path_list, a_online_path_list, a_call_back=None, a_metadata = {}, a_file_log_dict={}, a_sys_data_dict={}, a_check_convert_file=True):
        if len(a_sou_path_list) != len(a_online_path_list):
            raise Exception("media_file.upload_and_convert_image, the number of source and destination paths does not match)") 

        t_operation_files = operation_files(a_http_ip, a_token)
        return t_operation_files.upload_and_convert_image(a_fun, a_db, a_sou_path_list, a_online_path_list, a_metadata, a_call_back, a_file_log_dict, a_sys_data_dict, a_check_convert_file)
    
    @staticmethod
    def upload_and_convert_mov(a_fun, a_http_ip, a_token, a_db, a_sou_path_list, a_online_path_list, a_call_back=None, a_metadata = {}, a_file_log_dict={}, a_sys_data_dict={}, a_check_convert_file=True):

        if len(a_sou_path_list) != len(a_online_path_list):
            raise Exception("media_file.upload_and_convert_mov, the number of source and destination paths does not match)") 

        t_operation_files = operation_files(a_http_ip, a_token)
        return t_operation_files.upload_and_convert_mov(a_fun, a_db, a_sou_path_list, a_online_path_list, a_metadata, a_call_back, a_file_log_dict, a_sys_data_dict, a_check_convert_file)  
    
    @staticmethod
    def upload_and_convert_mov_image(a_fun, a_http_ip, a_token, a_db, a_sou_path_list, a_online_path_list, a_call_back=None, a_metadata = {}, a_file_log_dict={}, a_sys_data_dict={}, a_check_convert_file=True):

        if len(a_sou_path_list) != len(a_online_path_list):
            raise Exception("media_file.upload_and_convert_mov_image, the number of source and destination paths does not match)") 

        t_operation_files = operation_files(a_http_ip, a_token)
        return t_operation_files.upload_and_convert_mov_image(a_fun, a_db, a_sou_path_list, a_online_path_list, a_metadata, a_call_back, a_file_log_dict, a_sys_data_dict, a_check_convert_file) 
    
    @staticmethod
    def check_convert_mov(a_fun, a_http_ip, a_token, a_sou_path_list):
        #检查视频是否可以转码
        t_operation_files = operation_files(a_http_ip, a_token)
        return t_operation_files.check_convert_mov(a_fun, a_sou_path_list)
    
    @staticmethod
    def check_convert_image(a_fun, a_http_ip, a_token, a_sou_path_list):
        #检查图片是否可以转码
        t_operation_files = operation_files(a_http_ip, a_token)
        return t_operation_files.check_convert_image(a_fun, a_sou_path_list)
    
    @staticmethod
    def check_convert_mov_image(a_fun, a_http_ip, a_token, a_sou_path_list):
        #检查图片是否可以转码
        t_operation_files = operation_files(a_http_ip, a_token)
        return t_operation_files.check_convert_mov_image(a_fun, a_sou_path_list)
    
    #------------------------------私有-----------------------------------


class operation_files(object):
    m_total_size           = 0 #总大小
    m_already_perform_size = 0 #已执行大小
    m_current_name = '' #当前下载的文件名称
    
    CONVERT_IMAGE = 0 #转图片
    CONVERT_MOV = 1 #转视频
    CONVERT_MOV_IMAGE = 2 #视频或者图片
    
    MOV = 0
    IMAGE = 1
    
    def __init__(self, a_http_ip, a_token):
        super(operation_files, self).__init__()

        self.m_ct_file = ctlib.file()
        self.m_ct_mov  = ctlib.mov()
        self.m_http    = ctlib.media_http(a_http_ip, a_token)    
        self.m_ct_http = ctlib.http(a_http_ip, a_token)    
        self.m_os      = _lib.get_os()

    def download_filebox(self,a_fun, a_db, a_module, a_module_type, a_task_id, a_filebox_id, a_is_download_all, a_is_show_exist, a_des_dir="", a_call_back=None, a_argv_dict={}):
        '''
            a_argv_dict(dict)  其他更多参数  20220613 
                目前支持传入 
                1. {'keep_dir_structure':False} #当a_des_dir不为空(下载到其他路径)时. 下载的时候不保存文件框目录结构. 默认保持目录结构
                2. {'local_cache_key':''} 写入本地数据库.  与同步工具相同.  20220802
        '''
        #列 顺序
        t_table_column_list = ['id', 'des', 'des_dir', 'size', 'web_path', 'current_name', 'name','is_move_to_history','is_add_date','is_add_version','is_downloaded']
        #参数:argv_dict['keep_dir_structure'] 是否保持目录结构
        is_keep_dir_structure = a_argv_dict.get('keep_dir_structure',True)
        #参数:argv_dict['local_cache_key']
        t_default_cache_key = 'cgtw_media_file_download_filebox_default_key'
        t_local_cache_key  = to_unicode(a_argv_dict.get('local_cache_key', t_default_cache_key))
        #True False Y N L
        if isinstance(a_is_download_all,bool):
            t_is_all = 'Y' if a_is_download_all else 'N'
        else:
            t_is_all = a_is_download_all
        
        #数据库路径
        try:
            t_db_path = self.__get_db_path()
            t_sqlite = ctlib.sqlite(t_db_path)
        except Exception as error:
            raise Exception(u"Failed to connect sqlite. {}".format(error))
        #表名
        try:
            #加个时间范围. 当天内的. 才有效
            t_json_key = {'is_download_all':a_is_download_all,'des_dir':a_des_dir,'keep_dir_structure':is_keep_dir_structure,'local_cache_key':t_local_cache_key,'task_id':a_task_id, 'filebox_id':a_filebox_id}
            t_table = "{}_{}_{}".format(
                a_db, 
                str(_lib.now('%Y%m%d')), 
                ctlib.com.get_text_md5(json.dumps(t_json_key)))
        except Exception as error:
            raise Exception(u'Failed to get table name. {}'.format(error))
        #检查表是否存在. 并创建表. 
        try:
            t_res = t_sqlite.exist_table(t_table)
            if not t_res:
                t_res = t_sqlite.create_table("create table {} ({})".format(t_table, ",".join([i+' TEXT' for i in t_table_column_list])))
                if t_res != True:
                    raise Exception(u'Failed to create table({}). {}'.format(t_table, t_res))
                t_res = t_sqlite.exist_table(t_table)
                if not t_res:
                    raise Exception(u'Failed to create table({}). is not exists'.format(t_table))
        except Exception as error:
            raise Exception(u'Failed to check table exists or create table({}) error:{}'.format(t_table, error))
        #1. 检查本次所有media_file_id是否存在表中. 不存在则添加.
        #2. 检查表中的media_file_id是否都在本次任务中. 不存在则删除.
        #找出表中所有media_file_id.

        t_table_media_file_id_list = []#表中已存在的media_file_id
        if t_sqlite.count(t_table) != 0:
            t_table_media_file_id_list = [ i[0] for i in t_sqlite.get(t_table, ['id'], [])]
        
        #--获取下载文件信息
        t_current_folder_id=""
        res = a_fun("media_file", "get_filebox_bulk_download_data", {"db":a_db, "module":a_module, "module_type":a_module_type, "os":self.m_os, "is_all":t_is_all, "filebox_id":a_filebox_id, "task_id_array":[a_task_id]})
        folder_id_lis=[]#20231024
        for dic in res:
            t_current_folder_id = dic["current_folder_id"]
            t_data_list    = dic["data_list"]
            t_filebox_data = dic["filebox_data"]
            t_des_dir      = dic["des_dir"]
            t_server       = dic['server']   
            t_replace_server = t_server
            if a_des_dir.strip() != "":
                a_des_dir = a_des_dir.replace('\\','/')
                t_replace_server = a_des_dir
                #--判断a_des_dir是否存在
                if not os.path.exists(a_des_dir):
                    try:
                        os.makedirs(a_des_dir)
                    except Exception as e:
                        raise Exception("media_file.download_filebox, makedirs fail:({})".format(e))
                #--判断是否是目录
                if not os.path.isdir(a_des_dir):
                    raise Exception("media_file.download_filebox, des_dir is not dir")
                    
                #--替换目标路径
                a_des_dir = a_des_dir.rstrip('/')+'/'#--结尾必须是'/'   
                if a_argv_dict.get('keep_dir_structure',True) is False: #不保持目录结构.
                    t_des_dir = a_des_dir
                else:
                    t_des_dir = t_des_dir.replace(t_server, a_des_dir)                
            if not isinstance(t_data_list, list):
                continue

            for t_dict_data in t_data_list:
                if not isinstance(t_dict_data, dict) or "id"  not in t_dict_data or  "name"  not in t_dict_data or  "is_folder" not in t_dict_data:  
                    continue

                #20231024
                if to_unicode(t_dict_data["is_folder"]).strip().lower()=='y':
                    folder_id_lis.append(t_dict_data["id"])

                t_bulk_download_list = self.__get_bulk_download_list(a_fun, a_db,  t_dict_data, t_current_folder_id, t_replace_server, t_des_dir, t_filebox_data)
                t_new_bulk_download_list = []
                for _data in t_bulk_download_list:
                    if _data[0] in t_table_media_file_id_list:
                        t_table_media_file_id_list.remove(_data[0])
                        continue
                    t_new_bulk_download_list.append(_data)

                
                if len(t_new_bulk_download_list) <=0:
                    continue
              
                #插入sqlite
                if t_sqlite.bulk_insert(t_table, t_table_column_list, t_new_bulk_download_list) != True:
                    raise Exception(u'Failed to bulk insert sqlite table({})'.format(t_table))

        #删除本次任务不存在的id
        if t_table_media_file_id_list != []:
            t_sqlite.delete(t_table, [['id','in',t_table_media_file_id_list]])

        #从表中获取未下载的数据
        if t_sqlite.count(t_table) == 0:#总下载个数
            return []
        self.m_total_size           = self.__get_download_size(t_sqlite, t_table)
        self.m_already_perform_size = self.__get_download_size(t_sqlite, t_table, True)

        download_data_list = t_sqlite.get(t_table, t_table_column_list, [["is_downloaded", "!=", "Y"]])
        #更新已下载数据
        if len(download_data_list)<=0:
            t_sqlite.drop(t_table)
            return []
        
        download_data_list = [dict(zip(t_table_column_list[:-1], _data)) for _data in download_data_list]
        #下载
        self.m_call_back = a_call_back
        t_all_list       = []

        t_error = ""
        for _data in download_data_list:
            _id = _data['id']
            _des = _data['des']
            _size = _data['size']
            _name = _data['name']
            _web_path = _data['web_path']
            _current_name = _data['current_name']
            _des_dir = _data['des_dir']
            _is_move_to_history = _data['is_move_to_history']
            _is_add_date = _data['is_add_date']
            _is_add_version = _data['is_add_version']
            
            #current name
            self.m_current_name = _current_name
            t_temp_dict={}
            #备份路径存在. 从表格中获取数据. 备份文件路径已存在. 
            #备份路径存在. 修改了文件框移动历史数据问题. 
            try:
                _backup_path = self.__download_backup_path_of_download_filebox(_des, _des_dir, _is_move_to_history, _is_add_date, _is_add_version, _name)
                _download_res =  self.m_http.download(a_db, _id, _des, self.__call_back, _backup_path, t_temp_dict)
                #下载结果
                if _download_res:
                    self.m_already_perform_size += int(_size) #-成功才计入 已下载大小
                    if a_is_show_exist:
                        t_all_list.append(_des)
                    else:
                        #不显示已经存在的
                        if not isinstance(t_temp_dict, dict) or t_temp_dict.get('exist',False) != True:
                            t_all_list.append(_des)
                    t_sqlite.update(t_table,  {'is_downloaded':'Y'},[['id','=',_id]])
                else:#新的有返回false
                    t_error += u'mediaId:{} web_path:{} des_path:{} res:{}\n'.format(_id, _web_path, _des, _download_res)
            except Exception as error:
                t_error += u'mediaId:{} web_path:{} des_path:{} error:{}\n'.format(_id, _web_path, _des, error)
    
        #20231024--设置文件夹的修改时间
        if len(folder_id_lis)>0:
            t_folder_data = a_fun("media_file", "get_folder_modify_time", {"db": a_db, "current_folder_id":t_current_folder_id,  "id_array": folder_id_lis})#{path:time}
            for tmp_online in t_folder_data:
                tmp_time= t_folder_data[tmp_online]
                tmp_des=t_des_dir + "/" + to_unicode(tmp_online).strip("/")
                if os.path.exists(tmp_des) and to_unicode(tmp_time).strip()!="":
                    try:
                        self.m_ct_file.set_modify_time(tmp_des, tmp_time)
                    except Exception as e:
                        pass

        if t_error != "":
            if t_local_cache_key == t_default_cache_key:
                t_sqlite.drop(t_table)
            raise Exception(u'media_file.download_filebox download fail,\n{}'.format(t_error))
        else:
            t_sqlite.drop(t_table)
        return t_all_list         
    
    def upload_filebox(self, a_fun, a_db, a_module, a_module_type, a_task_id, a_filebox_id, a_sou_path_list, a_call_back=None, a_argv_dict={}):
        '''
            a_argv_dict(dict)  其他更多参数  
                目前支持传入 
                    exclude_path_list  针对路径中的字符串.  排除路径
        
        '''
        self.m_call_back = a_call_back
        
        t_controller=a_module_type
        if a_module=="etask":
            t_controller="etask"
        
        filebox_dict=a_fun(t_controller, "get_filebox", {"db":a_db, "module":a_module,  "id":a_task_id, "os":self.m_os, "filebox_id":a_filebox_id})
        if not isinstance(filebox_dict, dict):
            raise Exception("media_file.upload_filebox, get filebox data fail")
        else:
            if "path" not in filebox_dict or "server" not in filebox_dict:
                raise Exception("media_file.upload_filebox, get filebox data fail")
        
        
        if to_unicode(filebox_dict["is_version"]).lower().strip()=="y":
            raise Exception("media_file.upload_filebox, can't upload version filebox")
        
        #a_argv_dict
        t_exclude_path_list = a_argv_dict.get('exclude_path_list', False)
        if t_exclude_path_list!=False and not isinstance(t_exclude_path_list,list):
            raise Exception("media_file.upload_filebox. Argv a_argv_dict error. exclude_path_list must be list.")



        t_upload_dir=to_unicode(filebox_dict["path"]).replace(filebox_dict["server"], "/")
        t_new_upload_list=[]
        t_folder_data={}#文件夹的修改时间:{online:modify_time}---20231024
        #遍历出所有的源文件
        for n in range(len(a_sou_path_list)):
            t_sou_path=a_sou_path_list[n]
            t_sou_path=t_sou_path.replace("\\", "/")
            t_des_path=t_upload_dir+"/"+os.path.basename(t_sou_path)
            if os.path.isdir(t_sou_path):
                t_folder_data[t_des_path]=self.m_ct_file.get_modify_time(t_sou_path)#文件夹的修改时间:{online:modify_time}---20231024

                for i in self.m_ct_file.get_file_with_walk_folder(t_sou_path):
                    if self.__check_filter_path(i, t_exclude_path_list):
                        t_file_size=self.m_ct_file.get_size(i)
                        self.m_total_size += t_file_size
                        t_new_des_path=i.replace(t_sou_path, t_des_path)
                        t_new_des_path=to_unicode(t_new_des_path).replace("\\", "/")
                        t_new_upload_list.append({"sou":to_unicode(i).replace("\\", "/"), "des":t_new_des_path, "size":t_file_size})
            else:
                if self.__check_filter_path(t_sou_path, t_exclude_path_list):
                    t_file_size=self.m_ct_file.get_size(t_sou_path)
                    self.m_total_size += t_file_size
                    t_new_upload_list.append({"sou":t_sou_path, "des":t_des_path, "size":t_file_size})
                
        #开始上传
        for i in range( len(t_new_upload_list) ):
            t_sou=t_new_upload_list[i]["sou"]
            t_des=t_new_upload_list[i]["des"]
            #检查文件是否在服务器
            t_sou_dict=self.m_ct_file.get_chuck_md5(t_sou)    
            t_md5= t_sou_dict["md5"]
            t_chuck=t_sou_dict["chuck"]
            #t_session_id=_lib.uuid()
            t_session_id=t_md5
            
            t_file_size=t_new_upload_list[i]["size"]
            t_file_name=os.path.basename(t_des)
            self.m_current_name = t_des #新
            t_file_modify_time=self.m_ct_file.get_modify_time(t_sou)        
            #再media_folder中创建记录,并取回folder_id
            try:
                t_folder_id=a_fun("media_file", "create_path_and_get_folder_id", {"db":a_db, "path":os.path.dirname(t_des)})                
            except:
                raise Exception("media_file.upload_filebox, create path and get folder id fail")
            

            try:
                exist_file_res=a_fun("media_file", "exist_file", {"db":a_db, "file_name":t_file_name, "folder_id":t_folder_id, "md5":t_md5})   
            except:
                raise Exception("media_file.upload_filebox, get exist file fail")
                     
            exist_file_dic=dict(exist_file_res)
            if "md5_path" not in exist_file_dic or "is_exist_data" not in exist_file_dic or 'id' not in exist_file_dic:
                raise Exception("media_file.upload_filebox, get exist file fail, not key (id, md5_path, is_exist_data)")

            media_file_id  = to_unicode(exist_file_dic['id']).strip()
            is_exist_data=to_unicode(exist_file_dic["is_exist_data"]).strip().lower()#数据库是否存在数据
            server_md5_path=to_unicode(exist_file_dic["md5_path"]).strip()
            new_server_md5_path=server_md5_path
            if server_md5_path=="":#服务器不存在这个文件
                try:
                    new_server_md5_path=self.m_http.upload(t_session_id, t_sou, a_db, t_file_name, t_md5, t_chuck, self.__call_back)   

                except Exception as e:
                    raise Exception("media_file.upload_filebox, {}".format(e))
            else:
                self.__call_back(t_file_size,t_file_size,0)
            self.m_already_perform_size += t_file_size #计入已下载大小
            
            #20220224 增加判断
            t_new_file_size   = self.m_ct_file.get_size(t_sou)
            t_new_modify_time = self.m_ct_file.get_modify_time(t_sou)
            #仅判断文件大小和修改时间. 修改时间或文件大小改变时.报错.跳过.
            if t_new_file_size != t_file_size or t_new_modify_time != t_file_modify_time:
                raise Exception(u'media_file.upload_filebox. The source file({}) is modified.'.format(t_sou))

            #文件已经在服务器上。这个时候则需要插入数据
            if is_exist_data!="y" or server_md5_path=="" or media_file_id == "":#不存在数据    
                is_convert_format=self.m_ct_mov.is_convert_format(t_sou)
                try:
                    upload_res=a_fun("media_file", "upload", {"db":a_db, 
                                                                "file_name":t_file_name,
                                                                "folder_id":t_folder_id, 
                                                                "md5":t_md5, 
                                                                "md5_path":new_server_md5_path, 
                                                                "sys_size":to_unicode(t_file_size), 
                                                                "sys_modify_time":t_file_modify_time,
                                                                "is_convert_format":is_convert_format,
                                                                "sys_data_array":{"#link_id":a_task_id, "#module":a_module, "#module_type":a_module_type}
                                                                })  
                except Exception as e:
                    raise Exception("media_file.upload_filebox, upload data fail")
                
            else:
                #文件已经在服务器上。数据也存在的情况,
                #更改文件修改时间
                try:
                    update_modify_time_res=a_fun("media_file", "update_file_modify_time", {"db":a_db, "file_name":t_file_name, "folder_id":t_folder_id, "md5":t_md5, "file_modify_time":t_file_modify_time})
                except:
                    raise Exception("media_file.upload_filebox, update file_modify_time fail")                  
                
                #-目录的修改时间---20231024
        
        if t_folder_data != {}: 
            t_folder_data_res = a_fun("media_file", "update_folder_modify_time", {"db": a_db, "folder_data": t_folder_data})        
        return True
    
    def download(self, a_fun, a_db, a_online_path_list, a_des_path_list, a_call_back, a_backup_dir):
        t_fail_list = []
        self.m_call_back = a_call_back

        #--获取在线文件对应信息
        t_online_file_list = a_fun('media_file', 'get_online_file_path_array', {'db':a_db,'path_array':a_online_path_list})  
        if len(t_online_file_list) != len(a_des_path_list): #获取在线文数量不正确 
            raise Exception("media_file.download, Incorrect number of online files obtained,"+json.dumps(t_online_file_list))
        
        
        #--计算所有将下载文件的总大小
        for _online_file_dict in t_online_file_list:
            if isinstance(_online_file_dict, dict) and 'size' in _online_file_dict:
                self.m_total_size += int(_online_file_dict['size'])
        
        #--循环下载
        for index in range(len(t_online_file_list)):
            t_online_data   = t_online_file_list[index]
            t_media_file_id = t_online_data['id']
            t_sou           = t_online_data['path']
            t_size          = t_online_data['size']
            t_des           = a_des_path_list[index]

            try:
                if t_des.strip() == "" or t_media_file_id.strip() == "":
                    t_fail_list.append(t_sou)
                    self.m_already_perform_size += int(t_size)  #计算当前已经下载的所有大小 --->(成功的时候添加)  
                    continue
                
                t_name = os.path.basename(t_des)
                if t_sou[0] != '/':
                    self.m_current_name = '/'+t_sou
                else:
                    self.m_current_name = t_sou
                
                t_download_backup_path = self.__download_backup_path(t_des, {}, t_name, _lib.now('%Y-%m-%d-%H-%M-%S'), "", a_backup_dir)
                if not self.m_http.download(a_db, t_media_file_id, t_des, self.__call_back, t_download_backup_path):
                    t_fail_list.append(t_sou)
                else:    
                    self.m_already_perform_size += int(t_size)  #计算当前已经下载的所有大小 --->(成功的时候添加)  
                
            except Exception as e:
                t_fail_list.append(t_sou)

        if len(t_fail_list) > 0:
            raise Exception("media_file.download, download fail,"+json.dumps(t_fail_list))
            
        return True
    
    def upload(self,a_fun, a_db, a_sou_path_list, a_online_path_list, a_metadata, a_call_back, a_file_log_dict={}, a_folder_data={}):
        
        self.m_call_back = a_call_back
        t_fail_list = []
        t_folder_data=a_folder_data#文件夹的修改时间:{online:modify_time}---20231024

        #--计算总文件大小
        t_new_sou_path_list = [] #新的原文件列表{'size':'','md5':'','modify_time':'','sou':''}
        for index in range(len(a_sou_path_list)):
            _sou= a_sou_path_list[index]
            t_online = to_unicode(a_online_path_list[index]).replace("\\", "/")
            if  _sou.strip() == "" or not os.path.exists(_sou):
                t_fail_list.append(_sou)
                continue

            if os.path.isdir(_sou):
                if a_folder_data=={}:
                    t_folder_data[t_online]=self.m_ct_file.get_modify_time(_sou)#文件夹的修改时间:{online:modify_time}---20231024

                for i in self.m_ct_file.get_file_with_walk_folder(_sou):
                    t_file_size        = self.m_ct_file.get_size(i)
                    t_sou_dict         = self.m_ct_file.get_chuck_md5(i)
                    t_md5              = t_sou_dict["md5"]
                    t_chuck            = t_sou_dict["chuck"]
                    t_file_modify_time = self.m_ct_file.get_modify_time(i)
                    self.m_total_size  += t_file_size
                    
                    i=to_unicode(i).replace("\\", "/")
                    temp_sou=to_unicode(_sou).replace("\\", "/")
                    
                    t_new_des_path = i.replace(temp_sou, t_online)
                    t_new_des_path = to_unicode(t_new_des_path).replace("\\", "/")                    
                    t_new_sou_path_list.append({'size':t_file_size,'md5':t_md5, "chuck":t_chuck ,'modify_time':t_file_modify_time,'sou':i, "des": t_new_des_path})                    
            else:
                t_file_size        = self.m_ct_file.get_size(_sou)
                t_sou_dict         = self.m_ct_file.get_chuck_md5(_sou)
                t_md5              = t_sou_dict["md5"]
                t_chuck            = t_sou_dict["chuck"]
                t_file_modify_time = self.m_ct_file.get_modify_time(_sou)
                self.m_total_size  += t_file_size
                t_new_sou_path_list.append({'size':t_file_size,'md5':t_md5, "chuck":t_chuck ,'modify_time':t_file_modify_time,'sou':_sou, "des":t_online})
        
        #--存在不是文件 或不存在 或空的 直接返回
        if len(t_fail_list) > 0:
            raise Exception("media_file.upload, There are not file or not exists,please check,"+json.dumps(t_fail_list))
            
        for index in range(len(t_new_sou_path_list)):
            t_sou_data          = t_new_sou_path_list[index]
            t_sou               = t_sou_data['sou']
            t_file_modify_time  = t_sou_data['modify_time']
            t_md5               = t_sou_data['md5']
            t_chuck             = t_sou_data['chuck']
            t_file_size         = t_sou_data['size'] 
            t_des               = t_sou_data['des']
            try:
                if t_des[0] != "/":
                    t_des = "/" + t_des

                t_file_id = ""
                if t_des in a_file_log_dict:
                    t_file_id = a_file_log_dict[t_des]
                        
                t_session_id = t_md5
                t_file_name = os.path.basename(t_des)
                self.m_current_name = t_des
                t_folder_id = a_fun("media_file", "create_path_and_get_folder_id", {"db":a_db, "path":os.path.dirname(t_des)})
                exist_file_res = a_fun("media_file", "exist_file", {"db": a_db, "file_name": t_file_name, "folder_id": t_folder_id, "md5": t_md5, "file_id":t_file_id})
    
                exist_file_dic = dict(exist_file_res)

                if "md5_path" not in exist_file_dic or "is_exist_data" not in exist_file_dic or 'id' not in exist_file_dic:
                    t_fail_list.append(t_sou)
                    continue
                
                media_file_id         = exist_file_dic['id'].strip()
                is_exist_data   = to_unicode(exist_file_dic["is_exist_data"]).strip().lower()  # 数据库是否存在数据
                server_md5_path = to_unicode(exist_file_dic["md5_path"]).strip()
                new_server_md5_path = server_md5_path
                if server_md5_path == "":  # 服务器不存在这个文件
                    new_server_md5_path = self.m_http.upload(t_session_id, t_sou, a_db, t_file_name, t_md5, t_chuck, self.__call_back)
                else:
                    self.__call_back(t_file_size,t_file_size,0)
                self.m_already_perform_size += t_file_size  #计入已下载大小

                #20220224 增加判断
                t_new_file_size   = self.m_ct_file.get_size(t_sou)
                t_new_modify_time = self.m_ct_file.get_modify_time(t_sou)
                #仅判断文件大小和修改时间. 修改时间或文件大小改变时.报错.跳过.
                if t_new_file_size != t_file_size or t_new_modify_time != t_file_modify_time:
                    raise Exception(u'The source file({}) is modified.'.format(t_sou))

                # 文件已经在服务器上。这个时候则需要插入数据
                if is_exist_data != "y" or server_md5_path == "" or media_file_id == "":  # 不存在数据
                    is_convert_format=self.m_ct_mov.is_convert_format(t_sou)
                    # 文件记录---20190614

                        
                    upload_res = a_fun("media_file", "upload", {"db": a_db,
                                                                      "file_name": t_file_name,
                                                                      "folder_id": t_folder_id,
                                                                      "md5": t_md5,
                                                                      "md5_path": new_server_md5_path,
                                                                      "sys_size": to_unicode(t_file_size),
                                                                      "sys_modify_time": t_file_modify_time,
                                                                      "is_convert_format":is_convert_format,
                                                                      "meta_data_array": a_metadata,
                                                                      "file_id": t_file_id
                                                                      })
                else:
                    if media_file_id != "" and a_metadata != {}:
                        a_fun('media_file', 'set_metadata', {'db':a_db,'id':media_file_id,'meta_data_array':a_metadata})
 
                    update_modify_time_res = a_fun("media_file", "update_file_modify_time", {"db": a_db, "file_name": t_file_name, "folder_id": t_folder_id, "md5": t_md5, "file_modify_time": t_file_modify_time})
    
                    
    
            except Exception as error:
                t_fail_list.append('    File:{}  Error:{}'.format(t_sou, error))
    
        if len(t_fail_list) > 0:
            raise Exception("media_file.upload upload fail:\n{}".format('\n'.join(t_fail_list)))
        
        #-目录的修改时间---20231024
        if t_folder_data != {}: 
            t_folder_data_res = a_fun("media_file", "update_folder_modify_time", {"db": a_db, "folder_data": t_folder_data})
    
        return True            
    
    def download_lastest(self, a_fun, a_db, a_online_dir, a_des_dir, a_time, a_call_back):
        t_fail_list = []
        t_all_list  = []
        self.m_call_back = a_call_back
        a_online_dir=to_unicode(a_online_dir).rstrip("/").rstrip("\\")
        a_des_dir=to_unicode(a_des_dir).rstrip("/").rstrip("\\")
        filter_list=[ ["file.sys_create_time", ">", a_time] ]
        if to_unicode(a_online_dir).strip()=="":
            media_folder_id=""
        else:
            media_folder_id = a_fun('media_file', 'get_folder_id', {'db':a_db,'path':a_online_dir})
            if media_folder_id=="null":
                raise Exception("file.download_lastest, online dir not exist")
            filter_list=filter_list+[ "and", "(", ["#array_position(media_folder.all_p_id, '"+media_folder_id+"')", "!is", "null"], "or", ["#media_folder.id", "=", media_folder_id], ")" ]
            
        #--获取在线文件对应信息
        t_online_file_list = a_fun('media_file', 'get_online_file_with_filter', {'db':a_db,'filter_array':filter_list})          
        
        #--计算所有将下载文件的总大小
        for _online_file_dict in t_online_file_list:
            if isinstance(_online_file_dict, dict) and 'size' in _online_file_dict:
                self.m_total_size += int(_online_file_dict['size'])
        

        #--循环下载
        for _online_file_dict in t_online_file_list:
            t_media_file_id = _online_file_dict['id']
            t_sou           = _online_file_dict['path']
            t_size          = _online_file_dict['size']
            t_des           = a_des_dir + to_unicode(_online_file_dict['path']).replace(a_online_dir, "")
            try:
                if t_des.strip() == "" or t_media_file_id.strip() == "":
                    t_fail_list.append(t_sou)
                    self.m_already_perform_size += int(t_size)  #计算当前已经下载的所有大小 --->(成功的时候添加)  
                    continue
                
                t_name = os.path.basename(t_des)
                self.m_current_name = t_sou
                t_download_backup_path = self.__download_backup_path(t_des, {}, t_name, _lib.now('%Y-%m-%d-%H-%M-%S'))
                t_temp_dict={}
                if not self.m_http.download(a_db, t_media_file_id, t_des, self.__call_back, t_download_backup_path, t_temp_dict):
                    t_fail_list.append(t_sou)
                else:    
                    self.m_already_perform_size += int(t_size)  #计算当前已经下载的所有大小 --->(成功的时候添加)  
                    #t_all_list.append(t_des)
                    #不显示已经存在的
                    if isinstance(t_temp_dict, dict) and "exist" in t_temp_dict and t_temp_dict["exist"]:
                        continue
                    else:
                        t_all_list.append(t_des)                    
                
            except Exception as e:
                t_fail_list.append(t_sou)

        if len(t_fail_list) > 0:
            raise Exception("media_file.download_lastest, download fail,"+json.dumps(t_fail_list))
            
        return t_all_list        
    
    #---------转码上传使用----
    #上传图片并转码
    def upload_and_convert_image(self,a_fun, a_db, a_sou_path_list, a_online_path_list, a_metadata, a_call_back, a_file_log_dict={}, a_sys_data_dict={}, a_check_convert_file=True): #a_check_convert_file有的时候外面直接检查了。这边就不用了
        return self.__upload_and_convert(a_fun, self.CONVERT_IMAGE, a_db, a_sou_path_list, a_online_path_list, a_metadata, a_call_back, a_file_log_dict, a_sys_data_dict, a_check_convert_file)
    
    #上传视频并转码
    def upload_and_convert_mov(self,a_fun, a_db, a_sou_path_list, a_online_path_list, a_metadata, a_call_back, a_file_log_dict={}, a_sys_data_dict={}, a_check_convert_file=True): #a_check_convert_file有的时候外面直接检查了。这边就不用了
        return self.__upload_and_convert(a_fun, self.CONVERT_MOV, a_db, a_sou_path_list, a_online_path_list, a_metadata, a_call_back, a_file_log_dict, a_sys_data_dict, a_check_convert_file)
    
    #上传视频或图片并转码
    def upload_and_convert_mov_image(self,a_fun, a_db, a_sou_path_list, a_online_path_list, a_metadata, a_call_back, a_file_log_dict={}, a_sys_data_dict={}, a_check_convert_file=True): #a_check_convert_file有的时候外面直接检查了。这边就不用了
        return self.__upload_and_convert(a_fun, self.CONVERT_MOV_IMAGE, a_db, a_sou_path_list, a_online_path_list, a_metadata, a_call_back, a_file_log_dict, a_sys_data_dict, a_check_convert_file)
    
    def check_convert_mov(self, a_fun, a_sou_path_list):
        return self.check_convert_file(a_fun, a_sou_path_list, self.CONVERT_MOV)
    
    def check_convert_image(self, a_fun, a_sou_path_list):
        return self.check_convert_file(a_fun, a_sou_path_list, self.CONVERT_IMAGE)   
    
    def check_convert_mov_image(self, a_fun, a_sou_path_list):
        return self.check_convert_file(a_fun, a_sou_path_list, self.CONVERT_MOV_IMAGE)  
    
    def __upload_and_convert(self,a_fun, a_convert_type, a_db, a_sou_path_list, a_online_path_list, a_metadata, a_call_back, a_file_log_dict={}, a_sys_data_dict={}, a_check_convert_file=True):
        #a_sys_data_dict={"#module":, #module_type, #link_id:}
        self.m_call_back = a_call_back
        if a_check_convert_file:
            self.check_convert_file(a_fun, a_sou_path_list, a_convert_type)
        #获取上传数据
        t_upload_list=self.__get_upload_data(a_fun, a_sou_path_list, a_online_path_list)
        t_folder_id_dic = {}  # {"server_dir":folder_id}#防止重复验证生成folder_id
        for n in range(len(t_upload_list)):
            sou_data_dict = t_upload_list[n]["sou"]
            convert_dict = t_upload_list[n]["convert"]

            t_sou = sou_data_dict["sou"]
            t_media_type = sou_data_dict["media_type"] #20201103
            t_session_id = _lib.uuid()
            t_md5 = sou_data_dict["md5"]
            t_chuck = sou_data_dict["chuck"]  # 20190906
            t_modify_time = sou_data_dict["modify_time"]
            t_server_dir = sou_data_dict["server_dir"]
            t_file_name = sou_data_dict["file_name"]
            t_size = sou_data_dict["size"]
            t_is_convert_format = sou_data_dict["is_convert_format"]  # 是否为转码格式
            t_des = t_server_dir+"/"+t_file_name
            
            t_file_id = ""
            if t_des in a_file_log_dict:
                t_file_id = a_file_log_dict[t_des]
                
            
            # 再media_folder中创建记录,并取回folder_id
            if t_server_dir in t_folder_id_dic:
                t_folder_id = t_folder_id_dic[t_server_dir]
            else:
                t_folder_id = a_fun("media_file", "create_path_and_get_folder_id", {"db": a_db, "path": t_server_dir})

            # 检查文件是否在服务器
            exist_file_res = a_fun("media_file", "exist_file", {"db": a_db, "file_name": t_file_name, "folder_id": t_folder_id, "md5": t_md5, "convert_md5": convert_dict["convert_md5"], "file_id":t_file_id})
            exist_file_dic = dict(exist_file_res)
            if "md5_path" not in exist_file_dic and "convert_md5_path" not in exist_file_dic and "convert_image" not in exist_file_dic \
               and "is_exist_data" not in exist_file_dic and "is_exist_convert_data" not in exist_file_dic and "id" not in exist_file_dic and "store_type" not in exist_file_dic:
                raise Exception("get exist_file fail")

            is_exist_data = to_unicode(exist_file_dic["is_exist_data"]).strip().lower()  # 数据库是否存在数据
            is_exist_convert_data = to_unicode(exist_file_dic["is_exist_convert_data"]).strip().lower()  # 同一条记录中,数据库是否存在转码的数据
            server_md5_path = to_unicode(exist_file_dic["md5_path"]).strip()
            t_media_file_id = to_unicode(exist_file_dic["id"]).strip()  # 可能为空--20190614
            server_convert_md5_path = to_unicode(exist_file_dic["convert_md5_path"]).strip()
            server_convert_image = dict(exist_file_dic["convert_image"])
            store_type=to_unicode(exist_file_dic["store_type"]).strip()
            # 上传转码,后端同时生成缩略图-----------------------------------------------------------
            if server_convert_md5_path == "" or server_convert_image == {}:
                if t_media_type == self.MOV:
                    t_convert_dic = self.m_ct_http.upload_project_video_convert(convert_dict["convert_sou"], a_db, sou_data_dict["md5"], self.__call_back)
                elif t_media_type == self.IMAGE:
                    t_convert_dic = self.m_ct_http.upload_project_image_convert(convert_dict["convert_sou"], a_db, sou_data_dict["md5"], self.__call_back)
                else:
                    raise Exception("convert type error")
                if not isinstance(t_convert_dic, dict) or "md5_path" not in t_convert_dic or "min" not in t_convert_dic or "mid" not in t_convert_dic or "max" not in t_convert_dic:
                    raise Exception("upload convert file fail")
                convert_dict["convert_image"] = {"min": t_convert_dic["min"], "mid": t_convert_dic["mid"], "max": t_convert_dic["max"]}
                convert_dict["convert_md5_path"] = t_convert_dic["md5_path"]  # 上传后。返回md5_path添加到字典

            else:
                # 在线存在的话。直接用在线的数据
                convert_dict["convert_md5_path"] = server_convert_md5_path
                convert_dict["convert_image"] = server_convert_image
            
            # 添加已经操作过的文件大小
            self.m_already_perform_size += convert_dict["convert_size"]             

            # 上传源文件--------------------------------------------------------

            new_server_md5_path = server_md5_path
            self.m_current_file_size = t_size
            if server_md5_path == "":  # 服务器不存在这个文件
                if to_unicode(convert_dict["convert_md5"]).lower() == to_unicode(t_md5).lower() and to_unicode(store_type).strip()=="":  # 说明转码文件和源文件是同一个,之前转码在附件的接口传过了。这边就不用再传一次---这个前提是不是第三方存储
                    new_server_md5_path = convert_dict["convert_md5_path"]

                else:
                    new_server_md5_path = self.m_http.upload(t_session_id, t_sou, a_db, t_file_name, t_md5, t_chuck, self.__call_back)  # 20190906

            self.m_already_perform_size += t_size 

            #20220224 增加判断
            t_new_file_size   = self.m_ct_file.get_size(t_sou)
            t_new_modify_time = self.m_ct_file.get_modify_time(t_sou)
            #仅判断文件大小和修改时间. 修改时间或文件大小改变时.报错.跳过.
            if t_new_file_size != t_size or t_new_modify_time != t_modify_time:
                raise Exception(u'media_file.__upload_and_convert. The source file({}) is modified.'.format(t_sou))

            # 文件已经在服务器上。这个时候则需要插入数据
            
            if is_exist_data != "y" or server_md5_path == "" or is_exist_convert_data != "y":  # 不存在数据
                convert_data_dict = {
                                  "sys_convert_md5": convert_dict["convert_md5"],
                                  "sys_convert_md5_path": convert_dict["convert_md5_path"],
                                  "sys_convert_image": convert_dict["convert_image"],
                                  "sys_convert_size": to_unicode(convert_dict["convert_size"]),
                                  "sys_convert_file_name": convert_dict["convert_file_name"],
                                  "sys_convert_modify_time": convert_dict["convert_modify_time"]
                                  }
                if t_media_type == self.MOV:
                    convert_data_dict["sys_convert_frame"] = convert_dict["convert_frame"]
                    convert_data_dict["sys_convert_fps"] = convert_dict["convert_fps"]
                    convert_data_dict["sys_convert_duration"] = convert_dict["convert_duration"]

                # 文件记录---20190614


                a_fun("media_file", "upload", {"db": a_db,
                                                "md5": t_md5,
                                                "md5_path": new_server_md5_path,
                                                "file_name": t_file_name,
                                                "folder_id": t_folder_id,
                                                "sys_modify_time": t_modify_time,
                                                "sys_size": to_unicode(t_size),
                                                "sys_data_array": a_sys_data_dict,
                                                "convert_data_array": convert_data_dict,
                                                "is_convert_format": t_is_convert_format,
                                                "file_id": t_file_id,
                                                "tag": [],
                                                "is_upload_sou_and_convert": True
                                                })

                
        
        return True
        
    #检查转码文件
    def check_convert_file(self, a_fun, a_sou_path_list, a_convert_type):
        # 取允许格式
            
        t_allow_format_dict = a_fun('media_data', "get_convert_format", {}) #{mov:[avi, mp4, mov], "image":[jpg, gif, tif...]}
        if not isinstance(t_allow_format_dict, dict):
            raise Exception("media_file.check_convert_file, get allow convert format fail")
        
        for temp_sou in a_sou_path_list:
            if os.path.isdir(temp_sou):
                raise Exception("media_file.check_convert_file, can't convert folder")
            
            suffix = os.path.splitext(temp_sou)[1]
            suffix = to_unicode(suffix).strip(".").lower()            
            if a_convert_type == self.CONVERT_MOV:
                t_allow_format_list = t_allow_format_dict["mov"]
                t_media_type = self.MOV
                check_format = suffix in t_allow_format_list
                
            elif a_convert_type == self.CONVERT_IMAGE:
                t_allow_format_list = t_allow_format_dict["image"]
                t_media_type = self.IMAGE
                check_format = suffix in t_allow_format_list
                
                
            elif a_convert_type == self.CONVERT_MOV_IMAGE:
                t_allow_format_list = t_allow_format_dict["mov"]+t_allow_format_dict["image"]
                t_media_type = ""
                check_format = suffix in t_allow_format_dict["mov"] #先检测是否为mov
                if not check_format:
                    check_format = suffix in t_allow_format_dict["image"] #再检测是否为image
                    if check_format:
                        t_media_type = self.IMAGE
                else:
                    #是mov
                    t_media_type = self.MOV


            # 判断格式是否在允许的格式中
            if not check_format:
                raise Exception("media_file.check_convert_file, the format only in ({})".format(repr(', '.join(t_allow_format_list))) )
            
            if t_media_type == self.MOV:  # 转mov
                # 判断如果不是mov的话,就直接出错
                try:
                    old_info_dic = self.m_ct_mov.get_avi_info(temp_sou)
                except Exception as e:
                    raise Exception("media_file.check_convert_file, get mov info fail: {}".format(e) )
                else:
                    if old_info_dic == False:
                        raise Exception("media_file.check_convert_file, please confirm whether it is a video file: {}".format( repr(temp_sou )))
                    
            elif t_media_type == self.IMAGE:
                self.m_ct_mov.check_image_resolution(temp_sou) #检查图片分辨率不能超过10000*10000--20221024
                try:
                    old_info_dic = self.m_ct_mov.get_image_info(temp_sou)
                except Exception as e:
                    raise Exception("media_file.check_convert_file, get image info fail: {}".format(e) )
                else:
                    if old_info_dic == False:
                        raise Exception("media_file.check_convert_file, please confirm whether it is a image file: {}".format(repr(temp_sou) ))  
        return True
    
    #获取要上传的数据
    def __get_upload_data(self, a_fun, a_sou_path_list, a_online_path_list):
        t_allow_format_dict = a_fun('media_data', "get_convert_format", {}) #{mov:[avi, mp4, mov], "image":[jpg, gif, tif...]}
        if not isinstance(t_allow_format_dict, dict):
            raise Exception("media_file.check_convert_file, get allow convert format fail")
        t_mov_format_list = t_allow_format_dict["mov"]
        t_image_format_list = t_allow_format_dict["image"]
        
        t_upload_list = []
        for n in range(len(a_sou_path_list)):    
            t_sou = a_sou_path_list[n]
            t_des = a_online_path_list[n]
            t_convert_dict = {}
            t_sou_data_dict = {}
            t_convert_sou_file = ""
            
            #判断是视频还是图片
            suffix = os.path.splitext(t_sou)[1]
            suffix = to_unicode(suffix).strip(".").lower()   
            t_media_type = ""
            if suffix in t_mov_format_list:
                t_media_type = self.MOV
            elif suffix in t_image_format_list:
                    t_media_type = self.IMAGE            
            
            if t_media_type == self.MOV:  # 转mov
                # 判断是否为H264编码,相同则不转码
                is_h264_codec = False
                t_sou_dict = self.m_ct_file.get_chuck_md5(t_sou)  # 20200403
    
                temp_mov_info_dic = self.m_ct_mov.get_avi_info(t_sou)
                #t_suf = to_unicode(os.path.splitext(os.path.basename(t_sou))[1]).strip(".").lower()
                
                if isinstance(temp_mov_info_dic, dict) and 'CodecID' in temp_mov_info_dic:
                    if to_unicode(temp_mov_info_dic['CodecID']).strip().lower() == "avc1":
                        is_h264_codec = True
    
                if is_h264_codec:
                    t_convert_sou_file = t_sou
                else:
                    t_convert_sou_file=_lib.get_tmp_path()+"/convert_"+t_sou_dict["md5"]+".mp4" #转码视频路径写法，防止多次重复转码
                    is_exist_convert=False
                    if os.path.exists(t_convert_sou_file): #判断本地是否已存在转码文件
                        #获取下视频信息是否会h264,不是的话。需要再转码
                        try:
                            temp_convert_info_dic = self.m_ct_mov.get_avi_info(t_convert_sou_file) #有可能视频转码失败,因此建议先获取信息一次
                            if isinstance(temp_convert_info_dic, dict) and 'CodecID' in temp_convert_info_dic:
                                if to_unicode(temp_convert_info_dic['CodecID']).strip().lower() == "avc1":
                                    is_exist_convert=True
                        except:
                            pass
    
                    if not is_exist_convert:
                        try:
                            t_convert_sou_file = self.m_ct_mov.mov_to_mov(t_sou, t_convert_sou_file)
                        except Exception as e:
                            raise Exception("media_file.__get_upload_data, convert mov fail: {}".format(e) )

                if t_convert_sou_file == False:
                    raise Exception("media_file.__get_upload_data, convert mov fail: {}".format( repr(t_sou) ))
    
                # 相同编码的保持原先的格式
                if is_h264_codec:
                    t_convert_dict["convert_file_name"] = os.path.basename(t_des)
                else:
                    t_convert_dict["convert_file_name"] = os.path.splitext(os.path.basename(t_des))[0]+".mp4"
    
                # 上传源文件的的数据----------------------------------------
                t_file_size = self.m_ct_file.get_size(t_sou)
    
                t_sou_data_dict = {"sou": t_sou,
                                   "media_type":t_media_type,#20201103
                                    "file_name": os.path.basename(t_des),
                                    "md5": t_sou_dict["md5"],  # 20190906
                                    "chuck": t_sou_dict["chuck"],  # 20190906
                                    "size": t_file_size,
                                    "modify_time": self.m_ct_file.get_modify_time(t_sou),
                                    "server_dir": os.path.dirname(t_des),
                                    "is_convert_format": is_h264_codec
                                    }
                self.m_total_size = self.m_total_size+t_file_size
    
                # 转后mov信息---------------------------
                try:
                    mov_info_dic = self.m_ct_mov.get_avi_info(t_convert_sou_file)
                except Exception as e:
                    raise Exception("media_file.__get_upload_data, get mov info fail: {}".format(e) )

                if mov_info_dic == False:
                    raise Exception("media_file.__get_upload_data, get mov info failed: {}".format(repr(t_sou) ))
    
                # 转码的数据----------------------------------------
                t_convert_md5_dict = self.m_ct_file.get_chuck_md5(t_convert_sou_file)  # 20200403

                t_convert_file_size = self.m_ct_file.get_size(t_convert_sou_file)
                t_convert_dict["convert_sou"] = t_convert_sou_file
                t_convert_dict["convert_md5"] = t_convert_md5_dict["md5"]  # 20190906
                t_convert_dict["convert_size"] = t_convert_file_size
                t_convert_dict["convert_modify_time"] = self.m_ct_file.get_modify_time(t_convert_sou_file)
                t_convert_dict["convert_duration"] = mov_info_dic['Duration']
                t_convert_dict["convert_fps"] = mov_info_dic['FrameRate']
                t_convert_dict["convert_frame"] = mov_info_dic['FrameCount']
    
                self.m_total_size = self.m_total_size+t_convert_file_size  # 源文件和转码后的文件都加入到进度
    
            elif t_media_type == self.IMAGE:
                # 图片---
                is_convert_format = self.m_ct_mov.is_convert_format(t_sou)
                try:
                    if is_convert_format:  # 如果是转码格式的图片，不用转换
                        t_convert_sou_file = t_sou
                    else:
                        t_convert_sou_file = self.m_ct_mov.image_to_image(t_sou)
    
                except Exception as e:
                    raise Exception("media_file.__get_upload_data, convert image failed: {}".format(e) )

                else:
                    # 上传源文件的数据-------------------------------------
                    t_file_size = self.m_ct_file.get_size(t_sou)
                    t_sou_dict = self.m_ct_file.get_chuck_md5(t_sou)  # 20200403
    
                    t_sou_data_dict = {"sou": t_sou,
                                       "media_type":t_media_type,#20201103
                                        "file_name": os.path.basename(t_des),
                                        "md5": t_sou_dict["md5"],  # 20190906
                                        "chuck": t_sou_dict["chuck"],  # 20190906
                                        "size":  t_file_size,
                                        "modify_time": self.m_ct_file.get_modify_time(t_sou),
                                        "server_dir": os.path.dirname(t_des),
                                        "is_convert_format": is_convert_format
                                        }
    
                    self.m_total_size = self.m_total_size+t_file_size  # 源文件和转码后的文件都加入到进度
    
                    # convert的数据--------------------
                    t_convert_md5_dict = self.m_ct_file.get_chuck_md5(t_convert_sou_file)  # 20200403
    
                    t_convert_file_size = self.m_ct_file.get_size(t_convert_sou_file)
                    t_convert_dict["convert_file_name"] = os.path.splitext(os.path.basename(t_des))[0]+".png"
                    t_convert_dict["convert_sou"] = t_convert_sou_file
                    t_convert_dict["convert_md5"] = t_convert_md5_dict["md5"]  # 20190906
                    t_convert_dict["convert_size"] = t_convert_file_size
                    t_convert_dict["convert_modify_time"] = self.m_ct_file.get_modify_time(t_convert_sou_file)
    
                    self.m_total_size = self.m_total_size+t_convert_file_size  # 源文件和转码后的文件都加入到进度
    
            t_upload_list.append({"convert": t_convert_dict, "sou": t_sou_data_dict})
    
        return t_upload_list

    #---私有-------------
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
    def __get_db_path(self):
        t_db = '/cgteamwork/db/cgtw_download_filebox70.db'
        if ctlib.com().get_os() == "win":
            t_profile = os.environ["USERPROFILE"].replace("\\", "/")
            if ctlib.com().is_win_chinese_account():
                t_users = os.path.dirname(t_profile)
                t_sys_path = t_users + "/sys_cgteamwork"
                if os.path.exists(t_sys_path):
                    return t_sys_path + t_db
                else:
                    t_db_path = t_users + "/public/Documents" + t_db
            else:
                t_db_path= t_profile + t_db
        
        else:
            t_db_path = os.environ["HOME"] + t_db
        if not os.path.exists(os.path.dirname(t_db_path)):
            os.makedirs(os.path.dirname(t_db_path))
        return t_db_path      
    #下载使用--------
    def __download_backup_path(self, a_des, a_filebox_data, a_name, a_time, a_replace_dir="", a_backup_dir=""):
        #a_name有可能是文件夹名称/或者文件的名称
        #a_time: 2018-01-01-22-11-22
        t_time_no_char=to_unicode(a_time).replace("-", "") #a_time: 20180101221122
        base_name=os.path.basename(a_des)        
        lis=os.path.splitext(base_name)
        t_backup_dir=os.path.dirname(a_des)
        if to_unicode(a_backup_dir).strip()!="":
            t_backup_dir=to_unicode(a_backup_dir).rstrip("/").rstrip("\\")
            
        if len(lis)==2:
            backup_path=t_backup_dir+"/history/backup/"+lis[0]+"."+t_time_no_char+lis[1]
        else:
            backup_path=t_backup_dir+"/history/backup/"+base_name+"."+t_time_no_char
        if "move_to_history" in a_filebox_data  and "is_in_history_add_version" in a_filebox_data  and "path" in a_filebox_data and "is_in_history_add_datetime" in a_filebox_data:
            if to_unicode(a_filebox_data["move_to_history"]).lower()=="y":
                filebox_path=a_filebox_data["path"]
                #取文件框目录下层级的名称
                if a_replace_dir=="":
                    if to_unicode(a_filebox_data["is_in_history_add_datetime"]).lower()=="y":
                        des_path=filebox_path+"/history/"+a_time+"/"+a_name
                    else:
                        des_path=filebox_path+"/history/"+a_name
                    temp_des_file=des_path
                    if to_unicode(a_filebox_data["is_in_history_add_version"]).lower()=="y":
                        temp_des_file=self.__auto_add_version(des_path)                        
                else:
                    temp_des_file=a_replace_dir

                backup_path=to_unicode(a_des).replace(filebox_path+"/"+a_name, temp_des_file)
        return backup_path        
    def __auto_add_version(self, a_path):
        res=a_path
        temp=""
        size=0
        basename=os.path.basename(a_path)
        temp_list=os.path.splitext(basename)
        suf=to_unicode(temp_list[-1]).strip(".")
        if suf.strip()!="":
            #用isFile的话，如果文件不存在会不对
            cmp_basename=temp_list[0]
            t_dir=os.path.dirname(a_path)
            for i in range(10000):
                if i<100:
                    size=2
                elif i>=100 and i<1000:
                    size=3
                elif i>=1000 and i<10000:
                    size=4
                temp=t_dir+"/"+cmp_basename+"_v"+self.__start_add_zero(str(i+1), size)+"."+suf
                if not os.path.exists(temp):
                    res=temp
                    break
        else:
            absolute_path=a_path
            for i in range(10000):
                if i<100:
                    size=2
                elif i>=100 and i<1000:
                    size=3
                elif i>=1000 and i<10000:
                    size=4
                temp=absolute_path+"_v"+ self.__start_add_zero(str(i+1), size)
                if not os.path.exists(temp):
                    res=temp
                    break
        return res            
    def __start_add_zero(self, a_string, a_size=4):
        string=a_string
        temp=a_size-len(a_string)
        if temp>0:
            for i in range(temp):
                string="0"+string
        return string
    def __get_bulk_download_list(self, a_fun, a_db,  a_dict_data, a_current_folder_id, a_replace_server, a_des_dir, a_filebox_data):
        #获取下载数据. 准备插入sqlite
        t_name = a_dict_data["name"]
        t_uuid = _lib.uuid()
        t_is_folder = True if to_unicode(a_dict_data["is_folder"]).strip().lower()=='y' else False

        t_file_id_list   = [] if t_is_folder else [a_dict_data["id"]]
        t_folder_id_list = [a_dict_data["id"]] if t_is_folder  else []
        
        if len(t_file_id_list)<=0 and len(t_folder_id_list)<=0:
            return []

        t_res=a_fun("c_media_file", "bulk_download", {"db":a_db, "id_array":t_file_id_list, "folder_id_array":t_folder_id_list, "current_folder_id":a_current_folder_id })
        if not isinstance(t_res,list) or t_res == []:
            return []

        #取backup_path
        t_backup_replace_dir = ""
        t_download_list = []
        for temp_dict in t_res:
            if not isinstance(temp_dict, dict) or 'path' not in temp_dict or "id" not in temp_dict:
                continue
            t_des = a_des_dir+"/"+to_unicode(temp_dict["path"]).strip("/")
            t_online_path = t_des.replace(a_replace_server, '')
            t_current_name = '/'+t_online_path if t_online_path[0] != '/' else t_online_path
            #['id', 'des', 'des_dir', 'size', 'web_path', 'current_name', 'name','is_move_to_history','is_add_date','is_add_version','is_downloaded']
            t_download_list.append(
                [temp_dict["id"], t_des, a_des_dir, temp_dict['file_size'], temp_dict['web_path'], t_current_name, t_name,
                to_unicode(a_filebox_data.get('move_to_history','n')), 
                to_unicode(a_filebox_data.get('is_in_history_add_datetime','n')), 
                to_unicode(a_filebox_data.get('is_in_history_add_version','n')),
                'N']
            )
        return t_download_list
    def __get_download_size(self, a_sqlite, a_table, a_has_download=False):
        filters = [["is_downloaded", "=", "Y"]] if a_has_download else []
        size=a_sqlite.get_one(a_table, "sum(size)", filters)
        if size is None or str(size)=="":
            return 0
        return int(size) 
    def __download_backup_path_of_download_filebox(self, a_des, a_des_dir, a_is_move_to_history, a_is_add_date,  a_is_add_version, a_name):
        #下载到文件框
        #下载到其他路径 保持目录结构
        #下载到其他路径 不保持目录结构

        #文件框未设置移动历史插件
        #文件框设置移动历史插件  添加日期
        #文件框设置移动历史插件  添加版本
        #文件框设置移动历史插件  添加日期和添加版本

        #文件1: 文件框路径+'/sc001.mp4'
        #文件2: 文件框路径+'/sc001/11.mp4'
        a_time = _lib.now('%Y-%m-%d-%H-%M-%S')
        t_time_no_char=to_unicode(a_time).replace("-", "") #a_time: 20180101221122
        name_splitext = os.path.splitext(a_name)
        

        #下载同名版本历史文件时,备份目录取
        if a_des.find(a_des_dir.rstrip('/')+'/history/v') != -1:
            temp_des_dir = a_des[:len(a_des_dir.rstrip('/'))+len('/history/v')]
            version = a_des[len(temp_des_dir):len(temp_des_dir)+3]
            if str(version).isdigit():
                a_des_dir = a_des_dir.rstrip('/')+'/history/v{}'.format(version)

        #默认
        backup_dir = a_des_dir+'/history/backup'+'/'+name_splitext[0]+'_'+t_time_no_char+name_splitext[1]
        backup_path =  a_des.replace(a_des_dir+'/'+a_name, backup_dir)

        
    


        #移动历史数据
        if not to_unicode(a_is_move_to_history).lower().strip() == 'y':
            return backup_path

        #添加日期 添加版本
        if to_unicode(a_is_add_date).lower().strip() == 'y':
            backup_dir = a_des_dir+'/history/'+a_time+'/'+a_name
        else:
            backup_dir = a_des_dir+'/history'+'/'+a_name
        
        #添加版本
        if to_unicode(a_is_add_version).lower().strip() == 'y':
            backup_dir=self.__auto_add_version(backup_dir)

        backup_path = a_des.replace(a_des_dir+'/'+a_name, backup_dir)

    
        return backup_path
    #上传使用---
    def __check_filter_path(self, a_file, a_exclude_path_list):
        #检查文件是否上传
        #目前参数1: a_exclude_path_list   --> 排除路径.  当路径包含过滤字符串时. 则返回False  -> 不上传
        if not a_exclude_path_list is False:
            new_file = to_unicode(a_file).replace("\\", "/")
            for _str in a_exclude_path_list:
                if not isinstance(_str, basestring):
                    raise Exception('Argv a_argv_dict error. exclude_path_list must be list and element must be str/unicode')
                _nstr = to_unicode(_str).replace("\\", "/")
                if new_file.find(_nstr) != -1:
                    return False
        return True