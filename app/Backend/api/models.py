from sqlalchemy import Column, Integer, String
from ..datadase.database import Base


class Client(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)

