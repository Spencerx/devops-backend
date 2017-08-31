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

import paramiko


trans = paramiko.Transport(('192.168.15.255', 22))
# 建立连接
trans.connect(username='root', password='admin')

# 实例化一个 sftp对象,指定连接的通道
sftp = paramiko.SFTPClient.from_transport(trans)
# 发送文件
sftp.put(localpath='/Users/sunqilin/scripts/step1.sh', remotepath='/opt/step1.sh')
# 下载文件
# sftp.get(remotepath, localpath)




# 将sshclient的对象的transport指定为以上的trans
ssh = paramiko.SSHClient()
ssh._transport = trans
# 执行命令，和传统方法一样
stdin, stdout, stderr = ssh.exec_command('sh /opt/step1.sh')
print(stdout.read().decode())
print "=="
print(stderr.read().decode())
trans.close()

# 关闭连接
