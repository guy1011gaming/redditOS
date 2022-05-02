from reddit_user import User
from automate import Bot


user = User('RedditOS_', 'RedditOSMaxHenning2022')
bot = Bot(user)
#user.sendMessage('Test', 'Hello fellow user', 'Ill-Union9100')

resp = user.getPosts('new', 'all')

print(len(resp['posts']))

resp = user.getPosts('new', 'all', resp['last_id'])

print(len(resp['posts']))


#user.makePost('memes', 'Karma for Karma!', 'Hi, please upvote this post! Have a great day!')
#resp = bot.findSubreddits('GoneWil', 2)
#bot.autoPostToMultipleSubreddits(resp, 'Please give me some Karma for a test!', 'Would really appreciate some Karma thanks!!!')

#user.getPosts('hot', 'all', 100)
#bot.showSavedOfUser('controversial', 'all', 10, 'xFregas')

#bot.getRedditUsers(['gonewild', 'gonewildcolor', 'gonewildcouples', 'gonewildasian'], ['OF', 'only fans', 'onlyfans'], 100)

#bot.getCountOfResults('gonewild')
