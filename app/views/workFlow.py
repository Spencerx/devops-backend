#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from app.models.workflows import Workflow
from app.models.users import Users
from app.models.flow_type import FlowType
from app.models.services import Services
from app.models.bugs import Bugs
from flask import Blueprint, request
from app.tools.jsonUtils import response_json
from app.tools.redisUtils import create_redis_connection
from app.tools.ormUtils import id_to_user, id_to_service, id_to_team, id_to_status, id_to_flow_type, \
    service_to_id, querylastversion_by_id, flow_type_to_id
from app.tools.emailUtils import async_send_approved_email
import gevent.monkey
gevent.monkey.patch_all()

workflow = Blueprint('workflow', __name__)


@workflow.route('/history', methods=["GET", "POST"])
def history():
    """
    获取历史工作流接口
    :return:
    """
    if request.method == 'POST':
        form_data = request.get_json()
        per_size = form_data['size']
        page_count = form_data['page']
        if page_count == 0:
            ws = Workflow.select().limit(10).order_by(Workflow.w.desc())
        else:
            ws = Workflow.select().limit(int(per_size)).offset((int(page_count)-1)*int(per_size)).\
                order_by(Workflow.w.desc())
        data = []
        for workflow in ws:
            if workflow.is_except == 1:
                except_info = Bugs.select().where(Bugs.flow_id == workflow.w).get().exception_info
            else:
                except_info = ''
            per_flow = {
                'ID': workflow.w,
                'create_time': workflow.create_time.strftime('%Y-%m-%d %H:%M:%M'),
                'deploy_time': workflow.deploy_time.strftime('%Y-%m-%d %H:%M:%M') if workflow.deploy_time else '',
                'close_time': workflow.close_time.strftime('%Y-%m-%d %H:%M:%M') if workflow.close_time else '',
                'team_name': id_to_team(workflow.team_name),
                'dev_user': id_to_user(workflow.dev_user),
                'test_user': id_to_user(workflow.test_user),
                'create_user': id_to_user(workflow.create_user),
                'sql_info': workflow.sql_info,
                'production_user': id_to_user(workflow.production_user),
                'flow_type': id_to_flow_type(workflow.type),
                'current_version': workflow.current_version,
                'last_version': querylastversion_by_id(workflow.service),
                'comment': workflow.comment,
                'deploy_info': workflow.deploy_info,
                'status': workflow.status,
                'is_except': workflow.is_except,
                'except_info': except_info,
                'status_info': id_to_status(workflow.status),
                'service': id_to_service(workflow.service) if workflow.service else '',
                'approved_user': id_to_user(workflow.approved_user) if workflow.approved_user else '',
                'ops_user': id_to_user(workflow.ops_user) if workflow.ops_user else '',
                'config': workflow.config if workflow.config else '',
                'deny_info': workflow.deny_info if workflow.deny_info else '',
                'access_info': workflow.access_info if workflow.access_info else '',
            }
            data.append(per_flow)
        workflow_count = Workflow.select().count()
        return response_json(200, '', {"count": workflow_count, "data": data})


@workflow.route('/history/search', methods=['POST', 'OPTION'])
def workflow_history_search():
    # todo
    """
    历史工作流按照条件搜索接口
    :return:
    """
    if request.method == 'POST':
        form_data = request.get_json()
        try:
            id = form_data['id']
        except Exception, e:
            id = None
        if id:
            try:
                workflow = Workflow.select().where(Workflow.w == int(id)).get()
            except Exception, e:
                print e
                return response_json(200, '', {'count': 0, 'data': []})
            data = []
            per_flow = {
                'ID': workflow.w,
                'create_time': workflow.create_time.strftime('%Y-%m-%d %H:%M:%M'),
                'deploy_time': workflow.deploy_time.strftime(
                    '%Y-%m-%d %H:%M:%M') if workflow.deploy_time else '',
                'close_time': workflow.close_time.strftime('%Y-%m-%d %H:%M:%M') if workflow.close_time else '',
                'team_name': id_to_team(workflow.team_name),
                'dev_user': id_to_user(workflow.dev_user),
                'test_user': id_to_user(workflow.test_user),
                'create_user': id_to_user(workflow.create_user),
                'sql_info': workflow.sql_info,
                'production_user': id_to_user(workflow.production_user),
                'flow_type': id_to_flow_type(workflow.type),
                'current_version': workflow.current_version,
                'last_version': querylastversion_by_id(workflow.service),
                'comment': workflow.comment,
                'deploy_info': workflow.deploy_info,
                'status': workflow.status,
                'is_except': workflow.is_except,
                'status_info': id_to_status(workflow.status),
                'service': id_to_service(workflow.service) if workflow.service else '',
                'approved_user': id_to_user(workflow.approved_user) if workflow.approved_user else '',
                'ops_user': id_to_user(workflow.ops_user) if workflow.ops_user else '',
                'config': workflow.config if workflow.config else '',
                'deny_info': workflow.deny_info if workflow.deny_info else '',
                'access_info': workflow.access_info if workflow.access_info else '',
            }
            data.append(per_flow)
            flow_count = len(data)
            return response_json(200, '', {'count': flow_count, 'data': data})
        else:
            pass
    else:
        return response_json(200, '', '')


