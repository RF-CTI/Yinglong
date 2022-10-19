import os
import redis
import time
import json
import datetime
import pandas as pd
import logging
from config import DB_URL, TMP_FILE_DIR, DB_TEST_URL
from sqlalchemy import create_engine
from utils.file_utils import uploadFile
from utils.str_utils import encodeBase64
from utils.time_utils import getTodayTimestamp

logger = logging.getLogger()

INTELLIGENCE_TYPES = {
    "phishing": ('phishing_info', 1),
    "botnet": ('botnet_info', 2),
    "c2": ('c2_info', 3)
}

DB_TABLE_LIST = [
    'intelligence_type', 'user', 'phishing_info', 'botnet_info', 'c2_info',
    'data_record', 'data_source', 'api_log', 'role', 'score_history',
    'station_letter', 'user_log'
]


def saveWeekDataRecord():
    et = getTodayTimestamp()
    bt = et - 24 * 3600 * 7
    conn = create_engine(DB_URL, encoding='utf8')
    for key in INTELLIGENCE_TYPES.keys():
        sql = 'select * from {} where timestamp >= {} and timestamp < {};'.format(
            INTELLIGENCE_TYPES[key][0], bt, et)
        df = pd.read_sql_query(sql=sql, con=conn)
        sql = '''select * from {};'''.format('data_source')
        tdf = pd.read_sql_query(sql=sql, con=conn)
        for _, row in tdf.iterrows():
            df.loc[df['source'] == row['source_id'], ['source']] = row['name']
        bt_str = time.strftime("%Y-%m-%d", time.localtime(bt))
        et_str = time.strftime("%Y-%m-%d", time.localtime(bt))
        df = df.drop(df.columns[[0]], axis=1)
        csv_name = '{}_{}_{}_record.csv'.format(key, bt_str, et_str)
        csv_path = os.path.join(TMP_FILE_DIR, csv_name)
        df.to_csv(csv_path, index=False)
        with open(csv_path, 'r', encoding='utf-8') as f:
            sha, size, url = uploadFile(key, tuple(et_str.split('-')[:2]),
                                        csv_name, encodeBase64(f.read()))
            sql = '''select * from {};'''.format('data_record')
            tdf = pd.read_sql_query(sql=sql, con=conn)
            dic = [{
                'record_id': len(tdf) + 1,
                "begin_time": bt,
                "end_time": et,
                "intelligence_type": INTELLIGENCE_TYPES[key][1],
                'size': size,
                'sha_code': sha,
                'url': url
            }]
            ndf = pd.DataFrame(dic,
                               columns=[
                                   'record_id', 'begin_time', 'end_time',
                                   'size', 'sha_code', 'url'
                               ])
            pd.io.sql.to_sql(ndf,
                             "data_record",
                             conn,
                             if_exists='append',
                             index=None)
            logger.info('Update week data {} has {} items in file {}.'.format(
                key, len(df), csv_name))


def updateTestData():
    conn = create_engine(DB_URL, encoding='utf8')
    t_conn = create_engine(DB_TEST_URL, encoding='utf8')
    for key in DB_TABLE_LIST:
        sql = '''select * from {};'''.format(key)
        df = pd.read_sql_query(sql=sql, con=conn)
        pd.io.sql.to_sql(df, key, t_conn, if_exists='replace', index=None)
        logger.info('Update test database table {} .'.format(key))


def updateRedisToken():
    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
    conn = create_engine(DB_URL, encoding='utf8')
    sql = '''select token from user;'''
    df = pd.read_sql_query(sql=sql, con=conn)
    for item in df['token']:
        r.sadd('yonglong_tokens', item)
    logger.info("Update users token: {}.".format(len(df['token'])))


def updateRedisSecretCache():
    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
    for item in r.hkeys('yinglong_authentication'):
        if r.hget('yinglong_authentication',
                  item) == r.hget('yinglong_secret_cache', item):
            r.hdel('yinglong_authentication', item)
        else:
            r.hset('yinglong_secret_cache', item,
                   r.hget('yinglong_authentication', item))
    logger.info('Clear outtime secret.')


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
    logger.info('update daliy data.')


if __name__ == '__main__':
    updateRedisToken()
