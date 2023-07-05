import random
import api
import base
import receiver


class Handler:
    def __init__(self, request, app, db, viewed_class) -> None:
        self.api = api.API()
        self.base = base.Base(app, db, viewed_class)
        received_json = request.get_json()
        self.received = receiver.Receiver(received_json)

    def handle(self) -> None:
        if self.received.correct:
            text = self.received.text
            if text == '1' or text == 'start':
                self.next_user()
            elif text == '2':
                self.like()
            elif text == '3':
                self.dislike()
            elif text == '4':
                self.favorites_users()
            else:
                self.wrong_command()

    def next_user(self) -> None:
        if self.base.is_unrated_user_exists():
            the_unrated_user = self.base.get_unrated_user()
            user_info = self.api.get_user_info(the_unrated_user)
            self.api.send_user_info(self.received.from_id, user_info)
        else:
            first_name, last_name, age, gender, city = self.api.get_user_info(self.received.from_id)
            ids_of_users = self.api.get_users(city, age, int(gender))
            if ids_of_users:
                id_of_random_unrated_user = random.choice(ids_of_users)
                unrated_user_info = self.api.get_user_info(id_of_random_unrated_user)
                self.base.add_user(self.received.from_id, id_of_random_unrated_user)
                self.api.send_user_info(self.received.from_id, unrated_user_info)
            else:
                #  users not found for match
                message = 'There is no users to match! Sorry!'
                self.api.send_message(self.received.from_id, message)

    def like(self) -> None:
        self._rate(True)

    def dislike(self) -> None:
        self._rate(False)

    def favorites_users(self) -> None:
        favorites_users = self.base.get_favorites_users()
        self.api.send_favorites_users(self.received.from_id, favorites_users)

    def wrong_command(self) -> None:
        pass

    def _rate(self, rate) -> None:
        if self.base.is_unrated_user_exists():
            self.base.rate(rate)
            self.next_user()
        else:
            self.wrong_command()


