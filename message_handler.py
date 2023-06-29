class MessageHandler:
    def response(self, user_id, message):
        match message.strip():
            case 'like':
                self.like(user_id)
            case 'dislike':
                self.dislike(user_id)
            case 'next':
                self.next(user_id)
            case 'favorites':
                self.get_favorites_users(user_id)
            case _:
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

