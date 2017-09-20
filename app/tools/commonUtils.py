#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.private_config import MAIL_ACCOUNT, MAIL_HOST, MAIL_PASSWORD
from gevent import monkey
import gevent
from email.mime.text import MIMEText
from email.utils import formatdate
from smtplib import SMTP
monkey.patch_all()


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
    :param to_list:
    :param subject:
    :param data:
    :param e_type: 邮件类型 例如 审批等等
    :return:
    """
    if e_type == 1:
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
    <td style="background-color: #56b6c2">团队</td>
    <td style="background-color: grey">{1}</td>
  </tr>

  <tr>
    <td style="background-color: #56b6c2">服务名</td>
    <td style="background-color: grey">{2}</td>
  </tr>

  <tr>
    <td style="background-color: #56b6c2">版本</td>
    <td style="background-color: grey">{3}</td>
  </tr>

  <tr>
    <td style="background-color: #56b6c2">开发负责人</td>
    <td style="background-color: grey">{4}</td>
  </tr>

  <tr>
    <td  style="background-color: #56b6c2">测试负责人</td>
    <td style="background-color: grey">{5}</td>
  </tr>

  <tr>
    <td style="background-color: #56b6c2">产品负责人</td>
    <td style="background-color: grey">{6}</td>
  </tr>

  <tr>
    <td style="background-color: #56b6c2">发布时间</td>
    <td style="background-color: grey">{7}</td>
  </tr>

  <tr>
    <td style="background-color: #56b6c2">SQL</td>
    <td style="background-color: grey">{8}</td>
  </tr>
  
   <tr>
    <td style="background-color: #56b6c2">配置变更</td>
    <td style="background-color: grey">{9}</td>
  </tr>

  <tr>
    <td style="background-color: #56b6c2">上线详情</td>
    <td style="background-color: grey">{10}</td>
  </tr>

  <tr>
    <td style="background-color: #56b6c2">备注</td>
    <td style="background-color: grey">{11}</td>
  </tr>
  </tbody>
</table>
<div>
</body></html>      
        """.format(data["id"], data["team_name"], data["service"], data["version"],
                   data["dev_user"], data["test_user"], data["production_user"], data["create_time"], data["sql_info"],
                   data["config"], data['deploy_info'], data["comment"])

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

    task_list = []
    for to in to_list:
        task_list.append(gevent.spawn(send_mail, to, subject, html),)
    gevent.joinall(task_list)





html = """
     <table style="width: 550px"  border="1" cellpadding="13" cellspacing="1">
    <caption>
    请到运维平台完成审批
    </caption>
    <tr>
      <th style="background-color: lightgrey">工作流ID</th>
      <td>{0}</td>
    </tr>

    <tr>
      <th style="background-color: lightgrey">创建时间</th>
      <td>{1}</td>
    </tr>

    <tr>
      <th>团队</th>
      <td>{2}</td>
    </tr>

    <tr>
      <th>测试负责人</th>
      <td>{3}</td>
    </tr>

    <tr>
      <th>发布时间</th>
      <td>{4}-{5}</td>
    </tr>

    <tr>
      <th>SQL</th>
      <td>{6}</td>
    </tr>

    <tr>
      <th>备注</th>
      <td>{7}</td>
    </tr>
  </table>
<a href="http://www.baidu.com">hellos</a>
"""

html = """
         <table style="width: 550px"  border="1" cellpadding="13" cellspacing="1">
        <caption>
        请到运维平台完成审批
        </caption>
        <tr>
          <th style="background-color: lightgrey">工作流ID</th>
          <td>{0}</td>
        </tr>

        <tr>
          <th style="background-color: lightgrey">创建时间</th>
          <td>{1}</td>
        </tr>

        <tr>
          <th>团队</th>
          <td>{2}</td>
        </tr>

        <tr>
          <th>测试负责人</th>
          <td>{3}</td>
        </tr>

        <tr>
          <th>发布时间</th>
          <td>{4}-{5}</td>
        </tr>

        <tr>
          <th>SQL</th>
          <td>{6}</td>
        </tr>

        <tr>
          <th>备注</th>
          <td>{7}</td>
        </tr>
      </table>
    <hr>
    <a href="http://www.baidu.com">一键完成审批</a>
    """




