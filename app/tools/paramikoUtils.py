#!/usr/bin/env python
# -*- coding: utf-8 -*-

import paramiko


def upload_scripts(ip, port, user, password, local_file, remote_file):
    # 建立连接
    trans = paramiko.Transport((ip, port))
    trans.connect(username=user, password=password)
    # 实例化一个 sftp对象,指定连接的通道
    sftp = paramiko.SFTPClient.from_transport(trans)
    # 发送文件
    sftp.put(localpath=local_file, remotepath=remote_file)
    # 下载文件
    # sftp.get(remotepath, localpath)
    trans.close()


def remote_excute(ip, port, user, password, script):
    # 建立连接
    trans = paramiko.Transport((ip, port))
    trans.connect(username=user, password=password)
    # 将sshclient的对象的transport指定为以上的trans
    ssh = paramiko.SSHClient()
    ssh._transport = trans

    # 执行命令，和传统方法一样
    stdin, stdout, stderr = ssh.exec_command(script)
    print(stdout.read().decode())
    print(stderr.read().decode())
    trans.close()
