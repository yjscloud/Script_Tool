import json
import datetime
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ssl.v20191205 import ssl_client, models
from prettytable import PrettyTable
from PIL import Image, ImageDraw, ImageFont
import requests
from requests_toolbelt import MultipartEncoder


def domain_time_data():
    try:
        cred = credential.Credential("AKIxxxXxxxxxxxxxxxxxxx", "xffTxxxxxxxxxxxxxxx")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ssl.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ssl_client.SslClient(cred, "", clientProfile)
        req = models.DescribeCertificatesRequest()
        params = {
            "ExpirationSort": "DESC"
        }
        req.from_json_string(json.dumps(params))
        resp = client.DescribeCertificates(req)
        domain_data01 = resp.to_json_string()
        domain_data01 = json.loads(domain_data01)
        # print(domain_data01)
        # print(type(domain_data01))
        domain_data02 = domain_data01['Certificates']
        domain_time = []
        now = datetime.datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')
        for i in domain_data02:
            if i['StatusName'] != '已过期':
                domain01 = i['Domain']
                domain02 = i['CertEndTime']
                d1 = datetime.datetime.strptime(domain02, '%Y-%m-%d %H:%M:%S')
                d2 = datetime.datetime.strptime(str(now), '%Y-%m-%d %H:%M:%S')
                delta = d1 - d2
                domain03 = delta.days
                domain04 = i['Alias']
                domain_lis = [("域名", domain01), ("过期时间", domain02), ("证书剩余有效期时间", domain03),
                              ("备注", domain04)]
                domain_dic = dict(domain_lis)
                domain_time.append(domain_dic)
        # print(domain_time)
        return domain_time
        # print(domain_data02)
    except TencentCloudSDKException as err:
        print(err)


def get_data(true=None):
    image_key = uploadImage("/Users/xwq/Documents/infzm/script_doc/script/12345.PNG")
    data = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": true
              },
              "elements": [
                {
                  "tag": "hr"
                },
                {
                  "tag": "img",
                  "img_key": image_key,
                  "alt": {
                    "tag": "plain_text",
                    "content": ""
                  },
                  "mode": "fit_horizontal",
                  "preview": true
                }
              ],
              "header": {
                "template": "green",
                "title": {
                  "content": "腾讯云域名证书信息",
                  "tag": "plain_text"
                }
              }
        }
    }
    return json.dumps(data, ensure_ascii=True).encode("utf-8")


def req(data):
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/f1xxxxxxxxxxxxxxxxxxxxxxx"
    header = {
        "Content-type": "application/json",
        "charset": "utf-8"
    }
    requests.post(url, data=data, headers=header)


def image_file():
    tab = PrettyTable()
    tab.field_names = ["域名", "过期时间", "证书剩余有效期时间", "备注"]
    data_domain = domain_time_data()
    for i in data_domain:
        d1 = i["域名"]
        d2 = i["过期时间"]
        d3 = i["证书剩余有效期时间"]
        d4 = i["备注"]
        tab.add_row([d1, d2, d3, d4])
    tab_info = str(tab)
    space = 5

    # PIL模块中，确定写入到图片中的文本字体
    font = ImageFont.truetype('/Users/xwq/Documents/infzm/script_doc/script/MSYHMONO.ttf', 15, encoding='utf-8')
    im = Image.new('RGB', (10, 10), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im, "RGB")
    img_size = draw.multiline_textsize(tab_info, font=font)
    im_new = im.resize((img_size[0] + space * 2, img_size[1] + space * 2))
    del draw
    del im
    draw = ImageDraw.Draw(im_new, 'RGB')
    draw.multiline_text((space, space), tab_info, fill=(255, 255, 255), font=font)

    im_new.save('12345.PNG', "PNG")
    del draw


def feishu_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = "{\n    \"app_id\": \"cli_a3xxxxxxxxxxxx\",\n    \"app_secret\": \"etcwxxxxxxxxxxx\"\n}"
    headers = {
        'cache-control': "no-cache",
        'postman-token': "f3a0d4d7xxxxxxxxxxxxx"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    rep_dict = json.loads(response.text)
    return rep_dict['tenant_access_token']


def uploadImage(image_path):
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    form = {'image_type': 'message',
            'image': (open(image_path, 'rb'))}
    multi_form = MultipartEncoder(form)
    fs_token = feishu_token()
    headers = {'Authorization': 'Bearer %s' % fs_token, 'Content-Type': multi_form.content_type}
    response = requests.request("POST", url, headers=headers, data=multi_form)
    response.raise_for_status()
    content = response.json()
    if content.get("code") == 0:
        return content['data']['image_key']
    else:
        return Exception("Call Api Error, errorCode is %s" % content["code"])


if __name__ == '__main__':
    image_file()
    req(get_data())
