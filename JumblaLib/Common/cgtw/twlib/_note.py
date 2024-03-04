# coding: utf-8
import os, sys
from ._lib import _lib
from ._compat import *
from ._dom import _dom
class _note:

    @staticmethod
    def create(a_fun, a_http_ip, a_token, a_account_id, a_db, a_module, a_module_type, a_link_id_list, a_dom_text_list, a_cc_account_id="", a_image_list=[], a_tag_list=[], exec_event_filter=True,argv_dict={}, call_back=None):
        if len(a_link_id_list)==0:
            return False
        
        t_new_tag_list=[]
        for tag in a_tag_list: #20210203
            if isinstance(tag, basestring):
                t_new_tag_list.append(to_unicode(tag))
            else:
                t_new_tag_list.append(str(tag))
        
        t_sou_dom_text_list = []
        if isinstance(a_dom_text_list, basestring):
            t_sou_dom_text_list.append({'type':'text','content':a_dom_text_list})
        elif isinstance(a_dom_text_list, list):
            t_sou_dom_text_list += a_dom_text_list
        if isinstance(a_image_list, list):
            t_sou_dom_text_list += [{'type':'image','path':_path} for _path in a_image_list]

        t_dom_text_list = _dom.to_list(a_http_ip, a_token, a_db, t_sou_dom_text_list, a_call_back=call_back)
        
        note_field_data  = {"module":a_module,  "module_type":a_module_type, "#link_id":",".join(a_link_id_list), "dom_text":t_dom_text_list, "from_account_id":a_account_id }
        note_field_data  = dict(list(argv_dict.items()) +list(note_field_data.items()))
        t_sign_data_dict = {"db":a_db, "cc_account_id":a_cc_account_id, 'exec_event_filter':exec_event_filter,"field_data_array":note_field_data}
        
        if len(t_new_tag_list)>0:
            t_sign_data_dict["field_data_array"]["tag"]=to_unicode(u",").join(t_new_tag_list)
        
        return a_fun("note", "create", t_sign_data_dict)         
        
    @staticmethod
    def create_child(a_fun, a_http_ip, a_token, a_db, a_parent_id, a_dom_text_list, a_cc_account_id="", a_image_list=[], a_tag_list=[], exec_event_filter=True, call_back=None):
        t_new_tag_list=[]
        for tag in a_tag_list: #20210203
            if isinstance(tag, basestring):
                t_new_tag_list.append(to_unicode(tag))
            else:
                t_new_tag_list.append(str(tag))
        
        t_sou_dom_text_list = []
        if isinstance(a_dom_text_list, basestring):
            t_sou_dom_text_list.append({'type':'text','content':a_dom_text_list})
        elif isinstance(a_dom_text_list, list):
            t_sou_dom_text_list += a_dom_text_list
        if isinstance(a_image_list, list):
            t_sou_dom_text_list += [{'type':'image','path':_path} for _path in a_image_list]
        
        t_dom_text_list = _dom.to_list(a_http_ip, a_token, a_db, t_sou_dom_text_list, a_call_back=call_back)
        
        t_dict = {"db":a_db, "parent_id":a_parent_id, "dom_text":t_dom_text_list, "cc_account_id":a_cc_account_id, 'exec_event_filter':exec_event_filter}
        
        if len(t_new_tag_list)>0:
            t_dict["tag"]=to_unicode(u",").join(t_new_tag_list)
        
        return a_fun("note", "create_child", t_dict) 


    @staticmethod
    def set(a_fun, a_db, a_id, a_dom_text_list, a_tag_list=[], exec_event_filter=True):
        if str(a_id).strip()=="":
            return False
        
        t_new_tag_list=[]
        for tag in a_tag_list:
            if isinstance(tag, basestring):
                t_new_tag_list.append(to_unicode(tag))
            else:
                t_new_tag_list.append(str(tag))
        
        t_sign_data_dict = {"db":a_db, "id":a_id, "field_data_array":{"dom_text":a_dom_text_list},'exec_event_filter':exec_event_filter}
        if len(t_new_tag_list)>0:
            t_sign_data_dict["field_data_array"]["tag"]=to_unicode(u",").join(t_new_tag_list)
            
        return a_fun("note", "set", t_sign_data_dict) 