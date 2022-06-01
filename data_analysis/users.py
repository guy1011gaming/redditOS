import json
import sys
import os
from urllib import response
import requests

sys.path.insert(0, './wrapper')
from reddit_user import User


def actualiseList(vers: int):
    user = User('RedditOS_', 'RedditOSMaxHenning2022')
    try:
        with open('datasets/dataset-ver_' + str(vers) + '.txt') as json_file:
            allPosters = json.load(json_file)
    except:
        print('File doesnt seem to exist...')
        return

    vers = 0
    posts = {}
    posts['eol'] = False
    posts['last_id'] = ''

    for posterName in allPosters['data']:
        print('Processing: ' + allPosters['data'][posterName]['name'])

        allPosters['data'][posterName]['flags'] = {}

        allPosters['data'][posterName]['flags'] = checkIfUserActive(allPosters['data'][posterName]['name'], user.getHeader())
        

        if not allPosters['data'][posterName]['flags']['flagged']:
            userdata = requests.get('https://oauth.reddit.com/user/' + allPosters['data'][posterName]['name'] + '/about', headers=user.getHeader())
            results = checkForAccounts(userdata.json()['data']['subreddit']['public_description'], user.getHeader())

            poster = allPosters['data'][posterName]

            poster['has_OnlyFans'] = results[0]
            poster['OnlyFans_username'] = results[1]
            poster['has_Fansly'] = results[2]
            poster['Fansly_username'] = results[3]

            posts['eol'] = False
            while posts['eol'] == False:
                if posts['last_id'] == '':
                    posts = user.getPostsOfUser('new', 'all', 100, poster['name'])
                else:
                    posts = user.getPostsOfUser('new', 'all', 100, poster['name'], posts['last_id'])

                if not posts['last_id'] == '0':
                    poster['posting_history']['last_id'] = posts['last_id']

                if not posts['eol']:
                    for postName in posts['data']:
                        poster['posting_history'][postName] = {}
                        poster['posting_history'][postName] = posts['data'][postName]
                        param = {'id': postName}

                        respPostInfo = requests.get('https://oauth.reddit.com/api/info', params=param, headers=user.getHeader())
                        for postInfo in respPostInfo.json()['data']['children']:
                            postInfo = postInfo['data']

                            resultTitle = checkForAccounts(postInfo['title'], user.getHeader())

                            if not poster['has_OnlyFans']:
                                poster['has_OnlyFans'] = resultTitle[0]

                            if poster['OnlyFans_username'] == None:
                                poster['OnlyFans_username'] = resultTitle[1]

                            if not poster['has_Fansly']:
                                poster['has_Fansly'] = resultTitle[2]

                            if poster['Fansly_username'] == None:
                                poster['Fansly_username'] = resultTitle[3]

                            resultText = checkForAccounts(postInfo['selftext'], user.getHeader())

                            if not poster['has_OnlyFans']:
                                poster['has_OnlyFans'] = resultText[0]

                            if poster['OnlyFans_username'] == None:
                                poster['OnlyFans_username'] = resultText[1]

                            if not poster['has_Fansly']:
                                poster['has_Fansly'] = resultText[2]  

                            if poster['Fansly_username'] == None:
                                poster['Fansly_username'] = resultText[3]      
            

            allPosters['data'][posterName] = poster

        with open('datasets/new_dataset-ver_' + str(vers) + '.txt', 'w') as json_file:
            json.dump(allPosters, json_file)
        if os.path.exists('datasets/new_dataset-ver_' + str(vers-1) + '.txt'):
            os.remove('datasets/new_dataset-ver_' + str(vers-1) + '.txt')

        vers += 1


def checkIfUserActive(username:str, header):
    if 'u/' in username:
            username = username[2:]

    flags = {}
    flags['fatalError'] = False
    flags['deleted'] = False
    flags['suspended'] = False
    flags['other_error'] = False
    flags['flagged'] = False
    
    try:
        userdata = requests.get('https://oauth.reddit.com/user/' + username + '/about', headers=header)
    except:
        flags['fatalError'] = True
        flags['flagged'] = True
        return flags
    
    if userdata.status_code != 200:
        if userdata.status_code == 404:
            flags['deleted'] = True
        else:
            flags['other_error'] = True

    try:
        if userdata['data']['is_suspended'] == True:
            flags['suspended'] = True
    except:
        pass

    for flag in flags:
        if flags[flag]:
            flags['flagged'] = True
            break

    return flags


def checkForAccounts(text: str, header: dict):
    termsOF = ['OnlyFans', 'onlyfans', 'OF', 'ONLYFANS', 'Onlyfans', 'onlyFans']
    OnlyfansLink = ['https://onlyfans.com', 'www.onlyfans.com', 'https://www.onlyfans.com', 'onlyfans.com']
    termsFL = ['Fansly', 'fansly', 'FANSLY', 'FansLy']
    FanslyLink = ['https://fansly.com', 'www.fansly.com', 'https://www.fansly.com', 'fansly.com']
    

    hasOF = False
    OFName = None
    hasFansly = False
    FanslyName = None

    for term in termsOF:
        if term in text:
            hasOF = True
            break

    if hasOF:
        for term in OnlyfansLink:
            term = term.lower()
            if term in text:
                begIndex = text.find(term)
                endIndex = text.find(' ', begIndex)
                OFName = text[begIndex:endIndex]
                break
    
    for term in termsFL:
        if term in text:
            hasFansly = True
            break

    if hasFansly:
        for term in FanslyLink:
            term = term.lower()
            if term in text:
                begIndex = text.find(term)
                endIndex = text.find(' ', begIndex)
                FanslyName = text[begIndex:endIndex]
                break

    return hasOF, OFName, hasFansly, FanslyName
        




actualiseList(1515)

print('done')