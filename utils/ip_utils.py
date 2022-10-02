import requests
import json


def IPLocation(ip: str) -> dict:
    url = 'http://whois.pconline.com.cn/ipJson.jsp'
    param = {
        'ip': ip,
        'json': 'true'
    } 
    ree = requests.get(url, params = param)    
    re = json.loads(ree.text.replace("\\"," "))
    return re


def domainToIP(domain):
    import socket
    myaddr = socket.getaddrinfo(domain, 'http')[0][4][0]
    return myaddr


if __name__ == '__main__':
    print(IPLocation('61.235.82.163'))
