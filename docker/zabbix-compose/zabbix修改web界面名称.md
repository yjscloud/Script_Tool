# 进入zabbix的docker web
```
docker exec -it data_zabbix-web_1 /bin/bash
```

# 修改配置文件
```
vi /etc/zabbix/web/zabbix.conf.php
```

# 找到修改位置

修改位置即可`ZBX_SERVER_NAME`

```
$ZBX_SERVER      = getenv('ZBX_SERVER_HOST');
$ZBX_SERVER_PORT = getenv('ZBX_SERVER_PORT');
$ZBX_SERVER_NAME = '广州-Zabbix';
```


# 修改后无需重启docker，刷新页面即生效