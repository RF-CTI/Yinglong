from sqlalchemy import create_engine
from config import DB_URL


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
