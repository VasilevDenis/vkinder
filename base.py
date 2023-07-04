class Base:
    def __init__(self, app, db, user) -> None:
        self.app = app
        self.db = db
        self.user = user

    def is_unrated_user_exists(self) -> bool:
        """
        Checking for viewed user, who exist in the base, but not unrated. (like == None)
        :return: True or False
        """
        if self.get_unrated_user():
            return True
        else:
            return False

    def get_unrated_user(self) -> int or None:
        """
        :return: unrated user id from base or None
        """
        user = self.db.session.execute(self.db.select(self.user).where(self.user.like is None)).scalars()
        print(user)

    def delete_unrated_user(self) -> None:
        """
        Deletes record in the base, where viewed_user_id == None
        """

    def add_user(self, user_id: int, unrated_user: int) -> None:
        pass

    def set_like(self, unrated_user: int) -> None:
        pass

    def get_favorites_users(self) -> list or None:
        print('Returnin favorites')
        return [1, 2, 3, 4]

