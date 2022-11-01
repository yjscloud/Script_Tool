import requests
import json
import datetime
import random


def get_data(true=None):
    ISOTIMEFORMAT = '%Y年%m月%d日 %H:%M'
    theTime01 = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    message01 = '**异常报告时间：{}，广州内网异常请尽快调整科学上网节点** \n'.format(theTime01)
    data = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": true
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "content": message01,
                        "tag": "lark_md"
                    }
                }
            ],
            "header": {
                "template": "red",
                "title": {
                    "content": "👻 广州内网科学上网异常",
                    "tag": "plain_text"
                }
            }
        }
    }
    return json.dumps(data, ensure_ascii=True).encode("utf-8")


# 飞书信息发生函数
def req(data):
    # 填写你自己的飞书机器人wehook
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/f1604b48-xxxx-xxxxx-xxxxx-xxxxx-xxxxx"
    header = {
        "Content-type": "application/json",
        "charset": "utf-8"
    }
    requests.post(url, data=data, headers=header)


def get_status():
    try:
        user_agent = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        ]

        headers = {'User-Agent': random.choice(user_agent)}
        url = 'https://www.youtube.com'

        response = requests.get(url=url, headers=headers)
        return response.status_code
    except BaseException as error:
        # print("连接超时")
        return error


def main():
    ISOTIMEFORMAT02 = '%Y年%m月%d日 %H:%M'
    theTime02 = datetime.datetime.now().strftime(ISOTIMEFORMAT02)
    status = get_status()
    if status == 200:
        print(theTime02 + " success")
    else:
        req(get_data())


if __name__ == '__main__':
    main()
