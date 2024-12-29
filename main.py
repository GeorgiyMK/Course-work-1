import requests
import configparser
from pprint import pprint

config = configparser.ConfigParser()
config.read('settings.ini')
access_token = config['Tokens']['vk_token']
user_id = '6211236'
v = '5.199'

class VK:

    API_URL = 'https://api.vk.com/method/'

    def __init__(self, access_token, user_id, version=v):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': self.version,
            'user_ids': self.id
                        }

    def users_info(self):
        response = requests.get(self.API_URL + 'users.get', params = self.params)
        return response.json()

    def get_photo(self):
        params = ({         'owner_id' : self.id,
                            'album_id' : 'profile',
                            'rev' : '1',
                            'extended' : '1'
                            })
        params.update(self.params)
        response = requests.get(self.API_URL + 'photos.get', params = params)
        return response.json()

class WorkPHOTO:
    def __init__(self, access_token, user_id, version='5.199'):
        self.user_id = user_id
        self.vk = VK(access_token, user_id, version = '5.199')

    def __enter__(self):
        response = self.vk.get_photo()
        return response['response']['items']

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

with WorkPHOTO(access_token,user_id, version = '5.199') as photos:
    for photo in photos:
        pprint(photo)





vk = VK(access_token, user_id)

# pprint(vk.get_photo())