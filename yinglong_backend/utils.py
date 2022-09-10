import time


def strtime2time(string: str) -> int:
    d, t = string.split(' ')[0].split('-'), string.split(' ')[1].split(':')
    d = [int(i.replace('"', '')) for i in d]
    t = [int(i.replace('"', '')) for i in t]
    timeArray = (*d, *t, 0, 0, 0)
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def strdate2time(string: str) -> int:
    d = string.split('-')
    d = [int(i.replace('"', '')) for i in d]
    timeArray = (*d, 0, 0, 0, 0, 0, 0)
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def getIp(domain):
    import socket
    myaddr = socket.getaddrinfo(domain, 'http')[0][4][0]
    print(myaddr)


if __name__ == "__main__":
    getIp('wcp.cscxas.com')
