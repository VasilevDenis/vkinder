from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import handler
import constants


app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = constants.db_uri
db.init_app(app)


class UserContact(db.Model):
    __tablename__ = "users_contacts"

    user_id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, primary_key=True)
    like = db.Column(db.String(5), )


class RazorOfOccam(db.Model):
    __tablename__ = "occams"

    occam_id = db.Column(db.Integer, primary_key=True)


class AntiSimplicity(db.Model):
    __tablename__ = "antisimplicity"

    antisimplicity = db.Column(db.Integer, primary_key=True)


@app.route('/', methods=['GET', 'POST'])
def event() -> str:
    new_handler = handler.Handler(request, app, db, UserContact)
    new_handler.handle()
    return 'ok'


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001)

