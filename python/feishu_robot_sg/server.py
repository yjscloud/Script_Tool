#!/usr/local/python3/bin/python3.10

import os
import logging
import re
import requests
from api import MessageApiClient
from event import MessageReceiveEvent, UrlVerificationEvent, EventManager
from flask import Flask, jsonify
from dotenv import load_dotenv, find_dotenv
import json
from gevent import pywsgi
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.vpc.v20170312 import vpc_client, models

# load env parameters form file named .env
load_dotenv(find_dotenv())

app = Flask(__name__)

# load from env
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
VERIFICATION_TOKEN = os.getenv("VERIFICATION_TOKEN")
ENCRYPT_KEY = os.getenv("ENCRYPT_KEY")
LARK_HOST = os.getenv("LARK_HOST")

# init service
message_api_client = MessageApiClient(APP_ID, APP_SECRET, LARK_HOST)
event_manager = EventManager()

def Security_Group(Port=None, CidrBlock=None, PolicyDescription=None):
    try:
        # 填写腾讯云SecretId、SecretKey
        cred = credential.Credential("AKXxxxxxxxxxxxxxxxxxxxxxx","Rffuquxxxxxxxxxxxxxxxxxxxxxx")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "vpc.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = vpc_client.VpcClient(cred, "ap-guangzhou", clientProfile)
        req = models.CreateSecurityGroupPoliciesRequest()
        params = {
            # sg-xxxxxx改为实际的安全组id
            "SecurityGroupId": "sg-xxxxxx",
            "SecurityGroupPolicySet": {
                "Ingress": [
                    {
                        "Protocol": "TCP",
                        "Port": Port,
                        "CidrBlock": CidrBlock,
                        "Action": "ACCEPT",
                        "PolicyDescription": PolicyDescription
                    }
                ]
            }
        }
        req.from_json_string(json.dumps(params))
        client.CreateSecurityGroupPolicies(req)
        # print(resp.to_json_string())
        return 1

    except TencentCloudSDKException as err:
        # print(err)
        return 2

# 构造飞书卡片信息
def get_data(true=None,Port=None, CidrBlock=None, PolicyDescription=None):
    feishu_ip = '**新增IP: **{} \n'.format(CidrBlock)
    feishu_Port = '**新增端口：**{} \n'.format(Port)
    feishu_des = '**备注信息：**{} \n'.format(PolicyDescription)
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
                            "content": feishu_ip,
                            "tag": "lark_md"
                        }
                        },
                        {
                        "is_short": true,
                        "text": {
                            "content": feishu_Port,
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
                            "content": feishu_des,
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
                    "template": "blue",
                    "title": {
                    "content": "腾讯云安全组新增规则提醒",
                    "tag": "plain_text"
                    }
                }
        }
    }
    return json.dumps(data, ensure_ascii=True).encode("utf-8")


# 飞书信息发生函数
def req(data):
    # 填写你自己的飞书机器人wehook
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxxxxxx"
    header = {
        "Content-type": "application/json",
        "charset": "utf-8"
    }
    requests.post(url, data=data, headers=header)

@event_manager.register("url_verification")
def request_url_verify_handler(req_data: UrlVerificationEvent):
    # url verification, just need return challenge
    if req_data.event.token != VERIFICATION_TOKEN:
        raise Exception("VERIFICATION_TOKEN is invalid")
    return jsonify({"challenge": req_data.event.challenge})


@event_manager.register("im.message.receive_v1")
def message_receive_event_handler(req_data: MessageReceiveEvent):
    sender_id = req_data.event.sender.sender_id
    message = req_data.event.message
    if message.message_type != "text":
        logging.warn("Other types of messages have not been processed yet")
        return jsonify()
        # get open_id and text_content
    open_id = sender_id.open_id
    tencent_sg = eval(message.content)
    try:
        sg_list = (tencent_sg.get("text"," ")).split("-")
        user_input_ip = sg_list[0]
        trueIp = re.search(r'(([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])\.){3}([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])',user_input_ip)
        fs_CidrBlock = trueIp.group()
        # print(fs_CidrBlock)
        fs_Port = sg_list[1]
        fs_PolicyDescription = sg_list[2]
        sg_return = Security_Group(Port=fs_Port, CidrBlock=fs_CidrBlock, PolicyDescription=fs_PolicyDescription)
        if sg_return == 1:
            text_content = '{"text":"安全组规则添加成功"}'
            req(get_data(Port=fs_Port, CidrBlock=fs_CidrBlock, PolicyDescription=fs_PolicyDescription))
        else:
            text_content = '{"text":"出错啦~~~, 参数填写方法如下 (1)单端口: ip-端口-备注(eg: 172.16.149.3-22403-张三临时远程ip); (2)多端口: ip-端口,端口-备注(eg: 172.16.149.3-22,22403-张三临时远程ip)"}'
    # print(text_content)
    except BaseException as err:
        # print(err)
        text_content = '{"text":"输入的参数格式有误, 请重新填写; 参数填写方法如下 (1)单端口: ip-端口-备注(eg: 172.16.149.3-22-新增临时远程ip); (2)多端口: ip-端口,端口-备注(eg: 172.16.149.3-22,80-新增临时远程ip)"}'
    
    # echo text message
    message_api_client.send_text_with_open_id(open_id, text_content)
    return jsonify()


@app.errorhandler
def msg_error_handler(ex):
    logging.error(ex)
    response = jsonify(message=str(ex))
    response.status_code = (
        ex.response.status_code if isinstance(ex, requests.HTTPError) else 500
    )
    return response


@app.route("/", methods=["POST"])
def callback_event_handler():
    # init callback instance and handle
    event_handler, event = event_manager.get_handler_with_event(VERIFICATION_TOKEN, ENCRYPT_KEY)

    return event_handler(event)


if __name__ == "__main__":
    # init()
    # app.run(host="0.0.0.0", port=3000, debug=True)
    server = pywsgi.WSGIServer(('0.0.0.0', 3000), app)
    server.serve_forever()
