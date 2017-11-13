#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jinja2 import Template


def approve_template(**kwargs):
    """
    审批邮件模版 动态生成邮件模版
    :return:
    """
    t = Template(u"""
            <html>
            <head>
            </head>
            <body>
            <div>
              <h1>{{ title }}</h1>
              
              {% if token %}
              <h3>请到运维平台完成审批或点击快速审批按钮完成一键快速审批</h3>
              <button style="background-color: deepskyblue">
                  <a href="{{ email_url }}?token={{ token }}" style="text-decoration: none">
                    一键快速审批
                  </a></button>
              {% endif %}
            </div>
            <div style="margin-top: 1%">
              <table class="tb" border="0" cellpadding="12" cellspacing="2" style="width: 60%;
                  background-color: #f8f8f9;
                  border-top: 1px solid #E0E0E0;
                  border-left: 1px solid #E0E0E0;">
                <thead>
                
                {% if id %}
                <tr>
                  <th style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;width: 30%">工作流ID</th>
                  <th style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;"> {{ id }} </th>
                </tr>
                {% endif %}
                </thead>
                <tbody>
            
                {% if team %}
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">团队</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ team }}</td>
                </tr>
                {% endif %}
            
                {% if service %}
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">服务名</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ service }}</td>
                </tr>
                {% endif %}
                
                {% if version %}
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">版本</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ version }}</td>
                </tr>
                {% endif %}
                
                {% if create_user %}
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">创建人</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ create_user }}</td>
                </tr>
                {% endif %}
            
                {% if dev_user %}
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">开发负责人</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ dev_user }}</td>
                </tr>
                {% endif %}
            
                {% if test_user %}
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">测试负责人</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ test_user }}</td>
                </tr>
                {% endif %}
            
                {% if production_user %}
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">产品负责人</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ production_user }}</td>
                </tr>
                {% endif %}
            
                {% if create_time %}
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">创建时间</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ create_time }}</td>
                </tr>
                {% endif %}
            
                {% if deploy_time %}
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">部署时间</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ deploy_time }}</td>
                </tr>
                {% endif %}
            
                {% if sql_info %}
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">数据库变更详情</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ sql_info }}</td>
                </tr>
                {% endif %}
            
                {% if config %}
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">配置变更</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ config }}</td>
                </tr>
                {% endif %}
                
                
                {% if deploy_info %}
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">上线详情</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ deploy_info }}</td>
                </tr>
                {% endif %}
            
                {% if comment %}
                <tr>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">备注</td>
                  <td style="border-right: 1px solid #E0E0E0;border-bottom: 1px solid #E0E0E0;">{{ comment }}</td>
                </tr>
                {% endif %}
                </tbody>
              </table>
            </div>
            </body>
            </html>""")
    return t.render(title=kwargs['title'], email_url=kwargs['email_url'], token=kwargs['token'],
                    id=kwargs['id'], team=kwargs['team'], service=kwargs['service'],
                    version=kwargs['version'], dev_user=kwargs['dev_user'], test_user=kwargs['test_user'],
                    production_user=kwargs['production_user'], create_time=kwargs['create_time'],
                    deploy_time=kwargs['deploy_time'], sql_info=kwargs['sql_info'], config=kwargs['config'],
                    deploy_info=kwargs['deploy_info'], comment=kwargs['comment'], create_user=kwargs['create_user'])


def weekly_report(**kwargs):
    """
    周报统计上线模板
    :return:
    """
    t = Template(u"""
              <div style="text-align:center;">
                  <h2>上线统计</h2>
                  <h3>{{start_date}}- {{end_date}}</h3>
                  <table width="600" cellpadding="0" cellspacing="0" border="1" style="margin:0 auto;"><tbody>
                  
                  <th>
                    <div style="width:120px;text-align:left;font:12px/15px simsun;color:#000;background:#fff;">
                     服务
                    </div>
                  </th>
                
                  <th>
                    <div style="width:120px;text-align:left;font:12px/15px simsun;color:#000;background:#fff;">
                      上线次数
                    </div>
                  </th>
                
                
                  <th>
                    <div style="width:120px;text-align:left;font:12px/15px simsun;color:#000;background:#fff;">
                       回滚次数
                    </div>
                  </th>
                
                  <th>
                    <div style="width:120px;text-align:left;font:12px/15px simsun;color:#000;background:#fff;">
                      平均耗时(h)
                    </div>
                  </th>
                    
                 {% for service in services %}
                  <tr>
                    <td>{{ service.service_name }}</td>
                    <td>{{ service.count }}</td>
                    <td>{{ service.rollback }}</td>
                    <td>{{ service.average_time }}</td>
                  </tr>
                  {% endfor %}
                  
                  </tbody></table>
            </div>  """)

    return t.render(start_date=kwargs['start_date'],
                    end_date=kwargs['end_date'],
                    service=kwargs['services'])
