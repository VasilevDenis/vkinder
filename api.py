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

    def send_message(self, user_id, message):
        method = 'messages.send'
        params = self._interface_params(message,
                                        self.start_keyboard(), user_id)
        self._vk_request(method, params)

    def send_favorites_contacts(self, user_id, favorites_contacts: list) -> None:
        favorites_contacts = '\n'.join(favorites_contacts)
        method = 'messages.send'
        params = self._interface_params(favorites_contacts,
                                        self.start_keyboard(), user_id)
        self._vk_request(method, params)

    def wrong_command(self, user_id) -> None:
        method = 'messages.send'
        params = self._interface_params(f'Wrong command!',
                                        self.like_dislike_favorites_keyboard(), user_id)
        self._vk_request(method, params)

    def get_contacts(self, city: str, age: str, gender: int) -> list:
        method = 'users.search'
        city = city
        age = age
        gender = 3 - gender
        params = {
                'access_token': constants.APP_TOKEN,
                'hometown': city,
                'sex': gender,
                'age_from': age,
                'age_to': age
            }
        r = self._vk_request(method, params)
        found_users_list = []
        for item in r['response']['items']:
            found_users_list.append(item['id'])
        return found_users_list

    def send_contact_info(self, user_id, contact_id) -> None:
        contact_info = self.get_contact_info(contact_id)
        first_name_last_name = ' '.join(contact_info[:2])
        photo_ids = self.get_photos(contact_id)
        print(f'Sending user info to the chat! {user_id}')
        method = 'messages.send'
        photo_ids_string = '\n'.join(photo_ids)
        attachment = dict()
        attachment['type'] = 'photo'
        attachment['type'] = 'photo'
        attachment['owner_id'] = user_id
        attachment['media_id'] = ''
        params = self._interface_params(
            f'https://vk.com/id{contact_id}\n{first_name_last_name}\n',
            self.start_keyboard(), user_id, attachment)
        params["access_token"] = constants.TOKEN
        self._vk_request(method, params)

    def get_contact_info(self, contact_id: int) -> list or None:
        # по vk id выдает список: [имя, фамилия, возраст, пол, город, vk id]
        method = 'users.get'
        params = {'user_id': contact_id,
                  'fields': 'bdate, city, sex'}
                  #'access_token': constants.APP_TOKEN}
        r = self._vk_request(method, params)
        contact_info = r['response'][0]
        if 'city' in contact_info:
            city = contact_info['city']['title']
        else:
            city = 'Город не указан'
        first_name = contact_info['first_name']
        last_name = contact_info['last_name']
        age = int(datetime.now().year) - int(r['response'][0]['bdate'][-4:])
        gender = contact_info['sex']
        contact_info = [first_name, last_name, age, gender, city]
        return contact_info

    def get_user_or_contact_info(self, user_or_contact_id: int) -> list or None:
        # по vk id выдает список: [имя, фамилия, возраст, пол, город]
        method = 'users.get'
        params = {'user_id': user_or_contact_id,
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
        user_info = [first_name, last_name, age, gender, city]
        return user_info

    def get_photos(self, contact_id: int) -> None or dict:
        # по vk id выдает список с 3 фото размера Х с макс.кол-вом лайков
        method = 'photos.get'
        params = {'owner_id': contact_id,
                  'album_id': 'profile',
                  'extended': 1,
                  'access_token': constants.APP_TOKEN
                  }
        r = self._vk_request(method, params)
        print(r)
        photos = {}
        for item in r['response']['items']:
            likes = item['likes']['count']
            url = None
            for photo in item['sizes']:
                if photo['type'] == 'x':
                    url = photo['url']
            photos[url] = likes
        photos = dict(sorted(photos.items(), key=lambda elem: elem[1], reverse=True))
        return list(photos.keys())[:3]

    def _vk_request(self, method, params=None) -> dict:
        self.params.update(params)
        url = self.base_url + method
        request_obj = requests.get(url=url, params=self.params)
        time.sleep(0.3)
        return request_obj.json()

    @staticmethod
    def _interface_params(message, keyboard, user_id, attachment) -> dict:
        params = {'random_id': random.randint(100000, 999999),
                  'message': message,
                  'keyboard': keyboard,
                  'user_id': user_id,
                  'attachment': attachment
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







