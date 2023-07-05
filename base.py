class Base:
    def __init__(self, app, db, viewed_class) -> None:
        self.app = app
        self.db = db
        self.viewed_class = viewed_class

    def is_unrated_user_exists(self) -> bool:
        """
        Checking for viewed user, who exist in the base, but not unrated. (like == None)
        """
        if self.get_unrated_user():
            return True
        else:
            return False

    def get_unrated_user(self) -> int or None:
        """
        Returns unrated user vk_id.
        """
        unrated_user = list(self.db.session.execute(self.db.select(self.viewed_class)
                                                    .where(self.viewed_class.like is None)))
        if unrated_user:
            return unrated_user[0]
        else:
            return None

    def delete_unrated_user(self) -> None:
        """
        Deletes record in the base, where viewed_user_id == None
        """

    def add_user(self, user_id: int, unrated_user: int) -> None:
        viewed = self.viewed_class(vk_id=user_id, viewed_vk_id=unrated_user)
        self.db.session.add(viewed)
        self.db.session.commit()

    def rate(self, rate: bool) -> None:
        self.db.session.execute(
            self.db.update(self.viewed_class).where(self.viewed_class.like is None).values(like=rate))
        self.db.session.commit()

    def get_favorites_users(self) -> list:
        favorite_users = list(self.db.session.execute(
            self.db.select(self.viewed_class).where(self.viewed_class.like is True)))
        return favorite_users