@workflow.route('/create', methods=['POST', 'OPTION'])
def create_workflow():
    """
    新建工作流接口
    :return:
    """
    if request.method == 'POST':
        form_data = request.get_json()
        flow_type = form_data['flow_type']
        utc_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        approved_users = Users.select().where(Users.can_approved == '1')
        to_list = [[approved_user.id, approved_user.email] for approved_user in approved_users]
        # 判断工作流类型 来区分处理逻辑
        # 系统上线
        if flow_type == 1:
            services = form_data['service']
            mail_services = ''
            mail_ids = ''
            mail_versions = ''
            team_name = form_data['team_name']
            dev_user = int(form_data['dev_user'])
            test_user = int(form_data['test_user'])
            create_user = form_data['create_user']
            production_user = int(form_data['production_user'])
            sql_info = form_data['sql_info']
            # 部署date
            deploy_date = datetime.datetime.strptime(form_data['deploy_date'], utc_format). \
                strftime('%Y-%m-%d')
            deploy_date = datetime.datetime.strptime(deploy_date, '%Y-%m-%d') + datetime.timedelta(days=1)
            # 部署time
            deploy_time = form_data['deploy_time']
            # 发布时间 time+date
            deploy_order_time = datetime.datetime.strftime(deploy_date, "%Y-%m-%d") + " " + deploy_time
            comment = form_data['comment']
            deploy_info = form_data['deploy_info']
            config = form_data['config']
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            for service in services:
                service_name = service['service']
                version = service['version']
                mail_services = mail_services + service_name + " "
                mail_versions = mail_versions + version + " "
                w = Workflow(service=service_to_id(service_name), create_time=create_time,
                             dev_user=dev_user, test_user=test_user, production_user=production_user,
                             current_version=version, type=flow_type, deploy_time=deploy_order_time,
                             sql_info=sql_info, team_name=team_name, comment=comment,
                             deploy_info=deploy_info, config=config, create_user=create_user)
                w.save()
                w_id = w.w
                mail_ids = mail_ids + str(w_id) + " "  # 批量审批工作流的id字符串拼接值
            email_data = {
                "service": mail_services,
                "version": mail_versions,
                "team_name": id_to_team(team_name),
                "dev_user": id_to_user(dev_user),
                "test_user": id_to_user(test_user),
                "create_user": create_user,
                "production_user": id_to_user(production_user),
                "sql_info": sql_info,
                "comment": comment,
                "create_time": create_time,
                "deploy_info": deploy_info,
                "config": config,
                "id": mail_ids,
                "deploy_time": deploy_order_time,
            }
            r = create_redis_connection()
            r.rpush('email:consume:tasks', {'to_list': to_list, 'subject': u'上线审批',
                                            'data': email_data, 'e_type': flow_type})
            return response_json(200, '', 'ceate successful')

        # 数据库变更
        elif flow_type == 2:
            mail_ids = ''
            team_name = form_data['team_name']
            test_user = int(form_data['test_user'])
            dev_user = int(form_data['dev_user'])
            create_user = form_data['create_user']
            sql_info = form_data['sql_info']
            comment = form_data['comment']
            # 部署date
            deploy_date = datetime.datetime.strptime(form_data['deploy_date'], utc_format). \
                strftime('%Y-%m-%d')
            deploy_date = datetime.datetime.strptime(deploy_date, '%Y-%m-%d') + datetime.timedelta(days=1)
            # 部署time
            deploy_time = form_data['deploy_time']
            # 发布时间 time+date
            deploy_order_time = datetime.datetime.strftime(deploy_date, "%Y-%m-%d") + " " + deploy_time
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            w = Workflow(create_time=create_time, test_user=test_user, type=flow_type, dev_user=dev_user,
                         sql_info=sql_info, team_name=team_name, comment=comment, create_user=create_user,
                         deploy_time=deploy_order_time, deploy_end_time=deploy_order_time)
            w.save()
            w_id = w.w
            mail_ids = mail_ids + str(w_id) + " "  # 批量审批工作流的id字符串拼接值
            email_data = {
                "team_name": id_to_team(team_name),
                "test_user": id_to_user(test_user),
                "sql_info": sql_info,
                "comment": comment,
                "create_time": create_time,
                "deploy_time": deploy_order_time,
                "id": mail_ids,
                'create_user': id_to_user(int(create_user))
            }
            r = create_redis_connection()
            r.rpush('email:consume:tasks', {'to_list': to_list, 'subject': u'数据库变更审批',
                                            'data': email_data, 'e_type': flow_type})
            return response_json(200, '', 'ceate successful')

        # 配置变更
        elif flow_type == 3:
            team_name = form_data['team_name']
            test_user = int(form_data['test_user'])
            dev_user = int(form_data['dev_user'])
            create_user = form_data['create_user']
            config_info = form_data['config_info']
            comment = form_data['comment']
            # 部署date
            deploy_date = datetime.datetime.strptime(form_data['deploy_date'], utc_format). \
                strftime('%Y-%m-%d')
            deploy_date = datetime.datetime.strptime(deploy_date, '%Y-%m-%d') + datetime.timedelta(days=1)
            # 部署time
            deploy_time = form_data['deploy_time']
            # 发布时间 time+date
            deploy_order_time = datetime.datetime.strftime(deploy_date, "%Y-%m-%d") + " " + deploy_time
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            w = Workflow(create_time=create_time, test_user=test_user, type=flow_type,
                         config=config_info, team_name=team_name, comment=comment, create_user=create_user,
                         deploy_time=deploy_order_time, dev_user=dev_user)
            w.save()
            w_id = w.w
            email_data = {
                "team_name": id_to_team(team_name),
                "test_user": id_to_user(test_user),
                "dev_user": id_to_user(dev_user),
                "config": config_info,
                "comment": comment,
                "create_time": create_time,
                "deploy_time": deploy_order_time,
                "id": w_id,
            }
            async_send_approved_email(to_list, u"数据库变更审批", email_data, e_type=flow_type)
            return response_json(200, '', 'ceate successful')

        # 权限申请
        elif flow_type == 4:
            pass

        # 不明确的工作流类型
        else:
            return response_json(500, u'工作流类型不明确', '')
    else:
        return ''


