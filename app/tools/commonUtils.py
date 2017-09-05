#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yagmail, threading
from gevent import monkey
monkey.patch_all()


def send_email(to_list, subject, content):
    yag = yagmail.SMTP(user='xxxx', password='xxxxxxx', host='smtp.exmail.qq.com', port='465')
    for receiver in to_list:
        yag.send(to=receiver, subject=subject, contents=content)


def async_send_email(to_list, subject, data, e_type):
    if e_type == "approve":
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
    <td style="background-color: #56b6c2">ID</td>
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
    <td style="background-color: #56b6c2">回退版本</td>
    <td style="background-color: grey">{4}</td>
  </tr>

  <tr>
    <td style="background-color: #56b6c2">开发负责人</td>
    <td style="background-color: grey">{5}</td>
  </tr>

  <tr>
    <td  style="background-color: #56b6c2">测试负责人</td>
    <td style="background-color: grey">{6}</td>
  </tr>

  <tr>
    <td style="background-color: #56b6c2">产品负责人</td>
    <td style="background-color: grey">{7}</td>
  </tr>

  <tr>
    <td style="background-color: #56b6c2">发布时间</td>
    <td style="background-color: grey">{8}</td>
  </tr>

  <tr>
    <td style="background-color: #56b6c2">SQL</td>
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
        """.format(data["id"], data["team_name"], data["service"], data["current_version"], data["last_version"],
                   data["dev_user"], data["test_user"], data["production_user"], data["create_time"], data["sql_info"], data['deploy_info'], data["comment"])
    thr = threading.Thread(target=send_email, args=[to_list, subject, html])  # 创建线程
    thr.start()



