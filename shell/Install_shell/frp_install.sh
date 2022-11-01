#!/usr/bin/env bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

# fonts color
Green="\033[32m"
Red="\033[31m"
Yellow="\033[33m"
GreenBG="\033[42;37m"
RedBG="\033[41;37m"
Font="\033[0m"
# fonts color

# variable
LinuxRelease=/etc/os-release
SYSTEM_NAME=$(cat $LinuxRelease | grep -E "^NAME=" | awk -F '=' '{print$2}' | sed "s/[\'\"]//g")
SYSTEM_VERSION_NUMBER=$(cat $LinuxRelease | grep -E "VERSION_ID=" | awk -F '=' '{print$2}' | sed "s/[\'\"]//g")
WORK_PATH=$(dirname $(readlink -f $0))
FRPC_NAME=frpc
FRPS_NAME=frps
FRP_VERSION=0.43.0
FRP_PATH=/usr/local/frp

## 组合函数
function Combin_Function() {
    frp_start
    check_pkg
    frp_install_uninstall

}

## 系统环境检查
function check_arch() {
if [ $(uname -m) = "x86_64" ]; then
    echo -e "${Green}当前环境为x86环境${Font}"
else
    echo -e  "${RedBG}当前环境为ARM环境，不支持安装，脚本退出${Font}"
    break
fi
}

## 检查是否安装frp
function check_frp(){
if [ -f "/usr/local/frp/${FRP_NAME}" ] || [ -f "/usr/local/frp/${FRP_NAME}.ini" ] || [ -f "/lib/systemd/system/${FRP_NAME}.service" ];then
    echo -e "${Green}=========================================================================${Font}"
    echo -e "${RedBG}当前已退出脚本.${Font}"
    echo -e "${Green}检查到服务器已安装${Font} ${Red}${FRP_NAME}${Font}"
    echo -e "${Green}请手动确认和删除${Font} ${Red}/usr/local/frp/${Font} ${Green}目录下的${Font} ${Red}${FRP_NAME}${Font} ${Green}和${Font} ${Red}/${FRP_NAME}.ini${Font} ${Green}文件以及${Font} ${Red}/lib/systemd/system/${FRP_NAME}.service${Font} ${Green}文件,再次执行本脚本.${Font}"
    echo -e "${Green}参考命令如下:${Font}"
    echo -e "${Red}rm -rf /usr/local/frp/${Font}"
    echo -e "${Red}rm -rf /lib/systemd/system/${FRP_NAME}.service${Font}"
    echo -e "${Green}=========================================================================${Font}"
    exit 0
fi
}

## kill 掉系统原有frp
function frp_process() {
FRPCPID=$(ps -A | grep frp | awk 'NR==1 {print $1}')
kill -9 $FRPCPID
}

## 基础软件安装
function check_pkg() {
if type apt-get >/dev/null 2>&1 ; then
    if ! type wget >/dev/null 2>&1 ; then
        apt-get install wget -y
    fi
    if ! type curl >/dev/null 2>&1 ; then
        apt-get install curl -y
    fi
fi

if type yum >/dev/null 2>&1 ; then
    if ! type wget >/dev/null 2>&1 ; then
        yum install wget -y
    fi
    if ! type curl >/dev/null 2>&1 ; then
        yum install curl -y
    fi
fi
}


## 下载frp程序
function frp_download() {
if [ ${SOURCE} = "frps_install" ];then
    if [ ! -e ${FRP_PATH} ]; then
        mkdir  ${FRP_PATH}
        wget -P ${FRP_PATH} https://video.yjscloud.com/frps
        chmod 755 ${FRP_PATH}/frps
    else
        wget -P ${FRP_PATH} https://video.yjscloud.com/frps
        chmod 755 ${FRP_PATH}/frps
    fi
else [ ${SOURCE} = "frpc_install" ]
    if [ ! -e ${FRP_PATH} ]; then
        mkdir  ${FRP_PATH}
        wget -P ${FRP_PATH} https://video.yjscloud.com/frpc
        chmod 755 ${FRP_PATH}/frpc
    else
        wget -P ${FRP_PATH} https://video.yjscloud.com/frpc
        chmod 755 ${FRP_PATH}/frpc
    fi
fi
}

## 导入frp服务端配置文件
function frps_conf_install(){
cat >${FRP_PATH}/${FRPS_NAME}.ini <<EOF
[common]
bind_port = 7000
vhost_http_port = 80
vhost_https_port = 443
allow_ports = 22,2555,1433,443,80,443,4000-10000,20000-40000
token = yjscloud@123
use_encryption = true
use_compression = true
EOF

chmod 755 ${FRP_PATH}/${FRPS_NAME}.ini

# configure systemd
cat >/lib/systemd/system/${FRPS_NAME}.service <<EOF
[Unit]
Description=Frp Server Service
After=network.target syslog.target
Wants=network.target

[Service]
Type=simple
Restart=on-failure
RestartSec=5s
ExecStart=/usr/local/frp/frps -c /usr/local/frp/${FRPS_NAME}.ini

[Install]
WantedBy=multi-user.target
EOF

chmod 755 /lib/systemd/system/${FRPS_NAME}.service

frp_success

}

