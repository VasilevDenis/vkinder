from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    vk_id: Mapped[str] = mapped_column(String(30), unique=True)

    viewed_users: Mapped[List["ViewedUser"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, vk_id={self.vk_id!r})"


class ViewedUser(Base):
    __tablename__ = "viewed_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    vk_id: Mapped[str] = mapped_column(String(30), unique=True)
    like: Mapped[bool] = mapped_column(Boolean())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="viewed_users")

    def __repr__(self) -> str:
        return f"Viewed user(id={self.id!r}, vk_id={self.vk_id!r})"


class Unnecessary(Base):
    __tablename__ = "unnecessary"

    id: Mapped[int] = mapped_column(primary_key=True)

