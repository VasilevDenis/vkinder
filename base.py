class Base:
    def __init__(self, app, db, user_contact) -> None:
        self.app = app
        self.db = db
        self.user_contact = user_contact

    def is_unrated_contact_exists(self) -> bool:
        """
        Checking for viewed user, who exist in the base, but not unrated (like == None).
        """
        if self.get_unrated_contact():
            return True
        else:
            return False

    def get_unrated_contact(self) -> int or None:
        """
        Returns vk_id of unrated contact .
        """
        try:
            unrated_contact = self.db.session.execute(
                self.db.select(self.user_contact)
                .filter_by(like='None')).scalar_one()
            return unrated_contact.contact_id
        except Exception:
            return None

    def add_user_contact(self, user_id: int, contact_id: int) -> None:
        """
        Add a new record to the base.
        """
        user_contact = self.user_contact(user_id=user_id, contact_id=contact_id, like='None')
        self.db.session.add(user_contact)
        self.db.session.commit()

    def rate(self, contact_id, rate: bool) -> None:
        """
        Rates contact. Sets field 'like' in the base == True or False
        """
        print(contact_id, 'contact_id')
        if contact_id is None:
            record = self.db.session.execute(
                self.db.select(self.user_contact)
                .filter_by(like='None')).scalar_one()
        else:
            record = self.db.session.execute(
                self.db.select(self.user_contact)
                .filter_by(like='None')).scalar_one()
        record.like = rate
        self.db.session.commit()

    def get_favorites_contacts(self, user_id: int) -> list or True:
        """
        Returns favorites contacts.
        """
        favorite_contacts = self.db.session.execute(
            self.db.select(self.user_contact.contact_id)
            .filter_by(user_id=user_id)
            .filter_by(like='True')).scalars()
        favorite_contacts = [f'https://vk.com/id{str(elem)}' for elem in favorite_contacts]
        return favorite_contacts

    def get_all_contacts_for_user_id(self, user_id):
        """
        Returns all viewed contacts for user_id.
        """
        all_contacts = self.db.session.execute(
            self.db.select(self.user_contact.contact_id)
            .filter_by(user_id=user_id)).scalars()
        return all_contacts