@workflow.route('/myflow', methods=['POST', 'OPTION'])
def my_flow():
    """
    获取需要当前用户处理的工作流
    :return:
    """
    if request.method == "POST":
        req_data = request.get_json()
        uid = req_data['uid']
        u = Users.select().where(Users.id == uid).get()
        user_role = u.role
        can_approved = int(u.can_approved)
        workflow_list = []
        if int(user_role) == 1:
            flows = Workflow.select().where(Workflow.status == 2)
            for flow in flows:
                workflow_list.append(flow.w)

        if int(user_role) == 3:
            flows = Workflow.select().where((Workflow.status == 3) & (Workflow.test_user == uid))
            for flow in flows:
                workflow_list.append(flow.w)

        if can_approved:
            flows = Workflow.select().where(Workflow.status == 1)
            for flow in flows:
                workflow_list.append(flow.w)

        if not workflow_list:
            return response_json(200, "", {'data': [], 'count': 0})
        else:
            flow_data = []
            for flow_id in workflow_list:
                flows = Workflow.select().where(Workflow.w == flow_id)
                for per_flow in flows:
                    per_flow_data = {
                        'ID': per_flow.w,
                        'create_time': per_flow.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'deploy_time': per_flow.deploy_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'team_name': per_flow.team_name,
                        'sql_info': per_flow.sql_info if per_flow.sql_info else '',
                        'test_user': id_to_user(per_flow.test_user) if per_flow.test_user else '',
                        'create_user': id_to_user(per_flow.create_user) if per_flow.create_user else '',
                        'dev_user': id_to_user(per_flow.dev_user) if per_flow.dev_user else '',
                        'current_version': per_flow.current_version,
                        'comment': per_flow.comment if per_flow.comment else '',
                        'deploy_info': per_flow.deploy_info,
                        'service': id_to_service(per_flow.service),
                        'status_info': id_to_status(per_flow.status),
                        'status': per_flow.status,
                        'config': per_flow.config if per_flow.config else '',
                        'flow_type': id_to_flow_type(per_flow.type),
                    }
                    flow_data.append(per_flow_data)
            flow_count = len(flow_data)
            return response_json(200, "", {'data': flow_data, 'count': flow_count})

    else:
        return ''


