import requests
from urllib.parse import urlencode, urlparse
from time import sleep
import config
import operator
import json
from pprint import pprint

user_id = 'xxxxxxxxxx'
url_friends = 'https://api.vk.com/method/friends.get'
url_followers = 'https://api.vk.com/method/users.getFollowers'
url_groups = 'https://api.vk.com/method/groups.get'
url_users = 'https://api.vk.com/method/users.get'
url_groups_info = 'https://api.vk.com/method/groups.getById'
params = dict(v = config.api_v, user_id=user_id, access_token = config.access_token2)
response_friends = requests.get(url_friends, params).json()
print(response_friends)
response_followers = requests.get(url_followers, params).json()

# print(response_friends)
# print(response_followers)
friends_list = response_friends['response']['items']
followers_list = response_followers['response']['items']
global_list = set()
global_list.update(followers_list, friends_list)
# print(friends_list, followers_list, sep='\n')
total_persons = len(global_list)
counter = 0
groups_list=dict()
groups_set = set()
for each in global_list:
    counter+=1
    name = requests.get(url_users, dict(uid=each, fields='screen_name', access_token = config.access_token2)).json()['response'][0]['last_name']
    response_groups = requests.get(url_groups, dict(uid=each, fields='name', access_token = config.access_token2)).json()

    try:
        # print(response_groups)
        groups_list[each]=set(response_groups['response'])
        groups_set.update(response_groups['response'])
        print('#',counter, 'out of', total_persons, each, name)
        sleep(1)
        # pprint(groups_list)
    except:
        print('#',counter, 'out of', total_persons,each, name, 'something is wrong here, moving on though...')
        sleep(1)
print(groups_list)
member_count = dict()

member_count=dict(zip(groups_set, [0 for x in range(10000)]))

for each in groups_set:
    for every in groups_list.keys():
        if each in groups_list[every]:
            member_count[each] += 1

sorted_x = sorted(member_count.items(), key=operator.itemgetter(1), reverse=True)

print(sorted_x)
result = []
names
for each in sorted_x[:100]:
    result.append(dict(title=each[0],count=each[1]))

with open('groups.txt', 'w') as file:
    json.dump(result, file)
