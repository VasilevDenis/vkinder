import random
from datetime import datetime
import requests
import time
import constants
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class API:
    def __init__(self):
        self.base_url = "https://api.vk.com/method/"
        self.params = {"v": constants.API_VERSION, "access_token": constants.TOKEN}

    def send_favorites_users(self, received, favorites_users) -> None:
        """Отправляет список избранных пользователей в сообщении.
        Аргументы:
        received: Объект, содержащий информацию о полученном сообщении.
        favorites_users: Список идентификаторов избранных пользователей."""
        method = "messages.send"
        params = self._interface_params("Favorites!", self.start_keyboard(), received)
        self._vk_request(method, params)

    def wrong_command(self, received) -> None:
        """Отправляет сообщение о неверной команде."""
        method = "messages.send"
        params = self._interface_params(
            f"Wrong command!", self.like_dislike_favorites_keyboard(), received
        )
        self._vk_request(method, params)

    def get_users(self, city, age, gender) -> list:
        """Возвращает список идентификаторов пользователей, найденных по заданным критериям.
        Аргументы:
        city: Название города.
        age: Возраст.
        gender: Пол.
        """
        method = "users.search"
        city = city
        age = age
        gender = 3 - gender
        params = {
            "access_token": constants.APP_TOKEN,
            "hometown": city,
            "sex": gender,
            "age_from": age,
            "age_to": age,
        }
        r = self._vk_request(method, params)
        print(r["response"]["count"])
        found_users_list = []
        for item in r["response"]["items"]:
            found_users_list.append(item["id"])
        return found_users_list

    def send_user_info(self, user_id, user_info, received) -> None:
        """Отправляет информацию о пользователе в сообщении."""
        print(f"Sending user info to the chat! {user_id} {user_info}")
        method = "messages.send"
        params = self._interface_params(
            f"https://vk.com/id{user_id}\n{user_info}", self.start_keyboard(), received
        )
        self._vk_request(method, params)

    @staticmethod
    def _interface_params(message, keyboard, received) -> dict:
        """Возвращает параметры для отправки сообщения с клавиатурой."""
        params = {
            "random_id": random.randint(100000, 999999),
            "message": message,
            "keyboard": keyboard,
            "user_id": received.from_id,
        }
        return params

    @staticmethod
    def like_dislike_favorites_keyboard() -> dict:
        """Возвращает клавиатуру с кнопками "Favorites", "Like" и "Dislike"."""
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button(label="Favorites", color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(label="Like", color=VkKeyboardColor.POSITIVE)
        keyboard.add_button(label="Dislike", color=VkKeyboardColor.NEGATIVE)
        return keyboard.get_keyboard()

    @staticmethod
    def start_keyboard() -> dict:
        """Возвращает клавиатуру с кнопкой "Back"."""
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button(label="Back", color=VkKeyboardColor.PRIMARY)
        return keyboard.get_keyboard()

    def get_user_info(self, user_id: int) -> list or None:
        """Возвращает информацию о пользователе по его идентификатору.
        Аргументы:
        user_id: Идентификатор пользователя.
        Возвращаемое значение:
        Список с информацией о пользователе ([имя, фамилия, возраст, пол, город]).
        Строка "Город не указан", если город пользователя не указан.
        """
        method = "users.get"
        params = {"user_id": user_id, "fields": "bdate, city, sex"}
        r = self._vk_request(method, params)
        user_info = r["response"][0]
        if "city" in user_info:
            city = user_info["city"]["title"]
        else:
            return "Город не указан"
        first_name = user_info["first_name"]
        last_name = user_info["last_name"]
        age = int(datetime.now().year) - int(r["response"][0]["bdate"][-4:])
        gender = user_info["sex"]
        member_info = [first_name, last_name, age, gender, city]
        return member_info

    def get_photos(self, user_id: int) -> None or dict:
        """Возвращает список фотографий пользователя с наибольшим количеством лайков.
        Возвращаемое значение:
        Список URL-адресов фотографий пользователя с наибольшим количеством лайков."""
        method = "photos.get"
        params = {
            "owner_id": user_id,
            "album_id": "profile",
            "extended": 1,
            "access_token": constants.APP_TOKEN,
        }
        r = self._vk_request(method, params)
        photos = {}
        for item in r["response"]["items"]:
            likes = item["likes"]["count"]
            url = None
            for photo in item["sizes"]:
                if photo["type"] == "x":
                    url = photo["url"]
            photos[url] = likes
        photos = dict(sorted(photos.items(), key=lambda item: item[1], reverse=True))
        return list(photos.keys())[:3]

    def _vk_request(self, method, params=None) -> dict:
        """Выполняет запрос к API ВКонтакте."""
        self.params.update(params)
        url = self.base_url + method
        request_obj = requests.get(url=url, params=self.params)
        time.sleep(0.3)
        return request_obj.json()
