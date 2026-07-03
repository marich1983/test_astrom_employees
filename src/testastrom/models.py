from sqlalchemy import Column, Integer, Enum, String, Numeric, DateTime, Date
from sqlalchemy.orm import declarative_base
from datetime import datetime
from src.testastrom.enums import Gender

# alembic revision --autogenerate -m "initial migration"
# alembic upgrade head
Base = declarative_base()


# Валидация!!!!

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(200), nullable=False)
    middle_name = Column(String(200), nullable=True)
    last_name = Column(String(200), nullable=False)
    birthday = Column(Date, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    phone = Column(String(20), nullable=True)
    photo = Column(String(500), nullable=True)

    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f' {self.id} {self.first_name} {self.middle_name} {self.last_name} {self.birthday} {self.gender} {self.phone}'

