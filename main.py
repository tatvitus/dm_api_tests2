"""
curl -X 'PUT' \
  'http://5.63.153.31:5051/v1/account/b030e590-39c2-43ea-b6d6-268d129517bf' \
  -H 'accept: text/plain'
}'
"""
import pprint
import requests

# url = 'http://5.63.153.31:5051/v1/account'
# headers = {
#     'accept': '*/*',
#     'Content-Type': 'application/json'
# }
# json = {
#     "login": "tus_test2",
#     "email": "tus_test2@mail.ru",
#     "password": "112233"
# }
# response = requests.post(
#     url=url,
#     headers=headers,
#     json=json)

url = 'http://5.63.153.31:5051/v1/account/b030e590-39c2-43ea-b6d6-268d129517bf'
headers = {
    'accept': 'text/plain'
}
response = requests.put(
    url=url,
    headers=headers)

print(response.status_code)
pprint.pprint(response.json())
response_json = response.json()
print(response_json['resource']['rating']['quantity'])

