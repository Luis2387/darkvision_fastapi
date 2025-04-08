from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL


DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/darkvision_db"

url_object = URL.create(
    drivername="postgresql+psycopg",
    username="postgres",
    password="postgres",
    host="localhost",
    port=5432,
    database="darkvision_db",
)

engine = create_engine(url_object, connect_args={"client_encoding": "utf8"})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
