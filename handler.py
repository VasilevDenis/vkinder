import random
import api
import base
import receiver


class Handler:
    def __init__(self, request, app, db, Viewed) -> None:
        self.api = api.API()
        self.base = base.Base(app, db, Viewed)
        received_json = request.get_json()
        self.received = receiver.Receiver(received_json)

    def handle(self) -> None:
        """Обрабатывает входящие команды и вызывает соответствующие методы в зависимости от полученной команды."""
        if self.received.correct:
            text = self.received.text
            if text == "1" or text == "start":
                self.next_user()
            elif text == "2":
                self.like()
            elif text == "3":
                self.dislike()
            elif text == "4":
                self.favorites_users()
            else:
                self.wrong_command()

    def next_user(self) -> None:
        """Получает информацию о следующем пользователе для оценки и отправляет эту информацию пользователю."""
        if self.base.is_unrated_user_exists():
            the_unrated_user = self.base.get_unrated_user()
            user_info = self.api.get_user_info(the_unrated_user)
            self.api.send_user_info(self.received.from_id, user_info)
        else:
            ids_of_users = self.api.get_users()
            id_of_random_unrated_user = random.choice(ids_of_users)
            unrated_user_info = self.api.get_user_info(id_of_random_unrated_user)
            self.base.add_user(self.received.from_id, id_of_random_unrated_user)
            self.api.send_user_info(
                id_of_random_unrated_user, unrated_user_info, self.received
            )

    def like(self) -> None:
        """Устанавливает оценку "Нравится" для текущего пользователя."""
        self._rate(True)

    def dislike(self) -> None:
        """Устанавливает оценку "Не нравится" для текущего пользователя."""
        self._rate(False)

    def favorites_users(self) -> None:
        """Получает список избранных пользователей и отправляет его пользователю."""
        favorites_users = self.base.get_favorites_users()
        self.api.send_favorites_users(self.received, favorites_users)

    def wrong_command(self) -> None:
        """Обработка некорректной команды."""
        pass

    def _rate(self, rate) -> None:
        """Устанавливает оценку для текущего пользователя и переходит к следующему пользователю."""
        if self.base.is_unrated_user_exists():
            self.base.set_like(rate)
            self.next_user()
        else:
            self.wrong_command()
