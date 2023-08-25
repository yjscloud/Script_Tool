import requests
import parsel
import time
import re
import pymysql
import datetime


def spider_site(gz_site, gz_site_code):
    # 连接数据库
    connection = pymysql.connect(
        host='114.xx.xx.xx',
        user='lianjia',
        password='eRJxxxxxx',
        port=3306,
        database='lianjia'
    )
    # 获取当前时间
    current_time = datetime.datetime.now()
    table_name = '{}_{}'.format(gz_site, current_time.strftime('%Y%m%d'))
    print(table_name)

    # 检查表是否存在
    with connection.cursor() as cursor:
        check_table_sql = f"SHOW TABLES LIKE '{table_name}'"
        cursor.execute(check_table_sql)
        result = cursor.fetchone()

    if not result:  # 表不存在，创建新表
        # 创建数据表
        create_table_sql = f'''
        CREATE TABLE {table_name} (
            house_id BIGINT PRIMARY KEY,
            title VARCHAR(255),
            area VARCHAR(255),
            community VARCHAR(255),
            unit_type VARCHAR(255),
            acreage VARCHAR(255),
            path VARCHAR(255),
            furnish VARCHAR(255),
            floor VARCHAR(255),
            build_time VARCHAR(255),
            house_type VARCHAR(255),
            follow_man VARCHAR(255),
            updated VARCHAR(255),
            tag VARCHAR(255),
            total_price VARCHAR(255),
            unit_price VARCHAR(255),
            href VARCHAR(255)
        )
        '''

        # 执行SQL语句
        with connection.cursor() as cursor:
            cursor.execute(create_table_sql)
        connection.commit()

    for page in range(1, 200):
        time.sleep(1)
        url = f'https://gz.lianjia.com/ershoufang/pg{page}rs{gz_site_code}/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200 and "没有找到符合条件的房源" not in response.text:
            selector = parsel.Selector(response.text)
            lis = selector.css('.sellListContent li')
            for li in lis:
                title = li.css('.title a::text').get()  # 标题
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

                        # 插入数据
                        insert_sql = f'''
                        INSERT INTO {table_name} (
                            house_id, title, area, community, unit_type, acreage,
                            path, furnish, floor, build_time, house_type,
                            follow_man, updated, tag, total_price, unit_price, href
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s
                        )
                        '''

                        with connection.cursor() as cursor:
                            cursor.execute(insert_sql, (
                                house_id, title, area, community, unit_type, acreage,
                                path, furnish, floor, build_time, house_type,
                                follow_man, updated, tag, total_price, unit_price, href
                            ))
                        connection.commit()
                        print(house_id)
                    except Exception as e:
                        print(f"插入数据出错：{str(e)}")
                        pass
        else:
            break

    connection.close()


if __name__ == "__main__":
    gz_dit = {'shacun': '%E6%B2%99%E6%9D%91', 'yayuncheng': '%E4%BA%9A%E8%BF%90%E5%9F%8E',
              'fenghuangmingyan': '%E5%87%A4%E5%87%B0%E5%90%8D%E8%8B%91', 'heshenghuishangguoji': '%E5%90%88%E7%94%9F%E6%B9%96%E5%B1%B1%E5%9B%BD%E9%99%85'}
    for site, site_code in gz_dit.items():
        spider_site(site, site_code)

