import requests
import configparser
from pprint import pprint
import json

config = configparser.ConfigParser()
config.read('settings.ini')
access_token = config['Tokens']['vk_token']
user_id = config['Tokens']['user_id']
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

    def get_photo(self, count = 5):
        self.count = count
        params = ({         'owner_id' : self.id,
                            'album_id' : 'profile',
                            'rev' : '1',
                            'extended' : '1',
                            'count' : self.count
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
        if exc_type is IndexError:
            print(f'Произошла ошибка {exc_val}')
        return False

with WorkPHOTO(access_token,user_id, version = '5.199') as photos:
    for_write = []
    for photo in photos:
        # pprint(photo)
        photo_info = {}
        likes_count = photo['likes']['count'] if 'likes' in photo and 'count' in photo['likes'] else 0
        if any(item['file_name'] == likes_count for item in for_write):
            photo_info['file_name'] = f"{likes_count}_{photo['date']}"
        else:
            photo_info['file_name'] = likes_count
        if 'sizes' in photo:
            for size in photo['sizes']:
                if size['type'] == 'w':
                    # print(size['type'], size['url'])
                    photo_info['size'] = size['type']
                    # photo_info['url'] = size['url']
                    break
            else:
                photo_info['size'] = None
        else:
            photo_info['size'] = None
        for_write.append(photo_info)

with open('info.json', 'w', encoding='utf-8') as json_file:
    json.dump(for_write, json_file, indent=4, ensure_ascii=False)



vk = VK(access_token, user_id)

# pprint(vk.get_photo())