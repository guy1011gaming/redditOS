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
            self.authenticated = True
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
        data = { 'subject': subject, 'text': message, 'to': recipient}
        param = {'api_type': 'json'}
        resp = requests.post('https://oauth.reddit.com/api/compose', data=data, params=param, headers=self.header)

        if resp.status_code == 200:
            if resp.json()['json']['errors'] is not None:
                print('Message could not be sent.')
            else:
                print('Message successfully sent.')
            print(resp.json())
        else:
            print('Error whilst sending message.')
            print(resp.json())

    #set a hard limit of 50 posts per call?
    def getPosts(self, sort: str, timespan: str, from_post_id = ''):
        limit = 50
        posts = {}
        return_values = {}
        data = {'sort': sort, 't': timespan}
        param = {'limit': limit}

        if not from_post_id == '':
            if 't3_' in from_post_id:
                param['after'] = from_post_id
            else:
                param['after'] = 't3_' + from_post_id
        
        try:
            resp = requests.get('https://oauth.reddit.com/user/' + self.username + '/submitted', headers=self.header, data=data, params=param)

            if resp.status_code == 200:
                if len(resp.json()['data']['children']) > 0:
                    return_values['eol'] = False
                    for post in resp.json()['data']['children']:
                        posts[post['data']['id']] = post
                        return_values['last_id'] = 't3_' + post['data']['id']
                    
                    return_values['posts'] = posts
                    #print('User '+ self.username + ' posted in: ' + post['data']['subreddit'] + ', ' + post['data']['selftext'])
                else:
                    #End of list reached
                    return_values['eol'] = True
                    
                return return_values
            else:
                return None
                #print('There was an error fetching posts.')
            
        except:
            print('Something went wrong whilst fetching posts...')
            return None

    #Returns a list of subreddits which were returned by the reddit server with the search term
    def findSubreddits(self, searchTerm: str, from_sub_id = '', over_18_only = True):
        limit = 50  #change???
        params = {'q': searchTerm, 'include_over_18': 'on', 'limit': limit, 'show': 'all'}

        if not from_sub_id == '':
            if 't5_' in from_sub_id:
                params['after'] = from_sub_id
            else:
                params['after'] = 't5_' + from_sub_id

        subreddits = {}
        return_values = {}

        resp = requests.get('https://oauth.reddit.com/subreddits/search', params=params, headers=self.header)

        print(resp)

        if resp.status_code == 200:
            if len(resp.json()['data']['children']) > 0:
                return_values['eol'] = False

                for subreddit in resp.json()['data']['children']:
                    if (over_18_only and subreddit['data']['over18']) or not over_18_only:
                        subreddits[subreddit['data']['id']] = subreddit
                        return_values['last_id'] = 't5_' + subreddit['data']['id']
                
                return_values['subreddits'] = subreddits
            else:
                return_values['eol'] = True

            return return_values
        else:
            print('An error occurred whilst finding subreddits.')
            return

    #Pass a collection of subreddits to post a text post to 
    def autoPostToMultipleSubreddits(self, subreddits: list, title: str, text: str):
        for subreddit in subreddits:
            data = {'ad': False, 'api_type': 'json', 'text': text, 'title': title, 'sr': subreddit, 'kind': 'self'}
            #media=media for image?
            resp = requests.post('https://oauth.reddit.com/api/submit', headers=self.header, data=data)

            if resp.status_code == 200:
                print('Post to ' + subreddit + ' successful.')
            else:
                print('Post to ' + subreddit + ' unsuccessful.')

    #returns users in a list of subreddits which have any of the given terms in their public description, amount sets how many posts in a subreddit should be returned
    def getRedditUsers(self, subreddits: list):
        results = {}
        results['users'] = {}

        data = {'g': 'GLOBAL', 'show': 'all'}
        param = {'limit': 100}

        i = 0
        for subreddit in subreddits:
            if 'r/' in subreddit:
                subreddit = subreddit[2:]
            print('Getting info from r/' + subreddit)
            resp = requests.get('https://oauth.reddit.com/r/' + subreddit + '/top', headers=self.header, data=data, params=param)
            
            if resp.status_code == 200:
                #print(len(resp.json()['data']['children']))
                for k in resp.json()['data']['children']:
                    if not k['data']['author'] == '[deleted]':
                        userdata = requests.get('https://oauth.reddit.com/user/' + k['data']['author'] + '/about', headers=self.header)
                        #print(userdata.json())
                        if userdata.status_code == 200:
                            try:
                                results['users'][i] = userdata.json()['data']['name']
                                i += 1
                            except:
                                print('Problem at user: ' + userdata.json())

                        else:
                            print('Reddit Server had a problem.')
                    else:
                        print('User was deleted and could not be found.')
            else:
                print('Error with subreddit: ')
                print(resp.json())
        
        return results

    #Returns posts of given user, sorting, amount and timespan can be defined by parameter. if user is empty it will get posts of own user
    def getPostsOfUser(self, sort: str, timespan: str, count: int, user = '', from_post_id = ''):
        data = {'sort': sort, 't': timespan}
        param = {'limit': count}

        if not from_post_id == '':
            if 't3_' in from_post_id:
                param['after'] = from_post_id
            else:
                param['after'] = 't3_' + from_post_id

        returnValues = {}
        posts = {}

        if user == '':
            user = self.user.getUsername()
        
        try:
            resp = requests.get('https://oauth.reddit.com/user/' + user + '/submitted', headers=self.header, data=data, params=param)
        except:
            print('Error contacting reddit servers...')
            return

        #print(resp.json())
        if resp.status_code == 200:
            try:
                if len(resp.json()['data']['children']) > 0:
                    returnValues['eol'] = False
                    try:
                        for postSrc in resp.json()['data']['children']:
                            posts[postSrc['data']['name']] = {}
                            returnValues['last_id'] = postSrc['data']['name']

                            post = {}
                            post['subreddit'] = postSrc['data']['subreddit_name_prefixed']
                            post['upvotes'] = postSrc['data']['ups']
                            post['downvotes'] = postSrc['data']['downs']
                            post['received_awards'] = postSrc['data']['total_awards_received']
                            post['amount_comments'] = postSrc['data']['num_comments']

                            posts[postSrc['data']['name']] = post
                    except:
                        print('Error whilst reading post...')
                        print(postSrc)

                    returnValues['data'] = posts
                else:
                    returnValues['eol'] = True
                    returnValues['last_id'] = '0'
                return returnValues

            except:
                print('Error with returned posts...')
                return
        else:
            print('Status code 200 not received')
            returnValues['eol'] = True
            return returnValues

    #Returns if user has any of given terms in description
    def checkUserDescription(self, username: str, terms: list):
        if 'u/' in username:
            username = username[2:]

        userdata = requests.get('https://oauth.reddit.com/user/' + username + '/about', headers=self.header)

        hasTerm = False

        for term in terms:
            if term in userdata['data']['subreddit']['public_description']:
                hasTerm = True
                break
        
        return hasTerm
            
    def getAuthenticated(self):
        return self.authenticated

    def getHeader(self):
        return self.header

    def getUsername(self):
        return self.username