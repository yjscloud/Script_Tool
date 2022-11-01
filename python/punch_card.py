# -*- coding:utf-8 -*-
import requests
import json
import datetime


# 构造飞书卡片信息
def get_data(true=None):
    ISOTIMEFORMAT = '%Y年%m月%d日 %H:%M'
    theTime = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    host_theTime = '⌚ **当前时间：**\n{}\n\n 👥 **签到人**：\n <at id=7078484766856790017>幸文权</at> \n'.format(theTime)
    data = {
        "msg_type": "interactive",
        "card": {
            {
                "config": {
                    "wide_screen_mode": true
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "content": "非常开心在** 4月亲子家庭日互动活动 **上见到你~\n玩得开心吗？",
                            "tag": "lark_md"
                        }
                    }
                ],
                "header": {
                    "template": "yellow",
                    "title": {
                        "content": "👋 广州内网IP发生变化",
                        "tag": "plain_text"
                    }
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


if __name__ == "__main__":
    req(get_data())