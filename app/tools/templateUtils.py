#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jinja2 import Template


def deploy_approve_template(**kwargs):
    """
    系统上线审批邮件模版
    :return:
    """
    t = Template(u"""
            <html>
            <head>
            </head>
            <body>
            <div>
              <h1>{{ subject }}</h1>
              <h3>请到运维平台完成审批或点击快速审批按钮完成一键快速审批</h3>
              <button style="background-color: deepskyblue">
                  <a href="{{ email_url }}?token={{ token }}" style="text-decoration: none">
                    一键快速审批
                  </a></button>
            </div>
            <div style="margin-top: 1%">
              <table class="tb" border="0" cellpadding="12" cellspacing="2" style="width: 60%;
                  background-color: #f8f8f9;
                  border-top: 1px solid #E0E0E0;
                  border-left: 1px solid #E0E0E0;">
                <thead>
                <tr>
                  <th style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;width: 30%">工作流ID</th>
                  <th style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;"> {{ id }} </th>
                </tr>
                </thead>
                <tbody>
            
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">团队</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ team }}</td>
                </tr>
            
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">服务名</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ service }}</td>
                </tr>
            
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">版本</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ version }}</td>
                </tr>
            
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">开发负责人</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ dev_user }}</td>
                </tr>
            
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">测试负责人</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ test_user }}</td>
                </tr>
            
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">产品负责人</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ production_user }}</td>
                </tr>
            
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">创建时间</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ create_time }}</td>
                </tr>
            
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">发布时间</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ deploy_time }}</td>
                </tr>
            
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">SQL</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ sql_info }}</td>
                </tr>
            
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">配置变更</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ config }}</td>
                </tr>
            
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">上线详情</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ deploy_info }}</td>
                </tr>
            
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">备注</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ comment }}</td>
                </tr>
                </tbody>
              </table>
            </div>
            </body>
            </html>""")
    return t.render(subject=kwargs['subject'], email_url=kwargs['email_url'], token=kwargs['token'],
                    id=kwargs['id'], team=kwargs['team'], service=kwargs['service'],
                    version=kwargs['version'], dev_user=kwargs['dev_user'], test_user=kwargs['test_user'],
                    production_user=kwargs['production_user'], create_time=kwargs['create_time'],
                    deploy_time=kwargs['deploy_time'], sql_info=kwargs['sql_info'], config=kwargs['config'],
                    deploy_info=kwargs['deploy_info'], comment=kwargs['comment'])


def db_approve_template():
    """
    数据库变更审批邮件模版
    :return:
    """
    pass


def deploy_after_approved_template():
    """
    系统上线审批通过后邮件模版
    :return:
    """
    pass


def db_after_approved_template():
    """
    数据库变更审批通过邮件模版
    :return:
    """
    pass


def deploy_confirm_template():
    """
    系统上线确认部署通过后邮件模版
    :return:
    """
    pass


def db_confirm_template():
    """
    数据库变更确认部署邮件模版
    :return:
    """
    pass


def deploy_noticeall_template():
    """
    系统上线成功上线通知全部人员
    :return:
    """
    pass


def db_noticeall_template():
    """
    数据库变更成功通知全部人员
    :return:
    """
    pass


deploy_approve_template()

