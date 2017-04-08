import requests
from urllib.parse import urlencode, urlparse
from time import sleep
import config
import operator
import json
from pprint import pprint
from collections import Counter

def get_id():
    return input('Пожалуйста, введите ID интересующего человека:\n')

def get_friends_and_followers(person_id):
    friends_and_followers=set()
    url_friends = 'https://api.vk.com/method/friends.get'
    url_followers = 'https://api.vk.com/method/users.getFollowers'
    params = dict(v = config.api_v, user_id=person_id, access_token = config.access_token)
    response_friends = requests.get(url_friends, params).json()
    response_followers = requests.get(url_followers, params).json()
    friends_and_followers.update(response_friends['response']['items'], response_followers['response']['items'])
    return friends_and_followers

def get_friends_from_file():
    with open('friendsoffline.txt', 'r') as friends_offline:
        friends_and_followers=json.load(friends_offline)
    return (friends_and_followers)

def get_groups(friends_list):
    counter = 1
    number_persons=len(friends_list)
    url_groups = 'https://api.vk.com/method/groups.get'
    # groups_count=dict()
    groups_count = Counter()
    for each in friends_list:
        print('Идет обработка запроса: {0}/{1}. Номер пользователя: {2}'.format(counter, number_persons, each))
        counter += 1
        response_groups = requests.get(url_groups, dict(uid=each, fields='name', access_token = config.access_token)).json()
        # print(response_groups)
        try:
            groups_count+=(Counter(response_groups['response']))
            # print(groups_count)
            sleep(1/2)
        except:
            print(response_groups)
            print('#',counter, 'out of', number_persons, each, 'something is wrong here. Moving on...\n')
            sleep(1/2)
    pprint('Всего групп: {0}.'.format(len(groups_count)))
    return groups_count

def form_list_of_groups(groups):
    url_group_names = 'https://api.vk.com/method/groups.getById'
    sorted_groups = sorted(groups.items(), key=operator.itemgetter(1), reverse=True)
    group_lists = sorted_groups[:100]
    sorted_top_100 = list(map(lambda x: list(x),sorted_groups[:100]))
    groups_ids= str(list(zip(*sorted_top_100))[0])
    group_names_request=requests.get(url_group_names, dict(group_ids=groups_ids, fields='screen_name', access_token = config.access_token)).json()
    print('Выбран Топ-100')
    group_names = {}
    for each in group_names_request['response']:
        key, value = each['gid'], each['name']
        group_names[key]=value
    # pprint(len(group_names))
    top_100_list=[]
    for record in sorted_top_100:
        top_100_record={}
        top_100_record['group_id']=record[0]
        record_id = record[0]
        # print(record_id)
        top_100_record['title'] = group_names.get(record_id, 'ИМЯ НЕ НАЙДЕНО')
        top_100_record['count'] =record[1]
        top_100_list.append(top_100_record)
    return(top_100_list)

def write_results(list_of_groups):
    with open('top100.json', 'w') as file:
        json.dump(list_of_groups, file, indent=2)
    print('Результаты сохранены в файле')

if __name__=='__main__':
    person_id = get_id()
    # get_friends_from_file()
    friends_list = get_friends_and_followers(person_id)
    groups_count = get_groups(friends_list)
    list_of_groups = form_list_of_groups(groups_count)
    write_results(list_of_groups)



