import json
import requests

BASE = 'http://127.0.0.1:7000/'

mass = '200'
units = 'oz'
result_units = 'kg'

req_params = mass +'/' + units + '/' + result_units + '/'
mc_response = requests.get(BASE + req_params)
result_mass = float(json.loads(mc_response.text)['result_mass'])

print(BASE + req_params)
print(result_mass)
print(type(result_mass))
