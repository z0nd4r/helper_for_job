from typing import TYPE_CHECKING, TypeVar

from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTable,
)
from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

#UserIdType = TypeVar("UserIdType")


# class Client(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=True)
#     email = Column(String, nullable=True)

class UserRegTablename(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(LargeBinary, nullable=False)
    email = Column(String, nullable=False, unique=True)
    active = Column(Boolean, nullable=False, default=True)

    # Добавляет отношение access_tokens к UserRegTablename
    # back_populates="user" создает двунаправленное отношение, что упрощает навигацию между моделями
    access_tokens = relationship("AccessToken", back_populates="user")

class AccessToken(Base, SQLAlchemyBaseAccessTokenTable[Integer]):
    user_id: Mapped[Integer] = mapped_column(
        Integer,
        # поле user.id - внешний ключ, ссылается на поле id в таблице users
        # ondelete="cascade" - если юзер удалится, то и все токены связанные с ним - тоже
        ForeignKey("users.id", ondelete="cascade"),
        nullable=False,
    )

    # добавляет отношение user к AccessToken
    user: Mapped['UserRegTablename'] = relationship(back_populates="access_tokens")

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyAccessTokenDatabase(session, cls)

class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
