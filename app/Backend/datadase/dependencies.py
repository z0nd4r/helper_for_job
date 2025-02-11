from sqlalchemy.orm import Session
from .database import SessionLocal

def get_db(): #создать сессию базы данных и закрыть ее после завершения запроса
    db = SessionLocal()
    try:
        yield db #вернуть сессию базы данных которая будет использоваться в запросе
    finally:
        db.close() #закрыть сессию