## 导入frp客户端配置文件
function frpc_conf_install(){
cat >${FRP_PATH}/${FRPC_NAME}.ini <<EOF
[common]
token = yjscloud@123
server_addr = xx.xx.xx.xx
server_port = 7000
admin_addr = xx.xx.xx.xx
admin_port = 7400
admin_user = admin
admin_pwd = yjscloud@123
use_encryption = true
use_compression = true

#[ssh]
#type = tcp
#local_ip = 172.16.149.28
#local_port = 22
#remote_port = 36000
EOF

chmod 755 ${FRP_PATH}/${FRPC_NAME}.ini

cat >/lib/systemd/system/${FRPC_NAME}.service <<EOF
[Unit]  
Description=frps Daemon  
After=syslog.target network.target  
Wants=network.target  

[Service]  
Type=simple  
ExecStart=/usr/local/frp/frpc -c /usr/local/frp/${FRPC_NAME}.ini
Restart=on-failure
RestartSec=5s

[Install]  
WantedBy=multi-user.target
EOF

chmod 755 /lib/systemd/system/${FRPC_NAME}.service

frp_success

}

## 安装&&卸载frp
function frp_install_uninstall(){
if [[ ${SOURCE} = "frps_install" ]];then
    check_arch
    check_frp    
    frp_download
    frps_conf_install
elif [[ ${SOURCE} = "frpc_install" ]];then
    check_arch
    check_frp
    frp_download
    frpc_conf_install
elif [[ ${SOURCE} = "frp_uninstall" ]];then
    frp_process
    echo -e "${Red}rm -rf /usr/local/frp${Font}"
    rm -rf /usr/local/frp
    echo -e "${Red}rm -rf /lib/systemd/system/frp*.service${Font}"
    rm -rf /lib/systemd/system/frp*.service
    echo -e "${Red}卸载完成${Font}"
fi

}


function frp_success(){
if [ ${SOURCE} = "frps_install" ];then
    systemctl daemon-reload
    sudo systemctl start ${FRPS_NAME}
    sudo systemctl enable ${FRPS_NAME}
    echo -e "${Green}====================================================================${Font}"
    echo -e "${Green}安装成功,请先修改 ${FRPS_NAME}.ini 文件,确保格式及配置正确无误!${Font}"
    echo -e "${Red}vi /usr/local/frp/${FRPS_NAME}.ini${Font}"
    echo -e "${Green}修改完毕后执行以下命令重启服务:${Font}"
    echo -e "${Red}sudo systemctl restart ${FRPS_NAME}${Font}"
    echo -e "${Green}====================================================================${Font}"
elif  [ ${SOURCE} = "frpc_install" ];then
    systemctl daemon-reload
    sudo systemctl start ${FRPC_NAME}
    sudo systemctl enable ${FRPC_NAME}
    echo -e "${Green}====================================================================${Font}"
    echo -e "${Green}安装成功,请先修改 ${FRPC_NAME}.ini 文件,确保格式及配置正确无误!${Font}"
    echo -e "${Red}vi /usr/local/frp/${FRPC_NAME}.ini${Font}"
    echo -e "${Green}修改完毕后执行以下命令重启服务:${Font}"
    echo -e "${Red}sudo systemctl restart ${FRPC_NAME}${Font}"
    echo -e "${Green}====================================================================${Font}"
fi
}

function frp_start() {
    clear
    echo -e '+---------------------------------------------------+'
    echo -e '|                                                   |'
    echo -e '|   =============================================   |'
    echo -e '|                                                   |'
    echo -e '|            欢迎使用 frp 一键安装脚本           |'
    echo -e '|                                                   |'
    echo -e '|   =============================================   |'
    echo -e '|                                                   |'
    echo -e '+---------------------------------------------------+'
    echo -e ''
    echo -e ''
    echo -e ' ❖   frp服务端安装           1)'
    echo -e ' ❖   frp客户端安装           2)'
    echo -e ' ❖   frp服务端卸载           3)'
    echo -e ' ❖   frp客户端卸载           4)'
    echo -e ''
    echo -e '#####################################################'
    echo -e ''
    echo -e "        运行环境  ${SYSTEM_NAME} ${SYSTEM_VERSION_NUMBER}"
    echo -e "        系统时间  $(date "+%Y-%m-%d %H:%M:%S")"
    echo -e ''
    echo -e '#####################################################'
    CHOICE_A=$(echo -e "\n${BOLD}└─ 请选择并输入你的选项 [ 1~4 ]：${PLAIN}")
    read -p "${CHOICE_A}" INPUT
    case $INPUT in
    1)
        SOURCE="frps_install"
        ;;
    2)
        SOURCE="frpc_install"
        ;;
    3)
        SOURCE="frp_uninstall"
        ;;
    4)
        SOURCE="frp_uninstall"
        ;;
    *)
        echo -e "\n$WARN 输入错误，默认退出脚本"
        sleep 1s
        break
        ;;
    esac
}

Combin_Function
