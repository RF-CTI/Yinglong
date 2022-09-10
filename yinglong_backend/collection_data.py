import time
import requests
from yinglong_server.models import db, PhishingInfo, BotnetInfo
from utils import strdate2time, strtime2time


def collectionPhishData():
    url = 'https://phishstats.info/phish_score.csv'
    for _ in range(10):
        try:
            response = requests.request('get', url=url)
            break
        except Exception:
            time.sleep(20)
            continue
    with open('phish_score.csv', 'w', encoding='utf-8') as f:
        f.write(response.content)
    with open('phish_score.csv', 'r', encoding='utf-8') as f:
        data = f.readlines()
        data = data[9:]
        newdata = []
        for item in data:
            item = item.split(',')
            timeStamp = strtime2time(item[0])
            score = float(item[1].replace('"', ''))
            website = "/".join(item[2].replace('"', '').split('/')[:3])
            newdt = [
                timeStamp, website, item[3].replace('"', '').replace('\n', '')
            ]
            if score >= 4.0:
                newdata.append(newdt)
        db.session.bulk_insert_mappings(PhishingInfo, [
            dict(ip=item[-1], domain=item[1], create_time=item[0])
            for item in newdata
        ])
        db.session.commit()


def collectionBotnetData():
    headers = {
        "Content-Type":
        'application/json',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27'
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
            time.sleep(10)
            continue
    data = response.json()
    db.session.bulk_insert_mappings(BotnetInfo, [
        dict(ip=item['ip_address'],
             port=int(item['port']),
             country=item['country'],
             as_name=item['as_name'],
             as_number=int(item['as_number']),
             hostname=item['hostname'],
             status=item['status'],
             first_seen=strtime2time(item['first_seen']),
             last_online=strdate2time(item['last_online']),
             malware=item['malware']) for item in data
    ])
    db.session.commit()