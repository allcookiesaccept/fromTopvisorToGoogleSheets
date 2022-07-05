import requests
import json
from bs4 import BeautifulSoup


class YandexApi:

    def __init__(self):

        print('Load Keys')

        self.secret_keys = {}

        with open('D:\\pyprojects\\datastudio\\yandex-api\\secret_keys.txt', 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
            for line in lines:
                key = line.split(': ')[0]
                value = line.split(': ')[1]
                self.secret_keys[key] = value

        self.id = self.secret_keys['id']
        self.pswd = self.secret_keys['pswd']
        self.callback = self.secret_keys['callback']
        self.token = self.secret_keys['token']
        self.server_token_req = 'https://oauth.yandex.ru/authorize?response_type=token&client_id='


    def authorizing(self): # not finished

        print('Yandex OAuth authorizing')

        token_request_url = f'{self.server_token_req}{self.id}'

        req = requests.get(token_request_url)


    def get_user_id(self):

        print('Get User ID')

        user_get_url = 'https://api.webmaster.yandex.net/v4/user'
        payload = {

            "Authorization ": self.token
        }

        response = requests.get(user_get_url, headers=payload)

        response.json



if __name__ == '__main__':

    yapi = YandexApi()

    yapi.authorizing()