from urllib.parse import urlencode, urlparse, urljoin
from pprint import pprint
import requests
import metrika_config as met

class YandexMetrika(object):
    _METRIKA_STAT_URL = 'https://api-metrika.yandex.ru/stat/v1/data'
    _METRIKA_MANAGEMENT_URL = 'https://api-metrika.yandex.ru/management/v1/'
    token = None

    def __init__(self, token):
        self.token = token

    def get_header(self):
        header = {
                  'Content-Type':'application/json',
                  'Authorization':'OAuth {}'.format(self.token),
                 }
        return header

class Metrika_management(YandexMetrika):

    def get_counters(self):
        url = urljoin(self._METRIKA_MANAGEMENT_URL, 'counters')
        header = self.get_header()
        response = requests.get(url, headers=header)
        counter_list = [c['id'] for c in response.json()['counters']]
        with open('counters.txt', 'w') as file:
            file.write('\n'.join(map(lambda x:str(x), counter_list)))
        return response.json()

class Metrika_reports(YandexMetrika):
    def __init__(self, token, counter_id):
        self.token = token
        self.counter_id = counter_id

    def visits(self):
        url = urljoin(self._METRIKA_STAT_URL, 'data')
        header = self.get_header()
        params = {'id': 42765454, 'metrics':'ym:s:visits'}
        response = requests.get(url, params=params, headers=header)
        visits = response.json()['data'][0]['metrics'][0]
        return visits

    def views(self):
        url = urljoin(self._METRIKA_STAT_URL, 'data')
        header = self.get_header()
        params = {'id': 42765454, 'metrics':'ym:s:pageviews'}
        response = requests.get(url, params=params, headers=header)
        visits = response.json()['data'][0]['metrics'][0]
        return visits

    def users(self):
        url = urljoin(self._METRIKA_STAT_URL, 'data')
        header = self.get_header()
        params = {'id': 42765454, 'metrics':'ym:s:users'}
        response = requests.get(url, params=params, headers=header)
        visits = response.json()['data'][0]['metrics'][0]
        return visits


if __name__ == '__main__':
    yandex_test = Metrika_management(met.TOKEN)
    yandex_test2 = Metrika_reports(met.TOKEN, 4276545)
    pprint('Количество визитов: {}'.format(yandex_test2.visits()))
    pprint('Количество просмотров: {}'.format(yandex_test2.views()))
    pprint('Количество пользователей: {}'.format(yandex_test2.users()))


    # https://api-metrika.yandex.ru/stat/v1/data?ids=4276545&metrics=ym:s:visits&Authorization=OAuth AQAAAAAZqgDAAAQPp2e0pw3PqkppiLIfXdwZD9A
# {'ids': 4276545, 'metrics': 'ym:s:visits'}
# {'Content-Type': 'application/json', 'Authorization': 'OAuth AQAAAAAZqgDAAAQPp2e0pw3PqkppiLIfXdwZD9A'}