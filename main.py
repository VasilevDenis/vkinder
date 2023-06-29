from flask import Flask, request
import constants
import message_handler


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def event():
    m_handler = message_handler.MessageHandler()
    request_data = request.get_json()
    if request_data:
        if request_data['secret'] == constants.SECRET_KEY:
            if request_data['type'] == 'message_new':
                message_data = request_data['object']['message']
                user_id = message_data['from_id']
                message = message_data['text']
                m_handler.response(user_id, message)
    return 'ok'


if __name__ == "__main__":
    app.run(host='0.0.0.0')

