import requests


url = "http://127.0.0.1:5000/v1"

payload = {
    "prompt": """<s>[INST]Create the code for a python gui for a chatroom.[/INST]""",
    "max_tokens": 200,
    "temperature": 1,
    "top_p": 0.9,
    "seed": 10
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url=f'{url}/completions', headers=headers, json=payload, verify=False)


r = response.json()

print(r)