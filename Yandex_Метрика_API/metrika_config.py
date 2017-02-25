# ID: da12854d6ab942aa8786e9d29095f75d
# Пароль: 752234d4309f422385c943955f49e063
# Callback URL: https://oauth.yandex.ru/verification_code

AUTHORIZE_URL = 'https://oauth.yandex.ru/authorize'
APP_ID = 'da12854d6ab942aa8786e9d29095f75d'
auth_data = dict(response_type = 'token',
                 client_id = APP_ID
                 )
# print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))
TOKEN = 'AQAAAAAZqgDAAAQPp2e0pw3PqkppiLIfXdwZD9A'