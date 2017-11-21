#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from email.mime.text import MIMEText
from email.utils import formatdate
from smtplib import SMTP
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.tools.templateUtils import approve_template
env = os.environ.get('ads_env', 'dev')
if env == 'prod':
    from ..private_config import ProdConfig as Config
else:
    from ..private_config import DevConfig as Config


def send_mail(to, subject, content):
    """
       发送邮件接口
       :param to: 邮件接收人
       :param subject: 邮件主题
       :param content: 邮件主题正文
       :return:
       """
    msg = MIMEText(content, _subtype='html', _charset='utf-8')
    msg['To'] = to
    msg['From'] = Config.MAIL_ACCOUNT
    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=1)
    smtp_server = Config.MAIL_HOST
    # msg['Message-id'] = make_msgid() msg id
    smtp = SMTP(smtp_server)
    smtp.login(Config.MAIL_ACCOUNT, Config.MAIL_PASSWORD)
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp.quit()


def async_send_flow_email(to_list, subject, data, title=""):
    """
    gevent协程异步发送邮件
    :param to_list: 列表类型[[uid,email], [uid,email], [uid,email]]
    :param subject: 邮件标题
    :param data:  邮件内容
    :param title:  内容主题
    :return:
    """
    for to in to_list:
        html = approve_template(
            token=generate_confirm_email_token(to[0], data["id"]) if data['approved'] else '',
            email_url=Config.EMAIL_CONFIRM_PREFIX if data['approved'] else '',
            id=data["id"],
            team=data["team_name"],
            service=data["service"],
            version=data["version"],
            dev_user=data["dev_user"],
            test_user=data["test_user"],
            production_user=data["production_user"],
            create_time=data["create_time"],
            create_user=data["create_user"],
            sql_info=data["sql_info"],
            config=data["config"],
            deploy_info=data["deploy_info"],
            comment=data["comment"],
            deploy_time=data["deploy_time"],
            title=title
        )
        send_mail(to[1], subject, html)


def generate_confirm_email_token(uid, w_id):
    """
    邮件一键审批生成token信息
    :param uid: 审批人的用户id
    :param w_id: 工作流的id(可能我是多个id的拼接的字符串 examp:"1,5,2")
    :return: 用于加在审批链接后的get参数 用于后端识别审批者和审批工作流
    """
    s = Serializer(secret_key=Config.secret_key, expires_in=48*60*60)
    return s.dumps({'uid': uid, 'w_id': w_id})


def decrypt_email_token(token):
    """
    邮件token解密
    :param token: generate_confirm_email_token 加密后的token信息
    :return:  审批者id 工作流id
    """
    s = Serializer(secret_key=Config.secret_key)
    try:
        data = s.loads(token)
    except Exception, e:
        return False
    else:
        return data
