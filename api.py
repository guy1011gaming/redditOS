import requests
from requests.auth import HTTPBasicAuth

CLIENT_ID = 'blank'
CLIENT_SECRET = 'blank'

authentication = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)

data = {'grant_type': 'password',
        'username': 'blank',
        'password': 'blank'}

header = {'User-Agent' : 'ROS/0.0.1'}

def authentcate(authentication: HTTPBasicAuth, data: dict[str, str]):
        '''
        Authenticate at 'https://www.reddit.com/api/v1/access_token' to get an access token, needed for further interaction with the reddit api.

        Args:
                authentication: requests.auth.HTTPBasicAuthy
                        Object containing both the personal use script, as well as the secret of the application to authenticate
                data: dict[str, str]
                        Dict containing grant-type, username and password of the account to authenticate with
                        Follows the following scheme:
                        {
                                'grant_type' : '<grant-type here>'
                                'username' : '<username here>'
                                'password' : '<password here>'
                        }

        Returns:
                res: requests.models.Response
                        Object containing the response of the athentication, including the access-token
        '''
        headers = {'User-Agent' : 'ROS/0.0.1'}
        res = requests.post('https://www.reddit.com/api/v1/access_token', auth=authentication, data=data, headers=headers)
        return res