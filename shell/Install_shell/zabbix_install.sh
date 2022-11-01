#!/bin/bash
Timestamp=`date "+%Y-%m-%d %H:%M:%S"`
echo -e "$Timestamp 安装开始 " >> /root/zabbix_install/zabbix_install.log
echo -e "\033[1;32m$Timestamp 安装开始 \033[0m"
lsblk|grep -E sd'[b-z]' >/dev/null 2>&1
status=`echo $?`
if [ $status -eq 0 ]
then
    echo -e "$Timestamp 磁盘检测完成 " >> /root/zabbix_install/zabbix_install.log
    echo -e "\033[1;32m$Timestamp 磁盘检测完成 \033[0m"
else
    echo -e  "$Timestamp 数据盘不存在，请检查磁盘 " >> /root/zabbix_install/zabbix_install.log
    echo -e  "\033[1;31m$Timestamp 数据盘不存在，请检查磁盘 \033[0m" && exit
fi
 
#初始化环境
 
echo -e  "$Timestamp 关闭防火墙" >> /root/zabbix_install/zabbix_install.log
systemctl stop firewalld >> /root/zabbix_install/zabbix_install.log 2>&1
echo -e  "$Timestamp 禁用防火墙开机启动" >> /root/zabbix_install/zabbix_install.log
systemctl disable firewalld >> /root/zabbix_install/zabbix_install.log 2>&1
echo -e  "$Timestamp 禁用selinux" >> /root/zabbix_install/zabbix_install.log
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
setenforce 0 >> /root/zabbix_install/zabbix_install.log 2>&1
echo -e  "$Timestamp 检查防火墙状态" >> /root/zabbix_install/zabbix_install.log
systemctl status firewalld >> /root/zabbix_install/zabbix_install.log 2>&1
status=`echo $?`
if [ $status -gt 0 ]
then
    echo -e "$Timestamp 环境初始化完成 " >> /root/zabbix_install/zabbix_install.log
    echo -e "\033[1;32m$Timestamp 环境初始化完成 \033[0m"
else
    echo -e "$Timestamp 防火墙关闭失败，请手动关闭 " >> /root/zabbix_install/zabbix_install.log
    echo echo -e  "\033[1;31m$Timestamp 防火墙关闭失败，请手动关闭 \033[0m" && exit
fi
#初始化磁盘
 
if [ ! -d /data ];then
    mkdir /data
fi
 
echo -e "$Timestamp 创建数据盘分区 " >> /root/zabbix_install/zabbix_install.log
parted -s /dev/sdb mklabel msdos > /dev/null 2>&1
parted -s /dev/sdb mkpart primary 0% 100% > /dev/null 2>&1
echo -e "$Timestamp 格式化数据盘 " >> /root/zabbix_install/zabbix_install.log
mkfs.ext4  /dev/sdb1 > /dev/null 2>&1
echo -e "$Timestamp 挂载数据盘 " >> /root/zabbix_install/zabbix_install.log
if ! grep data /etc/fstab >/dev/null 2>&1
then
    echo "/dev/vdb1  /data  ext4  defaults   0 0"  >> /etc/fstab
fi
mount -a 
chmod 777 /data
 
 
#配置本地yum环境
echo -e "$Timestamp 解压zabbix安装包 " >> /root/zabbix_install/zabbix_install.log
tar -xvf ./zabbix_package.tar.gz -C /root/ >/dev/null 2>&1
echo -e "$Timestamp 创建zabbix yum源 " >> /root/zabbix_install/zabbix_install.log
if [ ! -d /etc/yum.repos.d/bak ];then
    mkdir /etc/yum.repos.d/bak
