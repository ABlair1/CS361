import requests

BASE = 'http://127.0.0.1:6000/'

response = requests.get(BASE)
print(response.json())
