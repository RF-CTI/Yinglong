import datetime
import time
import pandas as pd
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
    df = pd.read_csv(path, names=names)
    conn = create_engine(DB_URL, encoding='utf8')
    pd.io.sql.to_sql(df, sql_table, conn, if_exists=method, index=None)


def getTodayTimestamp() -> int:
    today = datetime.date.today()
    return int(time.mktime(time.strptime(str(today), '%Y-%m-%d')))


if __name__ == "__main__":
    getIp('wcp.cscxas.com')
