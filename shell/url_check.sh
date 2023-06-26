#!/bin/bash

#url="https://open.feishu.cn/open-apis/bot/v2/hook/f1604bxxxxxxxxxxxxxx"
url="https://open.feishu.cn/open-apis/bot/v2/hook/6bxxxxxxxx"

# 定义网站域名和端口号信息
Port="443"
# 定义数组
data=(
    "www"
    "nas"
    "blog"
    "santi"
    "kvm"
    "pve"
)


date >> /data/soft/ssl-monitor.txt
# 遍历数组并输出每个元素
for WebName in "${data[@]}"
do
    # 通过 Openssl 工具获取到当前证书的到期时间
    Cert_END_Time=$(echo | openssl s_client -servername ${WebName}.yjscloud.com -connect ${WebName}.yjscloud.com:${Port} 2> /dev/null | openssl x509 -noout -dates | grep 'After' | awk -F '=' '{print $2}' | awk '{print $1,$2,$4}')
    # 将证书的到期时间转化成时间戳
    Cert_NED_TimeStamp=$(date +%s -d "$Cert_END_Time")
    # 定义当前时间的时间戳
    Create_TimeStamp=$(date +%s)
    # 通过计算获取到证书的剩余天数
    Rest_Time=$(expr $(expr $Cert_NED_TimeStamp - $Create_TimeStamp) / 86400)
    if [ ${Rest_Time} -lt 30 ]; then
        # 配置告警提示信息
        echo "${WebName}.yjscloud.com  网站的 SSL 证书还有 ${Rest_Time} 天后到期" >> /data/soft/ssl-monitor.txt
        curl -X POST \
        $url \
        -H 'Content-Type: application/json' \
        -d '{
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": "域名证书到期提醒",
                        "content": [
                            [
                                {
                                    "tag": "text",
                                    "un_escape": true,
                                    "text": "'$WebName'.yjscloud.com  网站的 SSL 证书还有 '$Rest_Time' 天后到期"
                                }
                            ]
                        ]
                    }
                }
            }
        }'
    else
        echo "${WebName}.yjscloud.com  网站的 SSL 证书还有 ${Rest_Time} 天后到期" >> /data/soft/ssl-monitor.txt
    fi
done 
