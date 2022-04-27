import requests
from requests.auth import HTTPBasicAuth


class User:

    def __init__(self, username: str, password: str):
        self.CLIENT_ID = '2hmSSW13I6q5YsqsynosOw'
        self.CLIENT_SECRET = '_gCMwsDK3rd4zZriIPVqOch9QwsmCQ'
        self.userAgent = 'ROS/0.0.1'
        self.authentication = HTTPBasicAuth(self.CLIENT_ID, self.CLIENT_SECRET)

        self.username = username
        self.password = password

        code = None
        tries = 0
        while code is None:
            tries += tries
            if tries > 10:
                break
            code = self.authenticate()
            if code is not None:
                break

        if code.status_code != 200:
            print('Could not log in user.')
            exit(0)
        else:
            print('User successfully logged in.')
            self.token = code.json()['access_token']

        self.header = {'Authorization': 'bearer ' + self.token, 'User-Agent': self.userAgent}

    def authenticate(self):
        data = {'grant_type': 'password', 'username': self.username, 'password': self.password}
        header = {'User-Agent': self.userAgent}
        resp = requests.post('https://www.reddit.com/api/v1/access_token', auth=self.authentication, data=data,
                             headers=header)
        if resp.status_code == 200:
            return resp
        else:
            return None

    def getUserInfo(self):
        resp = requests.get('https://oauth.reddit.com/api/v1/me', headers=self.header)

        if resp.status_code == 200:
            print(resp.json())
        else:
            print('Something went wrong.')

    def makePost(self, subreddit: str, title: str, text: str):
        data = {'ad': False, 'api_type': 'json', 'text': text, 'title': title, 'sr': subreddit, 'kind': 'self'}

        resp = requests.post('https://oauth.reddit.com/api/submit', headers=self.header, data=data)

        if resp.status_code == 200:
            print('Post successful.')
            print(resp.json())
        else:
            print('There was a problem with submitting this post.')
            print(resp.json()['errors'])

    def sendMessage(self, subject: str, message: str, recipient: str):
        data = {'api_type': 'json', 'subject': subject, 'text': message, 'to': recipient}
        resp = requests.post('https://oauth.reddit.com/api/compose', data=data, headers=self.header)

        if resp.status_code == 200:
            if resp.json()['json']['errors'] is not None:
                print('Message could not be sent.')
            else:
                print('Message successfully sent.')
            print(resp.json())
        else:
            print('Error whilst sending message.')
            print(resp.json())