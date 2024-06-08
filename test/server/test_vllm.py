import requests
import requests

url = "http://localhost:8000/v1/chat/completions"
headers = {
    "Content-Type": "application/json"
}
data = {
    "model": "Qwen2-72B-Instruct-GPTQ-Int4",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "如何做西红柿牛腩"}
    ]
}

response = requests.post(url, headers=headers, json=data)

print(response.json())