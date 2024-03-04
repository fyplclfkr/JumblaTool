# coding: utf-8
import sys
from ._con_local import _con_local

G_cgtw_cache_argv_data = None

class _client:
    
    @staticmethod
    def _get_uuid():
        if len(sys.argv) < 2 :
            return ""
        else:
            return sys.argv[-1]
    
    @staticmethod
    def __get_argv_data():
        global G_cgtw_cache_argv_data
        if not G_cgtw_cache_argv_data:
            t_dic={"plugin_uuid":_client._get_uuid()}
            G_cgtw_cache_argv_data = _con_local.send_socket("main_widget", "get_plugin_data", t_dic, "get")
        return G_cgtw_cache_argv_data		

    @staticmethod
    def get_argv_key(T_key, T_argv_data={}):
        if T_argv_data=={}:
            T_argv_data=_client.__get_argv_data()
        if isinstance(T_argv_data, dict) and 'argv' in T_argv_data:
            if isinstance(T_argv_data['argv'], dict) and T_key in T_argv_data['argv']:
                return T_argv_data['argv'][T_key]
        return False	

    @staticmethod
    def get_sys_key(T_key):
        T_argv_data=_client.__get_argv_data()
        if isinstance(T_argv_data, dict) and T_key in T_argv_data:
            return T_argv_data[T_key]					
        return False	
        
    @staticmethod
    def get_database():
        return _client.get_sys_key('database')

    @staticmethod
    def get_id():
        return _client.get_sys_key('id_list')

    @staticmethod
    def get_link_id():
        return _client.get_sys_key('link_id_list')

    @staticmethod
    def get_link_module():
        return _client.get_sys_key('link_module')
        
    @staticmethod
    def get_module():
        return _client.get_sys_key('module')	
    
    @staticmethod
    def get_module_type():
        return _client.get_sys_key("module_type")
    
    @staticmethod
    def get_file():
        return _client.get_sys_key('file_path_list')

    @staticmethod
    def get_des_file():                              #获取拖入目标完整路径
        return _client.get_sys_key("des_file_path_list")
    
    @staticmethod
    def get_event_action():
        return _client.get_sys_key('action')
    @staticmethod
    def get_event_fields():
        return _client.get_sys_key('field_sign_list')
    @staticmethod
    def get_filebox_id():
        return _client.get_sys_key('filebox_id')
    