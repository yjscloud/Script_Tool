#!/bin/bash
Timestamp=`date "+%Y-%m-%d %H:%M:%S"`
echo -e "\033[1;32m$Timestamp 安装mailx \033[0m"
yum -y install sendmail mailx

echo -e "\033[1;32m$Timestamp 配置mail账号 \033[0m"
cat > /etc/mail.rc << EOF
set bsdcompat
set from=xxxxxxx@163.com
set smtp=smtp.163.com
set smtp-auth-user=xxxx@163.com
set smtp-auth-password=xxxxx
set smtp-auth=login
EOF

echo -e "\033[1;32m$Timestamp 测试发送邮件 \033[0m"
echo "CentOS7 邮件安装脚本测试邮件" | mail -s "Test Postfix" 1303460512@qq.com
if [ $? -eq 0 ];then
    echo -e "\033[1;32m$Timestamp 邮件发送成功 \033[0m"
else 
    echo -e "\033[1;31m$Timestamp 邮件发送失败  \033[0m" && exit
fi
