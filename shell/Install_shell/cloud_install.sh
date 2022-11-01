#!/bin/bash
Timestamp=`date "+%Y-%m-%d %H:%M:%S"`
echo -e "$Timestamp 安装开始 " >> /data/zip/logs/cloudnew_install.log
echo -e "\033[1;32m$Timestamp 安装开始 \033[0m"

# 停止云管web
echo -e "$Timestamp 停止云管web " >> /data/zip/logs/cloudnew_install.log
echo -e "\033[1;32m$Timestamp 停止云管web \033[0m"
supervisorctl stop digitalgd_portal_web  >> /data/zip/logs/cloudnew_install.log

# 卸载旧版本云管web程序
echo -e "$Timestamp 卸载旧版本云管web程序 " >> /data/zip/logs/cloudnew_install.log
UninstallSoft=`rpm -qa | grep digitalgd`
echo -e "\033[1;32m$Timestamp 当前云管web程序版本是: $UninstallSoft \033[0m"
echo -e "\033[1;32m$Timestamp 开始卸载旧版本云管web程序 \033[0m"
rpm -e $UninstallSoft >> /data/zip/logs/cloudnew_install.log
status=`echo $?`
if [ $status -eq 0 ]
then
    echo -e "$Timestamp 旧版本云管卸载成功 " >> /data/zip/logs/cloudnew_install.log
    echo -e "\033[1;32m$Timestamp 旧版本云管卸载成功 \033[0m"
else
    echo -e "$Timestamp 云管卸载失败 " >> /data/zip/logs/cloudnew_install.log
    echo -e "\033[1;31m$Timestamp 云管卸载失败，我也不知道发生了什么事情，你自己看着办吧 \033[0m" && exit
fi


# 安装云管rpm包
echo -e "$Timestamp 安装云管rpm包 " >> /data/zip/logs/cloudnew_install.log
read -p "请您输入需要更新的云管包版本:" version
echo -e "\033[1;32m\n您输入的云管包版本是:$version \033[0m"
echo -e "\033[1;32m$Timestamp 开始更新云管 \033[0m"
rpm -ivh $version >> /data/zip/logs/cloudnew_install.log
status=`echo $?`
if [ $status -eq 0 ]
then
    echo -e "$Timestamp 云管安装成功 " >> /data/zip/logs/cloudnew_install.log
    echo -e "\033[1;32m$Timestamp 云管安装成功 \033[0m"
else
    echo -e "$Timestamp 云管安装失败，请检查您输入的云管版本是否正确 " >> /data/zip/logs/cloudnew_install.log
    echo -e "\033[1;31m$Timestamp 云管安装失败，请检查您输入的云管版本是否正确 \033[0m" && exit    
fi


# 替换配置文件
echo -e "$Timestamp 替换配置文件 " >> /data/zip/logs/cloudnew_install.log
echo -e "\033[1;32m$Timestamp 替换配置文件 \033[0m"
\cp /data/digitalgd-portal-web/web/configs/config.stable.js  /data/digitalgd-portal-web/web/configs/config.default.js

# 重启云管web
echo -e "$Timestamp 重启云管web " >> /data/zip/logs/cloudnew_install.log
echo -e "\033[1;32m$Timestamp 重启云管web \033[0m"
supervisorctl restart digitalgd_portal_web >> /data/zip/logs/cloudnew_install.log

# 云管更新完成
netstat -nltp | grep 443
status=`echo $?`
if [ $status -gt 0 ]
then
    echo -e "$Timestamp 云管更新完成 " >> /data/zip/logs/cloudnew_install.log
    echo -e "\033[1;32m$Timestamp 云管更新完成 \033[0m"
    InstallSoft=`rpm -qa | grep digitalgd`
    echo -e "\033[1;32m$Timestamp 更新后云管web程序版本是: $InstallSoft \033[0m"
else
    echo -e "$Timestamp 云管更新失败 " >> /data/zip/logs/cloudnew_install.log
    echo echo -e  "\033[1;31m$Timestamp 云管更新失败，自己看着办吧 \033[0m" && exit
fi