@workflow.route('/approved', methods=['POST', 'OPTION'])
def approved_flow():
    """
    工作流审批接口
    :return:
    """
    if request.method == "POST":
        json_data = request.get_json()
        approved = json_data['approved']
        suggestion = json_data['suggestion']
        uid = json_data['uid']
        w_id = json_data['w_id']
        try:
            w = Workflow.select().where(Workflow.w == w_id).get()
        except Exception, e:
            return response_json(500, u'工作流不存在', '')
        if approved == "access":
            if int(w.status) != 1:
                return response_json(301, '', u'工作流状态检测到已经被改变')
            w.status = int(w.status) + 1
            w.access_info = suggestion
            w.approved_user = int(uid)
            w.save()

            # 审核完成 邮件通知工作流创建者和运维
            to_list = []
            create_user = Users.select().where(Users.id == int(w.create_user)).get()
            to_list.append(['', create_user.email])
            to_list.append(['', 'ops@haixue.com'])
            r = create_redis_connection()
            r.rpush('email:consume:tasks', {'to_list': to_list, 'subject': u"工作流实时进度",
                                            'data': "工作流ID: {0} 审核完成, 等待运维部署".format(w_id), 'e_type': 100})
            return response_json(200, "", "")
        elif approved == "deny":
            if int(w.status) != 1:
                return response_json(301, '', u'工作流状态检测到已经被改变')
            w.status = 5
            w.approved_user = uid
            w.deny_info = suggestion
            w.close_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            w.save()
            # 工作流被驳回邮件通知 创建者
            to_list = []
            create_user = Users.select().where(Users.id == int(w.create_user)).get()
            to_list.append(['', create_user.email])
            r = create_redis_connection()
            r.rpush('email:consume:tasks', {'to_list': to_list, 'subject': u"工作流实时进度",
                                            'data': "工作流ID: {0} 审核失败, 详情:{1}".format(w_id, suggestion), 'e_type': 100})

            return response_json(200, "", "")
        else:
            return response_json(500, u"审批参数无效", "")
    else:

        return response_json(200, '', '')


