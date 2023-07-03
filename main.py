from flask import Flask, request
import handler


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def event() -> str:
    new_handler = handler.Handler(request)
    new_handler.handle()
    return 'ok'


if __name__ == "__main__":
    app.run(host='0.0.0.0')

