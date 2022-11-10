import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.vod.v20180717 import vod_client, models
import xlwt
import pandas as pd


try:
    # 填写你的腾讯云SecretId和secretkey
    cred = credential.Credential("AKIDxxxxxxxxxxxxxxxxxx", "YzIXxxxxxxxxxxxxxxxxxx")
    httpProfile = HttpProfile()
    httpProfile.endpoint = "vod.tencentcloudapi.com"
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = vod_client.VodClient(cred, "", clientProfile)
    req = models.DescribeMediaPlayStatDetailsRequest()
    # FileId是你的视频ID，StartTime为统计的开始时间，EndTime为结束时间（ISO时间格式），Interval表示时间的颗粒度（Hour小时，Day为天）
    params = {
        "FileId": "3877000000000000",
        "StartTime": "2022-10-29T00:00:00+08:00",
        "EndTime": "2022-10-29T23:59:59+08:00",
        "Interval": "Hour"
    }
    req.from_json_string(json.dumps(params))
    resp = client.DescribeMediaPlayStatDetails(req)
    resp_data = eval(resp.to_json_string())
    resp_list = resp_data['PlayStatInfoSet']
    # time_play = {}
    # for i in resp_list:
    #     resp_time = i['Time']
    #     resp_playtimes = i['PlayTimes']
    #     time_play.update({resp_time: resp_playtimes})
    # print(time_play)
    pf = pd.DataFrame(list(resp_list))
    order = ['Time', 'FileId', 'PlayTimes']
    pf = pf[order]
    columns_vod = {
        'Time': '时间',
        'FileId': '视频ID',
        'PlayTimes': '播放次数'
    }
    pf.rename(columns=columns_vod, inplace=True)
    # 指定生成的Excel表格名称
    file_path = pd.ExcelWriter('tencent_vod.xlsx')
    pf.fillna(' ', inplace=True)
    pf.to_excel(file_path, encoding='utf-8', index=False)
    file_path.save()

except TencentCloudSDKException as err:
    print(err)