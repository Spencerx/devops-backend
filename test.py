#!/usr/bin/env python
# -*- coding: utf-8 -*-


#import datetime
#a = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#
#print type(a)
#
#from xpinyin import Pinyin
#
#p = Pinyin()
#
#print p.get_pinyin(u'孙麒麟','')
#
#from app.models.users import Users
#
#u = Users.select()
#for i in u:
#    if i.can_approved:
#     print i.can_approved
# 导入模块

import requests
import paramiko

#
# nginx = Config(events, http, worker_processes=4, error_log='error.log',)
# with file("nginx.conf", 'w') as f:
#     f.write(str(nginx))


import sqlparse

sql = "-- 删除该直播的观看记录 DELETE FROM studylog.webcastrecord WHERE webcastId IN ( SELECT id FROM highso.webcast WHERE liveId IN (39827, 39823, 39821, 39819, 39817, 39815, 39797, 39795, 39793, 39791, 39787, 39785, 39813, 39811, 39807, 39805, 39803, 39801) ) LIMIT 18"
sql = """

DROP TABLE IF EXISTS `webcastplaybacklog`;

CREATE TABLE `webcastplaybacklog` (

  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',

  `webcast_id` bigint(20) NOT NULL COMMENT '直播ID, 关联webcast表主键id',

  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '日志状态.=0表示未拉取完成.=1表示全部拉取完成',

  `status_playback` tinyint(1) NOT NULL DEFAULT '0' COMMENT '回放是否拉取完成标记.=1表示拉取完成',

  `status_visit` tinyint(1) NOT NULL DEFAULT '0' COMMENT '访问记录是否拉取完成标记.=1表示拉取完成',

  `status_qa` tinyint(1) NOT NULL DEFAULT '0' COMMENT '问答记录是否拉取完成标记.=1表示拉取完成',

  `status_chat` tinyint(1) NOT NULL DEFAULT '0' COMMENT '聊天记录是否拉取完成标记.=1表示拉取完成',

  `retry_count` int(11) NOT NULL DEFAULT '0' COMMENT '失败重试次数',

  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',

  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

  PRIMARY KEY (`id`),

  UNIQUE KEY `uk_playbacklog_webcastid` (`webcast_id`) USING BTREE

) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""
parsed = sqlparse.format(sql, strip_comments=True, reindent=True)
print parsed
# for i in parsed:
#     for j in i.tokens:
#         print j





