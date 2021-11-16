import requests
import json

base_url = "http://localhost:8080/"

#final_url = "/{0}/friendly/{1}/url".format(base_url, any_value_here)

payload = {'number': 2, 'value': 1}
response = requests.post(base_url, data=json.dumps(payload))
print(response.text)  # TEXT/HTML
print(response.status_code, response.reason)  # HTTP
