#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.private_config import MAIL_ACCOUNT, MAIL_HOST, MAIL_PASSWORD, EMAIL_CONFIRM_PREFIX
from email.mime.text import MIMEText
from email.utils import formatdate
from smtplib import SMTP
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.private_config import secret_key


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
    msg['From'] = MAIL_ACCOUNT
    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=1)
    smtp_server = MAIL_HOST
    # msg['Message-id'] = make_msgid() msg id
    smtp = SMTP(smtp_server)
    smtp.login(MAIL_ACCOUNT, MAIL_PASSWORD)
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp.quit()


def async_send_email(to_list, subject, data, e_type):
    """
    gevent协程异步发送邮件
    :param to_list: 列表类型[[uid,email], [uid,email], [uid,email]]
    :param subject: 邮件主题
    :param data:  邮件内容
    :param e_type: 邮件类型 例如 审批等等
    :return:
    """
    for to in to_list:
        if e_type == 1:
            html = """
        <html><body>
        <div>
                <h1>系统上线申请</h1>
<h3>请到运维平台完成审批或点击快速审批按钮完成一键快速审批</h3>
<button style="background-color: deepskyblue"><a href="{13}?token={12}" style="text-decoration: none">一键快速审批</a></button>
</div>
<div style="margin-top: 1%">
<table style="width: 550px"  border="0" cellpadding="13" cellspacing="1">
  <thead>
  <tr>
    <td style="background-color: lightgrey">工作流ID</td>
    <td style="background-color: lightgrey">{0}</td>
  </tr>

  <tr>
    <td style="background-color: lightgrey">团队</td>
    <td style="background-color: lightgrey">{1}</td>
  </tr>

  <tr>
    <td style="background-color: lightgrey">服务名</td>
    <td style="background-color: lightgrey">{2}</td>
  </tr>

  <tr>
    <td style="background-color: lightgrey">版本</td>
    <td style="background-color: lightgrey">{3}</td>
  </tr>

  <tr>
    <td style="background-color: lightgrey">开发负责人</td>
    <td style="background-color: lightgrey">{4}</td>
  </tr>

  <tr>
    <td  style="background-color: lightgrey">测试负责人</td>
    <td style="background-color: lightgrey">{5}</td>
  </tr>

  <tr>
    <td style="background-color: lightgrey">产品负责人</td>
    <td style="background-color: lightgrey">{6}</td>
  </tr>

  <tr>
    <td style="background-color: lightgrey">发布时间</td>
    <td style="background-color: lightgrey">{7}</td>
  </tr>

  <tr>
    <td style="background-color: lightgrey">SQL</td>
    <td style="background-color: lightgrey">{8}</td>
  </tr>
  
   <tr>
    <td style="background-color: lightgrey">配置变更</td>
    <td style="background-color: lightgrey">{9}</td>
  </tr>

  <tr>
    <td style="background-color: lightgrey">上线详情</td>
    <td style="background-color: lightgrey">{10}</td>
  </tr>

  <tr>
    <td style="background-color: lightgrey">备注</td>
    <td style="background-color: lightgrey">{11}</td>
  </tr>
  </tbody>
</table>
<div>
</body></html>      
        """.format(data["id"], data["team_name"], data["service"], data["version"],
                   data["dev_user"], data["test_user"], data["production_user"], data["create_time"], data["sql_info"],
                   data["config"], data['deploy_info'], data["comment"],
                   generate_confirm_email_token(to[0], data["id"]), EMAIL_CONFIRM_PREFIX)

        elif e_type == 2:
            html = """
                <html><body>
                <div>
                        <h1>上线申请</h1>
        <h4>请到运维平台完成审批</h4>
        </div>
        <div style="margin-top: 1%">
        <table style="width: 550px"  border="0" cellpadding="13" cellspacing="1">
          <thead>
          <tr>
            <td style="background-color: #56b6c2">工作流ID</td>
            <td style="background-color: grey">{0}</td>
          </tr>
          
           <tr>
            <td style="background-color: #56b6c2">创建时间</td>
            <td style="background-color: grey">{1}</td>
          </tr>

          <tr>
            <td style="background-color: #56b6c2">团队</td>
            <td style="background-color: grey">{2}</td>
          </tr>

          <tr>
            <td  style="background-color: #56b6c2">测试负责人</td>
            <td style="background-color: grey">{3}</td>
          </tr>

          <tr>
            <td style="background-color: #56b6c2">发布时间</td>
            <td style="background-color: grey">{4} - {5}</td>
          </tr>

          <tr>
            <td style="background-color: #56b6c2">SQL</td>
            <td style="background-color: grey">{6}</td>
          </tr>

          <tr>
            <td style="background-color: #56b6c2">备注</td>
            <td style="background-color: grey">{7}</td>
          </tr>
          </tbody>
        </table>
        <div>
        </body></html>      
                """.format(data["id"], data['create_time'], data["team_name"], data["test_user"],
                           data["deploy_start_time"], data["deploy_end_time"], data["sql_info"], data["comment"])

        send_mail(to[1], subject, html)


def generate_confirm_email_token(uid, w_id):
    """
    邮件一键审批生成token信息
    :param uid: 审批人的用户id
    :param w_id: 工作流的id(可能我是多个id的拼接的字符串 examp:"1,5,2")
    :return: 用于加在审批链接后的get参数 用于后端识别审批者和审批工作流
    """
    s = Serializer(secret_key=secret_key)
    return s.dumps({'uid': uid, 'w_id': w_id})


def decrypt_email_token(token):
    """
    邮件token解密
    :param token: generate_confirm_email_token 加密后的token信息
    :return:  审批者id 工作流id
    """
    s = Serializer(secret_key=secret_key)
    try:
        data = s.loads(token)
    except Exception, e:
        return False
    else:
        return data
