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
            if response.status_code != 202:
                print(f"Ошибка загрузки файла {filename}: {response.json()}")

class WorkPHOTO:

    def __init__(self, access_token, user_id, version='5.199'):
        self.user_id = user_id
        self.vk = VK(access_token, user_id, version = '5.199')

    def __enter__(self):
        response = self.vk.get_photo()
        if response and 'response' in response:
            return response['response']['items']
        elif 'error' in response:
            print(f"Ошибка VK API: {response['error']['error_msg']}")
        else:
            print("Неожиданный ответ от VK API:")
            pprint(response)
        return []

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is IndexError:
            print(f'Произошла ошибка {exc_val}')
        return False

with WorkPHOTO(access_token,user_id, version = '5.199') as photos:
    for_write = []
    photos_with_resolution = []
    for photo in photos[:45]:
        photo_info = {}
        likes_count = photo['likes']['count'] if 'likes' in photo and 'count' in photo['likes'] else 0
        if any(item['file_name'] == likes_count for item in for_write):
            photo_info['file_name'] = f"{likes_count}_{photo['date']}"
        else:
            photo_info['file_name'] = likes_count
        if 'sizes' in photo:
            max_size_photo = max(photo['sizes'], key=lambda size: size.get('width', 0) * size.get('height', 0))
            photos_with_resolution.append({
                'likes': photo['likes']['count'] if 'likes' in photo and 'count' in photo['likes'] else 0,
                'date': photo['date'],
                'resolution': max_size_photo.get('width', 0) * max_size_photo.get('height', 0),
                'url': max_size_photo.get('url', None)
            })
        else:
            photo_info['size'] = None
            photo_info['url'] = None

    sorted_photos = sorted(photos_with_resolution, key=lambda x: x['resolution'], reverse=True)
    top_photos = sorted_photos[:3]
for photo in top_photos:
        photo_info = {
            'file_name': f"{photo['likes']}_{photo['date']}",
            'url': photo['url']
        }
        for_write.append(photo_info)

with open('info.json', 'w', encoding='utf-8') as json_file:
    json.dump(for_write, json_file, indent=4, ensure_ascii=False)

uploader = UPYADI(YA_TOKEN)
uploader.upload_photos(for_write, folder_name='IMAGES_COURSE_WORK')