import requests
from requests import auth

CLIENT_ID = 'blank'
CLIENT_SECRET = 'blank'

authentication = auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)

data = {'grant_type': 'password',
        'username': 'blank',
        'password': 'blank'}

header = {'User-Agent' : 'ROS/0.0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=authentication, data=data, headers=header)

TOKEN = res.json()
print(TOKEN)

header = {**header, }

test_response = requests.get('https://www.reddit.com/api/v1/me', auth=authentication, data=data, headers=header)