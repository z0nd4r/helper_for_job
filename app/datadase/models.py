import enum

from sqlalchemy import Column, Integer, String, Boolean, LargeBinary, ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass

class UserRegTablename(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(LargeBinary, nullable=False)
    email = Column(String, nullable=False, unique=True)
    active = Column(Boolean, nullable=False, default=True)

    refresh_token = relationship('RefreshTokens', back_populates='user')

class RefreshTokens(Base):
    __tablename__ = 'refresh_tokens'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='cascade'))
    token: Mapped[str] = mapped_column(nullable=False, unique=True)

    user: Mapped['UserRegTablename'] = relationship(back_populates='refresh_token')


class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

class FriendshipStatus(enum.Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

class Friend(Base):
    __tablename__ = 'friends'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='cascade'))
    friend_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='cascade'))
    status: Mapped[str] = mapped_column(Enum(FriendshipStatus), default=FriendshipStatus.PENDING)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

