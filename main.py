from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import handler
import constants


app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = constants.db_uri
db.init_app(app)


class Viewed(db.Model):
    """Модель таблицы viewed в базе данных."""
    __tablename__ = "viewed"

    vk_id = db.Column(db.Integer, primary_key=True)
    viewed_vk_id = db.Column(db.Integer, primary_key=True)
    like = db.Column(db.Boolean())


class RazorOfOccam(db.Model):
    """Модель таблицы occams в базе данных."""
    __tablename__ = "occams"

    occam_id = db.Column(db.Integer, primary_key=True)


class AntiSimplicity(db.Model):
    """Модель таблицы antisimplicity в базе данных."""
    __tablename__ = "antisimplicity"

    antisimplicity = db.Column(db.Integer, primary_key=True)


@app.route("/", methods=["GET", "POST"])
def event() -> str:
    """Декоратор маршрута, определяющий обработку запросов по корневому URL.
    Аргументы:
    '/': Корневой URL."""
    new_handler = handler.Handler(request, app, db, Viewed)
    new_handler.handle()
    return "ok"


if __name__ == "__main__":
    """Блок кода, который будет выполнен только в случае, если данный скрипт запущен напрямую (а не импортирован как модуль).
    Действия:
    Создание всех таблиц в базе данных при помощи метода db.create_all().
    Запуск приложения Flask на адресе 0.0.0.0 и порту 5001."""
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5001)
