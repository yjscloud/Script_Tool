import requests
import parsel
import csv
import time
import re

f = open('数据.csv', mode='a', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
    '房子id',
    '标题',
    '小区名',
    '地区',
    '户型',
    '面积',
    '朝向',
    '装修',
    '楼层',
    '总价/万',
    '单价/元每平',
    '建立时间',
    '房子类型',
    '关注人数',
    '发布时间',
    '标签',
    '详情页'
])
csv_writer.writeheader()

for page in range(1, 100):
    time.sleep(1)
    url = f'https://gz.lianjia.com/ershoufang/pg{page}rs%E6%B2%99%E6%9D%91/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200 and "没有找到符合条件的房源" not in response.text:
        selector = parsel.Selector(response.text)
        lis = selector.css('.sellListContent li')
        for li in lis:
            title = li.css('.title a::text').getall()  # 标题
            if title:
                try:
                    href = li.css('.title a::attr(href)').get()  # 详情页
                    house_id = re.search(r'/(\d+)\.html$', href).group(1)
                    area_list = li.css('.flood a::text').getall()
                    community = area_list[0]  # 小区名
                    area = area_list[1]  # 地区
                    house_info = li.css('.houseInfo::text').get().split('|')
                    if '车位' in house_info[0]:  # 跳过车位数据
                        continue
                    unit_type = house_info[0]  # 户型 几室几厅
                    acreage = house_info[1]  # 面积
                    path = house_info[2]  # 朝向
                    furnish = house_info[3]  # 装修
                    floor = house_info[4]  # 楼层
                    build_time = ''
                    if len(house_info) >= 6:
                        build_time = house_info[5]
                    house_type = house_info[-1].split()  # 房子类型
                    follow_info = li.css('.followInfo::text').get().split('/')  # 关注人数
                    follow_man = follow_info[0]  # 关注人数
                    updated = follow_info[1]  # 发布时间
                    tag_list = li.css('.tag span::text').getall()  # 标签
                    tag = '-'.join(tag_list)
                    total_price = li.css('.totalPrice span::text').get()  # 总价
                    unit_price = li.css('.unitPrice span::text').get().replace('元/平', '')  # 单价
                    dit = {
                        '房子id': house_id,
                        '标题': title,
                        '小区名': community,
                        '地区': area,
                        '户型': unit_type,
                        '面积': acreage,
                        '朝向': path,
                        '装修': furnish,
                        '楼层': floor,
                        '总价/万': total_price,
                        '单价/元每平': unit_price,
                        '建立时间': build_time,
                        '房子类型': house_type,
                        '关注人数': follow_man,
                        '发布时间': updated,
                        '标签': tag,
                        '详情页': href
                    }
                    csv_writer.writerow(dit)
                    # print(area_list)
                    # print(title)
                    print(house_id, title, area, community, unit_type, acreage, path, furnish, floor,build_time, house_type, follow_man, updated, tag, total_price, unit_price, sep='|')

                except:
                    pass
    else:
        break

f.close()
