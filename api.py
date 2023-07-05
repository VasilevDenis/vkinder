import random
from datetime import datetime
import requests
import time
import constants
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class API:
    def __init__(self):
        self.base_url = 'https://api.vk.com/method/'
        self.params = {"v": constants.API_VERSION, "access_token": constants.TOKEN}

    def send_favorites_users(self, received, favorites_users) -> None:
        method = 'messages.send'
        params = self._interface_params('Favorites!',
                                        self.start_keyboard(), received)
        self._vk_request(method, params)

    def wrong_command(self, received) -> None:
        method = 'messages.send'
        params = self._interface_params(f'Wrong command!',
                                        self.like_dislike_favorites_keyboard(), received)
        self._vk_request(method, params)

    def get_users(self, city, age, gender) -> list:
        method = 'users.search'
        self.city = city
        self.age = age
        self.gender = 3 - gender
        params = {
                'access_token': constants.APP_TOKEN,
                'v': 5.131,
                'hometown': self.city,
                'sex': self.gender,
                'age_from': self.age,
                'age_to': self.age
            }
        r = self._vk_request(method, params)
        print(r['response']['count'])
        found_users_list = []
        for item in r['response']['items']:
            found_users_list.append(item['id'])
        return found_users_list

    def send_user_info(self, user_id, user_info, received) -> None:
        print(f'Sending user info to the chat! {user_id} {user_info}')
        method = 'messages.send'
        params = self._interface_params(f'https://vk.com/id{user_id}\n{user_info}',
                                        self.start_keyboard(), received)
        self._vk_request(method, params)


    @staticmethod
    def _interface_params(message, keyboard, received) -> dict:
        params = {'random_id': random.randint(100000, 999999),
                  'message': message,
                  'keyboard': keyboard,
                  'user_id': received.from_id
                  }
        return params

    @staticmethod
    def like_dislike_favorites_keyboard() -> dict:
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button(label='Favorites', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(label='Like', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button(label='Dislike', color=VkKeyboardColor.NEGATIVE)
        return keyboard.get_keyboard()

    @staticmethod
    def start_keyboard() -> dict:
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button(label='Back', color=VkKeyboardColor.PRIMARY)
        return keyboard.get_keyboard()

    def get_user_info(self, user_id: int) -> list or None:
        # по vk id выдает список: [имя, фамилия, возраст, пол, город]
        method = 'users.get'
        params = {'user_id': user_id,
                  'fields': 'bdate, city, sex'}
        r = self._vk_request(method, params)
        user_info = r['response'][0]
        if 'city' in user_info:
            city = user_info['city']['title']
        else:
            return 'Город не указан'
        first_name = user_info['first_name']
        last_name = user_info['last_name']
        age = int(datetime.now().year) - int(r['response'][0]['bdate'][-4:])
        gender = user_info['sex']
        member_info = [first_name, last_name, age, gender, city]
        return member_info

    def get_photos(self, user_id: int) -> None or dict:
        # по vk id выдает список с 3 фото размера Х с макс.кол-вом лайков
        method = 'photos.get'
        params = {'owner_id': user_id,
                  'album_id': 'profile',
                  'extended': 1,
                  'access_token': constants.APP_TOKEN
                  }
        r = self._vk_request(method, params)
        photos = {}
        for item in r['response']['items']:
            likes = item['likes']['count']
            url = None
            for photo in item['sizes']:
                if photo['type'] == 'x':
                    url = photo['url']
            photos[url] = likes
        photos = dict(sorted(photos.items(), key=lambda item: item[1], reverse=True))
        return list(photos.keys())[:3]

    def _vk_request(self, method, params=None) -> dict:
        self.params.update(params)
        url = self.base_url + method
        request_obj = requests.get(url=url, params=self.params)
        time.sleep(0.3)
        return request_obj.json()







