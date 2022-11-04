import requests
import json
import datetime
import os
from requests_toolbelt import MultipartEncoder
import time


def get_data(true=None, file_name=None):
    ISOTIMEFORMAT01 = '%Y年%m月%d日'
    ISOTIMEFORMAT02 = '%Y年%m月%d日 %H:%M'
    theTime01 = datetime.datetime.now().strftime(ISOTIMEFORMAT01)
    theTime02 = datetime.datetime.now().strftime(ISOTIMEFORMAT02)
    feishu_url = word_url(upload_time=run_time)
    word_message = '亲爱的同事们，\n本次健康检查结果显示，当前所有云资源运行稳定，无重大风险项。\n详细检查项，请参阅[《{}》]({})'.format(
        file_name, feishu_url)
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
                    "content": "【巡检通知】" + theTime01 + "某某xxxx巡检报告",
                    "tag": "plain_text"
                }
            }
        }
    }
    return json.dumps(data, ensure_ascii=True).encode("utf-8")


def req(data):
    # webhook
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxx-xxxx-xxxx-xxxx-xxxx"
    header = {
        "Content-type": "application/json",
        "charset": "utf-8"
    }
    requests.post(url, data=data, headers=header)


def feishu_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = "{\n    \"app_id\": \"cli_a3bfbxxxxxxxxxx\",\n    \"app_secret\": \"etxxxxJxxxpkMexxxxxxxxx\"\n}"
    headers = {
        'cache-control': "no-cache",
        'postman-token': "f3axx4d7-xxxxx-xxxxx-xxxxx-xxxx-xxxx"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    rep_dict = json.loads(response.text)
    return rep_dict['tenant_access_token']


def upload_file(file_path, file_name):
    file_size = os.path.getsize(file_path)
    url = "https://open.feishu.cn/open-apis/drive/v1/files/upload_all"
    form = {'file_name': file_name,
            'parent_type': 'explorer',
            'parent_node': 'fldcxxxxxxxxxxxxxx',
            'size': str(file_size),
            'file': (open(file_path, 'rb'))}
    multi_form = MultipartEncoder(form)
    fs_token = feishu_token()
    headers = {'Authorization': 'Bearer %s' % fs_token, 'Content-Type': multi_form.content_type}
    response = requests.request("POST", url, headers=headers, data=multi_form)


def doc_time(doc_token=None, false=None):
    url = "https://open.feishu.cn/open-apis/drive/v1/metas/batch_query"
    payload = json.dumps({
        "request_docs": [
            {
                "doc_token": doc_token,
                "doc_type": "file"
            }
        ],
        "with_url": false
    })

    fs_token = feishu_token()
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % fs_token}
    response = requests.request("POST", url, headers=headers, data=payload)
    rep_time_json = json.loads(response.text)
    for i in rep_time_json['data']['metas']:
        rep_time = i["create_time"]
        return rep_time
        # print(rep_time)


def word_url(upload_time=None):
    url = "https://open.feishu.cn/open-apis/drive/v1/files?folder_token=fldcxxxxxxxxxxxxxx&page_size=10"
    payload = ''
    fs_token = feishu_token()
    headers = {'Authorization': 'Bearer %s' % fs_token}
    response = requests.request("GET", url, headers=headers, data=payload)
    rep_data = json.loads(response.text)
    rep_list = rep_data['data']['files']
    dict_token_url = {}
    for i in rep_list:
        rep_token = i['token']
        rep_url = i['url']
        dict_token_url.update({rep_token: rep_url})
    for j in dict_token_url.keys():
        doc_real_time = doc_time(doc_token=j)
        if int(doc_real_time) > upload_time:
            rep_url = dict_token_url.get(j)
            # print(rep_url)
            return rep_url
        else:
            pass


if __name__ == "__main__":
    run_time = int(time.time())
    time.sleep(1)
    # 填写你的文件路径和文件名称
    upload_file(
        "/Users/xwq/Desktop/xxxxx/xxxxx/某某报告-20221104.docx",
        "某某报告-20221104.docx")
    # 填写你的文件名称
    req(get_data(file_name='某某报告-20221104.docx'))
