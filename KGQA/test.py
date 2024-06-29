import requests
import json

url = "https://api.chatanywhere.tech/v1/chat/completions"

payload = json.dumps({
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "user",
            "content": "Hello!"
        }
    ]
})
headers = {
    'Authorization': 'Bearer sk-MjDZOW5dPHFb74D2NJGqRMQaNlTZJ3Y4Wdzn0LRcTdLT3UTw',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
