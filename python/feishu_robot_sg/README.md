## 运行环境

- [Python 3](https://www.python.org/)

## 准备工作

1、在[开发者后台](https://open.feishu.cn/app/) **新建企业自建应用**，点击应用名称进入应用详情页。

2、点击**凭证与基础信息**切换页面，拿到 `App ID` 和 `App Secret`值，点击**事件订阅**切换页面：拿到 `Encrypt Key` 和 `Verification Token` 值。


4、修改环境值

修改`.env`文件中应用凭证数据为真实数据。

  ```text
  APP_ID=cli_9fxxxx00b
  APP_SECRET=EX6xxxxOF
  APP_VERIFICATION_TOKEN=cq3xxxxxxkUS
  ENCRYPT_KEY=
  ```

以上参数可以在 [开发者后台](https://open.feishu.cn/app) 查看，其中 Encrypt Key 可以为空。


## 本地运行

1、创建并激活一个新的虚拟环境

**mac/linux**

```commandline
python3 -m venv venv
. venv/bin/activate
```

**windows**

```commandline
python3 -m venv venv
venv\Scripts\activate
```

激活后，终端会显示虚拟环境的名称

```
(venv) **** python %
```

2、安装依赖

```
pip3 install -r requirements.txt
```     

3、运行

```
python3 server.py
```

## 完成配置，体验机器人

机器人接收的消息都会以回调事件请求形式，通过 POST 请求方式，送达到服务端处理。所以本地服务端启动之后，回调事件无法请求到内网，需要配置公网请求 URL。

配置分为如下: 在应用的**事件订阅**页面配置公网请求 URL。


1、点击**机器人**切换页面>打开**启用机器人**开关。

2、在**事件订阅**页面：配置**请求网址 URL**。

使用工具生成的域名，填写请求网址 URL，如下图所示。
![image.png](https://sf3-cn.feishucdn.com/obj/open-platform-opendoc/336d89fde0b7a5313ce9f90951cce581_nupZP6M8bb.png)

**注意**：配置请求网址URL和发送消息给机器人，都会有请求到后端服务，请求期间需要保证服务为启动状态。

3、为机器人选择监听事件。

在**事件订阅**页面，点击**添加事件**，选择`接收消息`事件并订阅。

4、申请权限

在**权限管理**页面，搜索需要的**权限配置**，并开通权限。

- 依赖权限清单
    - 获取与发送单聊、群组消息
    - 获取用户发给机器人的单聊消息

**注意**：`获取用户发给机器人的单聊消息`权限未展示在**已添加事件**中，必须切换到**权限管理**页面开通。

5、在**版本管理与发布**页面：**创建版本**>**申请发布**。

注意：本次涉及需要审核的权限，可以利用 [测试企业与人员功能](https://open.feishu.cn/document/home/introduction-to-custom-app-development/testing-enterprise-and-personnel-functions)
，生成测试版应用（无需发布，配置直接生效），完成测试。

**注意**：成功发布后，可以根据是否能搜到机器人，判断用户是否在机器人可用性范围内。

6、打开**飞书**，搜索**机器人名称**并开始体验机器人自动回复。
