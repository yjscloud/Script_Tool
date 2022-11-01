#!/usr/local/python3/bin/python3.10
# -*- coding:utf-8 -*-
import time
import asyncio
import os
from watchdog.observers import Observer
from watchdog.events import *
from feishuapi import LarkCustomBot
from feishuapi.larkcustombot import post

# 此脚本支持监控多级目录
# 使用脚本前要先安装最新的python3版(参考：CentOS7编译安装Python3.md文档)本和安装以下依赖"pip3 install watchdog requests feishuapi"
def feishu_bot(message):
    # 添加你的飞书机器api接口地址
    webhook = 'https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxxxxxxxxxxxx'
    feishu = LarkCustomBot(webhook=webhook)
    first_line = [post.content_text(message)]
    asyncio.run(feishu.send_post(first_line))

class FileEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        pass

    def on_created(self, event):
        if event.is_directory:
            message01=str('%s'%time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())) + str(f"{event.src_path}文件夹被创建")
            feishu_bot(message01)
        else:
            message01=str('%s'%time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())) + str(f"{event.src_path}文件被创建")
            feishu_bot(message01)

    def on_deleted(self, event):
        if event.is_directory:
            message02=str('%s'%time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())) + str(f"{event.src_path}文件夹被删除")
            feishu_bot(message02)
        else:
            message02=str('%s'%time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())) + str(f"{event.src_path}文件被删除")
            feishu_bot(message02)

    # def on_modified(self, event):
    #     if event.is_directory:
    #         message03=str('%s'%time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())) + str(f"{event.src_path}文件夹被修改")
    #         feishu_bot(message03)
    #         # print(f"{event.src_path} 被修改")
    #     else:
    #         message03=str('%s'%time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())) + str(f"{event.src_path}文件被修改")
    #         feishu_bot(message03)

    def on_moved(self, event):
        if event.is_directory:
            message04=str('%s'%time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())) + str(f"{event.src_path}文件夹被移动到{event.dest_path}")
            feishu_bot(message04)
        else:
            message04=str('%s'%time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())) + str(f"{event.src_path}文件被移动到{event.dest_path}")
            feishu_bot(message04)

if __name__ == "__main__":
    import time

    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler, r"/wwwroot/medias/image/layout", True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
