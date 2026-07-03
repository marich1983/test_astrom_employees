from pydantic import BaseModel, Field, ConfigDict, AfterValidator
from datetime import date
from typing import Optional, Annotated
from src.testastrom.enums import Gender
from src.testastrom.utils import age_calculate
from src.testastrom.validators import validate_phone, validate_name


Name = Annotated[
    str,
    Field(min_length=3, max_length=50),
    AfterValidator(validate_name),
]

Phone = Annotated[
    str | None,
    Field(min_length=5, max_length=20),
    AfterValidator(validate_phone),
]

class EmployeeBase(BaseModel):
    first_name: Name
    middle_name: Optional[Name] = None
    last_name: Name
    phone: Phone
    birthday: date
    gender: Gender
    photo: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    first_name: Optional[Name] = None
    middle_name: Optional[Name] = None
    last_name: Optional[Name] = None

    phone: Optional[Phone] = None
    birthday: Optional[date] = None
    gender: Optional[Gender] = None
    photo: Optional[str] = None



class EmployeeResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: str | None = None
    birthday: date
    # fio: str
    phone: str | None = None
    gender: str
    gender_rus: str
    photo: str | None = None
    age: int

    model_config = ConfigDict(from_attributes=True)

    @property
    def fio(self):
        return f"{self.last_name} {self.first_name} {self.middle_name or ''}".strip()

    @classmethod
    def from_employee(cls, obj):
        return cls(
            id=obj.id,
            first_name=obj.first_name,
            last_name=obj.last_name,
            middle_name=obj.middle_name,
            # fio=f"{obj.first_name} {obj.middle_name or ''} {obj.last_name}",
            phone=obj.phone,
            gender=obj.gender,
            gender_rus=obj.gender.label(),
            photo=obj.photo,
            birthday=obj.birthday,
            age=age_calculate(obj.birthday),
        )