# 仓库说明


## docker目录
1、***zabbix-compose***

docker安装zabbix yaml脚本


## python目录

1、***sitemap_sql.py***

站点地图生成脚本

2、***AipContentCensor.py***

调用百度图片审核接口对图片进行分析（鉴黄那些的啥的）

3、***directory_monitor.py***

监控linux目录脚本，如有新增文件会推送信息到飞书机器人, 脚本只支持单目录监控

4、***dir_watchdog.py***

监控linux目录脚本，如有新增文件会推送信息到飞书机器人, 脚本支持多级目录监控

5、***iftop.py***

监听端口流量进行统计，如果流量大于某个阀值（自己定义）该脚本可以自动封禁（iptables）端口

6、***ip_check.py***

进程版的监控家庭宽带公网IP，如果公网IP发生变化会将消息发送到飞书机器人

7、***dir_watchdog_v2.py***

监控linux目录脚本，如有新增文件会推送信息到飞书机器人，支持python和python3, 脚本支持多级目录监控

8、***feishu_check_message.py***

上传文档到飞书云文档并发送飞书卡片消息

9、***cos_upload.py***

上传文件到腾讯云对象存储

10、***feishu_robot_sg***

抄飞书应用机器人demo改吧改吧弄了一个修改腾讯云安全组的机器人，能用就行~

11、***youtube_check***

探测家庭局域网能不能访问油管，如果能访问表示局域网科学上网正常，否则就GG了会发一个飞书告警信息。

12、***ip_check_v2.py***

定时任务版的监控家庭宽带公网IP的脚本，如果公网IP发生变化会将消息发送到飞书机器人

13、***tencent_vod_time.py***

腾讯云点播每小时的播放数据导出execl脚本

14、***apk_cdn.py***

apk包上传到cdn服务器并自动预热腾讯云CDN

## shell目录

1、***buff_cache.sh***

清理buff/cache的搅拌

2、***diff_file.sh***

对比两个文件的差异，脚本里注释有注释

3、***monitor_man.sh***

不知道用来干嘛的，忘了

4、***tool_ip_scan_live.sh***

局域网ip探活脚本

5、***tool_ssh_key_add.sh***

批量分发密钥

6、***tool_user_add.sh***

Linux批量添加用户设置密码


### Install_shell目录
1、***cloud_install.sh***

上家公司安装云管平台用的脚本，已废弃

2、***frp_install.sh***

frp一键安装脚本，适用于CentOS7 x86平台

3、***mail_install.sh***

mail一键安装脚本，适用于CentOS7 x86平台

4、***mysql_install.sh***

mysql一键安装脚本，适用于CentOS7 x86平台

5、***proxmox_7_mail_install.sh***

pve mail一键安装脚本

6、***zabbix_install.sh***

zabbix一键安装脚本，适用于CentOS7 x86平台



## SQL目录

还没有东西，忽略该目录

## yum目录

记录了一下yum的配置文件
