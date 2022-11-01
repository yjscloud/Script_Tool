#!/usr/bin/bash

#扫描ip
>ip.txt
for i in {20..254}
do
        ip=172.16.149.$i
        {
        ping -c1 -W1 $ip &> /dev/null
        if [ $? -eq 0 ];then
                echo "$ip"  >> ip.txt
        fi
        }&

done

# 生成秘钥
        if [ ! -f ~/.ssh/id_rsa ];then
                ssh-keygen -P "" -f ~/.ssh/id_rsa
        fi

# 批量分发秘钥
        while read line
        do
                /usr/bin/expect <<-EOF
                set pass 123456
                set timeout 2
                spawn ssh-copy-id  $line
                expect {
                        "yes/no" {send "yes\r";exp_continue}
                        "password:" { send "123456\r" }         
                }
                expect eof 
        EOF
        done < ip.txt