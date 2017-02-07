import requests
from urllib.parse import urlencode, urlparse
from time import sleep
import json

app_id = 5862420
auth_url = 'https://oauth.vk.com/authorize'
api_ver = '5.60'

# auth_data = dict(client_id=app_id,
#                  display='mobile',
#                  response_type='token',
#                  scope='friends, status',
#                  v=api_ver)
# print('?'.join([auth_url, urlencode(auth_data)]))

token = 'https://oauth.vk.com/blank.html#access_token=29bfe6b1a89e76fb4ed3bf4de5d5a998cb8a77fcc5a6060ad14cd0828da53f08dfeb05d3eb6b640f8aa72&expires_in=86400&user_id=1946565'
o = urlparse(token)
fragments = dict(i.split('=') for i in o.fragment.split('&'))
access_token = fragments['access_token']

def get_friends_list(user_id):
    params = dict(user_id=user_id,
                  access_token=access_token,
                  v=api_ver)
    response = requests.get('https://api.vk.com/method/friends.getOnline', params)
    friend_list = response.json()['response']
    # print(response.json())
    return friend_list

initial_list = get_friends_list('1946565')
all_friends_of_friends_online = set(initial_list)
users_online_list = dict()

for user in initial_list:
    online_friends = get_friends_list(user)
    print(user, len(online_friends))
    users_online_list[user] = online_friends
    all_friends_of_friends_online.update(online_friends)
    sleep(0.7)
    print(len(all_friends_of_friends_online), '\n')

# with open('data.txt', 'r') as file:
#     users_online_list = json.load(file)
# initial_list = list(users_online_list.keys())

def find_common_friends(initial_list, users_online_list):
    first_fr = set(users_online_list[initial_list[0]])
    for each in range(len(initial_list)):
        second_fr = set(users_online_list[initial_list[each]])
        control_set = first_fr.intersection(second_fr)
        first_fr = set(control_set)
        print(control_set)
    return list(control_set)

find_common_friends(initial_list, users_online_list)