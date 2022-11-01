#!/usr/bin/bash

>ip.txt
for i in {1..254}
do
        ip=172.16.149.$i
        {
        ping -c1 -W1 $ip &> /dev/null
        if [ $? -eq 0 ];then
                echo "$ip"  >> ip.txt
        fi
        }&

done
        wait
        echo "IP OK!"