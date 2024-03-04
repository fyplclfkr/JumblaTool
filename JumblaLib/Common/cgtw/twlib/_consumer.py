#!/usr/bin/env python
#coding:utf-8
import os, sys
import sys
import six
import json
import threading
from ._compat import *

#import logging#测试使用
#logging.basicConfig()
#import ssl
import time
try:
    if sys.version_info[0] == 2:
        inside_path=os.path.dirname(os.path.dirname(__file__)).replace("\\", "/")+"/py2lib"
    elif sys.version_info[1] == 9:
        inside_path=os.path.dirname(os.path.dirname(__file__)).replace("\\", "/")+"/py39lib"
    else:
        inside_path=os.path.dirname(os.path.dirname(__file__)).replace("\\", "/")+"/py3lib"
    
    inside_path in sys.path or sys.path.append(inside_path)
    import ctlib
    import websocket
    import requests
    requests.packages.urllib3.disable_warnings()

except Exception as e:
    raise Exception("Import module(websocket, requests) fail. {}".format(e))


class _consumer:
    '''消费者'''
    
    def __init__(self, a_msg_server_ip, a_app_key, a_tw):
        if not isinstance(a_msg_server_ip, basestring) or not isinstance(a_app_key, basestring):
            raise Exception("_consumer.__init__, argv error (str, str, obj)")   
        
        if to_unicode(a_msg_server_ip).find("wss://")==-1:
            a_msg_server_ip="wss://"+a_msg_server_ip
        self.__m_url=a_msg_server_ip
        self.__m_app_key=a_app_key
        self.__m_tw=a_tw
        self.__m_con=None
        self.__m_is_stop=False
    
    def working(self, a_dict, a_tw):
        '''继承的方法'''
        pass
    
    def __new_task(self, a_server_connect_id):
        '''获取相关任务'''
        data_dict=self.__m_tw.send_web("msg_queue", "get", {"app_key": self.__m_app_key, "connection_id":a_server_connect_id})
        if isinstance(data_dict, dict) and "queue_id" in data_dict and "argv" in data_dict and isinstance(data_dict["argv"], dict):
            queue_id=data_dict["queue_id"]
            if queue_id=="":
                return
            self.working(data_dict["argv"], self.__m_tw)
    
            
    def run(self):
        '''阻塞执行'''
        while True:
            if self.__m_is_stop:
                break
            try:
                self.__m_con=mq_con(self.__m_url, self.__m_app_key, self.__new_task)
                self.__m_con.run()                
            except  Exception as e:
                self.__m_con=None
                raise Exception(e)   
            time.sleep(60)#60秒重新连接        

    def exec_success(self):
        '''任务执行成功'''
        if hasattr(self.__m_con, "get_connect_id"):
            connect_id=self.__m_con.get_connect_id()
            if connect_id!="":
                return self.__m_tw.send_web("msg_queue", "success", {"connection_id":connect_id})
        return False
    
    def exec_fail(self, a_error_msg=""):
        '''任务执行失败'''
        if hasattr(self.__m_con, "get_connect_id"):
            connect_id=self.__m_con.get_connect_id()
            if connect_id!="":        
                return self.__m_tw.send_web("msg_queue", "fail", {"msg": a_error_msg, "connection_id":connect_id})
        return False
    
    def get_task(self):
        '''获取任务'''
        if hasattr(self.__m_con, "get_task"):
            return self.__m_con.get_task()
        return False
        
    def stop(self):
        '''停止'''
        self.__m_is_stop=True
        if hasattr(self.__m_con, "stop"):
            return self.__m_con.stop()
        return False


class mq_con:
    '''连接消息服务器队列'''
    def __init__(self, a_url, a_app_key, a_new_task_fun):
        self.m_ws = None
        self.m_url = ''       
        self.m_server_connect_id="" #服务器的connection_id
        self.m_app_key=a_app_key
        self.m_new_task_fun=a_new_task_fun
        self.m_live_timer=None
        if isinstance(a_url, basestring) == False or a_url.strip() == '':
            raise Exception("mq_con.__init__, argv error(str, str, fun)")        
        self.m_url = a_url
        #连接
        self.__connect()
        

    def stop(self):
        '''关闭连接'''
        self.m_ws.close()
        return True
    
    def run(self):
        '''阻塞执行'''
        self.m_ws.run_forever(sslopt={"cert_reqs": 0})
    
    def get_connect_id(self):
        '''获取消息服务器的socket_id'''
        return self.m_server_connect_id
    
    def get_task(self):
        '''获取新的任务'''
        self.__send({"method":"get_task", "app_key": self.m_app_key})
        return True
    
    
    def __connect(self):
        '''连接'''
        try:
            self.m_ws = websocket.WebSocketApp(self.m_url,
                                               on_message= self.__on_message, 
                                               on_error = self.__on_error,
                                               on_close= self.__on_close,
                                               on_open= self.__on_open)
        except Exception as e:
            self.m_ws = None
            raise Exception(e)
        print("connect:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        
        
    def __on_message(self, a_ws, a_message):
        '''消息进入'''
        dic=self.__get_data(a_message)
        if isinstance(dic, dict) and "method" in dic:
            method=dic["method"]
            if method=="get_connection_id":#得到服务器的connection_id
                self.m_server_connect_id=dic["connection_id"]
                #print "get connenct_id ",self.m_server_connect_id
                self.get_task()#有时候第一次连接，会收不到new_task
                
            elif method=="new_task":#有新的任务
                if self.m_server_connect_id=="":
                    return
                self.m_new_task_fun(self.m_server_connect_id)
                
    def __on_error(self, a_ws, a_error_obj):
        '''连接错误'''
        #暂停心跳
        if hasattr(self.m_live_timer, "cancel"):
            self.m_live_timer.cancel()
        self.m_server_connect_id=""
        print("on_error:", repr(a_error_obj), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    
    def __on_close(self, a_ws):
        '''连接关闭'''
        #暂停心跳
        if hasattr(self.m_live_timer, "cancel"):
            self.m_live_timer.cancel()
        self.m_server_connect_id=""
    
    def __on_open(self, a_ws):
        '''连接成功'''
        
        #先注册消费者
        self.__send({"method":"init_consumer", "app_key": self.m_app_key})
        
        #启动定时心跳
        self.__live()

    def __live(self):
        '''心跳'''
        self.__send({}, True)
        
        self.m_live_timer=threading.Timer(40, self.__live)#每60秒的心跳定时器,这个start后。只会执行一次，因此要循环调用自己
        self.m_live_timer.start()
    
    def __send(self, a_data_dict, a_is_live=False):
        if a_is_live:
            return self.m_ws.send("live|")
        else:
            return self.m_ws.send("queu|"+json.dumps({"data":a_data_dict}))
    
    def __get_data(self, a_msg):
        '''解析数据'''
        try:
            recv = json.loads(a_msg)
        except Exception as e:
            raise Exception(e)
        if isinstance(recv, dict) == False:
            raise Exception(repr(recv))
        if not isinstance(recv, dict) or "data" not in recv:
            return {}
        data = recv["data"]
        if "code" not in recv:
            return data
        else:
            if recv["code"]=="1":
                return data
            else:
                #code为0的
                print("data error:", repr(data))
                return {}

