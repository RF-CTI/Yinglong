import time
import datetime


def getTodayTimestamp() -> int:
    today = datetime.date.today()
    return int(time.mktime(time.strptime(str(today), '%Y-%m-%d')))

def getDateTimestamp(date: datetime.date) -> int:
    return int(time.mktime(time.strptime(str(date), '%Y-%m-%d')))


def timestamp2Datastring(timestamp: float) -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))


def getToday() -> datetime.date:
    return datetime.date.today()


def getTodayString() -> str:
    return str(datetime.date.today())


def getTime() -> float:
    return time.time()

def getTimeInt() -> int:
    return int(time.time())
