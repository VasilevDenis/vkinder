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
                print(text)
                self.wrong_command()

    def next_user(self) -> None:
        if self.base.is_unrated_contact_exists():
            the_unrated_contact_id = self.base.get_unrated_contact()
            try:
                self.api.send_contact_info(self.received.from_id, the_unrated_contact_id)
            except Exception:
                self.base.rate(None, False)
                print('Error! Next_user')
                self.next_user()
        else:
            first_name, last_name, age, gender, city = self.api.get_user_or_contact_info(self.received.from_id)
            contacts = self.api.get_contacts(city, age, int(gender))
            if contacts:
                viewed_contacts = self.base.get_all_contacts_for_user_id(self.received.from_id)
                contacts = self.api.get_contacts(city, age, gender)
                not_viewed_contacts = set(contacts) - set(viewed_contacts)
                if len(not_viewed_contacts) > 0:
                    id_of_random_new_contact = random.choice(list(not_viewed_contacts))
                    self.base.add_user_contact(self.received.from_id, id_of_random_new_contact)
                else:
                    #  users not found for match
                    message = 'There is no users to match! Sorry!'
                    print(message)
                    self.api.send_message(self.received.from_id, message)
                    return
                try:
                    self.api.send_contact_info(self.received.from_id, id_of_random_new_contact)
                except Exception:
                    print('Error! Next_user')
                    self.base.rate(None, False)
                    self.next_user()
            else:
                #  users not found for match
                message = 'There is no users to match! Sorry!'
                self.base.rate(None, False)
                self.api.send_message(self.received.from_id, message)

    def like(self) -> None:
        self._rate('True')

    def dislike(self) -> None:
        self._rate('False')

    def favorites_contacts(self) -> None:
        favorites_users = self.base.get_favorites_contacts(self.received.from_id)
        if not favorites_users:
            self.api.send_message(self.received.from_id, 'There is no favorites!')
        else:
            print('Sending the favorites!')
            self.api.send_favorites_contacts(self.received.from_id, favorites_users)

    def wrong_command(self) -> None:
        self.api.wrong_command(self.received.from_id)

    def _rate(self, rate) -> None:
        if self.base.is_unrated_contact_exists():
            self.base.rate('None', rate)
            self.next_user()
        else:
            self.wrong_command()


