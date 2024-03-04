# coding: utf-8
import json
from ._compat import *
from six.moves.urllib.parse import urlparse
#try:
    #import requests

#except Exception, e:
    #raise Exception("Import module( requests) fail")
    
class _con:

    @staticmethod
    def is_cgtw_domain(a_http_server):
        # 判断server是否是cgteamwork二级域名
        hostname = urlparse("https://" + a_http_server).hostname
        if isinstance(hostname, basestring):
            return hostname.endswith("cgteamwork.com")
        return False

    @staticmethod
    def get_server_ip(a_request_session, a_http_server):
        #说明填写时cgtw的二级域名
        if _con.is_cgtw_domain(a_http_server):
            try:
                #t_ip="update.cgteamwork.com:60000"
                t_ip="114.215.190.60:60000"                
                res = a_request_session.get("http://"+t_ip+"/index.php?controller=c_lic&method=get_ddns_ip&ddns_name="+a_http_server,  timeout=20)            
                ip=res.text
                if ip!="":
                    if to_unicode(a_http_server).find(":")==-1:
                        return ip
                    else:
                        lis=to_unicode(a_http_server).split(":")
                        return ip+":"+lis[1]
            except Exception as e:
                pass
        return a_http_server
    
    @staticmethod
    def send(a_request_session, a_http_server, a_token, a_controller, a_method, a_data_dict):
        try:
            a_data_dict["controller"]=a_controller
            a_data_dict["method"]=a_method
            a_data_dict["app"]="api"
            if not "language" in a_data_dict or not a_data_dict["language"] in ["en", "zh"]:
                a_data_dict["language"]="en"
            
            t_post_data={"data": json.dumps(a_data_dict)}        
            req_headers = {"cookie":"token="+a_token}
            res = a_request_session.post("https://"+a_http_server+"/api.php", data=t_post_data, headers=req_headers, verify=False)
        except Exception as e:
            raise Exception("_con.send, post data timeout.{}".format(e))
        else:
            try:
                T_dict_data=json.loads(res.text)
            except Exception as  e:
                raise Exception(e)
            else:
                if not isinstance(T_dict_data, dict):
                    raise Exception(repr(res))
                else:
                    if ('data' in T_dict_data)==False or ('code' in T_dict_data)==False or ('type' in T_dict_data)==False :
                        raise Exception(repr(res))
                    else:
                        if T_dict_data['code']=='0' and T_dict_data['type']=='msg':
                            raise Exception(repr(T_dict_data['data']))
                        elif T_dict_data['code']=='2':
                            raise Exception("_con.send, the token has expired, please login")
                        
                        return T_dict_data["data"]
    
 