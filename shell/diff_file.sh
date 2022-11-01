#!/bin/bash

# 首先要让原始文件中的重复行只出现一次并将结果保存到两个新文件（uniq1和uniq2）中。再逐行读取两个新文件内容并使用for循环嵌套，遍历进行字段比较，将两个新文件相同内容输出到thesame文件，再在两个新文件中使用sed命令将换行的空格替换成 |，进一步反向过滤掉thesame文件内容就分别得到了两文件的独有内容。由于thesame文件使用了追加的方式，如果第二次执行脚本就会将新的内容追加到第一次执行内容之后，而不能单独得出第二次比对的结果，所以在开头设定如果之前有脚本运行产生的thesame文件存在，那么就删掉该文件重新建立新的文件，这样第二次文本对比的结果就不会受第一次的影响。

[  -e "thesame" ]&&{
        rm -f thesame
        }
[ "$#" != "2" ]&& {
        echo "input error"
        exit 0
        }
sort -u $1 > uniq1
sort -u $2 > uniq2
for Text1 in `cat  uniq1`
do
        for Text2 in `cat uniq2`
        do
                if [ "$Text1" =  "$Text2" ]
                then
                echo $Text1 >> thesame
                fi
        done
done
Except=`sed 's/ /|/g' thesame`
grep -vE "$Except" uniq1 > onlyinfile1
grep -vE "$Except" uniq2 > onlyinfile2
