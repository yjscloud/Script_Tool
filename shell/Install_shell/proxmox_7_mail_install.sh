#!/bin/bash
Timestamp=`date "+%Y-%m-%d %H:%M:%S"`
echo -e "\033[1;32m$Timestamp 这是一个PVE邮件服务安装脚本 \033[0m"
echo -e "\033[1;32m$Timestamp 开始相关安装依赖 \033[0m"
apt-get install -y libsasl2-modules lsscsi sysstat net-tools

echo -e "\033[1;32m$Timestamp 配置 Postfix 信息 \033[0m"
yourhostname=`hostname`
cat > /etc/postfix/main.cf << EOF
# See /usr/share/postfix/main.cf.dist for a commented, more complete version
myhostname=$yourhostname.lan
smtpd_banner = $myhostname ESMTP $mail_name (Debian/GNU)
biff = no
append_dot_mydomain = no
alias_maps = hash:/etc/aliases
alias_database = hash:/etc/aliases
mydestination = $myhostname, localhost.$mydomain, localhost
mynetworks = 127.0.0.0/8
inet_interfaces = loopback-only
recipient_delimiter = +
smtputf8_autodetect_classes = sendmail, verify
smtputf8_enable = no
strict_smtputf8 = no
compatibility_level = 2
relayhost = smtp.163.com:465
smtp_sasl_auth_enable = yes
smtp_sasl_security_options = noanonymous
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_sender_dependent_authentication = yes
smtp_generic_maps = hash:/etc/postfix/generic
smtp_use_tls = yes
smtp_tls_wrappermode = yes
smtp_tls_security_level = encrypt
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt
EOF

echo -e "\033[1;32m$Timestamp 配置 SMTP 信息 \033[0m"
cat > /etc/postfix/sasl_passwd << EOF
smtp.163.com xxxxxx@163.com:xxxxxx
EOF

echo -e "\033[1;32m$Timestamp 重启SMTP服务 \033[0m"
postmap /etc/postfix/sasl_passwd
chmod 600 /etc/postfix/sasl_passwd

echo -e "\033[1;32m$Timestamp 配置发件人邮箱 \033[0m"
cat > /etc/postfix/generic << EOF
smtp.163.com:465 xxxxx@163.com
EOF
postmap /etc/postfix/generic

echo -e "\033[1;32m$Timestamp 重启 Postfix 服务 \033[0m"
systemctl reload postfix

echo -e "\033[1;32m$Timestamp 测试发送邮件 \033[0m"
echo "Proxmox 邮件安装脚本测试邮件" | mail -s "Test Proxmox Postfix" 1303460512@qq.com
if [ $? -eq 0 ];then
    echo -e "\033[1;32m$Timestamp Proxmox 邮件发送成功 \033[0m"
else 
    echo -e "\033[1;31m$Timestamp Proxmox 邮件发送失败  \033[0m" && exit
fi
