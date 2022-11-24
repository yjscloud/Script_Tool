import datetime
import os
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cdn.v20180606 import cdn_client, models
import paramiko
import requests
import time
from tqdm import tqdm

# 服务器信息
hostname = 'x.x.x.x'
port = 22
user = 'root'
password = 'xxxxxxxxxxxxxxxxxxx'

# 腾讯云密钥
SecretId = 'xxxxxxxxxxxxxxxxxxx'
SecretKey = 'xxxxxxxxxxxxxxxxxxx'


def upload(local_file, remote_path):
    try:
        t = paramiko.Transport((hostname, port))
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        print('开始上传文件%s ' % datetime.datetime.now())

        try:
            sftp.put(local_file, remote_path)
        except Exception as e:
            sftp.mkdir(os.path.split(remote_path)[0])
            sftp.put(local_file, remote_path)
            print("从本地： %s 上传到： %s" % (local_file, remote_path))
        print('文件上传成功 %s ' % datetime.datetime.now())
        t.close()
    except Exception as e:
        print(repr(e))


def cdnUrl(SecretId, SecretKey, url_lists):
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "cdn.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = cdn_client.CdnClient(cred, "", clientProfile)
        req = models.PushUrlsCacheRequest()
        params = {
            "Urls": [url_lists]
        }
        req.from_json_string(json.dumps(params))
        resp = client.PushUrlsCache(req)
        print(resp.to_json_string())
    except TencentCloudSDKException as err:
        print(err)


def tqdm_download(url_lists, desc):
    resp = requests.get(url_lists, stream=True)
    # 获取文件大小
    file_size = int(resp.headers['content-length'])
    with tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024, ascii=True, desc=desc) as bar:
        with requests.get(url_lists, stream=True) as r:
            with open(desc, 'wb') as fp:
                for chunk in r.iter_content(chunk_size=512):
                    if chunk:
                        fp.write(chunk)
                        bar.update(len(chunk))
    return bar


def get_data(true=None, apk_url=None):
    apk_download = tqdm_download(url_lists, desc)
    message = '** CDN预热后下载测速**：\n {}'.format(apk_download)
    url = '** 预热地址：** \n {}'.format(apk_url)
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
                    "content": url,
                    "tag": "lark_md"
                  }
                },
                {
                      "tag": "div",
                      "text": {
                          "tag": "lark_md",
                          "content": message
                      }
                  }
              ],
              "header": {
                "template": "turquoise",
                "title": {
                  "content": "👻  CDN预热",
                  "tag": "plain_text"
                }
              }
            }
        }
    return json.dumps(data, ensure_ascii=True).encode("utf-8")


def req(data):
    # 飞书webhook地址
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxxxxxxxxxxxx"
    header = {
        "Content-type": "application/json",
        "charset": "utf-8"
    }
    requests.post(url, data=data, headers=header)


if __name__ == '__main__':
    # 文件名
    apk_name = 'xxxx.apk'
    # 文件本地路径
    local_file = r'/Users/xwq/Documents/infzm/infzm_app/{}'.format(apk_name)
    # 远程服务器的路径
    remote_path = os.path.join('/store/codes/wwwroot/images/mobile', apk_name)
    desc = apk_name
    # CDN预热地址
    url_lists = 'https://blog.yjscloud.com/mobile/{}'.format(apk_name)
    upload(local_file, remote_path)
    time.sleep(3)
    cdnUrl(SecretId, SecretKey, url_lists)
    print("等待300秒（腾讯云CDN预热刷新）")
    time.sleep(300)
    tqdm_download(url_lists, desc)
    req(get_data(apk_url=url_lists))