fi
mv /etc/yum.repos.d/*.repo /etc/yum.repos.d/bak
touch /etc/yum.repos.d/zabbix.repo
cat >> /etc/yum.repos.d/zabbix.repo << EOF
[zabbix]
name=zabbix
baseurl=file:///root/zabbix_package
gpgcheck=0
enabled=1
EOF
yum clean all >/dev/null 2>&1
 
if [ -e /etc/yum.repos.d/zabbix.repo ]
then 
    echo -e "$Timestamp 本地yum配置完成 " >> /root/zabbix_install/zabbix_install.log
    echo -e "\033[1;32m$Timestamp 本地yum配置完成 \033[0m"
else
    echo -e "$Timestamp 本地yum配置失败，请手动配置 " >> /root/zabbix_install/zabbix_install.log
    echo -e  "\033[1;31m$Timestamp本地yum配置失败，请手动配置 \033[0m" && exit
fi
#安装服务
echo -e "$Timestamp 安装服务 " >> /root/zabbix_install/zabbix_install.log
cd /root/zabbix_package/
echo -e "$Timestamp 安装Perl环境 " >> /root/zabbix_install/zabbix_install.log
yum install perl* -y >> /root/zabbix_install/zabbix_install.log 2>&1
echo -e "$Timestamp 更新mariadb-libs库 " >> /root/zabbix_install/zabbix_install.log
yum update mariadb-libs -y >> /root/zabbix_install/zabbix_install.log 
echo -e "$Timestamp 安装Zabbix服务 " >> /root/zabbix_install/zabbix_install.log
echo -e "\033[1;32m$Timestamp zabbix服务安装中 \033[0m"
yum install zabbix* -y >> /root/zabbix_install/zabbix_install.log 2>&1
echo -e "$Timestamp 安装grafana服务 " >> /root/zabbix_install/zabbix_install.log
echo -e "\033[1;32m$Timestamp grafana服务安装中 \033[0m"
yum install grafana -y >> /root/zabbix_install/zabbix_install.log 
echo -e "$Timestamp 安装MariaDB数据库 " >> /root/zabbix_install/zabbix_install.log
echo -e "\033[1;32m$Timestamp 数据库服务安装中 \033[0m"
yum install mariadb  mariadb-server  -y >> /root/zabbix_install/zabbix_install.log 
rpm -Uvh --force gnutls-3.1.18-8.el7.x86_64.rpm > /dev/null 2>&1
 
cd ..
 
echo -e "$Timestamp 修改MariaDB配置文件 " >> /root/zabbix_install/zabbix_install.log
TOTAL_MEM=`free -m|grep Mem|awk '{print $2}'`
DB_MEM=$(($TOTAL_MEM/2))
cat > /etc/my.cnf << EOF
[mysqld]
symbolic-links=0
datadir=/data/mysql
innodb_file_per_table=1
innodb_buffer_pool_size=${DB_MEM}M
innodb_log_file_size = 512M
innodb_flush_log_at_trx_commit =0
innodb_open_files=65535
port            = 3306
socket          = /var/lib/mysql/mysql.sock
skip-external-locking
lower_case_table_names = 1
skip-name-resolve
key_buffer_size = M
table_open_cache = 256
sort_buffer_size = 1M
read_buffer_size = 1M
read_rnd_buffer_size = 4M
myisam_sort_buffer_size = 64M
bulk_insert_buffer_size = 64M
query_cache_size= 16M
thread_cache_size = 8
[mysqld_safe]
log-error=/var/log/mariadb/mariadb.log
pid-file=/var/run/mariadb/mariadb.pid
 
# include all files from the config directory
#
!includedir /etc/my.cnf.d
EOF
 
echo -e "$Timestamp 启动MariaDB服务 " >> /root/zabbix_install/zabbix_install.log
systemctl enable mariadb >> /root/zabbix_install/zabbix_install.log 2>&1
systemctl start mariadb >> /root/zabbix_install/zabbix_install.log 2>&1
systemctl status mariadb >> /root/zabbix_install/zabbix_install.log 2>&1
status=`echo $?`
if [ $status -eq 0 ]
then
    echo -e "$Timestamp 数据库服务启动成功 " >> /root/zabbix_install/zabbix_install.log
    echo -e "\033[1;32m$Timestamp 数据库服务启动成功 \033[0m"
else
    echo -e "$Timestamp mariadb安装失败，请检查配置文件 " >> /root/zabbix_install/zabbix_install.log
    echo -e "\033[1;31m$Timestamp mariadb安装失败，请检查配置文件 \033[0m" && exit    
fi
 
#初始化数据库
echo -e "$Timestamp 数据库初始化 " >> /root/zabbix_install/zabbix_install.log
echo -e "\033[1;32m$Timestamp 数据库初始化中 \033[0m"
mysql -e 'drop database if exists zabbix'
mysql -e 'create database zabbix character set utf8 collate utf8_bin;'
mysql -e "grant all privileges on zabbix.* to zabbix@localhost identified by 'zabbix';"
zcat /usr/share/doc/zabbix-server-mysql-3.2.*/create.sql.gz | mysql -uzabbix -pzabbix zabbix
 
