class MessageHandler:
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
        pass

    def dislike(self, user_id):
        pass

    def next(self, user_id):
        pass

    def get_favorites_users(self, user_id):
        pass

    def wrong_message(self, user_id):
        pass

