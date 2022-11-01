#!/bin/bash
Timestamp=`date "+%Y-%m-%d %H:%M:%S"`
mkdir -p /data/mysql_install/
touch /data/mysql_install/mysql_install.log
echo -e "$Timestamp 安装开始 " >> /data/mysql_install/mysql_install.log
echo -e "\033[1;32m$Timestamp 安装开始 \033[0m"

#初始化环境
echo -e  "$Timestamp 关闭防火墙" >> /data/mysql_install/mysql_install.log
systemctl stop firewalld >> /data/mysql_install/mysql_install.log 2>&1
echo -e  "$Timestamp 禁用防火墙开机启动" >> /data/mysql_install/mysql_install.log
systemctl disable firewalld >> /data/mysql_install/mysql_install.log 2>&1
echo -e  "$Timestamp 禁用selinux" >> /data/mysql_install/mysql_install.log
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
setenforce 0 >> /data/mysql_install/mysql_install.log 2>&1
echo -e  "$Timestamp 检查防火墙状态" >> /data/mysql_install/mysql_install.log
systemctl status firewalld >> /data/mysql_install/mysql_install.log 2>&1
status=`echo $?`
if [ $status -gt 0 ]
then
    echo -e "$Timestamp 环境初始化完成 " >> /data/mysql_install/mysql_install.log
    echo -e "\033[1;32m$Timestamp 环境初始化完成 \033[0m"
else
    echo -e "$Timestamp 防火墙关闭失败，请手动关闭 " >> /data/mysql_install/mysql_install.log
    echo echo -e  "\033[1;31m$Timestamp 防火墙关闭失败，请手动关闭 \033[0m" && exit
fi

#初始化磁盘 
if [ ! -d /data ];then
    mkdir /data
fi
chmod 777 /data

# 解压mysql二进制包
echo -e  "\033[1;32m$Timestamp 本脚本默认安装路径为/data，请将相关MySQL安装包上传到/data下面 \033[0m"
echo -e  "\033[1;32m$Timestamp 这里已安装mysql-5.7.32-linux-glibc2.12-x86_64.tar.gz为例 \033[0m"
tar -zxvf /data/mysql-5.7.32-linux-glibc2.12-x86_64.tar.gz -C /data/  >> /data/mysql_install/mysql_install.log
mv /data/mysql-5.7.32-linux-glibc2.12-x86_64/ /data/mysql/
mkdir /data/mysql/data


# 创建数据库用的用户
echo -e  "\033[1;32m$Timestamp 创建数据库用的用户 \033[0m"
groupadd mysql
useradd -r -s /sbin/nologin -g mysql mysql -d /data/mysql

# 初始化数据库
echo -e  "\033[1;32m$Timestamp 初始化数据库 \033[0m"
yum -y install numactl libaio  >> /data/mysql_install/mysql_install.log
/data/mysql/bin/mysqld --initialize-insecure --user=mysql --basedir=/data/mysql --datadir=/data/mysql/data


# 生成MySQL配置文件

echo -e "$Timestamp 修改MySQL配置文件 " >> /data/mysql_install/mysql_install.log
echo -e "\033[1;32m$Timestamp 修改MySQL配置文件 \033[0m"
cat > /etc/my.cnf << EOF
[mysqld] 
basedir=/data/mysql
datadir=/data/mysql/data
socket=/tmp/mysql.sock
character_set_server=utf8
user=mysql
port = 3306

symbolic-links=0
[mysqld_safe]
log-error=/data/mysql/data/error.log
pid-file=/data/mysql/data/mysql.pid
tmpdir = /tmp
EOF
 
 
# 配置MySQL开机自动启动
echo -e "\033[1;32m$Timestamp 配置MySQL开机自动启动 \033[0m"
cp /data/mysql/bin/mysqld /usr/bin/
touch /usr/lib/systemd/system/mysql.service
cat > /usr/lib/systemd/system/mysql.service << EOF
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target

[Install]
WantedBy=multi-user.target

[Service]
User=mysql
Group=mysql


PIDFile=/data/mysql/data/mysqld.pid

# Disable service start and stop timeout logic of systemd for mysqld service.
TimeoutSec=0

# Execute pre and post scripts as root
PermissionsStartOnly=true
# Needed to create system tables
#ExecStartPre=/usr/bin/mysqld_pre_systemd

# Start main service
ExecStart=/usr/bin/mysqld --daemonize --pid-file=/data/mysql/data/mysqld.pid
#注意这里要加上 --daemonize 
# Use this to switch malloc implementation
#EnvironmentFile=-/etc/sysconfig/mysql

# Sets open_files_limit
LimitNOFILE = 5000

Restart=on-failure

RestartPreventExitStatus=1

PrivateTmp=false
EOF

# 启动MySQL
echo -e "$Timestamp 启动MySQL服务 " >> /data/mysql_install/mysql_install.log
echo -e "\033[1;32m$Timestamp 启动MySQL服务 \033[0m"
systemctl start mysql.service
systemctl enable mysql.service >> /data/mysql_install/mysql_install.log
status=`echo $?`
if [ $status -eq 0 ]
then
    echo -e "$Timestamp 数据库服务启动成功 \033[0m" >> /data/mysql_install/mysql_install.log
    echo -e "\033[1;32m$Timestamp 数据库服务启动成功 \033[0m"
else
    echo -e "$Timestamp MySQL安装失败，请检查配置文件 \033[0m" >> /data/mysql_install/mysql_install.log
    echo -e "\033[1;31m$Timestamp mariadb安装失败，请检查配置文件 \033[0m" && exit    
fi

 
#初始化数据库
echo -e "$Timestamp 数据库初始化 " >> /data/mysql_install/mysql_install.log
echo -e "\033[1;32m$Timestamp 数据库初始化中 \033[0m"
mysql -e 'SET PASSWORD FOR 'root'@localhost=PASSWORD('123456');'
mysql -e 'use mysql;'
mysql -e "update user set host='%' where user='root' limit 1;"
mysql -e "flush privileges;"
echo -e "\033[1;32m MySQL的root默认密码为：123456 \033[0m"

# 检查MySQL是否安装完成
netstat -nltp | grep 3306
status=`echo $?`
if [ $status -gt 0 ]
then
    echo -e "$Timestamp MySQL安装完成 " >> /data/mysql_install/mysql_install.log
    echo -e "\033[1;32m$Timestamp MySQL安装完成 \033[0m"
else
    echo -e "$Timestamp MySQL安装失败 " >> /data/mysql_install/mysql_install.log
    echo echo -e  "\033[1;31m$Timestamp MySQL安装失败，自己看着办吧 \033[0m" && exit
fi
