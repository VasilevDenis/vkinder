import requests
import time
import constants


class API:
    def __init__(self):
        self.base_url = 'https://api.vk.com/method/'
        self.params = {"v": constants.API_VERSION, "access_token": constants.TOKEN}

    def send_message(self, user_id, message):
        method = 'messages.send'
        params = {'user_id': user_id,
                  'random_id': 0,
                  'message': message}
        self._get(method, params)

    def _get(self, method, params=None):
        if params is not None:
            params.update(self.params)
        else:
            params = self.params
        url = self.base_url + method
        request_obj = requests.get(url=url, params=params)
        time.sleep(0.1)
        return request_obj.json()


if __name__ == '__main__':
    api = API()
    api.send_message('789313157', 'Message #1!')

