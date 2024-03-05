# -*- coding: utf-8 -*-
import json
import sys
from datetime import date
from PyQt5.QtCore import QTime

sys.path.append(r'\\nas01\shares\dev\cgtw\base')
import cgtw2

USER_NAME = ''
USER_ID = ''
ACCOUNT_LIST = {}
AVATAR_URL = ''

try:
    USER_NAME = cgtw2.tw().login.account()
    USER_ID = cgtw2.tw().login.account_id()
    ACCOUNT_LIST = cgtw2.tw().account.get([USER_ID], cgtw2.tw().account.fields(), limit='5000', order_sign_list=[])[0]

    ip_address = cgtw2.tw().login.http_server_ip().split(':')[0]
    image_info = json.loads(ACCOUNT_LIST[0]['account.image'])
    min_image_url = image_info[0]['min']
    AVATAR_URL = f'http://{ip_address}{min_image_url}'
    # [{'account.entity': 'yuping.fan', 'account.name': '范毓平', 'account.id': '548ABBCA-DB14-95A6-25C7-793627371C68',
    # 'account.status': 'Y', 'account.department': 'IT', 'account.image': '', 'account.password': 'aM<HvV=F(OfK',
    # 'account.sex': '男', 'account.mail': '', 'account.description': '', 'account.signature': '',
    # 'account.department_sort_id': '0013', 'account.group': '管理员权限,项目制片权限', 'account.create_time': '2023-05-18
    # 10:08:42', 'account.create_by': '管理员', 'account.last_update_time': '2024-01-11 17:14:16',
    # 'account.last_update_by': '范毓平', 'account.talk_permission': '内部', 'account.black_list': '',
    # 'account.project_permission': 'All', 'account.mobile': '', 'account.position': '', 'account.project_group': '',
    # 'account.driver_map': '', 'account.expire_time': '', 'account.login_time': '2024-03-01 09:18:20',
    # 'department.id': 'DFD11576-B19A-49EE-BFE7-3280A1513CAC', 'department.entity': 'IT',
    # 'id': '548ABBCA-DB14-95A6-25C7-793627371C68'}]
except Exception as e:
    print(e)


def get_project_list():
    """获取所有启用的项目"""
    try:
        field_sign_list = ['project.entity', 'project.full_name', 'project.id', 'project.database']
        filter_list = [['project.status', '=', 'Active']]
        id_list = cgtw2.tw().project.get_id(filter_list, limit="5000", start_num="")
        project_list = cgtw2.tw().project.get(id_list, field_sign_list, limit="5000", order_sign_list=[])
        return project_list
    except Exception as e:
        print(e)
        return []


def get_my_task(db):
    """获取我的任务列表"""
    _module = ['asset', 'shot']
    _task_list = []
    try:
        for module in _module:
            if module == 'asset':
                field_sign_list = ['asset.entity', 'task.account', 'task.artist', 'task.entity', 'task.url',
                                   'task.expected_time', 'task.total_use_time', 'task.status', 'task.module',
                                   'task.link_id', 'task.id']
                # field_sign_list = t_tw.task.fields(db, module)
                filter_list = [['task.account', '=', USER_NAME]]
                id_list = cgtw2.tw().task.get_id(
                    db, module, filter_list, limit="5000", start_num="")
                task_list = cgtw2.tw().task.get(
                    db, module, id_list, field_sign_list, limit="5000", order_sign_list=[])
                _task_list.extend(task_list)
            elif module == 'shot':
                field_sign_list = ['shot.entity', 'task.account', 'task.artist', 'task.entity', 'task.url',
                                   'task.expected_time', 'task.total_use_time', 'task.status', 'task.module',
                                   'task.link_id', 'task.id']
                # field_sign_list = t_tw.task.fields(db, module)
                filter_list = [['task.account', '=', USER_NAME]]
                id_list = cgtw2.tw().task.get_id(db, module, filter_list, limit="5000", start_num="")
                task_list = cgtw2.tw().task.get(db, module, id_list, field_sign_list, limit="5000", order_sign_list=[])
                _task_list.extend(task_list)
        return _task_list
    except Exception as e:
        print(e)
        return []


def get_daily_timelog(_date):
    """获取当前cgtw登录用户某天的工时,日期格式为:2024-01-09"""
    try:
        _time_log = []
        _project = get_project_list()
        for i in _project:
            db = i['project.database']
            field_list = ['date', 'tag', 'artist', 'project', 'link_entity', 'text', 'start_time', 'end_time',
                          'use_time']
            # field_list = t_tw.timelog.fields()
            # field_list.extend(['tag'])
            filter_list = [['account_id', '=', USER_ID], ['date', 'start', _date]]
            # filter_list = [['account_id', '=', userid]]
            id_list = cgtw2.tw().timelog.get_id(db, filter_list, limit="5000")
            _time_log.extend(cgtw2.tw().timelog.get(db, id_list, field_list, limit="5000", order_list=['end_time']))
        return _time_log
    except Exception as e:
        print(e)
        return []


def get_clock_in_time(user_name):
    outputUrl = r'//nas01/shares/dev/jumbla/attendance/'
    try:
        with open(outputUrl + str(date.today()) + '.json', 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            for item in json_data:
                if item['姓名'] == user_name:
                    if item['上班1打卡时间'] is None:
                        return None
                    else:
                        return item['上班1打卡时间']
            print('没有人员记录')
    except:
        return None


def sub_time_log(_dict):
    try:
        _timelog_id = cgtw2.tw().timelog.create(_dict['db'], _dict['link_id'], _dict['module'], _dict['module_type'],
                                                _dict['use_time'], _dict['date'], _dict['text'], tag='')

        return cgtw2.tw().timelog.set(_dict['db'], _timelog_id,
                                      {'start_time': _dict['start_time'], 'end_time': _dict['end_time']})
    except Exception as e:
        print(e)


def reload_task_info(db, module, id):
    if module == 'shot':
        field_sign_list = ['shot.entity', 'task.account', 'task.artist', 'task.entity', 'task.url',
                           'task.expected_time', 'task.total_use_time', 'task.status', 'task.module', 'task.link_id',
                           'task.id']
        task = cgtw2.tw().task.get(db, module, id, field_sign_list, limit="5000", order_sign_list=[])
        return task
    elif module == 'asset':
        field_sign_list = ['asset.entity', 'task.account', 'task.artist', 'task.entity', 'task.url',
                           'task.expected_time', 'task.total_use_time', 'task.status', 'task.module', 'task.link_id',
                           'task.id']
        task = cgtw2.tw().task.get(db, module, id, field_sign_list, limit="5000", order_sign_list=[])
        return task
