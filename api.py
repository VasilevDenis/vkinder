import random
from datetime import datetime
import requests
import time
import constants
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class API:
    def __init__(self):
        self.base_url = 'https://api.vk.com/method/'
        self.params = {"v": constants.API_VERSION,
                       "access_token": constants.TOKEN,
                       'random_id': random.randint(100000, 999999)
                       }

    def send_message(self, user_id, message):
        method = 'messages.send'
        params = {'message': message,
                  'access_token': constants.TOKEN,
                  'keyboard': self.like_dislike_favorites_keyboard(),
                  'user_id': user_id}
        print('Sending message!')
        self._vk_request(method, params)

    def send_favorites_contacts(self, user_id, favorites_contacts: list) -> None:
        favorites_contacts = '\n'.join(favorites_contacts)
        print(favorites_contacts)
        method = 'messages.send'
        params = {'message': favorites_contacts,
                  'access_token': constants.TOKEN,
                  'keyboard': self.favorites_keyboard(),
                  'user_id': user_id}
        self._vk_request(method, params)

    def wrong_command(self, user_id) -> None:
        method = 'messages.send'
        params = {'message': 'Wrong command!',
                  'access_token': constants.TOKEN,
                  'keyboard': self.like_dislike_favorites_keyboard(),
                  'user_id': user_id}
        self._vk_request(method, params)

    def get_contacts(self, city: str, age: int, gender: int) -> list:
        method = 'users.search'
        city = city
        age = age
        gender = 3 - gender
        params = {
            'access_token': constants.APP_TOKEN,
            'hometown': city,
            'sex': gender,
            'age_from': age - 5,
            'age_to': age + 5
        }
        r = self._vk_request(method, params)
        found_users_list = []
        for item in r['response']['items']:
            found_users_list.append(item['id'])
        return found_users_list

    def send_contact_info(self, user_id, contact_id) -> None or True:
        contact_info = self.get_user_or_contact_info(contact_id)
        photo_ids = self.get_photos(contact_id)
        method = 'messages.send'
        attachment = f'{photo_ids[0]},{photo_ids[1]},{photo_ids[2]}'
        print(attachment)
        message = f'{contact_info[0]} {contact_info[1]}\nhttps://vk.com/id{contact_id}'
        params = {'message': message,
                  'keyboard': self.like_dislike_favorites_keyboard(),
                  'user_id': user_id,
                  'attachment': attachment,
                  "access_token": constants.TOKEN}
        print(f'Sending contact info of {contact_id}')
        self._vk_request(method, params)

    def get_user_or_contact_info(self, contact_id: int) -> list or None:
        # по vk id выдает список: [имя, фамилия, возраст, пол, город, vk id]
        method = 'users.get'
        params = {'user_id': contact_id,
                  'fields': 'bdate, city, sex'}
        # 'access_token': constants.APP_TOKEN}
        r = self._vk_request(method, params)
        print('user_data', r)
        contact_info = r['response'][0]
        city = contact_info['city']['title']
        first_name = contact_info['first_name']
        last_name = contact_info['last_name']
        age = int(datetime.now().year) - int(r['response'][0]['bdate'][-4:])
        gender = contact_info['sex']
        contact_info = [first_name, last_name, age, gender, city]
        print(contact_info)
        return contact_info

    def get_photos(self, contact_id: int) -> None or list:
        # по vk id выдает список с id 3 фото с макс.кол-вом лайков
        method = 'photos.getAll'
        params = {'owner_id': contact_id,

                  'extended': 1,
                  'access_token': constants.APP_TOKEN
                  }
        r = self._vk_request(method, params)
        print(r)
        photos = {}
        for item in r['response']['items']:
            likes = item['likes']['count']
            photos[f"photo{contact_id}_{item['id']}"] = likes
        photos = dict(sorted(photos.items(), key=lambda item: item[1], reverse=True))
        return list(photos.keys())[:3]

    def _vk_request(self, method, params=None) -> dict:
        self.params.update(params)
        url = self.base_url + method
        request_obj = requests.get(url=url, params=self.params)
        if self.params['access_token'] == constants.TOKEN:
            time.sleep(0.1)
        else:
            time.sleep(0.3)
        print(request_obj.json())
        return request_obj.json()

    @staticmethod
    def like_dislike_favorites_keyboard() -> dict:
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button(label='Favorites', color=VkKeyboardColor.PRIMARY, payload='4')
        keyboard.add_line()
        keyboard.add_button(label='Like', color=VkKeyboardColor.POSITIVE, payload='2')
        keyboard.add_button(label='Dislike', color=VkKeyboardColor.NEGATIVE, payload='3')
        return keyboard.get_keyboard()

    @staticmethod
    def favorites_keyboard() -> dict:
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button(label='Next user', color=VkKeyboardColor.PRIMARY, payload='1')
        return keyboard.get_keyboard()

