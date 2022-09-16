import redis
import time
import json
import datetime
import pandas as pd
from config import DB_URL
from sqlalchemy import create_engine


def updateRedisToken():
    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
    conn = create_engine(DB_URL, encoding='utf8')
    sql = '''select token from user;'''
    df = pd.read_sql_query(sql=sql, con=conn)
    for item in df['token']:
        r.sadd('yonglong_tokens', item)


def updateRedisSecretCache():
    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
    for item in r.hkeys('yinglong_authentication'):
        if r.hget('yinglong_authentication',
                  item) == r.hget('yinglong_secret_cache', item):
            r.hdel('yinglong_authentication', item)
        else:
            r.hset('yinglong_secret_cache', item,
                   r.hget('yinglong_authentication', item))


def updateRedisDaliyData():
    today = datetime.date.today()
    ts = int(time.mktime(time.strptime(str(today), '%Y-%m-%d')))
    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
    conn = create_engine(DB_URL, encoding='utf8')
    sql = '''select * from phishing_info where timestamp >= {};'''.format(ts)
    df = pd.read_sql_query(sql=sql, con=conn)
    v_json = df.to_json(orient='records',
                        date_format='epoch',
                        force_ascii=False)
    r.hset('yinglong_phishing', str(today), json.dumps(v_json))


if __name__ == '__main__':
    updateRedisToken()
