import datetime
import time
from sqlalchemy import create_engine
from config import DB_URL


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


if __name__ == "__main__":
    getIp('wcp.cscxas.com')
