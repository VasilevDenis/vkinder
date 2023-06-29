import vk_api


class MessageHandler:
    def __init__(self):
        self.api = vk_api.API()

    def response(self, user_id, message):
        message = message.strip()
        if message == 'like':
            self.like(user_id)
        elif message == 'dislike':
            self.dislike(user_id)
        elif message == 'next':
            self.next(user_id)
        elif message == 'favorites':
            self.get_favorites_users(user_id)
        else:
            self.wrong_message(user_id)

    def like(self, user_id):
        self.api.send_message(user_id, 'Like!')

    def dislike(self, user_id):
        self.api.send_message(user_id, 'Dislike!')

    def next(self, user_id):
        self.api.send_message(user_id, 'Next!')

    def get_favorites_users(self, user_id):
        self.api.send_message(user_id, 'Favorites!')

    def wrong_message(self, user_id):
        self.api.send_message(user_id, 'Wrong message!')

