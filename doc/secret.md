## 如何获取Signature

方法为：将token、secret、timestamp三项通过“-”连接成一个新的字符串，然后通过MD5编码，转换为16进制utf-8编码的字符串

Python示例如下：
```python
md5('-'.join([token, secret, timestamp]).encode('utf-8')).hexdigest()
```

## 分步讲解

第一步，获取Secret

```python
token = '260d0421********7a939f41'
response = requests.request(
    'post',
    url='http://127.0.0.1:8000/api/verification/?token={}'.format(token))
secret = response.json().get('secret')
```

这时拿到了服务器提供的secret，接下来将token、secret、timestamp三项合成Signature

```python
timestamp = str(int(time.time()))
signature = md5('-'.join([token, secret, timestamp]).encode('utf-8')).hexdigest()
```

最后，将这三个参数通过POST方法请求API，注意需要用JSON格式提交

```python
headers = {"Content-Type": 'application/json'}
payload = json.dumps({
    'token': token,
    'timestamp': timestamp,
    'signature': signature
})
url = 'http://127.0.0.1:8000/api/phishing/'
response = requests.request('post', url=url, headers=headers, data=payload)
```

## 完整示例代码

```python
import json
import requests
from hashlib import md5

token = '260d0421********7a939f41'
response = requests.request(
    'post',
    url='http://127.0.0.1:8000/api/verification/?token={}'.format(token))
secret = response.json().get('secret')
timestamp = str(int(time.time()))
signature = md5('-'.join([token, secret, timestamp]).encode('utf-8')).hexdigest()
headers = {"Content-Type": 'application/json'}
payload = json.dumps({
    'token': token,
    'timestamp': timestamp,
    'signature': signature
})
url = 'http://127.0.0.1:8000/api/phishing/'
response = requests.request('post', url=url, headers=headers, data=payload)
```