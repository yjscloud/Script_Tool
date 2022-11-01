# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from docx2pdf import convert


# 上传文件到腾讯云对象存储
def word_cos(word_name):
    # 填写你的腾讯云token
    secret_id = 'xxxxxxxxxxxxxxxxxxx'
    secret_key = 'xxxxxx'
    region = 'ap-guangzhou'
    token = None
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)  # 获取配置对象
    convert('/Users/xwq/Documents/%s.docx' % word_name, '%s.pdf' % word_name)
    client = CosS3Client(config)
    pdf_name = 'word_name' + '.pdf'
    print(pdf_name)
    object_key = pdf_name
    with open('/Users/xwq/Documents/%s' % pdf_name, 'rb') as fp:
        client.put_object(
            Bucket='xxxx-1252260644',  # Bucket 由 BucketName-APPID 组成
            Body=fp,
            Key=object_key,
            EnableMD5=True,
            StorageClass='STANDARD',
            ContentType='text/html; charset=utf-8'
        )
    pdf_url = 'https://xxxx-252260644.cos.ap-guangzhou.myqcloud.com/' + pdf_name
    print(pdf_url)


word_cos('test.docx')
