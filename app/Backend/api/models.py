from sqlalchemy import Boolean, Column, Integer, String
from app.Backend.api.database import Base


class Item(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    status = Column(Boolean, default=True)

