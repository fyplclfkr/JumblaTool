# coding: utf-8
import os, sys, re, json
from ._compat import *
from ._lib import _lib
import ctlib
'''
publish只针对有启用版本的文件框,
功能有:
1.自动识别版本号, 生成publish的版本号以及对应的提交文件记录
2.检查命名规则
3.备份旧文件到历史
4.复制文件到服务器
5.上传到网盘 (文件框有设置上传网盘, 同时有设置转视频或转图片的,也会就行转换)
6.提交跑流程 (文件框有设置提交检查)
'''
class _publish(object):

    def __init__(self, a_fun, a_http_ip, a_token, a_db, a_module, a_module_type, a_id, a_sou_list, a_filebox_sign, a_version="", a_version_argv={}, a_note_list=[], a_note_argv={}, a_callback=None, a_argv_dict={}):
        super(_publish, self).__init__()
        self.m_fun = a_fun
        self.m_http_ip = a_http_ip
        self.m_token = a_token
        self.m_db = a_db
        self.m_module = a_module
        self.m_module_type =a_module_type
        self.m_id = a_id
        self.m_sou_list = a_sou_list
        self.m_filebox_sign = a_filebox_sign
        self.m_outside_version = to_unicode(a_version).strip() #外部传递的版本
        self.m_callback = a_callback
        self.m_is_upgrade_version=True #是否升级版本
        self.m_file_log_dict={}
        self.m_version_id = ""
        self.m_note_list = a_note_list
        
        self.m_ct_file = ctlib.file()
        self.m_ct_com = ctlib.com()
        self.m_version_argv=a_version_argv
        self.m_note_argv = a_note_argv
        self.m_argv_dict = a_argv_dict#-20220509 新增参数. 目前可传字典key:is_upload_follow_filebox 上传网盘是否根据文件框设置, False/True --> 默认True, is_submit 是否跑流程, False/True，默认True
        #20220915 参数write_json 默认True 跳过生成json
    
    #执行的路口
    def _exec(self):
        
        #检查文件是否存在------
        not_exist_list=[]
        for sou in self.m_sou_list:
            if not os.path.exists(sou):
                not_exist_list.append(sou)
        if len(not_exist_list)>0:
            raise Exception("the path not exist:\n {}".format(  repr(not_exist_list))    )     
        
        #获取文件框信息
        t_os=_lib.get_os()
        if self.m_module_type == "info":
            t_task_class="info"
        else:
            t_task_class="task"
            if self.m_module=="etask":
                t_task_class="etask"

        self.m_filebox_info_dict=self.m_fun(t_task_class, "get_sign_filebox", {"db":self.m_db, "module":self.m_module,  "id":self.m_id, "os":t_os, "filebox_sign":self.m_filebox_sign})
        self.m_filebox_info_dict=dict(self.m_filebox_info_dict)
        if self.m_filebox_info_dict=={}:
            raise Exception("_publish._exec, the filebox not found (sign: "+self.m_filebox_sign+")")#没有找到标识对应文件框
        if not set(self.m_filebox_info_dict) >= {"rule", "path", "version_type", "is_version", "max_version", "is_submit", "is_upload_online", "convert_type", "version_length", "is_follow", "follow_version", "reviewer_account_id"}:
            raise Exception("_publish._exec, get filebox data error")
        
        #没有启用版本功能,则报错
        if to_unicode(self.m_filebox_info_dict["is_version"]).lower().strip()!="y":
            raise Exception("_publish._exec, the filebox version disabled") 
        
        #检查是否有启用上传到网盘并转码的，有转码的，检查文件是否符合转码----
        from ._media_file import _media_file
        t_is_upload_online = to_unicode(self.m_filebox_info_dict["is_upload_online"]).lower().strip()
        t_convert_type_list = self.m_filebox_info_dict["convert_type"]
        #20220509 增加判断 is_upload_follow_filebox
        is_upload_follow_filebox = self.m_argv_dict.get('is_upload_follow_filebox',True)
        if is_upload_follow_filebox is False:#只有当为False的时候才不根据文件框设置走
            t_is_upload_online = 'n'
            
        if t_is_upload_online=="y" and t_convert_type_list!=[]:
            if t_convert_type_list==["mov"]:
                _media_file.check_convert_mov(self.m_fun, self.m_http_ip, self.m_token, self.m_sou_list)
            elif t_convert_type_list==["image"]:
                _media_file.check_convert_image(self.m_fun, self.m_http_ip, self.m_token, self.m_sou_list)     
                
            elif "image" in t_convert_type_list and "mov" in t_convert_type_list: #同时支持图片和视频
                _media_file.check_convert_mov_image(self.m_fun, self.m_http_ip, self.m_token, self.m_sou_list)               
        
        #生成版本----
        self.m_version="" #最终的版本号
        old_max_version=self.m_filebox_info_dict["last_max_version"]#---20210702
        old_link_id=self.m_filebox_info_dict["last_link_id"]#最后版本的任务ID---20210702
        t_is_follow= self.m_filebox_info_dict["is_follow"] #是否启用跟随
        t_follow_version=self.m_filebox_info_dict["follow_version"]        
        t_version_length= self.m_filebox_info_dict["version_length"] #版本号位数---20200922
        t_is_force_upgrade_version= self.m_filebox_info_dict["is_upgrade_version"] #数据库最大版本和提交版本是同版本的时候, 是否强制升级版本----20201216
        if old_link_id!=self.m_id:
            #最大版本的任务ID和当前的任务ID不一样(同阶段多任务会出现这个问题),则需要强制升版本---20210702
            t_is_force_upgrade_version="Y"  
            
        t_version_length_rule = u'%0'+t_version_length+'d' #版本号位数规则, 如 %03d, %04d---20200922
        if to_unicode(old_max_version).strip()=="":
            old_max_version=to_unicode(t_version_length_rule)%(0) #如000----20200922
        else:
            old_max_version=to_unicode(t_version_length_rule)%(int(old_max_version))#---20200922
            
            
        if str(t_is_follow).lower().strip()=="y":
            #启用跟随
            if to_unicode(t_follow_version).strip()=="":
                #被跟随的文件框的版本号为空
                raise Exception("_publish._exec, please submit the following filebox first")#请先提交被跟随的文件框

            t_follow_version=to_unicode(t_version_length_rule)%(int(t_follow_version))#---20200922
            self.m_version=t_follow_version
            if to_unicode(t_follow_version).lstrip("0") == to_unicode(old_max_version).lstrip("0"):#---20200922
                self.m_is_upgrade_version=False
        else:
            #如果外部版本有传递的话。用外部的
            if self.m_outside_version!="":
                #检查version是否符合规则，必须是3位数的纯数字
                t_find_rule=r'\d'*int(t_version_length) #如r"\d\d\d" 和版本号的位数一致
                if re.findall(t_find_rule, self.m_outside_version)==[] or len(self.m_outside_version)!=int(t_version_length): #----20200923
                    raise Exception("_publish._exec, version format error, like '"+old_max_version+"'")
                
                #检查传递的版本小于系统版本则报错
                if self.m_outside_version < old_max_version:
                    raise Exception("_publish._exec, The max system version is greater than the file version (System: "+old_max_version+" <--> File: "+self.m_outside_version+")")
                
                
                self.m_version=self.m_outside_version #使用外部的
                if to_unicode(self.m_outside_version).lstrip("0")==to_unicode(old_max_version).lstrip("0"):#拖入版本=之前的最大版本，说明是重复拖入,或者替换了再拖入--这种不升版本。
                    self.m_is_upgrade_version=False #拖入版本和原先的版本一样。就不升版本，其他的操作照常
            else:
                #没有传递的。获取文件所在的版本
                sou_file_version=self.get_sou_file_version()
                if to_unicode(sou_file_version).strip()!="" and to_unicode(sou_file_version).lstrip("0")==to_unicode(old_max_version).lstrip("0") and to_unicode(t_is_force_upgrade_version).lower().strip()!="y":#拖入版本=之前的最大版本，说明是重复拖入,或者替换了再拖入--这种不升版本。-----------这个的前提是不强制升版本
                    self.m_version=old_max_version
                    self.m_is_upgrade_version=False #拖入版本和原先的版本一样。就不升版本，其他的操作照常
                    
                else:
                    #会有的情况有: 1：拖入版本 < 最大版本, 2：拖入版本 = 最大版本+1, 3：拖入版本 > 最大版本+1---都要生版本
                    #提升一个版本
                    self.m_version=int(old_max_version)+1
                    self.m_version=to_unicode(t_version_length_rule)%(int(self.m_version))#---20200922
                    if sou_file_version > self.m_version: #拖入版本 > 最大版本+1,这种要询问按哪种版本升，按拖入的版本还是按max_version
                        self.m_version=sou_file_version #使用拖入文件的版本
    
        #替换文件框路径中有{ver}------
        self.m_path = self.m_filebox_info_dict["path"]
        self.m_path = to_unicode(self.m_path).replace("{ver}", self.m_version)
        
        #检查命名规则---
        self.check_rule()
        
        #生成目标文件列表和在线网盘的列表-----
        t_server = self.m_filebox_info_dict["server"]
        self.m_des_list = []
        self.m_online_list = []
        t_des_data={} #{des_path: online}---20231024
        for temp_path in self.m_sou_list:
            if _lib.get_os() == "mac":
                if os.path.isfile(temp_path):
                    t_des = self.m_path+"/"+os.path.basename(temp_path)
                else:
                    temp_basename = os.path.basename(to_unicode(temp_path).rstrip("/").rstrip("\\"))
                    t_des = self.m_path+"/"+temp_basename+"/"
            else:
                t_des = self.m_path+"/"+os.path.basename(temp_path)
            self.m_des_list.append(t_des)
            t_online = to_unicode(t_des).replace(t_server, "/")
            self.m_online_list.append(t_online)
            t_des_data[t_des] = t_online #20231024
        
        #移动文件----
        if self.m_filebox_info_dict["version_type"]=="same":
            #---如果同名版本的话，则将文件移动到文件所在的版本下。如/history/v001/下----
            self.same_version_move_to_history()
        else:
            #文件版本和目录版本移动到历史
            self.file_and_folder_version_move_to_history()
        
        #复制文件----
        self.m_ct_file.copy_files(self.m_sou_list, self.m_des_list)
        
        #创建version和file---这边会生成新的self.m_version_id
        self.upload_version()
        
        #上传网盘---
        if t_is_upload_online=="y":
            t_sys_data_dict={"#module":self.m_module, "#module_type":self.m_module_type, "#link_id":self.m_id}
            if t_convert_type_list==["mov"]:
                #上传源视频和转码
                _media_file.upload_and_convert_mov(self.m_fun, self.m_http_ip, self.m_token, self.m_db, self.m_sou_list, self.m_online_list, self.m_callback, {}, self.m_file_log_dict, t_sys_data_dict, False)
            elif t_convert_type_list==["image"]:
                #上传源图片和转码
                _media_file.upload_and_convert_image(self.m_fun, self.m_http_ip, self.m_token, self.m_db, self.m_sou_list, self.m_online_list, self.m_callback, {}, self.m_file_log_dict, t_sys_data_dict, False)
                
            elif "image" in t_convert_type_list and "mov" in t_convert_type_list: #同时支持图片和视频
                _media_file.upload_and_convert_mov_image(self.m_fun, self.m_http_ip, self.m_token, self.m_db, self.m_sou_list, self.m_online_list, self.m_callback, {}, self.m_file_log_dict, t_sys_data_dict, False)
                
            else:
                #只是源文件

                #文件夹的修改时间---20231024
                t_folder_data={}
                for tmpdes in t_des_data:
                    if os.path.exists(tmpdes) and tmpdes in t_des_data:
                        tmp_online=t_des_data[tmpdes]
                        tmp_time=self.m_ct_file.get_modify_time(tmpdes)
                        t_folder_data[tmp_online]=tmp_time

                _media_file.upload(self.m_fun, self.m_http_ip, self.m_token, self.m_db, self.m_sou_list, self.m_online_list, self.m_callback, {}, self.m_file_log_dict, t_folder_data)
        
        #提交跑流程----
        is_submit = self.m_argv_dict.get('is_submit',True)
        if to_unicode(self.m_filebox_info_dict["is_submit"]).lower().strip()=="y" and is_submit == True:
            self.m_fun("work_flow", "submit", {"db":self.m_db, "module":self.m_module, "task_id":self.m_id, "filebox_id":self.m_filebox_info_dict["#id"], 
                                                      "dom_array":self.m_note_list, "version_id":self.m_version_id, "note_argv":self.m_note_argv, "qc_account_id":self.m_filebox_info_dict["reviewer_account_id"]})
        else:
            #非提交文件框,有note的输入note---20220323
            if len(self.m_note_list)>0:
                cc_account_id = self.m_note_argv.get("cc_account_id", "") #20230112
                note_field_data={"module":self.m_module,  "module_type":self.m_module_type, "#link_id":self.m_id, "dom_text":self.m_note_list, "version_id":self.m_version_id, "version":self.m_version, "version_data":{self.m_id:{"version_id":self.m_version_id, "version":self.m_version}}}
                note_field_data=dict(list(self.m_note_argv.items())+ list(note_field_data.items()))
                self.m_fun("note", "create", {"db":self.m_db, "field_data_array":note_field_data, "cc_account_id":cc_account_id})          
        
        return True
    
    #获取源文件的版本,用于比对file的最大版本
    def get_sou_file_version(self):        
        #判断是否启用版本v6.2
        version=""
        if to_unicode(self.m_filebox_info_dict["is_version"]).lower().strip()=="y":    
            version_type=self.m_filebox_info_dict["version_type"]
            t_version_length= self.m_filebox_info_dict["version_length"] #版本号位数---20200922
            t_version_length_rule = u'%0'+t_version_length+'d' #版本号位数规则, 如 %03d, %04d---20200922
            
            if version_type=="folder":#目录版本
                t_ver_path = to_unicode(self.m_filebox_info_dict["path"]).replace("\\", "/") #带有{ver}---  z:/test/aa/v{ver}/work
                index=to_unicode(t_ver_path).find("{ver}")
                if index!=-1:
                    left_str=t_ver_path[:index] #z:/test/aa/v
                    #匹配源文件的版本
                    for sou_path in self.m_sou_list:
                        sou_path=to_unicode(sou_path).replace("\\", "/").lower()
                        if to_unicode(sou_path).find(left_str.lower())!=-1:
                            #说明是同一个盘符的,--------如果不同盘符的。直接返回空
                            end_index=to_unicode(sou_path).find("/", index)
                            if end_index!=-1:
                                drag_ver=sou_path[index: end_index]
                                try:
                                    drag_ver=int(drag_ver) #如果drag_ver不是数字则会报错
                                except:
                                    pass
                                else:
                                    version=to_unicode(t_version_length_rule %drag_ver)#---20200922
                        
            elif version_type == "file":#文件版本
                version = self.m_ct_com.get_file_version(self.m_sou_list, self.m_filebox_info_dict["rule"], int(t_version_length))   

        return version    


    
    #文件和目录版本移动到历史
    def file_and_folder_version_move_to_history(self):
        local_des_exist_list=[]#本地目标文件存在的文件列表,用于移动到history
        for i in range(len(self.m_sou_list)):
            sou = self.m_sou_list[i]
            des = self.m_des_list[i]

            if os.path.exists(des):
                if to_unicode(sou).replace("\\", "/").strip().lower()==to_unicode(des).replace("\\", "/").strip().lower(): #如果源路径和目录的一致的话。跳过,本地不做移动，在线还是要做移动
                    continue
                local_des_exist_list.append(des)
    

        #生成本地文件移动的列表,并且开始移动本地历史---------
        if len(local_des_exist_list)>0:
            #生成本地文件移动的列表
            t_move_sou_list=[]
            t_move_des_list=[]
            for t_des in local_des_exist_list:
                t_name = os.path.basename(t_des)
                t_dir = os.path.dirname(t_des)
                t_move_sou_list.append(t_des)
                
                lis = os.path.splitext(t_name)
                if len(lis) == 2:
                    backup_path = t_dir+"/history/backup/"+lis[0]+"."+_lib.now('%Y%m%d%H%M%S')+lis[1]
                else:
                    backup_path = t_dir+"/history/backup/"+t_name+"."+_lib.now('%Y%m%d%H%M%S')
                t_move_des_list.append(backup_path)

            #开始移动本地
            if len(t_move_sou_list)>0 and len(t_move_des_list)>0:
                self.m_ct_file.move_files(t_move_sou_list, t_move_des_list)
        
        return True
    
    #同名版本移动到历史
    def same_version_move_to_history(self):
        t_server = self.m_filebox_info_dict["server"]
        t_online_dir=to_unicode(self.m_path).replace(t_server, "/")  #有替换{ver}
        
        #20221201获取目标的文件名,移动旧版本按目标存在的,防止第一版和第二版提交只是大小写不一致，导致不能移动到历史
        def find_des(a_dir):
            tmpdic={}
            import glob
            for tmp_path in glob.iglob(os.path.join(a_dir, "*")):
                tmpname = os.path.basename(tmp_path)
                tmpdic[to_unicode(tmpname).lower()] = tmpname
            return tmpdic
        t_exist_des_name_dict = find_des(self.m_path) #{小写名字: 正常名字}

        t_dic={"file":[], "folder":[]}
        file_path_list = [] #记录的目标的详细的所有的文件列表
        local_des_exist_list=[]#本地目标文件存在的文件列表,用于移动到history
        for i in range(len(self.m_sou_list)):
            sou = self.m_sou_list[i]
            des = self.m_des_list[i]
            name = os.path.basename(des)

            #20221201--替换成正确的名字版本
            if to_unicode(name).lower() in t_exist_des_name_dict: #目标有存在的用目标的文件名
                name= t_exist_des_name_dict[to_unicode(name).lower()]
                des = self.m_path+"/"+ name

            if os.path.isfile(sou):#用源文件来判断是否是文件。用目标判断的话。有可能不存在
                t_dic["file"].append(name)
            else:
                t_dic["folder"].append(name)
            
            if os.path.exists(des):
                if to_unicode(sou).replace("\\", "/").strip().lower()==to_unicode(des).replace("\\", "/").strip().lower(): #如果源路径和目录的一致的话。跳过,本地不做移动，在线还是要做移动
                    continue
                local_des_exist_list.append(des)

        
        #获取文件名对应的version数据--{name:{"id":xx, "ver":xxx, "is_file":"N"},  aa.py:{"id":xx, "ver":xxx, "is_file":"N"}} id为file的id或者media_folder的ID
        t_res_dic = self.m_fun("file", "get_version_data", {"db": self.m_db, "module": self.m_module, "module_type": self.m_module_type, "online_dir": t_online_dir, "file_name_array": t_dic["file"], "folder_name_array": t_dic["folder"]})
        t_res_dic=dict(t_res_dic)
        
        #开始移动旧版本的文件或者文件夹到/history/v###下-------------------
        #生成file log移动的列表---
        t_online_move_list=list(t_res_dic.values())# [{"id":xx, "ver":xxx, "is_file":"N"}]--用于file进行移动到历史
        
        #生成本地文件移动的列表,并且开始移动本地历史---------
        if len(local_des_exist_list)>0:
            old_log_path=self.m_path+"/history/publish_"+self.m_id+".json" #旧log路径
            new_log_path=self.m_path+"/history/metadata/publish_"+self.m_id+".json" #新log路径            
            log_id = self.get_new_publish_json_id(new_log_path)
            if str(log_id).strip()!="":
                t_ver_dict = self.m_fun("metadata", "get_data", {"db": self.m_db, "id": log_id})
            else:
                t_ver_dict = self.get_old_publish_json(old_log_path)
            
            #20221201--将文件名都改成小写进行备份,防止中间名称更改大小写
            t_new_ver_dict={}
            for t_key in t_ver_dict:
                t_new_ver_dict[to_unicode(t_key).lower()]=t_ver_dict[t_key]

            #生成本地文件移动的列表
            t_move_sou_list=[]
            t_move_des_list=[]
            t_backup_time = _lib.now('%Y-%m-%d-%H-%M-%S')
            for t_des in local_des_exist_list:
                t_name = os.path.basename(t_des)
                t_dir = os.path.dirname(t_des)

                #20221201--旧的文件也需要备份,没有找到ver记录的
                t_check_name = to_unicode(t_name).lower() #转为小写，防止后面版本的资产名称或者镜头号改大小写
                if t_check_name in t_new_ver_dict and isinstance(t_new_ver_dict[t_check_name], dict) and "ver" in t_new_ver_dict[t_check_name]:
                    t_ver="v"+t_new_ver_dict[t_check_name]["ver"] #默认加上v
                    t_move_sou_list.append(t_des)
                    t_move_des_list.append(t_dir+"/history/"+t_ver+"/"+t_name)
                else:
                    #20221201-旧的文件也需要备份,没有找到ver记录的
                    t_move_sou_list.append(t_des)
                    t_move_des_list.append(t_dir + "/history/backup/" + t_backup_time + "/" + t_name)
            
            #开始移动本地
            if len(t_move_sou_list)>0 and len(t_move_des_list)>0:
                self.m_ct_file.move_files(t_move_sou_list, t_move_des_list)
        
        #移动file log的记录到history
        if len(t_online_move_list)>0:
            self.m_fun("file", "move_to_history", {"db": self.m_db, "online_dir": t_online_dir, "data_array": t_online_move_list})

        return True 
    

    # 上传version和上传file
    def upload_version(self):
        # 获取文件框信息
        t_submit_dir =  self.m_path #有替换{ver}
        t_sign = self.m_filebox_info_dict["sign"]
        #t_submit_type = self.m_filebox_info_dict["submit_type"]
        #t_is_submit = self.m_filebox_info_dict["is_submit"]
        t_server_id = self.m_filebox_info_dict["server_id"]
        t_server = self.m_filebox_info_dict["server"]
        t_version_type = self.m_filebox_info_dict["version_type"]
        
        ver_log={} #写入版本的日志（publish.json）
    
        # 生成path_list
        file_data_list = [] #记录文件的信息列表,用file::create
        
        online_submit_path_list=[]
        online_submit_file_path_list=[]
        online_submit_dir=to_unicode(t_submit_dir).replace(t_server, "/")
        
        for i in range(len(self.m_sou_list)):
            sou=self.m_sou_list[i]
            des=self.m_des_list[i]
            name=os.path.basename(des)
            if os.path.isfile(sou):
                ver_log[name]={"ver":"", "is_file":"Y"} #后面再加版本号
                file_data_list.append({"path":des, "size": str(self.m_ct_file.get_size(sou)), "modify_time":self.m_ct_file.get_modify_time(sou)})
                
                online_submit_file_path_list.append(to_unicode(des).replace("\\", "/").replace( to_unicode(t_server).replace("\\", "/"), "/")) #20210623
                
            else:
                #目录
                #遍历源文件，最终生成目标的列表
                for n in self.m_ct_file.get_file_with_walk_folder(sou):
                    n=to_unicode(n).replace("\\", "/")
                    sou=to_unicode(sou).replace("\\", "/")
                    des=to_unicode(des).replace("\\", "/")
                    t_new_des= n.replace(sou, des) 
                    file_data_list.append({"path":t_new_des, "size": str(self.m_ct_file.get_size(n)), "modify_time":self.m_ct_file.get_modify_time(n)})
                    
                    online_submit_file_path_list.append(to_unicode(t_new_des).replace("\\", "/").replace( to_unicode(t_server).replace("\\", "/"), "/")) #20210623
                    
                    
                ver_log[name]={"ver":"", "is_file":"N"} #后面再加版本号
            online_submit_path_list.append(to_unicode(des).replace("\\", "/").replace( to_unicode(t_server).replace("\\", "/"),  "/")) #20210623

        t_os = _lib.get_os()

        version_field_data={}
        if not self.m_is_upgrade_version: #不升版本的
            version_id=self.m_filebox_info_dict["last_max_version_id"] #用文件框获取到的信息---20210702
            version=self.m_filebox_info_dict["last_max_version"] #用文件框获取到的信息---20210702
            #不升级版本的。删除原先的version记录
            self.m_fun("version", "delete", {"db": self.m_db, "id_array": [version_id]})
            version_field_data={"#id":version_id, "entity":version}
            
        else:
            version_field_data={"entity":self.m_version} #版本号是从前面传的
            if not "#id" in self.m_version_argv:
                version_field_data["#id"]=_lib.uuid()
            else:
                version_field_data["#id"]=self.m_version_argv["#id"]
        
        # 写到内存中
        self.m_version_id = version_field_data["#id"]
        
        # 先插入file记录
        file_data = self.m_fun("file", "create", {"db": self.m_db, "module": self.m_module, "module_type": self.m_module_type, "link_id": self.m_id, "version_id": self.m_version_id, \
                                                    "file_data_array": file_data_list,  "server_id": t_server_id, "os": t_os, "submit_dir":t_submit_dir, "is_from_api":False})

        self.m_file_log_dict= file_data  # 提交文件的记录。。用于在线文件使用{在线路径: file_id}


        # 再创建version
        version_field_data=dict(list(self.m_version_argv.items())+ list(version_field_data.items())) #20211101添加其他版本的参数
        version_data = self.m_fun("version", "client_create", {"db": self.m_db, "link_id": self.m_id, "sign": t_sign, "submit_dir": online_submit_dir, "submit_path_array": online_submit_path_list, "server_id": t_server_id, "field_data_array":version_field_data})
        if not isinstance(version_data, dict) and "id" not in version_data and "version" not in version_data:
            raise Exception("create version data error")      
    
        # version_id=version_data["id"]
        version=version_data["version"]        

        
        #写入本地日志(只有同名版本才写入)v6.2---用于网盘下载同名版本的文件使用
        if t_version_type=="same":
            #添加上版本号
            for key in ver_log:
                ver_log[key]["ver"]=version
            #20220915 跳过生成json文件
            if self.m_argv_dict.get('write_json',True) is False:
                return True
            #开始写入
            try:
                old_log_path=t_submit_dir+"/history/publish_"+self.m_id+".json"
                new_log_path=t_submit_dir+"/history/metadata/publish_"+self.m_id+".json"
                t_create_dir = os.path.dirname(new_log_path)
                if not os.path.exists(t_create_dir):
                    try:
                        os.makedirs(t_create_dir)
                    except:
                        raise Exception("Make dirs error ({})".format(repr(t_create_dir)))
                try:
                    tmp_log_id = self.get_new_publish_json_id(new_log_path)
                    t_dict = ver_log
                    if tmp_log_id=="":
                        #表示第一次生成,要合并旧的log
                        old_dict = self.get_old_publish_json(old_log_path)
                        t_dict=dict(list(old_dict.items())+ list(ver_log.items()))
                        
                    #写入到数据库
                    log_id = self.m_fun("metadata", "set_data", {"db": self.m_db, "id": tmp_log_id, "data": t_dict})                    
                    #id写入到本地
                    if tmp_log_id != log_id:
                        with open(new_log_path, 'wb') as fw:
                            fw.write(log_id.encode())
                            
                        
                except Exception as e:
                    raise e              
            except Exception as e:
                raise Exception("create same version log fail:\n {}".format(e))

        return True
    
    def get_old_publish_json(self, a_log_path):
        #读取旧的记录
        old_dict={}
        if os.path.exists(a_log_path):
            try:
                with open(a_log_path, 'rb') as fr:
                    old_json=fr.read()
                    try:
                        if old_json!="" and old_json != b'': #20210802
                            old_dict=json.loads(old_json)
                            if not isinstance(old_dict, dict):
                                old_dict={}
                    except  Exception as e:
                        raise e
                    
            except Exception as e:
                raise e
        return old_dict
    
    def get_new_publish_json_id(self, a_log_path):
        t_id = ""
        if os.path.exists(a_log_path):
            try:
                with open(a_log_path, 'rb') as fr:
                    t_id=fr.read()
            except Exception as e:
                raise e
        return to_unicode(t_id)      
    
    def is_match(self, a_rule, a_string):
        a_rule=re.sub('([()[]|])', r'[\1]', a_rule)
        a_rule=a_rule.replace("#", "[0-9]").replace("?", "[a-zA-Z]").replace("*", "[\s\S]*").replace(".", "\.")
        res=re.match("^"+a_rule+"$", a_string)
        if res==None:
            return False
        return True
    
    #检查命名规则
    def check_rule(self):
        rule_list=self.m_filebox_info_dict["rule"]
        new_rule_list=[]
        error_list=[]
        for rule in rule_list:
            rule=to_unicode(rule).replace("{ver}", self.m_version)
            new_rule_list.append(rule)
            
        #遍历源文件找到最小的版本号
        for sou in self.m_sou_list:
            t_base_name=os.path.basename(sou)
            is_has_match=False
            for i in range(len(new_rule_list)):
                #符合命名规则，获取版本号
                if self.is_match(new_rule_list[i], t_base_name):   
                    is_has_match=True
                    break
            
            if not is_has_match:
                error_list.append(t_base_name)
                    
        if len(error_list)>0:
            raise Exception("File rule not match: \n Rule: {}\n File: {}".format( repr(new_rule_list), repr(error_list) ) )
            
        return True