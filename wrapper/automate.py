import json
from queue import Empty
from reddit_user import User
import requests

class Bot():

    #Give bot a user account to use
    def __init__(self, user: User):
        self.user = user
        if not self.user.getAuthenticated():
            print('User has not been authenticated.')
            return
        else:
            print('User has been automated.')

    #Returns a list of subreddits which were returned by the reddit server with the search term
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

    #Pass a collection of subreddits to post a text post to 
    def autoPostToMultipleSubreddits(self, subreddits: list, title: str, text: str):
        for subreddit in subreddits:
            data = {'ad': False, 'api_type': 'json', 'text': text, 'title': title, 'sr': subreddit, 'kind': 'self'}
            
            resp = requests.post('https://oauth.reddit.com/api/submit', headers=self.user.getHeader(), data=data)

            if resp.status_code == 200:
                print('Post to ' + subreddit + ' successful.')
            else:
                print('Post to ' + subreddit + ' unsuccessful.')

    #returns users in a list of subreddits which have any of the given terms in their public description, amount sets how many posts in a subreddit should be returned
    def getRedditUsers(self, subreddits: list, terms: list, amount: int):
        data = {'g': 'GLOBAL', 'show': 'all'}
        param = {'limit': amount}
        header = self.user.getHeader()
        for subreddit in subreddits:
            resp = requests.get('https://oauth.reddit.com/r/' + subreddit + '/new', headers=header, data=data, params=param)
            if resp.status_code == 200:
                print(len(resp.json()['data']['children']))
                try:
                    for k in resp.json()['data']['children']:
                        if not k['data']['author'] == '[deleted]':
                            userdata = requests.get('https://oauth.reddit.com/user/' + k['data']['author'] + '/about', headers=self.user.getHeader())
                            
                            if userdata.status_code == 200:
                                marked = False
                                for term in terms:
                                    if not marked:
                                        if term.lower() in userdata.json()['data']['subreddit']['public_description'].lower():
                                            description = (userdata.json()['data']['subreddit']['public_description']).replace('\n', ' ')
                                            print('u/' + k['data']['author'] + ' says: ' + description)
                                            marked = True
                            else:
                                print('Reddit Server had a problem.')
                        else:
                            print('User was deleted and could not be found.')
                except:
                    print('User threw an exception.')
            else:
                print('Error with subreddit.')

    #Testing function for getting how many posts the reddit server sends back upon request
    def getCountOfResults(self, subreddit: str):
        header = self.user.getHeader()
        header['limit'] = '100'
        data = {'g': 'GLOBAL', 'show': 'all'}
        resp = requests.get('https://oauth.reddit.com/r/' + subreddit + '/new', headers=header, data=data, params={'limit': 100})
        print(len(resp.json()['data']['children']))

    #Returns posts of given user, sorting, amount and timespan can be defined by parameter. if user is empty it will get posts of own user
    def showPostsOfUser(self, sort: str, timespan: str, count: int, user = ''):
        data = {'sort': sort, 't': timespan}
        param = {'limit': count}

        if user is Empty:
            user = self.user.getUsername()

        resp = requests.get('https://oauth.reddit.com/user/' + user + '/submitted', headers=self.user.getHeader(), data=data, params=param)

        print(resp)
        print(sort + ' posts of u/' + user + ':')
        for post in resp.json()['data']['children']:
            print('r/' + post['data']['subreddit'] + ':\nTitle: ' + post['data']['title'] + '\nText: ' + post['data']['selftext'] + '\nLinks: ' + post['data']['url'] + '\n\n')
