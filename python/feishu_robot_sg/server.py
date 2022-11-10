#!/usr/bin/python3

import os
import re
import logging
import requests
from api import MessageApiClient
from event import MessageReceiveEvent, UrlVerificationEvent, EventManager
from flask import Flask, jsonify
from dotenv import load_dotenv, find_dotenv
from gevent import pywsgi
from feishu_security import *

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
        sg_list = (tencent_sg.get("text", " ")).split("-")
        print(sg_list)
        user_input_ip = sg_list[0]
        print(user_input_ip)
        trueIp_list = re.findall(
            r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", user_input_ip)
        fs_CidrBlock = trueIp_list[0]
        print(fs_CidrBlock)
        fs_Port = sg_list[1]
        fs_PolicyDescription = sg_list[2]
        sg_return = Security_Group(
            Port=fs_Port, CidrBlock=fs_CidrBlock, PolicyDescription=fs_PolicyDescription)
        if sg_return == 1:
            text_content = '{"text":"安全组规则添加成功"}'
            req(get_data(Port=fs_Port, CidrBlock=fs_CidrBlock,
                PolicyDescription=fs_PolicyDescription))
        else:
            text_content = '{"text":"出错啦~~~, 参数填写方法如下 (1)单端口: ip-端口-备注(eg: 172.16.149.3-22403-张三临时远程ip); (2)多端口: ip-端口,端口-备注(eg: 172.16.149.3-22,22403-张三临时远程ip)"}'
    # print(text_content)
    except BaseException as err:
        # print(err)
        text_content = '{"text":"输入的参数格式有误, 请重新填写; 参数填写方法如下 (1)单端口: ip-端口-备注(eg: 172.16.149.3-22403-张三临时远程ip); (2)多端口: ip-端口,端口-备注(eg: 172.16.149.3-22,22403-张三临时远程ip)"}'

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
    event_handler, event = event_manager.get_handler_with_event(
        VERIFICATION_TOKEN, ENCRYPT_KEY)

    return event_handler(event)


if __name__ == "__main__":
    # init()
    # app.run(host="0.0.0.0", port=37778, debug=True)
    server = pywsgi.WSGIServer(('0.0.0.0', 37778), app)
    server.serve_forever()