echo -e "$Timestamp 修改Zabbix配置文件 " >> /root/zabbix_install/zabbix_install.log
cat > /etc/zabbix/zabbix_server.conf << EOF
LogFile=/var/log/zabbix/zabbix_server.log
LogFileSize=100
PidFile=/var/run/zabbix/zabbix_server.pid
DBHost=localhost
DBName=zabbix
DBUser=zabbix
DBPassword=zabbix
StartPingers=5
StartDiscoverers=5
SNMPTrapperFile=/var/log/snmptrap/snmptrap.log
CacheSize=512M
HistoryCacheSize=1G
TrendCacheSize=256M
ValueCacheSize=512M
Timeout=20
AlertScriptsPath=/usr/lib/zabbix/alertscripts
ExternalScripts=/usr/lib/zabbix/externalscripts
LogSlowQueries=3000
EOF
 
echo -e "$Timestamp 启动Zabbix服务 " >> /root/zabbix_install/zabbix_install.log
systemctl restart zabbix-server >> /root/zabbix_install/zabbix_install.log 2>&1
systemctl enable zabbix-server >> /root/zabbix_install/zabbix_install.log 2>&1
systemctl status zabbix-server >> /root/zabbix_install/zabbix_install.log 2>&1
status=`echo $?`
if [ $status -eq 0 ]
then
    echo -e "$Timestamp zabbix-server启动成功 " >> /root/zabbix_install/zabbix_install.log
    echo -e "\033[1;32m$Timestamp zabbix-server启动成功 \033[0m"
else
    echo -e "$Timestamp zabbix-server安装失败，请检查配置文件 " >> /root/zabbix_install/zabbix_install.log 
    echo -e "\033[1;31 $Timestamp mzabbix-server安装失败，请检查配置文件 \033[0m" && exit    
fi
 
echo -e "$Timestamp http参数优化 " >> /root/zabbix_install/zabbix_install.log
cat > /etc/httpd/conf.d/zabbix.conf << EOF
 
# Zabbix monitoring system php web frontend
 
Alias /zabbix /usr/share/zabbix
 
<Directory "/usr/share/zabbix">
    Options FollowSymLinks
    AllowOverride None
    Require all granted
 
    <IfModule mod_php5.c>
        php_value max_execution_time 300
        php_value memory_limit 128M
        php_value post_max_size 16M
        php_value upload_max_filesize 2M
        php_value max_input_time 300
        php_value always_populate_raw_post_data -1
    php_value date.timezone  Asia/Shanghai
    </IfModule>
</Directory>
 
<Directory "/usr/share/zabbix/conf">
    Require all denied
</Directory>
 
<Directory "/usr/share/zabbix/app">
    Require all denied
</Directory>
 
<Directory "/usr/share/zabbix/include">
    Require all denied
</Directory>
 
<Directory "/usr/share/zabbix/local">
    Require all denied
</Directory>
EOF
 
