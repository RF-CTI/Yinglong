import requests
import json

url = "http://127.0.0.1:8000/api/subscribe/"

payload = json.dumps({
    "type": 1,
    "username": "hello",
    "content": [
        "hello",
        "world"
    ]
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)