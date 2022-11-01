# -*- coding:utf-8 -*-
import socket
from watchdog.observers import Observer
from watchdog.events import *
import requests
import json
import datetime

# 此脚本支持监控多级目录，支持python2和python3
# 使用脚本前安装以下依赖"pip install watchdog requests"

# 构造飞书卡片信息
def get_data(true=None, ip=None, theTime=None, hostname=None, file_src_path=None, src_action=None):

    host_ip = '**主机IP：**\n{}'.format(ip)
    host_theTime = '**时间：**\n{}'.format(theTime)
    host_message = '【文件监控提醒】 {}有文件{}'.format(hostname, src_action)
    data = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": true
            },
            "elements": [
                {
                    "fields": [
                        {
                            "is_short": true,
                            "text": {
                                "content": host_ip,
                                "tag": "lark_md"
                            }
                        },
                        {
                            "is_short": true,
                            "text": {
                                "content": host_theTime,
                                "tag": "lark_md"
                            }
                        }
                    ],
                    "tag": "div"
                },
                {
                    "tag": "markdown",
                    "content": file_src_path
                },
                {
                    "tag": "hr"
                }
            ],
            "header": {
                "template": "yellow",
                "title": {
                    "content": host_message,
                    "tag": "plain_text"
                }
            }
        }
    }
    return json.dumps(data, ensure_ascii=True).encode("utf-8")


# 飞书信息发生函数
def req(data):
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxx-xxxx-xxxx-xxxx"
    header = {
        "Content-type": "application/json",
        "charset": "utf-8"
    }
    requests.post(url, data=data, headers=header)


# watchdog 监控代码
class FileEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        pass

    def on_created(self, event):
        ISOTIMEFORMAT = '%Y年%m月%d日 %H:%M'
        theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        if event.is_directory:
            file_src_path = str(event.src_path)
            host_file_src_path = '**文件路径：**\n{}'.format(file_src_path)
            message01 = get_data(ip=ip, theTime=theTime, hostname=hostname, file_src_path=host_file_src_path,
                                 src_action='夹被创建')
            req(message01)
        else:
            file_src_path = str(event.src_path)
            host_file_src_path = '**文件路径：**\n{}'.format(file_src_path)
            message01 = get_data(ip=ip, theTime=theTime, hostname=hostname, file_src_path=host_file_src_path,
                                 src_action='被创建')
            req(message01)

    def on_deleted(self, event):
        ISOTIMEFORMAT = '%Y年%m月%d日 %H:%M'
        theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        if event.is_directory:
            file_src_path = str(event.src_path)
            host_file_src_path = '**文件路径：**\n{}'.format(file_src_path)
            message02 = get_data(ip=ip, theTime=theTime, hostname=hostname, file_src_path=host_file_src_path,
                                 src_action='夹被删除')
            req(message02)
        else:
            file_src_path = str(event.src_path)
            host_file_src_path = '**文件路径：**\n{}'.format(file_src_path)
            message02 = get_data(ip=ip, theTime=theTime, hostname=hostname, file_src_path=host_file_src_path,
                                 src_action='被删除')
            req(message02)

    def on_moved(self, event):
        ISOTIMEFORMAT = '%Y年%m月%d日 %H:%M'
        theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        if event.is_directory:
            file_src_path = str(event.src_path)
            file_dest_path = str(event.dest_path)
            host_file_src_path = '**动作：**\n{}文件夹被移动到{}'.format(file_src_path, file_dest_path)
            message03 = get_data(ip=ip, theTime=theTime, hostname=hostname, file_src_path=host_file_src_path,
                                 src_action='夹被移动')
            req(message03)
        else:
            file_src_path = str(event.src_path)
            file_dest_path = str(event.dest_path)
            host_file_src_path = '**动作：**\n{}文件被移动到{}'.format(file_src_path, file_dest_path)
            message03 = get_data(ip=ip, theTime=theTime, hostname=hostname, file_src_path=host_file_src_path,
                                 src_action='被移动')
            req(message03)


if __name__ == "__main__":
    import time

    observer = Observer()
    event_handler = FileEventHandler()
    # 监控路径要改为实际的路径
    observer.schedule(event_handler, r"/wwwroot/xxx/xxxx", True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
