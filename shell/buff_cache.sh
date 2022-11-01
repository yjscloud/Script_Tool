#!/bin/bash
buff_cache=$(free -g|grep Mem:|awk '{print $6}')
server_ip=$(hostname -I |awk '{print $1}')
if [ $buff_cache -ge 1 ];then
    sync
    echo 3 > /proc/sys/vm/drop_caches
    echo "$server_ip 节点触发buff/cache自动清理任务" | mail -s "$server_ip 节点触发buff/cache自动清理任务" 1303460512@qq.com
else
   break  

fi
