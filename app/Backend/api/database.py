import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

DATABASE_USER = "postgres.zyfosgbvyefnreuglbdy" # Usually postgres
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = "aws-0-us-west-1.pooler.supabase.com"
DATABASE_PORT = "5432"
DATABASE_NAME = "postgres"

SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"


try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except OperationalError as e:
    print(f"Error connecting to database: {e}")

Base = declarative_base()



