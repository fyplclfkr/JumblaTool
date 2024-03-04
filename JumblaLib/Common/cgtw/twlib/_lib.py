# coding: utf-8
import os, json
import  platform
import uuid
import time
import hashlib
import datetime
import re
import six 
from ._compat import *

class _lib:
    
    @staticmethod
    def is_json(value):
        try:
            eval(value)
        except Exception as e:
            pass
            return False
        else:
            return True

    @staticmethod
    def decode(value):#json_decode
        if _lib.is_json(value):
            return json.loads(value)
        else:
            return value                

    @staticmethod
    def encode(value):#json_encode
        if isinstance(value, dict):
            try:
                json_str=json.dumps(value)
                return json_str
            except Exception as e:
                raise Exception(e)
        else:
            return False

    @staticmethod
    def format_data_to_dict(a_data_list, a_sign_list):#返回值为单层array, 用于get_one
        if isinstance(a_data_list, list)==False or isinstance(a_sign_list, list)==False:
            raise Exception("_lib.format_data_to_dict argv error, format_data_to_dict(list, list)")                        
        if len(a_data_list)!=len(a_sign_list):
            raise Exception("_lib.format_data_to_dict data error , (a_data_list's length is not equal to a_sign_list's)")
        t_result_dict={}
        n=len(a_data_list)-1
        for i in range(len(a_data_list)):
            #t_sign=a_sign_list[i].replace("#", "")
            t_sign=a_sign_list[i]
            if i==n and ".id" in a_sign_list[i]:
                t_sign=a_sign_list[i].split(".")[-1].strip()
            t_result_dict[t_sign]=a_data_list[i]
        return t_result_dict

    @staticmethod
    def format_data(a_data_list, a_sign_list):#多层
        if isinstance(a_data_list, list)==False or isinstance(a_sign_list, list)==False:
            raise Exception("_lib.format_data argv error, format_data(list, list)")
        t_result_array=[]
        for data in a_data_list:
            t_tmp_dict=_lib.format_data_to_dict(data, a_sign_list)
            if t_tmp_dict==False:
                raise Exception("_lib.format_data data error")
            t_result_array.append(t_tmp_dict)
        return t_result_array
    
    @staticmethod
    def get_os():
        t_os=platform.system().lower()
        if t_os=="windows":
            return "win"
        elif t_os=="linux":
            return "linux"
        elif t_os=="darwin":
            return "mac"
        else:
            return ""
        
    @staticmethod
    def uuid():
        return str(uuid.uuid4())
    
    @staticmethod
    def now(a_format='%Y-%m-%d %H:%M:%S'):
        '''
        描述: 取当前时间
        返回: 字符串
        '''
        t_time=""
        try:
            t_time=time.strftime(a_format, time.localtime(time.time()))
        except Exception as e:
            pass
        return t_time    
    
    
    @staticmethod
    def get_tmp_path():
        '''
        描述: 取temp路径
        返回: 字符串
        '''
        if _lib.get_os() == 'win':
            if _lib.is_win_chinese_account():
                # 先判断是否sys_cgteamwork目录，如果有的话使用sys_cgteamwork，没有的话使用public目录
                users_dir = os.path.dirname(os.environ["USERPROFILE"])
                path = users_dir + "\\sys_cgteamwork\\temp"
                if os.path.exists(path):
                    return path
                else:
                    path = users_dir + "\\public\\\Documents\\tmp"
                    if not os.path.exists(path):
                        os.makedirs(path)
                    return path
            return os.environ["TMP"]
        else:
            return "/tmp"   
        
    @staticmethod
    def is_win_chinese_account():

        # 判断是否为window的中文账号
        if _lib.get_os() != "win":
            return False

        try:
            t_user_profile_dir = os.environ["USERPROFILE"]
            t_account = os.path.basename(t_user_profile_dir)
            t_account = t_account.replace(".", "")  # 先去掉.
            match = re.compile(u'[^\w-]')  # \w        等同于[a-z0-9A-Z_]匹配大小写字母、数字和下划线
            res = match.search(t_account)
            if res:
                return True
            else:
                return False
        except:
            return False
            
    @staticmethod
    def get_text_md5(a_text):
        '''
        描述: 取文本md5
        调用: get_text_md5(a_text)
              --> a_string为str/unicode
        返回: 字符串
        '''        

        if not isinstance(a_text, basestring):
            raise Exception("a_text is str/unicode")
        md5=hashlib.md5()
        if _lib.__is_utf8(a_text):
            a_text=a_text.encode('unicode-escape').decode('string_escape')#unicode转str
        else:
            try:
                a_text=a_text.encode('unicode-escape').decode('string_escape')#unicode转str
            except:
                pass

        md5.update(a_text)
        return md5.hexdigest()    
    
    @staticmethod
    def limit_length(a_id_list):
        """
        描述:列表长度不得大于20000.
        """
        if not isinstance(a_id_list, list) or len(a_id_list)>20000:
            raise Exception('id_list length greater than 20000.')
        
    @staticmethod
    def get_modify_time(a_path):
        '''
        描述: 读取文件的修改时间,出错抛出异常
        调用: get_modify_time(a_path)
              -->  a_path 为文件路径
        返回: 字符串 如'2018-01-01 22:01:22'
        '''
        if not isinstance(a_path, basestring):
            raise Exception("argv error ,there must be ( str/unicode)")
        if os.path.exists(a_path) == False:
            raise Exception("the a_path not exist")

        t_timestamp = os.path.getmtime(a_path.replace("\\", "/"))
        date = datetime.datetime.fromtimestamp(t_timestamp)
        return date.strftime('%Y-%m-%d %H:%M:%S') 
    
    @staticmethod
    def get_config_path(a_is_user=False):
        '''
        描述: 获取config.ini的路径, config.ini中获取server, msg_port,https_port用a_is_user=False,其他的key用a_is_user=True
        调用: get_config_path(a_bin_path, a_is_user=False)
        返回: 字符串
        '''
        
        t_bin_path = to_unicode(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))).replace("\\", "/")
        pub_config_path = t_bin_path + "/cgtw/config.ini"
        if not os.path.exists(pub_config_path):
            Exception("The config.ini not exist")
        if not a_is_user:
            return pub_config_path
        
        import six.moves.configparser as configparser
        config = configparser.ConfigParser()
        config.read(pub_config_path)
        try:
            t_is_share_client=False
            if config.has_option("General", "share_client") and config.get("General", "share_client").lower().strip() == "y":
                t_is_share_client=True
            return os.path.join(_lib.get_app_config_dir(t_is_share_client), "config.ini").replace("\\", "/")
        except:
            Exception("Get config.ini failed")
    
    @staticmethod
    def get_app_config_dir(a_is_share_client):
        t_bin_path = to_unicode(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))).replace("\\", "/")
        if a_is_share_client:
            config_dir = os.path.abspath(os.path.join(_lib.__get_user_home(), "cgteamwork", "config", _lib.__get_app_hash(t_bin_path)))
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
        else:
            config_dir = os.path.realpath(os.path.abspath(t_bin_path + "/cgtw"))
        return config_dir

    #--------------------------私有----------------------------------
    @staticmethod
    def __is_utf8(a_data):
        try:
            to_unicode(a_data).encode('gb2312')#执行失败为带有中文的str
        except:
            return False
        else:
            return True        

    @staticmethod
    def __get_user_home():
        if _lib.get_os() == "win":
            user_profile = os.getenv("USERPROFILE")
            try:
                user_name = os.path.basename(user_profile).replace(".", "")
                pattern = re.compile(u'[^\w-]')  # \w	等同于[a-z0-9A-Z_]匹配大小写字母、数字和下划线
                match = pattern.search(user_name)
                if match:
                    users_dir = os.path.dirname(user_profile)
                    sys_dir = os.path.abspath(os.path.join(users_dir, "sys_cgteamwork"))
                    if os.path.exists(sys_dir):
                        return sys_dir
                    else:
                        return os.path.abspath(os.path.join(users_dir, "Public", "Documents"))
            except:
                pass
            return os.path.abspath(user_profile)
        else:
            return os.path.abspath(os.getenv("HOME"))
    @staticmethod
    def __get_app_hash(a_bin_path):
        app_dir = os.path.realpath(os.path.abspath(a_bin_path + "/cgtw"))
        hash_obj = hashlib.md5()
        hash_obj.update(app_dir.encode("utf-8"))
        return hash_obj.hexdigest()

