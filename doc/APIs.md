# API使用方法

## 基础API

### 获取secret

- url: /api/verification/
- method: POST
- data: args

#### 参数列表

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| token | str | 令牌，用户注册即可获得 |

#### 返回结果参数列表

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| code | int | 代码，用来判断是否成功 |
| msg | str | 说明，在失败时返回，用来查看失败的原因 |
| secret | str | 秘钥，成功时返回，用来接入业务API |

####  测试方法

```python
token = '260d0421********7a939f41'
url = 'http://127.0.0.1:8000/api/verification/?token={}'.format(token)
response = requests.request('post',url=url)
secret = response.json().get('secret')
```

#### 返回示例

成功示例

```json
{
    "code": 200,
    "secret": "a972a332********77b2c13c"
}
```

失败示例

```json
{
    "code": 301,
    "msg": "Incorrect token entered."
}
```

### 订阅API

- url: /api/subscribe/
- method: POST
- data: json

#### 参数列表

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| username | str | 用户名 |
| type | int | 订阅方式（邮箱，站内信） |
| content | list | 订阅内容 |

#### 测试方法

```python
url = "http://127.0.0.1:8000/api/subscribe/"
payload={
    'username': 'hello',
    'type': 1,
    'content': [
        'ip',
        'address',
        'e-mail'
    ]
}
headers = {
    'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data=payload)
```

## 业务API

### 钓鱼网站API

- url: /api/v1/phishing/
- method: POST

#### 参数列表

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| token | str | 令牌，注册用户即可获得 |
| timestamp | str | 时间戳，如1662952368 |
| signature | str | 签名，通过鉴权接口获得secret后按照一定规则生成 |

#### 测试方法

```python
url = "http://127.0.0.1:8000/api/v1/phishing/"
headers = {
    "Content-Type": "application/json"
}
payload = json.dumps({
    "token": "260d0421********7a939f41",
    "timestamp": "1662952368",
    "signature": "f43f4525********af7af30a"
})

response = requests.request("POST", url, headers=headers, data=payload)
```

#### 返回示例

成功示例

```json
{
    "result": [
        {
            "timestamp": 1662567590,
            "domain": "http://lun.d356xzuxasms5v.amplifyapp.com",
            "ip": "13.225.214.9"
        },
        {
            "timestamp": 1662567560,
            "domain": "http://bnmcellli.net",
            "ip": "2606:4700:3031::6815:331f"
        },
        {
            "timestamp": 1662567533,
            "domain": "http://53131.ru.com",
            "ip": "172.94.68.49"
        }
    ]
}
```

失败示例

```json
{
    "code": 300,
    "msg": "Verification failed!"
}
```

### 僵尸网络API

- url: /api/v1/botnet/
- method: POST

#### 参数列表

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| token | str | 令牌，注册用户即可获得 |
| timestamp | str | 时间戳，如1662952368 |
| signature | str | 签名，通过鉴权接口获得secret后按照一定规则生成 |

#### 测试方法

```python
url = "http://127.0.0.1:8000/api/v1/botnet/"
headers = {
    "Content-Type": "application/json"
}
payload = json.dumps({
    "token": "260d0421********7a939f41",
    "timestamp": "1662952368",
    "signature": "f43f4525********af7af30a"
})

response = requests.request("POST", url, headers=headers)
```

#### 返回示例

成功示例

```json
{
    "result": [
        {
            "as_name": "SINGTEL-FIBRE Singtel Fibre Broadband",
            "as_number": 9506,
            "country": "SG",
            "first_seen": 1662654824,
            "hostname": "bb121-7-223-38.singnet.com.sg",
            "ip_address": "121.7.223.38",
            "last_online": 1662652800,
            "malware": "QakBot",
            "port": 2222,
            "status": "online"
        },
        {
            "as_name": "FASTNET-AS-ID Linknet-Fastnet ASN",
            "as_number": 23700,
            "country": "ID",
            "first_seen": 1662662662,
            "hostname": null,
            "ip_address": "139.195.63.45",
            "last_online": 1662652800,
            "malware": "QakBot",
            "port": 2222,
            "status": "online"
        },
        {
            "as_name": "MULTIMEDIA-AS",
            "as_number": 47402,
            "country": "BG",
            "first_seen": 1662674056,
            "hostname": null,
            "ip_address": "84.238.253.171",
            "last_online": 1662652800,
            "malware": "QakBot",
            "port": 443,
            "status": "offline"
        }
    ]
}
```

失败示例

```json
{
    "code": 300,
    "msg": "Verification failed!"
}
```