@workflow.route('/confirm_deploy', methods=['POST', 'OPTION'])
def sure_deploy():
    """
    确认工作流中服务上线接口
    :return:
    """
    if request.method == "POST":
        json_data = request.get_json()
        uid = json_data['uid']
        w_id = json_data['w_id']
        flow_type_id = int(flow_type_to_id(json_data['flow_type']))
        w = Workflow.select().where(Workflow.w == w_id).get()
        if flow_type_id == 1:
            s = Services.select().where(Services.s == int(w.service)).get()
            if int(w.status) != 2:
                return response_json(301, '', u'工作流状态检测到已经被改变')
            s.current_version = w.current_version  # 修改该服务的最新版本为当前上线版本
            w.status = int(w.status) + 1
            w.ops_user = uid
            try:
                w.save()
                s.save()

                # 部署完成 邮件通知相关测试和工作流创建者
                to_list = []
                create_user = Users.select().where(Users.id == int(w.create_user)).get()
                test_user = Users.select().where(Users.id == int(w.test_user)).get()
                to_list.append(['', create_user.email])
                to_list.append(['', test_user.email])
                r = create_redis_connection()
                r.rpush('email:consume:tasks', {'to_list': to_list, 'subject': u"工作流实时进度",
                                                'data': "工作流ID: {0} 部署完成, 等待测试确认".format(w_id), 'e_type': 100})
                return response_json(200, '', '')
            except Exception, e:
                return response_json(500, e, '')
        elif flow_type_id == 2 or flow_type_id == 3:
            w = Workflow.select().where(Workflow.w == w_id).get()
            if int(w.status) != 2:
                return response_json(301, '', u'工作流状态检测到已经被改变')
            w.status = int(w.status) + 1
            w.ops_user = uid
            try:
                w.save()

                # 部署完成 邮件通知相关测试和工作流创建者
                to_list = []
                create_user = Users.select().where(Users.id == int(w.create_user)).get()
                test_user = Users.select().where(Users.id == int(w.test_user)).get()
                to_list.append(['', create_user.email])
                to_list.append(['', test_user.email])
                r = create_redis_connection()
                r.rpush('email:consume:tasks', {'to_list': to_list, 'subject': u"工作流实时进度",
                                                'data': "工作流ID: {0} 部署完成, 等待测试确认".format(w_id), 'e_type': 100})
                return response_json(200, '', '')
            except Exception, e:
                return response_json(500, e, '')
    else:
        return ""


@workflow.route('/confirm_test', methods=['POST', 'OPTION'])
def sure_test():
    """
    测试确认上线服务正常接口
    :return:
    """
    if request.method == "POST":
        json_data = request.get_json()
        w_id = json_data['flow_id']
        is_except = json_data['is_except']
        w = Workflow.select().where(Workflow.w == w_id).get()
        if int(w.status) != 3:
            """检测工作流是否被修改"""
            return response_json(301, '', u'工作流状态检测到已经被改变')

        if is_except:
            """测试上线异常"""
            except_info = json_data['except_info']
            b = Bugs(flow_id=int(w_id), exception_info=except_info)
            b.save()
            w.is_except = 1
            w.status = 6
            w.close_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            w.save()

            # 邮件通知与工作流相关的人员
            to_list = []
            create_user = Users.select().where(Users.id == int(w.create_user)).get()
            test_user = Users.select().where(Users.id == int(w.test_user)).get()
            dev_user = Users.select().where(Users.id == int(w.dev_user)).get()
            to_list.append(['', create_user.email])
            to_list.append(['', test_user.email])
            to_list.append(['', dev_user.email])
            to_list.append(['', 'ops@haixue.com'])
            r = create_redis_connection()
            r.rpush('email:consume:tasks', {'to_list': to_list, 'subject': u"工作流实时进度",
                                            'data': "工作流ID: {0} 测试发现异常, 异常信息{1}".
                    format(w_id, except_info), 'e_type': 100})
            return response_json(200, '', '')
        else:
            """测试上线没有异常"""
            w.close_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                w.status = int(w.status) + 1
                w.is_except = 2
                w.save()

                # 邮件通知与工作流相关的人员
                to_list = []
                create_user = Users.select().where(Users.id == int(w.create_user)).get()
                test_user = Users.select().where(Users.id == int(w.test_user)).get()
                dev_user = Users.select().where(Users.id == int(w.dev_user)).get()
                to_list.append(['', create_user.email])
                to_list.append(['', test_user.email])
                to_list.append(['', dev_user.email])
                to_list.append(['', 'ops@haixue.com'])
                r = create_redis_connection()
                r.rpush('email:consume:tasks', {'to_list': to_list, 'subject': u"工作流实时进度",
                                                'data': "工作流ID: {0} 测试确认部署完成,工作流关闭)".format(w_id), 'e_type': 100})
                return response_json(200, '', '')
            except Exception, e:
                return response_json(500, e, '')
    else:
        return ""


@workflow.route('/type')
def flow_type_list():
    """
    获取工作流所有类型接口
    :return:
    """
    ts = FlowType.select()
    data = []
    for t in ts:
        per_type = {
            'id': t.id,
            'type': t.type
        }
        data.append(per_type)
    return response_json(200, '', data=data)



