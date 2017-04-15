import requests
from time import sleep
import config
import operator
import json
from pprint import pprint
from collections import Counter


class Person(object):
    def __init__(self, person_id):
        self.id = person_id
        print('Создан объект - пользователь')

    def get_friends(self):
        url_friends = 'https://api.vk.com/method/friends.get'
        params_friends = dict(v=config.api_v, user_id=self.id, access_token=config.access_token)
        response_friends = requests.get(url_friends, params_friends).json()
        # print(response_friends['response']['items'])
        return response_friends['response']['items']

    def get_followers(self):
        url_num_followers = 'https://api.vk.com/method/users.get'
        url_followers = 'https://api.vk.com/method/users.getFollowers'
        offset = 0
        number_of_followers_left = int(requests.get(url_num_followers,
                                                    dict(v=config.api_v,
                                                         user_id=self.id,
                                                         access_token=config.access_token,
                                                         fields='followers_count')
                                                    ).json().get('response', None)[0].get('followers_count'))
        followers_list = []
        while number_of_followers_left > 0:
            params_followers = dict(v=config.api_v, user_id=self.id, access_token=config.access_token, count=1000,
                                    offset=offset)
            response_followers = requests.get(url_followers, params_followers).json()
            offset += 1000
            number_of_followers_left -= 1000
            sleep(0.34)
            followers_list.extend(response_followers['response']['items'])
            print('Подгружается информация о подписчиках, осталось:', number_of_followers_left + 1000)
        print(len(followers_list))
        return followers_list

    def unite_linked_users(self):
        friends = self.get_friends()
        followers = self.get_followers()
        united_list = []
        united_list.extend(friends)
        united_list.extend(followers)
        self.linked_users = united_list
        return united_list

    def get_groups(self):
        counter = 1
        number_persons = len(self.linked_users)
        url_groups = 'https://api.vk.com/method/groups.get'
        groups_count = Counter()
        for each in self.linked_users:
            print('Идет обработка запроса: {0}/{1}. Номер пользователя: {2}'.format(counter, number_persons, each))
            counter += 1
            response_groups = requests.get(url_groups,
                                           dict(uid=each, fields='name', access_token=config.access_token)).json()
            try:
                groups_count += (Counter(response_groups['response']))
                sleep(0.34)
            except:
                print(response_groups)
                print('#', counter, 'out of', number_persons, each, 'something is wrong here. Moving on...\n')
                sleep(0.34)
        pprint('Всего групп: {0}.'.format(len(groups_count)))
        self.groups_count = groups_count

        with open('all_groups.json', 'w') as file:
            json.dump(groups_count, file, indent=2)

        return groups_count

    def form_list_of_groups(self):
        groups = self.groups_count
        url_group_names = 'https://api.vk.com/method/groups.getById'
        sorted_groups = sorted(groups.items(), key=operator.itemgetter(1), reverse=True)
        sorted_top_100 = list(map(lambda x: list(x), sorted_groups[:100]))
        groups_ids = str(list(zip(*sorted_top_100))[0])
        group_names_request = requests.get(url_group_names, dict(group_ids=groups_ids, fields='screen_name',
                                                                 access_token=config.access_token)).json()
        print('Выбран Топ-100')
        group_names = {}
        for each in group_names_request['response']:
            key, value = each['gid'], each['name']
            group_names[key] = value
        top_100_list = []
        for record in sorted_top_100:
            top_100_record = {'group_id': record[0]}
            record_id = record[0]
            # print(record_id)
            top_100_record['title'] = group_names.get(record_id, 'ИМЯ НЕ НАЙДЕНО')
            top_100_record['count'] = record[1]
            top_100_list.append(top_100_record)
        with open('top100.json', 'w') as file:
            json.dump(top_100_list, file, indent=2)
        return top_100_list

celebrity = Person(input('Пожалуйста, введите ID интересующего человека:\n'))
celebrity.unite_linked_users()
celebrity.get_groups()
celebrity.form_list_of_groups()
