import random
import api
import base
import receiver


class Handler:
    def __init__(self, request, app, db, user_contact) -> None:
        self.api = api.API()
        self.base = base.Base(app, db, user_contact)
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
                self.favorites_contacts()
            else:
                self.wrong_command()

    def next_user(self) -> None:
        if self.base.is_unrated_contact_exists():
            the_unrated_user = self.base.get_unrated_contact()
            first_name, last_name = self.api.get_user_or_contact_info(the_unrated_user)[:1]
            photos = self.api.get_photos(self.received.from_id)
            self.api.send_contact_info(self.received.from_id, first_name, last_name, photos)
        else:
            first_name, last_name, age, gender, city = self.api.get_user_or_contact_info(self.received.from_id)
            not_viewed_contacts = self.api.get_contacts(city, age, int(gender))
            if not_viewed_contacts:
                viewed_contacts = self.base.get_all_contacts_for_user_id(self.received.from_id)
                contacts = self.api.get_contacts(city, age, gender)
                not_viewed_contacts = set(contacts) - set(viewed_contacts)
                id_of_random_new_contact = random.choice(list(not_viewed_contacts))
                self.base.add_user_contact(self.received.from_id, id_of_random_new_contact)
                self.api.send_contact_info(self.received.from_id, id_of_random_new_contact)
            else:
                #  users not found for match
                message = 'There is no users to match! Sorry!'
                self.api.send_message(self.received.from_id, message)

    def like(self) -> None:
        self._rate(True)

    def dislike(self) -> None:
        self._rate(False)

    def favorites_contacts(self) -> None:
        favorites_users = self.base.get_favorites_contacts()
        self.api.send_favorites_contacts(self.received.from_id, favorites_users)

    def wrong_command(self) -> None:
        pass

    def _rate(self, rate) -> None:
        if self.base.is_unrated_contact_exists():
            self.base.rate(rate)
            self.next_user()
        else:
            self.wrong_command()


