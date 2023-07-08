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

    def send_favorites_users(self, user_id, favorites_users) -> None:
        method = 'messages.send'
        params = self._interface_params('Favorites!',
                                        self.start_keyboard(), user_id)
        self._vk_request(method, params)

    def wrong_command(self, user_id) -> None:
        method = 'messages.send'
        params = self._interface_params(f'Wrong command!',
                                        self.like_dislike_favorites_keyboard(), user_id)
        self._vk_request(method, params)

    def get_users(self, city: str, age: str, gender: int) -> list:
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
        photo_ids = self.get_photos(contact_id)
        if len(photo_ids) < 3:
            return "No photo"
        else:
            print(f'Sending user info to the chat! {user_id}')
            method = 'messages.send'
            attachment = f'{photo_ids[0]},{photo_ids[1]},{photo_ids[2]}'
            params = self._interface_params(f'{contact_info[0]} {contact_info[1]}\n'
                f'https://vk.com/id{contact_id}', self.start_keyboard(), user_id, attachment)
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
        if 'bdate' in r['response'][0]:
            age = int(datetime.now().year) - int(r['response'][0]['bdate'][-4:])
        else:
            age = None
        gender = contact_info['sex']
        contact_info = [first_name, last_name, age, gender, city]
        return contact_info

    def get_photos(self, contact_id: int) -> None or dict:
        # по vk id выдает список с id 3 фото с макс.кол-вом лайков
        method = 'photos.getAll'
        params = {'owner_id': contact_id,
                  'extended': 1,
                  'access_token': constants.APP_TOKEN
                  }
        r = self._vk_request(method, params)
        photos = {}
        if 'response' in r: 
            for item in r['response']['items']:
                likes = item['likes']['count']
                photos[f"photo{contact_id}_{item['id']}"] = likes
        photos = dict(sorted(photos.items(), key=lambda item: item[1], reverse=True))
        return list(photos.keys())[:3]

    def _vk_request(self, method, params=None) -> dict:
        self.params.update(params)
        url = self.base_url + method
        request_obj = requests.get(url=url, params=self.params)
        time.sleep(0.3)
        return request_obj.json()

    @staticmethod
    def _interface_params(message, keyboard, user_id, attachment=None) -> dict:
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


api = API()
# print(api.get_contact_info(1))
# for i in range (788770608, 788770706):

#     print(api.send_contact_info(788770602, i), i)
#     i += 1

# print(api.send_contact_info(788770602, 788770678))
# print(api.get_photos(788770678))
api.send_contact_info(788770602, 788770678)
