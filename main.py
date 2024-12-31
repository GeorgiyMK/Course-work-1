import requests
import configparser
from pprint import pprint
import json
from tqdm import tqdm


config = configparser.ConfigParser()
config.read('settings.ini')
access_token = config['Tokens']['vk_token']
user_id = config['Tokens']['user_id']
YA_TOKEN = config['Tokens']['YA_TOKEN']
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
        # self.count = count
        params = {          'owner_id' : self.id,
                            'album_id' : 'profile',
                            'rev' : '1',
                            'extended' : '1',
                            }
        params.update(self.params)
        response = requests.get(self.API_URL + 'photos.get', params = params)
        return response.json()

class UPYADI:
    ya_url = 'https://cloud-api.yandex.net/v1/disk/resources'
    upl_ya_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    def __init__(self, YA_TOKEN):
        self.token = YA_TOKEN
        self.headers = {
            'Authorization' : YA_TOKEN
        }

    def create_folder(self, folder_name):
        params = {'path': folder_name}
        response = requests.put(self.ya_url, headers=self.headers, params=params)
        if response.status_code == 201:
            print(f"Папка '{folder_name}' успешно создана.")
        elif response.status_code == 409:
            print(f"Папка '{folder_name}' уже существует.")
        else:
            print(f"Ошибка создания папки: {response.json()}")

    def upload_photos(self, info_list, folder_name='IMAGES_COURSE_WORK'):
        self.create_folder(folder_name)
        for photo in tqdm(info_list, desc="Загрузка фотографий на Яндекс.Диск", unit="фото"):
            filename = f"{photo['file_name']}.jpg"
            photo_url = photo['url']
            params = {'path' : f'{folder_name}/{filename}',
                        'url' : photo_url}
            response = requests.post(self.upl_ya_url, headers = self.headers, params = params)
            upload_url = response.json()['href']
            requests.put(upload_url, params = params)
            # pprint(response.json())

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
    count = 0
    for photo in photos:
        if count >= 5:
            break
        # pprint(photo)
        photo_info = {}
        likes_count = photo['likes']['count'] if 'likes' in photo and 'count' in photo['likes'] else 0
        if any(item['file_name'] == likes_count for item in for_write):
            photo_info['file_name'] = f"{likes_count}_{photo['date']}"
        else:
            photo_info['file_name'] = likes_count
        if 'sizes' in photo:
            for size in photo['sizes']:
                if size['type'] == 'w' and size.get('url'):
                    photo_info['size'] = size['type']
                    photo_info['url'] = size['url']
                    break
            else:
                photo_info['size'] = None
        else:
            photo_info['size'] = None

        if photo_info.get('url'):
            for_write.append(photo_info)
            count += 1

with open('info.json', 'w', encoding='utf-8') as json_file:
    json.dump(for_write, json_file, indent=4, ensure_ascii=False)

with open(r'info.json', encoding='utf-8') as f:
    info_list = json.load(f)

vk = VK(access_token, user_id)
uploader = UPYADI(YA_TOKEN)
uploader.upload_photos(info_list, folder_name='IMAGES_COURSE_WORK')