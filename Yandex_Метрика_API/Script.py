from urllib.parse import urlencode, urlparse, urljoin
from pprint import pprint
import requests

# TODO: finish homeworke, now code only copied - think throught the task and implement

# ID: da12854d6ab942aa8786e9d29095f75d
# Пароль: 752234d4309f422385c943955f49e063
# Callback URL: https://oauth.yandex.ru/verification_code


AUTHORIZE_URL = 'https://oauth.yandex.ru/authorize'
APP_ID = 'da12854d6ab942aa8786e9d29095f75d'
auth_data = dict(response_type = 'token',
                 client_id = APP_ID
                 )

print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))

TOKEN = 'AQAAAAAZqgDAAAQPp2e0pw3PqkppiLIfXdwZD9A'

class YandexMetrika(object):
    _METRIKA_STAT_URL = 'https://api-metrika.yandex.ru/stat/v1'
    _METRIKA_MANAGEMENT_URL = 'https://api-metrika.yandex.ru/management/v1'
    token = None

    def __init__(self, token):
        self.token = token

    def get_header(self):
        return {
            'Content-Type' : 'application/json',
            'Authorization' : 'OAuth {}'.format(self.token),
            'User-Agent' : 'asdasdasd'
                }
    @property

    def counter_list(self):
        url = urljoin(self._METRIKA_MANAGEMENT_URL, 'counters')
        headers = self.get_header()
        response = requests.get(url, headers=headers)
        counter_list = [c['id'] for c in response.json()['counters']]

    def get_visits_count(self, counter_id):
            url = urljoin(self._METRIKA_MANAGEMENT_URL, 'data')
            headers = self.get_header()
            params = {
                'id':counter_id,
                'metrics': 'ym:s:visits'
                }
            response = requests.get(url, params, headers=headers)
            pprint(response.json())
            visit_count = response.json()['data'][0]['metrics'][0]
            return visit_count

metrika = YandexMetrika(TOKEN)
print(YandexMetrika.__dict__)
print(metrika.__dict__)
# print(metrika.counter_list)