import redis
import json
from hashlib import md5
import requests
import time
# from yinglong_backend.collection_data import collectionPhishData
from yinglong_backend.update_daliy import updateRedisDaliyData

if __name__ == '__main__':
    # collectionPhishData()
    # print(time.time())
    # updateRedisDaliyData()
    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
    token = '260d04212bcea9e7d0dbc85b7a939f41'
    response = requests.request(
        'post',
        url='http://82.156.3.168/api/verification/?token={}'.format(token))
    secret = response.json().get('secret')
    # r.sadd('yonglong_tokens', token)
    # print(r.smembers('yonglong_tokens'))
    # print(r.hgetall('yinglong_authentication'))
    timestamp = str(int(time.time()))
    headers = {"Content-Type": 'application/json'}
    payload = json.dumps({
        'token':
        token,
        'date': '2022-9-11',
        'timestamp':
        timestamp,
        'signature':
        md5('-'.join([token, secret, timestamp]).encode('utf-8')).hexdigest()
    })
    response = requests.request('post',
                                url='http://82.156.3.168/api/phishing/',
                                headers=headers,
                                data=payload)
    print(response.text)
