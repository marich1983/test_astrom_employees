from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)

def get_session():
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

if __name__ == '__main__':
    with engine.connect() as conn:
        print("Подключение успешно!")
