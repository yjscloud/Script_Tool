#!/usr/bin/python3
import requests
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.vpc.v20170312 import vpc_client, models
import requests


def Security_Group(Port=None, CidrBlock=None, PolicyDescription=None):
    try:
        # 填写腾讯云SecretId、SecretKey
        cred = credential.Credential(
            "AKxxxxx9XigRxxxxxxxxxxxxx", "Rfxxxxxxxuxxxxxxxxx")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "vpc.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = vpc_client.VpcClient(cred, "ap-guangzhou", clientProfile)
        req = models.CreateSecurityGroupPoliciesRequest()
        params = {
            "SecurityGroupId": "sg-xxxxxxx",
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


def get_data(true=None, Port=None, CidrBlock=None, PolicyDescription=None):
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
    # url = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxxxxxxxxxxxx"
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxxxxxxxxxxxx"
    header = {
        "Content-type": "application/json",
        "charset": "utf-8"
    }
    requests.post(url, data=data, headers=header)