echo -e "$Timestamp 重启http服务 " >> /root/zabbix_install/zabbix_install.log
systemctl start httpd >> /root/zabbix_install/zabbix_install.log 2>&1
systemctl enable httpd >> /root/zabbix_install/zabbix_install.log 2>&1
systemctl status httpd >> /root/zabbix_install/zabbix_install.log 2>&1
status=`echo $?`
if [ $status -eq 0 ]
then
    echo -e "$Timestamp httpd启动成功 " >> /root/zabbix_install/zabbix_install.log
    echo -e "\033[1;32m$Timestamp httpd启动成功 \033[0m"
else
    echo -e "$Timestamp httpd安装失败，请检查配置文件 " >> /root/zabbix_install/zabbix_install.log
    echo -e "\033[1;31m$Timestamp httpd安装失败，请检查配置文件 \033[0m" && exit    
fi
 
#install grafana
echo -e "$Timestamp 配置grafana服务 " >> /root/zabbix_install/zabbix_install.log
echo -e "$Timestamp 安装grafana zabbix插件 " >> /root/zabbix_install/zabbix_install.log
if [ ! -d /var/lib/grafana/plugins ];then
    mkdir /var/lib/grafana/plugins
    chown grafana:grafana /var/lib/grafana/plugins
fi
echo -e "\033[1;32m$Timestamp 安装grafana插件 \033[0m"
echo -e "$Timestamp 解压grafana zabbix插件 " >> /root/zabbix_install/zabbix_install.log
tar -xvf /root/zabbix_package/alexanderzobnin-grafana-zabbix-v3.4.0-0-g14a7fd4.tar.gz -C /var/lib/grafana/plugins/ > /dev/null 2>&1
echo -e "$Timestamp 重启grafana服务 " >> /root/zabbix_install/zabbix_install.log
systemctl daemon-reload >> /root/zabbix_install/zabbix_install.log 2>&1
systemctl enable grafana-server >> /root/zabbix_install/zabbix_install.log 2>&1
systemctl restart grafana-server >> /root/zabbix_install/zabbix_install.log 2>&1
systemctl status grafana-server >> /root/zabbix_install/zabbix_install.log 2>&1
status=`echo $?`
if [ $status -eq 0 ]
then
    echo -e "$Timestamp grafana-server启动成功 " >> /root/zabbix_install/zabbix_install.log
    echo -e "\033[1;32m$Timestamp grafana-server启动成功 \033[0m"
else
    echo -e "$Timestamp grafana-server安装失败，请检查配置文件 " >> /root/zabbix_install/zabbix_install.log
    echo -e "\033[1;31m$Timestamp grafana-server安装失败，请检查配置文件 \033[0m" && exit    
fi
 
if [ -d /var/lib/grafana/plugins/alexanderzobnin-grafana-zabbix-v3.4.0-0-g14a7fd4 ]
then
    echo -e "$Timestamp grafana-zabbix插件安装成功 " >> /root/zabbix_install/zabbix_install.log
    echo -e "\033[1;32m$Timestamp grafana-zabbix插件安装成功 \033[0m"
else
    echo -e "$Timestamp grafana-zabbix插件安装失败，请检查配置文件 " >> /root/zabbix_install/zabbix_install.log
    echo -e "\033[1;31m$Timestamp grafana-zabbix插件安装失败，请检查配置文件 \033[0m" && exit
fi
 
ip=`ip -o -f inet addr |grep -E eno'[0-9]' |awk '{print $4}'|awk -F '/' '{print $1}'`
    echo -e "$Timestamp 所有服务安装成功 " >> /root/zabbix_install/zabbix_install.log
    echo -e "\033[1;32m$Timestamp 所有服务安装成功 \033[0m"
    echo -e "$Timestamp 请在浏览器输入：$ip/zabbix 登录zabbix管理页面 " >> /root/zabbix_install/zabbix_install.log
    echo -e "\033[1;32m请在浏览器输入：http://$ip/zabbix 登录zabbix管理页面 \033[0m"
