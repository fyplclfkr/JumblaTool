#coding:utf-8
import os
import sys
import six
import types
from ._compat import *
import ctlib
class _dom:
    
    m_image_list = [".jpg", ".jpeg", ".png", ".exr", ".tiff", ".tif", ".tga", ".dpx",'.gif']
    
    m_video_list = [
        ".3g2", ".3gp", ".3gp2", ".3gpp", ".amv", ".asf", ".avi", ".bik", ".divx", ".drc", ".dv",
        ".f4v", ".flv", ".gvi", ".gxf", ".iso", ".m1v", ".m2v", ".m2t", ".m2ts", ".m4v", ".mkv",
        ".mov", ".mp2", ".mp2v", ".mp4", ".mp4v", ".mpe", ".mpeg", ".mpeg1", ".mpeg2", ".mpeg4",
        ".mpg", ".mpv2", ".mts", ".mtv", ".mxf", ".mxg", ".nsv", ".nuv", ".ogg", ".ogm", ".ogv",
        ".ogx", ".ps", ".rec", ".rm", ".rmvb", ".rpl", ".thp", ".tod", ".ts", ".tts", ".txd",
        ".vob", ".vro", ".webm", ".wm", ".wmv", ".wtv", ".xesc"
    	]
    
    m_total_size           = 0 #总大小
    m_already_perform_size = 0 #已执行大小
    m_current_name         = '' #当前下载的文件名称
    m_call_back            = None
    m_current_size         = 0 
    @staticmethod
    def convert(a_list):
        t_new_list = []
        for _file in a_list:
            if not isinstance(_file, basestring):
                raise Exception('_dom.convert Invalid format,Lists can only pass str/unicode')
            t_basename = os.path.basename(_file)
            t_suffix   = os.path.splitext(t_basename)[1].lower()
            if t_suffix in _dom.m_image_list:
                t_new_list.append({'type':'image','path':_file})
            elif t_suffix in _dom.m_video_list:
                t_new_list.append({'type':'video','path':_file})
            else:
                t_new_list.append({'type':'attachment','path':_file})
        return t_new_list
            
            
    @staticmethod
    def to_list(a_http_ip, a_token, a_db, a_content, a_attachment_type='note', a_call_back=None):
        #-http
        t_http=ctlib.http(a_http_ip, a_token)   
        #tip
        t_error_tip = 'list format reference:\
                    [{"type":"text","content":"test"},\
                    {"type":"a","title":"aa","url":"g:/1.jpg"},\
                    {"type":"image","path":"1.jpg"},\
                    {"type":"attachment","path":"1.jpg"},\
                    {"type":"video","path":"1.mov"}\
                    {"type":"br"} \
                    {"type":"audio","path":"1.mp3"}]'
        
        _dom.m_call_back = a_call_back

        #list'
        if isinstance(a_content, basestring):
            if a_content=="":
                return []
            return [{'type':'text','content':a_content}] 
        if not isinstance(a_content, list):
            raise Exception('func (note/content/text) argv type must be list or str/unicode/list')
        
        #计算所有文件总大小
        _dom.m_total_size = 0
        _dom.m_already_perform_size = 0 #已执行大小
        
        for _data in a_content:
            if 'path' in _data:
                _path = _data['path']
                if not os.path.exists(_path) or not os.path.isfile(_path):
                    raise Exception("path:{} not exists or not is file".format(repr(_path)))
                
                _dom.m_total_size += ctlib.file.get_size(_data['path'])
        
        t_new_context     = [] #列表
        t_attachment_list = [] #附件列表
        #-判断是否是图片或者视频
        #_
        for _data in a_content:
            _file_size = 0 
            if not isinstance(_data, dict) or 'type' not in _data: 
                raise Exception(repr(t_error_tip))
            t_type = _data['type'].strip()     
            #-note/content/text  type  must be  ['text','a','image','attachment']
            if t_type not in ['text', 'a', 'image', 'attachment', 'video', 'audio','br']:
                raise Exception(repr(t_error_tip))

            #-check---------------------------
            if  t_type not in ['text', 'a', 'br'] :
                if 'path' not in _data :
                    raise Exception(repr(t_error_tip))
                else:
                    _file = _data['path']
                    if not isinstance(_file, basestring) or not os.path.exists(_file):
                        raise Exception('image:{} file not exists'.format(repr(_file) )) 
                    _file_size = ctlib.file.get_size(_file)
                    _dom.m_current_size = _file_size
                    _dom.m_current_name = os.path.basename(_file)
            #text
            if t_type == 'text' : 
                if'content' not in _data or not isinstance(_data['content'], basestring):
                    raise Exception(repr(t_error_tip))
                t_new_context.append({"type":'text', "content":_data['content']})
                
            #br,换行
            elif t_type == 'br' : 
                t_new_context.append({"type":'br'})
                    
            #a
            elif t_type == 'a' :
                if 'title' not in _data or 'url' not in _data or \
                    not isinstance(_data['title'], basestring) or not isinstance(_data['url'], basestring):
                    raise Exception(repr(t_error_tip))
                t_url   = _data['url'].strip()
                t_lower = _data['url'].lower().strip()
                if t_lower.startswith('www.') or t_lower.startswith('https:') or t_lower.startswith('http:'):
                    if t_lower.startswith('www.'):
                        t_url = 'http://'+t_url
                elif not t_lower.startswith('file:///'):
                    t_url = 'file:///'+t_url

                t_new_context.append({'type':'url','title':_data['title'],'content':t_url})
                
            #image
            elif t_type == 'image':
                res=t_http.upload_project_img(_file, a_db, {"type":a_attachment_type}, a_call_back=_dom.__call_back)
                if not isinstance(res, dict) or "max" not in res or "min" not in res or 'att_id' not in res:
                    raise Exception('_dom.to_list, upload image fail')
                _dom.__call_back(_file_size, 0, 0)
                t_new_context.append({"min":res["min"], "max":res["max"], "type":"image",'att_id':res['att_id']})                        
                
            #video
            elif t_type == 'video':
                res=t_http.upload_project_video(_file, a_db, {"type":a_attachment_type}, a_call_back=_dom.__call_back)
                if not isinstance(res, dict) or "web_path" not in res  or 'att_id' not in res or 'thumbnail' not in res:
                    raise Exception('_dom.to_list, upload video fail')          
                _dom.__call_back(_file_size, 0, 0)        
                t_new_context.append({"video":res['web_path'],'image':res['thumbnail'],"type":"video",'att_id':res['att_id']})     
                                    
                
            #audio
            elif t_type == 'audio':   
                try:
                    t_video_info = ctlib.mov().get_audio_info(_file)
                except Exception as e:
                    raise Exception('_dom.tolist, get audio time fail,{}'.format(e) )

                if not isinstance(t_video_info, dict) or 'Duration' not in t_video_info:
                    raise Exception('_dom.tolist, get audio duration fail')
                res=t_http.upload_project_audio(_file, a_db, {"type":a_attachment_type}, None, a_call_back=_dom.__call_back)
                if not isinstance(res, dict) or "web_path" not in res or 'att_id' not in res:
                    raise Exception('_dom.to_list, upload audio fail')        
                _dom.__call_back(_file_size, 0, 0)
                t_new_context.append({"content":res['web_path'],"type":"audio",'att_id':res['att_id'],'time':t_video_info['Duration']})                     
                
            #attachment
            else: 
                res=t_http.upload_project_file(_file, a_db, {"type":a_attachment_type}, a_call_back=_dom.__call_back)
                if not isinstance(res, dict) or "web_path" not in res or 'att_id' not in res:
                    raise Exception('_dom.to_list, upload attachment fail')
                _dom.__call_back(_file_size, 0, 0)
                t_attachment_list.append({"content":res["web_path"],  "type":"attachment", 'title':os.path.basename(_file), 'size':_file_size,'att_id':res['att_id']})
            _dom.m_already_perform_size += _file_size
        return t_new_context+t_attachment_list


    @staticmethod
    def __call_back(a,b,c):
        func = _dom.m_call_back
        if func != None and (isinstance(func, types.FunctionType) or isinstance(func, types.MethodType) ): 
            t_argcount =  func.__code__.co_argcount
            t_varnames =  func.__code__.co_varnames   
            t_args =  list(t_varnames)[0:t_argcount]
            if len(t_args) == 4: 
                func(_dom.m_already_perform_size+a, b, _dom.m_total_size, _dom.m_current_name)
            elif len(t_args) == 3:
                func(_dom.m_already_perform_size+a, b, _dom.m_total_size)