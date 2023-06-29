from flask import Flask, request
import constants


app = Flask(__name__)


class ChatBot:
    @app.route('/', methods=['GET', 'POST'])
    def event(self):
        request_data = request.get_json()
        if request_data:
            if request_data['secret'] == constants.SECRET_KEY:
                if request_data['type'] == 'message_new':
                    message_data = request_data['object']
                    user_id = message_data['user_id']
                    message = message_data['body']
                    self.response(user_id, message)
                    return 'ok'

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


if __name__ == "__main__":
    app.run(host='0.0.0.0')

