import os
from urllib.request import urlopen
import requests
import json
import datetime

log_base_dir = "/Users/xwq/Documents/code/Script_Tool/python/ip_test"
file_name = os.path.join(log_base_dir, "ip.txt")
if not os.path.exists(log_base_dir):
    os.mkdir(log_base_dir)


# 构造飞书卡片信息
def get_data(true=None, new_ip=None, old_ip=None):
    ISOTIMEFORMAT = '%Y年%m月%d日 %H:%M'
    theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    host_theTime = '⌚ **当前时间：**{}\n'.format(theTime)
    new_ip = "**当前公网IP：**{}\n".format(new_ip)
    old_ip = "**旧公网IP：**{}\n".format(old_ip)
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
                                "content": host_theTime,
                                "tag": "lark_md"
                            }
                        },
                        {
                            "is_short": true,
                            "text": {
                                "content": "",
                                "tag": "lark_md"
                            }
                        },
                        {
                            "is_short": true,
                            "text": {
                                "content": new_ip,
                                "tag": "lark_md"
                            }
                        },
                        {
                            "is_short": true,
                            "text": {
                                "content": "",
                                "tag": "lark_md"
                            }
                        },
                        {
                            "is_short": true,
                            "text": {
                                "content": old_ip,
                                "tag": "lark_md"
                            }
                        }
                    ],
                    "tag": "div"
                },
                {
                    "tag": "hr"
                }
            ],
            "header": {
                "template": "yellow",
                "title": {
                    "content": "👋 广州联通公网IP发生变化",
                    "tag": "plain_text"
                }
            }
        }
    }
    return json.dumps(data, ensure_ascii=True).encode("utf-8")


# 飞书信息发生函数
def req(data):
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/f1604b48-9f11-49a5-8b71-470e32e628cb"
    header = {
        "Content-type": "application/json",
        "charset": "utf-8"
    }
    requests.post(url, data=data, headers=header)


def ip_render():
    new_ip = urlopen('http://icanhazip.com').read()
    current_ip = new_ip.decode(encoding='utf-8')
    with open(file_name, "r", encoding='utf-8') as read_file:
        r = read_file.readlines()
        read_ip = r[-1]
        if current_ip == read_ip:
            print("ip无变化")
        else:
            req(get_data(new_ip=current_ip, old_ip=read_ip))

    with open(file_name, "a", encoding='utf-8') as write_file:
        write_file.write(current_ip)


if __name__ == "__main__":
    ip_render()
