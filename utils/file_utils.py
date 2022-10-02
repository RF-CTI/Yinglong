import json
import requests
from config import GIT_ACCESS_TOKEN


def uploadFile(dirname:str,datetime:tuple,filename:str,content:str):
    url = 'https://api.github.com/repos/RF-CTI/IntelligenceDataRecord/contents/{}/{}/{}/{}'.format(dirname,*datetime,filename)

    data = json.dumps({
    "message": "commit from Yinglong",
    "content": content
    })

    response = requests.request('PUT',url=url,data=data,auth=('RFCTI',GIT_ACCESS_TOKEN))
    res = response.json()['content']
    return res['sha'], res['size'], res['download_url']


def deleteFile(dirname:str,datetime:tuple,filename:str):
    url = 'https://api.github.com/repos/RF-CTI/IntelligenceDataRecord/contents/{}/{}'.format(dirname,*datetime,filename)

    data = json.dumps({
        "message": "delete a file",
        "sha": "0d5a690c8fad5e605a6e8766295d9d459d65de42"
    })

    requests.request('DELETE',url=url,data=data,auth=('RFCTI',GIT_ACCESS_TOKEN))
