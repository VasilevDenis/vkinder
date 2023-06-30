import random
import requests
import time
import constants
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class API:
    def __init__(self):
        self.base_url = 'https://api.vk.com/method/'
        self.params = {"v": constants.API_VERSION, "access_token": constants.TOKEN}

    def back(self, received):
        method = 'messages.send'
        params = self._interface_params('Back!',
                                        self.like_dislike_favorites_keyboard(), received)
        self._get(method, params)

    def like(self, received):
        method = 'messages.send'
        params = self._interface_params('Like!',
                                        self.like_dislike_favorites_keyboard(), received)
        self._get(method, params)

    def dislike(self, received):
        method = 'messages.send'
        params = self._interface_params('Dislike!',
                                        self.like_dislike_favorites_keyboard(), received)
        self._get(method, params)

    def favorites_users(self, received):
        method = 'messages.send'
        params = self._interface_params('Favorites!',
                                        self.start_keyboard(), received)
        self._get(method, params)

    def wrong_command(self, received):
        method = 'messages.send'
        if received.text == 'Back':
            return
        params = self._interface_params(f'{received.text} - is wrong command!',
                                        self.like_dislike_favorites_keyboard(), received)
        print(self._get(method, params))

    @staticmethod
    def _interface_params(message, keyboard, received):
        params = {'random_id': random.randint(100000, 999999),
                  'message': message,
                  'keyboard': keyboard,
                  'user_id': received.from_id
                  }
        return params

    def _get(self, method, params=None):
        if params is not None:
            params.update(self.params)
        else:
            params = self.params
        url = self.base_url + method
        request_obj = requests.post(url=url, params=params)
        time.sleep(0.1)
        return request_obj.json()

    @staticmethod
    def like_dislike_favorites_keyboard():
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button(label='Favorites', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(label='Like', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button(label='Dislike', color=VkKeyboardColor.NEGATIVE)
        return keyboard.get_keyboard()

    @staticmethod
    def start_keyboard():
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button(label='Back', color=VkKeyboardColor.PRIMARY)
        return keyboard.get_keyboard()

