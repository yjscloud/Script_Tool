import requests
import json
import datetime
import os
from requests_toolbelt import MultipartEncoder

# 脚本功能：上传文档到飞书云文档并发送飞书卡片消息
def get_data(true=None, file_name=None):
    ISOTIMEFORMAT01 = '%Y年%m月%d日'
    ISOTIMEFORMAT02 = '%Y年%m月%d日 %H:%M'
    theTime01 = datetime.datetime.now().strftime(ISOTIMEFORMAT01)
    theTime02 = datetime.datetime.now().strftime(ISOTIMEFORMAT02)
    feishu_url = word_url()
    word_message = '亲爱的同事们，\n本次健康检查结果显示，当前所有云资源运行稳定，无重大风险项。\n详细检查项，请参阅[《{}》]({})'.format(file_name, feishu_url)
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
                                "content": "**巡检时间**\n" + theTime02,
                                "tag": "lark_md"
                            }
                        }
                    ],
                    "tag": "div"
                },
                {
                    "tag": "div",
                    "text": {
                        "content": word_message,
                        "tag": "lark_md"
                    }
                },
                {
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "content": "我已知悉",
                                "tag": "plain_text"
                            },
                            "type": "primary",
                            "value": {
                                "key": "value"
                            }
                        }
                    ],
                    "tag": "action"
                },
                {
                    "tag": "hr"
                }
            ],
            "header": {
                "template": "green",
                "title": {
                    "content": "【巡检通知】" + theTime01 + "xxxxxxxx资源巡检报告",
                    "tag": "plain_text"
                }
            }
        }
    }
    return json.dumps(data, ensure_ascii=True).encode("utf-8")


def req(data):
    # 填写你的飞书机器人wehook
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxx-xxxx-xxxx-xxxx-xxxx-xxxx"
    header = {
        "Content-type": "application/json",
        "charset": "utf-8"
    }
    requests.post(url, data=data, headers=header)


def feishu_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    # 将"cli_xxxxxxx"替换为你的飞书应用App ID，将"xxxxxxxx"替换为你的飞书应用App Secret
    payload = "{\n    \"app_id\": \"cli_xxxxxxx\",\n    \"app_secret\": \"xxxxxxxx\"\n}"
    headers = {
        'cache-control': "no-cache",
        'postman-token': "f3a0d4d7-b55d-f8c3-9608-2cecf48d9abe"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    rep_dict = json.loads(response.text)
    return rep_dict['tenant_access_token']


def upload_file(file_path, file_name):
    file_size = os.path.getsize(file_path)
    url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
    # 将"fsdsfikKdfgQiHxJgSksJdgdh"替换为你实际的飞书云文档的文件夹token
    form = {'file_name': file_name,
            'parent_type': 'explorer',
            'parent_node': 'fsdsfikKdfgQiHxJgSksJdgdh',
            'size': str(file_size),
            'file': (open(file_path, 'rb'))}
    multi_form = MultipartEncoder(form)
    fs_token = feishu_token()
    headers = {'Authorization': 'Bearer %s' % fs_token, 'Content-Type': multi_form.content_type}
    response = requests.request("POST", url, headers=headers, data=multi_form)


def word_url():
    # 将url链接里面的"fsdsfikKdfgQiHxJgSksJdgdh"替换为你实际的飞书云文档的文件夹token
    url = "https://open.feishu.cn/open-apis/drive/v1/files?folder_token=fsdsfikKdfgQiHxJgSksJdgdh&page_size=10"
    payload = ''
    fs_token = feishu_token()
    headers = {'Authorization': 'Bearer %s' % fs_token}
    response = requests.request("GET", url, headers=headers, data=payload)
    rep_data = json.loads(response.text)
    rep_url = rep_data['data']['files'][-1]['url']
    return rep_url


if __name__ == '__main__':
    # 填写你的文件路径和文件名称
    upload_file("/home/test/word-20220930.docx", "word-20220930.docx")
    # 填写你的文件名称
    req(get_data(file_name='word-20220930.docx'))
