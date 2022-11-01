from aip import AipImageCensor
from multiprocessing.pool import ThreadPool

checks = []
file_dumps = open("./dump.txt", "w", encoding='utf-8')

# 此脚本运行于python3环境，运行脚本前请安装如下依赖pip3 install baidu-aip bce-python-sdk utils protocol chardet
APP_ID = 'xxxxx''
API_KEY = 'xxxxxxxxxx'
SECRET_KEY = 'xxxxxxxxxxxxxxxx'


def onetest(url):
    try:
        client = AipImageCensor(APP_ID, API_KEY, SECRET_KEY)
        result = client.imageCensorUserDefined(url)
        print("审核结果:", result.get("conclusion"), ";url地址:", url)
    except Exception as e:
        print(e)

# 将需要审核的图片地址放在urls.txt里面
def loaddata():
    with open("./urls.txt", "r", encoding='utf-8') as file:
        for line in file.readlines():
            checks.append(line)


def main():
    loaddata()
    pool = ThreadPool(processes=50)
    pool.map(onetest, checks)
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
