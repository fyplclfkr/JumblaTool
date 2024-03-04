# coding: utf-8
import os
import json
import six
from ._lib import _lib
from ._compat import *
try:
    #from websocket import create_connection
    from websocket import *
except Exception as e:
    raise Exception("Import module( websocket) fail")


class _con_local:
    http_server_port = 64998 #tw初始化的时候会重置
    socket_server_port = 64999 #tw初始化的时候会重置

    @staticmethod
    def send_http(T_module, T_database, T_action,  T_other_data_dict, T_type="send"):
        T_tw_ws = ""
        T_result = ""

        # 修正连接houdini17有问题-----------
        try:
            if _lib.get_os() == "win":
                import socket
                if hasattr(socket, "TCP_KEEPCNT"):
                    DEFAULT_SOCKET_OPTION.pop()
                if hasattr(socket, "TCP_KEEPINTVL"):
                    DEFAULT_SOCKET_OPTION.pop()
        except Exception as e:
            pass
        # 修正连接houdini17有问题-----------

        try:
            T_tw_ws = create_connection("wss://127.0.0.1:%d" % _con_local.http_server_port, sslopt={"cert_reqs": 0})
        except Exception as  e:
            raise Exception("_con_local.send_http,  Cgteamwork client is not login \n {}".format(e))
        try:
            new_data_dict = dict(list({"module": T_module, "db": T_database, "action": T_action}.items())+list(T_other_data_dict.items()))
            T_tw_ws.send("#@start@#"+json.dumps({"data": new_data_dict, "name": "python",  "type": T_type})+"#@end@#")
        except Exception as  e:
            raise Exception("_con_local.send_http, send data to cgteamwork fail \n{}".format(e))
        else:
            if isinstance(T_type, basestring) and to_unicode(T_type).strip().lower() == "get":
                try:
                    T_recv = T_tw_ws.recv()
                    T_tw_ws.close()
                except Exception as  e:
                    raise Exception("_con_local.send_http, get data from (127.0.0.1) fail \n {}".format(e))
                else:
                    T_dict_data = json.loads(T_recv)
                    if not isinstance(T_dict_data, dict):
                        raise Exception(repr(T_recv))
                    else:
                        if ('data' in T_dict_data) == False:
                            raise Exception(repr(T_recv))
                        else:
                            return _lib.decode(T_dict_data["data"])
            else:
                return True

    @staticmethod
    def send_socket(T_sign, T_method, T_data, T_type="get"):
        T_tw_ws = ""
        T_result = ""

        # 修正连接houdini17有问题-----------
        try:
            if _lib.get_os() == "win":
                import socket
                if hasattr(socket, "TCP_KEEPCNT"):
                    DEFAULT_SOCKET_OPTION.pop()
                if hasattr(socket, "TCP_KEEPINTVL"):
                    DEFAULT_SOCKET_OPTION.pop()
        except Exception as e:
            pass
        # 修正连接houdini17有问题-----------

        try:
            T_tw_ws = create_connection("ws://127.0.0.1:%d" % _con_local.socket_server_port)
        except Exception as  e:
            raise Exception("_con_local.send_socket, Cgteamwork client is not login, error:{}".format(e))
        try:
            T_tw_ws.send(json.dumps(dict(list({"sign": T_sign, "method": T_method, "type": T_type}.items())+list(T_data.items()))))
        except Exception as  e:
            raise Exception(e)
        else:
            try:
                T_recv = T_tw_ws.recv()
                T_tw_ws.close()
            except Exception as  e:
                raise Exception(e)
            else:
                try:
                    T_dict_data = json.loads(T_recv)
                except Exception as  e:
                    raise Exception(e)
                else:
                    if not isinstance(T_dict_data, dict):
                        raise Exception(repr(T_recv))
                    else:
                        if ('data' in T_dict_data) == False or ('code' in T_dict_data) == False:
                            raise Exception(repr(T_recv))
                        else:
                            if T_dict_data['code'] == '0':
                                raise Exception(repr(T_dict_data['data']))
                            return _lib.decode(T_dict_data["data"])
