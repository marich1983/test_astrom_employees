from datetime import date

from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.testastrom.models import Employee
from src.testastrom.schemas import EmployeeCreate, EmployeeUpdate
from src.testastrom.utils import birthday_calculate
from src.testastrom.enums import Gender


def create_employee(
        session: Session,
        employee: EmployeeCreate
) -> Employee:
    new_employee = Employee(
        first_name=employee.first_name,
        middle_name=employee.middle_name,
        last_name=employee.last_name,
        birthday=employee.birthday,
        gender=employee.gender,
        phone=employee.phone,
        photo=employee.photo
    )

    session.add(new_employee)
    session.commit()

    return new_employee

def get_employees_list(
        session: Session,
        skip: int = 0,
        limit: int = 10
):
    emp_list = session.query(Employee).offset(skip).limit(limit).all()
    return emp_list


def get_employee_by_id(
        session: Session,
        employee_id: int
):
    employee = session.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        return None

    return employee

def update_employee(
        session: Session,
        employee_id: int,
        employee_update: EmployeeUpdate
):
    employee = get_employee_by_id(session, employee_id)

    if not employee:
        return None

    for key, value in employee_update.model_dump(exclude_unset=True).items():
        setattr(employee, key, value)

    session.commit()
    session.refresh(employee)

    return employee

def delete_employee(
        session: Session,
        employee_id: int
):
    employee = get_employee_by_id(session, employee_id)

    if not employee:
        return False

    session.delete(employee)
    session.commit()

    return True


def search_employees(
    session: Session,
    # fio: str | None = None,
    # phone: str | None = None,
    search: str | None = None,
    age_from: int | None = None,
    age_to: int | None = None,
    gender: Gender | None = None,
    skip: int = 0,
    limit: int = 10,
):
    query = session.query(Employee)

    if search:
        pattern = f"%{search}%"

        query = query.filter(
            or_(
                Employee.first_name.ilike(pattern),
                Employee.middle_name.ilike(pattern),
                Employee.last_name.ilike(pattern),
                Employee.phone.ilike(pattern) if Employee.phone is not None else False
            )
        )

    if age_from is not None:
        max_birthday = birthday_calculate(age_from)
        query = query.filter(Employee.birthday <= max_birthday)

    if age_to is not None:
        min_birthday = birthday_calculate(age_to)
        query = query.filter(Employee.birthday >= min_birthday)

    # if phone:
    #     query = query.filter(Employee.phone.ilike(f"%{phone}%"))

    if gender:
        query = query.filter(Employee.gender == gender.value)
    print(query)

    return (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

if __name__ == '__main__':
    from src.testastrom.database import SessionLocal
    from datetime import date

    session = SessionLocal()

    try:
        emp1 = Employee(
        first_name='Александр',
        middle_name='Сергеевич',
        last_name='Пушкин',
        birthday=date(1799,6,6),
        gender='male'
    )

        create_employee(session, emp1)
        print(get_employees_list(session))
    finally:
        session.close()