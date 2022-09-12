import time
import requests
import pandas as pd
from sqlalchemy import create_engine


def collectionPhishData():
    url = 'https://phishstats.info/phish_score.csv'
    for _ in range(10):
        try:
            response = requests.request('get', url=url)
            break
        except Exception:
            time.sleep(60)
            continue
    with open('phish_score.csv', 'w', encoding='utf-8') as f:
        f.write(response.text)
    conn = create_engine('sqlite:///yinglong_server/tmp/yinglong.sqlite3',
                         encoding='utf8')
    df = pd.read_csv('phish_score.csv',
                     names=['timestamp', 'score', 'domain', 'ip'],
                     error_bad_lines=False)
    df = df.drop(range(9), axis=0, inplace=False)
    # df['score'] = df['score'].astype(float, errors='raise')
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    df = df[df['score'].notna()]
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['timestamp'] = df['timestamp'].astype('int64') // 1e9
    df['domain'] = df['domain'].str.split('/', expand=True)[2]
    df.drop_duplicates(subset=['domain', 'ip'], keep='first', inplace=True)
    df = df[df['score'] >= 6.0]
    df = df.drop(['score'], axis=1, inplace=False)
    df = df.sort_values(by='timestamp')
    sql_cmd = "SELECT * FROM {}".format('phishing_info')
    tdf = pd.read_sql(sql=sql_cmd, con=conn)
    df_filter1 = df[~df['domain'].isin(tdf['domain'])]
    df_filter2 = df[~df['ip'].isin(tdf['ip'])]
    df_filter = pd.merge(df_filter1,
                         df_filter2,
                         on=['ip', 'domain', 'timestamp'],
                         how='outer')
    df_filter = df_filter.sort_values(by='timestamp')
    df_filter.insert(loc=0,
                     column='phishing_id',
                     value=range(len(tdf) + 1,
                                 len(tdf) + len(df_filter) + 1))
    print("Import {} items in to sql.".format(len(df_filter)))
    pd.io.sql.to_sql(
        df_filter,
        "phishing_info",
        conn,
        if_exists='append',  # append
        index=None)


def collectionBotnetData():
    headers = {
        "Content-Type": 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    url = 'http://feodotracker.abuse.ch/downloads/ipblocklist_recommended.json'
    for _ in range(20):
        try:
            response = requests.request('get',
                                        url,
                                        headers=headers,
                                        verify=False)
            break
        except Exception:
            time.sleep(30)
            continue
    data = response.json()
    df = pd.DataFrame(data)
    sql_cmd = "SELECT * FROM {}".format('botnet_info')
    conn = create_engine('sqlite:///yinglong_server/tmp/yinglong.sqlite3', encoding='utf8')
    tdf = pd.read_sql(sql=sql_cmd, con=conn)
    df['first_seen'] = pd.to_datetime(df['first_seen'])
    df['first_seen'] = df['first_seen'].astype('int64') // 1e9
    df['last_online'] = pd.to_datetime(df['last_online'])
    df['last_online'] = df['last_online'].astype('int64') // 1e9
    df_filter1 = df[~df['as_name'].isin(tdf['as_name'])]
    df_filter2 = df[~df['ip_address'].isin(tdf['ip_address'])]
    df_filter = pd.merge(df_filter1,
                         df_filter2,
                         on=[
                             'as_name', 'as_number', 'country', 'first_seen',
                             'hostname', 'ip_address', 'last_online',
                             'malware', 'port', 'status'
                         ],
                         how='outer')
    df_filter = df_filter.sort_values(by='last_online')
    df_filter.insert(loc=0,
                     column='botnet_id',
                     value=range(len(tdf) + 1,
                                 len(tdf) + len(df_filter) + 1))
    print("Import {} items in to sql.".format(len(df_filter)))
    pd.io.sql.to_sql(
        df_filter,
        "botnet_info",
        conn,
        if_exists='append',  # append
        index=None)
