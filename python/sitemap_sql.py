#!/usr/bin/python3
# -*- coding: utf-8 -*-

# python生成sitemap，超过5万条数据自动生成新文件。

import os, datetime
import pymysql

# import sys

# reload(sys)

# sys.setdefaultencoding('utf-8')
# 手动设置你网站的域名，别忘记了结尾的斜杠!
host = 'https://blog.yjscloud.com/'

# 自动新建一个存放sitemap.xml的文件夹，默认叫sitemap，可自行修改。
# dir = os.popen('mkdir static')
# dir = os.mkdir('sitemap')

# 设定sitemap.xml文件存放的路径，别忘记了结尾的斜杠!
path = '/root/xwq/'

lastmod = datetime.date.today()

# 连接mysql读取文章id并生成urls.txt文件

# 打开数据库连接
db = pymysql.connect(host='x.x.x.x',
                     user='root',
                     password='xxxx',
                     database='databases')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

#sql="select id from nfzmcms.cms_contents where status=1;"
sql="select id from nfzmcms.cms_contents where status=1 and published_at > '2022-01-01 00:00:00';"

yjscloud_content="https://blog.yjscloud.com/contents/"
try:
    # 执行SQL语句
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        cms_id = row[0]
        yjscloud_url = str(yjscloud_content) + str(cms_id)
        # a追加模式写入
        f= open("urls.txt","a")
        f.write(yjscloud_url)
        f.write("\n")
except:
    print("Error: unable to fetch data")
db.close()


def add_file(j, f1, host, path):
    file_name = 'yjscloud_sitemap_%s.xml'%(j)
    f1.write("  <sitemap>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n  </sitemap>\n"%(host, file_name, lastmod))
    # a追加模式写入
    f = open("%s%s"%(path, file_name), "a")
    f.write('<?xml version="1.0" encoding="utf-8"?>\n')
    f.write('<urlset>\n')
    return f

# 判断总的URL数
c = 0

for i in open('urls.txt'):
    url = i.strip()
    if len(url) == 0:
        pass
    else:
        c+=1

# 判断需要生成的sitemap个数
file_num = c%50000

if file_num == 0:
    file_num = c/50000
    print ('总共有%s条URL, 生成%s个sitemap个文件' % (c, file_num))
else:
    file_num = (c/50000)+1
    print ('总共有%s条URL, 生成%s个sitemap文件' % (c, file_num))

# 自动按5W条URL生成sitemap，并自动命名为sitemap_1.xml
i = 0
j = 2
# https://docs.python.org/3/library/functions.html#open
f = open('%s/yjscloud_sitemap_1.xml'%(path), 'w+')
f.write('<?xml version="1.0" encoding="utf-8"?>\n')
f.write('<urlset  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" xmlns:video="http://www.google.com/schemas/sitemap-video/1.1" xmlns:geo="http://www.google.com/geo/schemas/sitemap/1.0" xmlns:news="http://www.google.com/schemas/sitemap-news/0.9" xmlns:mobile="http://www.google.com/schemas/sitemap-mobile/1.0" xmlns:pagemap="http://www.google.com/schemas/sitemap-pagemap/1.0" xmlns:xhtml="http://www.w3.org/1999/xhtml" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">\n')
# a追加模式写入
f1 = open('%s/sitemap.xml'%(path), 'a')
f1.write('<?xml version="1.0" encoding="utf-8"?>\n')
f1.write('<sitemapindex xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/siteindex.xsd">\n')
f1.write("  <sitemap>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n  </sitemap>\n"%(host, 'yjscloud_sitemap_1.xml', lastmod))

for url in open("urls.txt"):
    url = url.strip()
    i += 1
    c -= 1
    if i == 50000 or j == 50000:
        f.write('</urlset>')
        f.close()
        i = 0
        if c > 0:
            f = add_file(j, f1, host, path)
        j += 1
    f.write("  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>0.8</priority>\n  </url>\n"%(url, lastmod))
    if c == 0 and i != 50000:
        f.write('</urlset>')
        f.close()
        break

f1.write('</sitemapindex>')
f1.close()


# 删除urls.txt
if os.path.exists("urls.txt"):
  os.remove("urls.txt")
else:
  print("The file does not exist")
