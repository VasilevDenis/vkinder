class Base:
    def __init__(self, app, db, Viewed) -> None:
        self.app = app
        self.db = db
        self.viewed = Viewed

    def is_unrated_user_exists(self) -> bool:
        """
        Проверяет наличие просмотренного пользователя, который существует в базе данных, но не имеет оценки (like == None).
        Возвращаемое значение:
        Логическое значение True, если просмотренный но неоцененный пользователь существует.
        Логическое значение False, если просмотренный но неоцененный пользователь не существует.
        """
        if self.get_unrated_user():
            return True
        else:
            return False

    def get_unrated_user(self) -> int or None:
        """
        Возвращает идентификатор просмотренного, но неоцененного пользователя из базы данных или None, если такого пользователя нет.
        """
        unrated_user = list(
            self.db.session.execute(
                self.db.select(self.viewed).where(self.viewed.like is None)
            )
        )
        if unrated_user:
            return unrated_user[0]
        else:
            return None

    def delete_unrated_user(self) -> None:
        """
        Удаляет запись из базы данных, где идентификатор просмотренного пользователя равен None.
        """

    def add_user(self, user_id: int, unrated_user: int) -> None:
        """Добавляет запись о пользователе в базу данных."""
        viewed = self.viewed(vk_id=user_id, viewed_vk_id=unrated_user)
        self.db.session.add(viewed)
        self.db.session.commit()

    def set_like(self, unrated_user: int) -> None:
        """Устанавливает оценку для просмотренного пользователя."""
        pass

    def get_favorites_users(self) -> list or None:
        """Возвращает список избранных пользователей из базы данных."""
        print("Returnin favorites")
        return [1, 2, 3, 4]
