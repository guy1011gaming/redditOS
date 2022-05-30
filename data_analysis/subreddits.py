import csv
import requests
import sys
import json
import os

sys.path.insert(0, './wrapper')
from reddit_user import User

def getListFromFile(path: str):
    try:
        with open('./data_analysis/sheet.csv') as csvfile:
            spamreader = csv.reader(csvfile)
            subredditList = {}
            majorCategory = ""
            minorCategory = ""
            lastLine = ""
            i = 0

            for row in spamreader:
                currLine = ''.join(row)
                if 'r/' in currLine:
                    subredditList[majorCategory][minorCategory][i] = currLine[1:]
                    i += 1
                else:
                    if not "r/" in lastLine and not lastLine == "":
                        majorCategory = lastLine
                        minorCategory = currLine
                        subredditList[majorCategory] = {}
                        subredditList[majorCategory][minorCategory] = {}
                        i = 0
                    elif "r/" in lastLine:
                        minorCategory = currLine
                        subredditList[majorCategory][minorCategory] = {}
                        i = 0
                lastLine = currLine

        return subredditList

    except:
        print("Something went wrong...")
        return None

user = User('RedditOS_', 'RedditOSMaxHenning2022')  

#user.getRedditUsers(['The_donald'], ['OF', 'only fans', 'onlyfans', 'fansly', 'fans.ly', 'onlyfans.com', 'fansly.com'], 100)

resp = getListFromFile("")
vers = 0

finalData = {}
finalData['data'] = {}
for major in resp:
    for minor in resp[major]:
        for k in resp[major][minor]:
            last_id = ''
            for i in range(1):
                test = resp[major][minor][k]
                respUsers = user.getRedditUsers([resp[major][minor][k]])

                for respUserNr in respUsers['users']:
                    respUser = respUsers['users'][respUserNr]
                    if not respUser in finalData['data']:
                        try:
                            userdata = requests.get('https://oauth.reddit.com/user/' + respUser + '/about', headers=user.getHeader())
                            finalData['data'][userdata.json()['data']['id']] = {}
                            finalData['data'][userdata.json()['data']['id']]['name'] = userdata.json()['data']['name']
                            finalData['data'][userdata.json()['data']['id']]['karma'] = userdata.json()['data']['total_karma']
                            finalData['data'][userdata.json()['data']['id']]['has_OnlyFans'] = None
                            finalData['data'][userdata.json()['data']['id']]['OnlyFans_username'] = None
                            finalData['data'][userdata.json()['data']['id']]['has_Fansly'] = None
                            finalData['data'][userdata.json()['data']['id']]['Fansly_username'] = None
                            finalData['data'][userdata.json()['data']['id']]['posting_history'] = {}
                        except:
                            print('User error 4:')
                            print(userdata.json())
            with open('datasets/dataset-ver_' + str(vers) + '.txt', 'w') as json_file:
                json.dump(finalData, json_file)
            if os.path.exists('datasets/dataset-ver_' + str(vers-1) + '.txt'):
                os.remove('datasets/dataset-ver_' + str(vers-1) + '.txt')
            vers += 1

