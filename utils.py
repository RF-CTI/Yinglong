import datetime
import time
import requests
import json
import base64
from sqlalchemy import create_engine
from config import DB_URL, GIT_ACCESS_TOKEN


def encodeBase64(content: str):
    b64_byt = base64.b64encode(content.encode('utf-8'))
    return b64_byt.decode('utf-8')


def uploadFile(dirname: str, datetime: tuple, filename: str, content: str):
    url = 'https://api.github.com/repos/RF-CTI/IntelligenceDataRecord/contents/{}/{}/{}/{}'.format(
        dirname, *datetime, filename)

    data = json.dumps({"message": "commit from Yinglong", "content": content})

    response = requests.request('PUT',
                                url=url,
                                data=data,
                                auth=('RFCTI', GIT_ACCESS_TOKEN))
    res = response.json()['content']
    return res['sha'], res['size'], res['download_url']


def deleteFile(dirname: str, datetime: tuple, filename: str):
    url = 'https://api.github.com/repos/RF-CTI/IntelligenceDataRecord/contents/{}/{}'.format(
        dirname, *datetime, filename)

    data = json.dumps({
        "message": "delete a file",
        "sha": "0d5a690c8fad5e605a6e8766295d9d459d65de42"
    })

    requests.request('DELETE',
                     url=url,
                     data=data,
                     auth=('RFCTI', GIT_ACCESS_TOKEN))


def getIp(domain):
    import socket
    myaddr = socket.getaddrinfo(domain, 'http')[0][4][0]
    print(myaddr)


def commonQueryOrder(ModelName, ItemName, Limit):
    return ModelName.query.order_by(ItemName.desc()).limit(Limit).all()


def commonQueryCompare(ModelName, ItemName, Limit, _type):
    if _type == '>':
        return ModelName.query.filter(ItemName >= Limit).all()
    elif _type == '<':
        return ModelName.query.filter(ItemName <= Limit).all()
    elif _type == '==':
        return ModelName.query.filter(ItemName == Limit).all()


def csv2sql(path: str, names: list, sql_table: str, method: str):
    import pandas as pd
    df = pd.read_csv(path, names=names)
    conn = create_engine(DB_URL, encoding='utf8')
    pd.io.sql.to_sql(df, sql_table, conn, if_exists=method, index=None)


def getTodayTimestamp() -> int:
    today = datetime.date.today()
    return int(time.mktime(time.strptime(str(today), '%Y-%m-%d')))


def getNoNoneItem(content: list):
    if not all(content):
        return -1, None
    elif not any(content):
        for i, item in enumerate(content):
            if item is not None:
                return i, item
    else:
        return 0, content[0]


def timestamp2Datastring(timestamp: float) -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))


if __name__ == "__main__":
    getIp('wcp.cscxas.com')
