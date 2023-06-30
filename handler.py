import api
import receiver


class Handler:
    def __init__(self, request) -> None:
        self.api = api.API()
        received_json = request.get_json()
        self.received = receiver.Receiver(received_json)

    def handle(self):
        if self.received.correct:
            text = self.received.text
            if text == 'Back':
                self.back()
            if text == 'Like':
                self.like()
            elif text == 'Dislike':
                self.dislike()
            elif text == 'Favorites':
                self.favorites_users()
            else:
                self.wrong_command()

    def back(self):
        self.api.back(self.received)

    def like(self):
        self.api.like(self.received)

    def dislike(self):
        self.api.dislike(self.received)

    def favorites_users(self):
        self.api.favorites_users(self.received)

    def wrong_command(self):
        self.api.wrong_command(self.received)


