#!/usr/bin/bash

#for i in $(cat user.txt)
#do 
#       id $i &>/dev/null
#       if [ $? -ne 0 ];then
#               useradd $i && \
#               echo "123456" | passwd --stdin $i &> /dev/null
#               echo "$i add ok"
#       else
#               echo "$i is create faile !!!"
#       fi
#done

#while read user
#do
#       id $user &>/dev/null
#       if [ $? -eq 0 ];then
#               echo "useradd $user is already exists"
#       else
#               useradd $user &>/dev/null
#               echo "useradd $user is created."
#       fi
#done<user.txt

while read user
do
       u=$(echo $user|awk '{print $1}')
       p=$(echo $user|awk '{print $2}')
       id $u &>/dev/null
       if [ $? -eq 0 ];then
               echo "useradd $u  is already exists"
       else
               useradd $u &&\
               echo "$p" | passwd --stdin $u &>>/dev/null
               echo "useradd $u is created password is ok."
       fi
done<user.txt
