#!/usr/local/python3/bin/python3.10
# -*- coding:utf-8 -*-
import os
import pyinotify
import time
import asyncio
from feishuapi import LarkCustomBot
from feishuapi.larkcustombot import post


# 此脚本不支持监控子目录, dir_watchdog.py脚本支持多级目录
# 使用脚本前要先安装最新的python3版本(参考：CentOS7编译安装Python3.md)和安装以下依赖"pip3 install pyinotify requests feishuapi"
def feishu_bot(message):
    # 添加你的飞书机器api接口地址
    webhook = 'https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxxxxxxxxxxxx'
    feishu = LarkCustomBot(webhook=webhook)
    first_line = [post.content_text(message)]
    asyncio.run(feishu.send_post(first_line))

class MyEvent(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        message01=str('%s'%time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())) + str("{}目录下有文件创建，文件名：{}".format(event.path, event.name))
        feishu_bot(message01)
        with open('/root/pan/directory_monitor.log', 'a') as f:
            print('%s'%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "{}目录下有文件被创建，文件名：{}".format(event.path, event.name), file=f)

    def process_IN_ACCESS(self, event):
        message02=str('%s'%time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())) + str("{}目录下有文件被访问（调用），文件名：{}".format(event.path, event.name))
        feishu_bot(message02)
        with open('/root/pan/directory_monitor.log', 'a') as f:
            print('%s'%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "{}目录下有文件被访问（调用），文件名：{}".format(event.path, event.name), file=f)

    def process_IN_DELETE(self, event):
        message03=str('%s'%time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())) + str("{}目录下有文件被删除，文件名：{}".format(event.path, event.name))
        feishu_bot(message03)
        with open('/root/pan/directory_monitor.log', 'a') as f:
            print('%s'%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "{}目录下有文件被删除，文件名：{}".format(event.path, event.name), file=f)

    def process_IN_MODIFY(self, event):
        message04=str('%s'%time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())) + str("{}目录下有文件被写入数据，文件名：{}".format(event.path, event.name))
        feishu_bot(message04)
        with open('/root/pan/directory_monitor.log', 'a') as f:
            print('%s'%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "{}目录下有文件被写入数据，文件名：{}".format(event.path, event.name), file=f)

    def process_IN_ATTRIB(self, event):
         message05=str('%s'%time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())) + str("{}目录下有文件属性被修改，文件名：{}".format(event.path, event.name))
         feishu_bot(message05)
         with open('/root/pan/directory_monitor.log', 'a') as f:
             print('%s'%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "{}目录下有文件属性被修改，文件名：{}".format(event.path, event.name), file=f)

    def process_IN_MOVED_FROM(self, event):
        message06=str('%s'%time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())) + str("{}目录下有文件被移走，文件名：{}".format(event.path, event.name))
        feishu_bot(message06)
        with open('/root/pan/directory_monitor.log', 'a') as f:
            print('%s'%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "{}目录下有文件被移走，文件名：{}".format(event.path, event.name), file=f)

    def process_IN_MOVED_TO(self, event):
        message07=str('%s'%time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())) + str("{}目录下有文件被移入，文件名：{}".format(event.path, event.name))
        feishu_bot(message08)
        with open('/root/pan/directory_monitor.log', 'a') as f:
            print('%s'%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "{}目录下有文件被移入，文件名：{}".format(event.path, event.name), file=f)



def main():
    wm = pyinotify.WatchManager()
    wm.add_watch("/wwwroot/medias/image/layout", pyinotify.ALL_EVENTS, rec=True)
    ev = MyEvent()
    notifier = pyinotify.Notifier(wm, ev)
    notifier.loop()


if __name__ == "__main__":
    main()
