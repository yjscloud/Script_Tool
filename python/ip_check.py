import os
import threading
from feishuapi import LarkCustomBot
from feishuapi.larkcustombot import post
from urllib.request import urlopen
import logging
import asyncio

## 使用前请先安装如下依赖：pip3 install requests feishuapi asyncio

log_base_dir = "/root/xwq"
file_name = os.path.join(log_base_dir, "ip.txt")
log_name = os.path.join(log_base_dir, "get_ip.log")

if not os.path.exists(log_base_dir):
    os.mkdir(log_base_dir)

logger = logging.getLogger('logger')
logger.setLevel(level=logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

file_handler = logging.FileHandler(log_name, 'a+', encoding='utf-8')
file_handler.setLevel(level=logging.INFO)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


# 飞书发送消息
def feishu_bot(message):
    # 填写你的飞书机器人接口地址
    webhook = 'https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxx'
    feishu = LarkCustomBot(webhook=webhook)
    first_line = [post.content_text(message)]
    asyncio.run(feishu.send_post(first_line))


# 获取ip并对比
def ip_render():
    try:
        new_ip = urlopen('http://icanhazip.com').read()
        current_ip = new_ip.decode(encoding='utf-8')
        logger.info('获取当前IP：{}'.format(current_ip))

        flag = compare_last_ip(current_ip)
        if flag:
            logger.info("记录当前IP")
            # message01 = str("广州区当前公网ip为：" + current_ip)
            # feishu_bot(message01)
    except Exception as e:
        logger.error("远程调用获取IP异常:{}".format(e))

    timer = threading.Timer(300, ip_render)  # 300秒 获取IP一次
    timer.start()


# 对比上次获取的ip
def compare_last_ip(current_ip):
    with open(file_name, "a+", encoding='utf-8') as input_file:
        last_ip = read_last_ip()
        logger.info('获取到最后一次记录的IP：{}'.format(last_ip))
        if len(last_ip) == 0:
            logger.info('获取到最后一次记录的IP：首次获取')
            input_file.write(current_ip)
            return True
        if last_ip != current_ip:
            logger.info('IP地址变化')
            input_file.write(current_ip)
            message01 = str("广州区公网IP发生变化，当前公网IP为：" + current_ip + "旧IP为：" + last_ip)
            feishu_bot(message01)
            return True
    logger.info('IP地址无变化')
    return False


# 读取上次保存的ip
def read_last_ip():
    try:
        with open(file_name, "r", encoding='utf-8') as read_file:
            contents = read_file.readlines()
            if (len(contents) > 0):
                return contents[-1]
            else:
                return ''
    except FileNotFoundError:
        logger.error("ip.txt文件不存在")
        return ''


if __name__ == "__main__":
    timer = threading.Timer(5, ip_render)  # 5s后开始循环线程
    timer.start()
