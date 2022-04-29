from reddit_user import User
import requests

class Bot():

    def __init__(self, user: User):
        self.user = user
        if not self.user.getAuthenticated():
            print('User has not been authenticated.')
            return
        else:
            print('User has been automated.')

    def findSubreddits(self, searchTerm: str, amount: int):
        data = {'include_over_18': True, 'include_profiles': False, 'limit': amount, 'query': searchTerm}
        resp = requests.post('https://oauth.reddit.com/api/search_subreddits', data=data, headers=self.user.getHeader())

        print(resp)

        if resp.status_code == 200:
            print('Following subreddits were found:')
            collection = []
            for x in resp.json()['subreddits']:
                print('r/' + x['name'])
                collection.append(x['name'])
            return collection
        else:
            print('An error occurred whilst finding subreddits.')
            return

    def autoPostToMultipleSubreddits(self, collection: list, title: str, text: str):
        for x in collection:
            data = {'ad': False, 'api_type': 'json', 'text': text, 'title': title, 'sr': x, 'kind': 'self'}
            resp = requests.post('https://oauth.reddit.com/api/submit', headers=self.user.getHeader(), data=data)

            if resp.status_code == 200:
                print('Post to ' + x + ' successful.')
            else:
                print('Post to ' + x + ' unsuccessful.')