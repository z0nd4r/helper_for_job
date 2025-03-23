from sqlalchemy import Column, Integer, String, Boolean, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass

class UserRegTablename(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(LargeBinary, nullable=False)
    email = Column(String, nullable=False, unique=True)
    active = Column(Boolean, nullable=False, default=True)

class BlackListToken(Base):
    __tablename__ = 'blacklist_tokens'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    jti: Mapped[str] = mapped_column(nullable=False)


class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
