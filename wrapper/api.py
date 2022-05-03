from reddit_user import User

def test_login_user():
    return User('RedditOS_', 'RedditOSMaxHenning2022')

def test_get_user_posts(user: User):
    resp = {}
    resp['last_id'] = ''
    resp['eol'] = False
    while not resp['eol']:
        resp = user.getPosts('new', 'all', resp['last_id'])
    
def test_send_message(user: User):
    user.sendMessage('Test', 'Hello fellow user', 'Ill-Union9100')

def test_make_post(user: User):
    user.makePost('memes', 'Karma for Karma!', 'Hi, please upvote this post! Have a great day!')

def test_find_subreddits(user: User):
    return user.findSubreddits('gonewild')

def test_auto_post(user: User):
    user.autoPostToMultipleSubreddits(resp, 'Please give me some Karma for a test!', 'Would really appreciate some Karma thanks!!!')

user = test_login_user()

test_find_subreddits(user)

#user.getPosts('hot', 'all', 100)
#bot.showSavedOfUser('controversial', 'all', 10, 'xFregas')

#bot.getRedditUsers(['gonewild', 'gonewildcolor', 'gonewildcouples', 'gonewildasian'], ['OF', 'only fans', 'onlyfans'], 100)

#bot.getCountOfResults('gonewild')
