from datetime import date
from http.client import HTTPResponse
from typing import Optional
from pathlib import Path
import shutil

from fastapi import FastAPI, Depends, Query, Request, Form, File, UploadFile, HTTPException

from sqlalchemy.orm import Session
from src.testastrom.schemas import EmployeeResponse, EmployeeCreate, EmployeeUpdate
from src.testastrom.database import get_session
from src.testastrom.crud import create_employee, update_employee, delete_employee, search_employees
from starlette import status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse

from src.testastrom.enums import Gender
from src.testastrom.models import Employee

# poetry run uvicorn src.testastrom.main:app --reload

app = FastAPI(
    title="TestAstromEmployee API",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get(
    "/",
    response_class=HTMLResponse,
    summary='Страница добавления'
)
async def create_page(request: Request):
    return templates.TemplateResponse(request,"employee_list.html")


@app.get(
    "/employees",
    response_model=list[EmployeeResponse],
    summary='Получение списка сотрудников',
    status_code=status.HTTP_200_OK
)
def get_employees(
    search: str | None = Query(None),
    age_from: int | None = Query(None, ge=0),
    age_to: int | None = Query(None, ge=0),
    gender: Gender | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session),
):
    employees = search_employees(
        session=session,
        # fio=fio,
        # phone=phone,
        search=search,
        age_from=age_from,
        age_to=age_to,
        gender=gender,
        skip=skip,
        limit=limit,
    )

    return [EmployeeResponse.from_employee(e) for e in employees]

@app.get(
    "/create-employee",
    response_class=HTMLResponse,
    summary='Страница реестра'
)
def add_employee_page(request: Request):
    return templates.TemplateResponse(request,"create_employee.html")

@app.post(
    '/employees',
    response_model=EmployeeResponse,
    summary='Создание нового сотрудника',
    status_code=status.HTTP_201_CREATED
)
def create(
    first_name: str = Form(...),
    last_name: str = Form(...),
    middle_name: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    birthday: Optional[date] = Form(None),
    gender: Gender = Form(...),
    photo: Optional[UploadFile] = File(None),
    session: Session = Depends(get_session),
):
# def create(
#         employee: EmployeeCreate,
#         session: Session = Depends(get_session)
# ):
    photo_name = None

    # Внимание!!!! Добавить uuid для фото

    if photo:
        upload_dir = Path("static/photos")
        upload_dir.mkdir(parents=True, exist_ok=True)

        photo_name = photo.filename

        with open(upload_dir / photo_name, "wb") as buffer:
            print("WRITING FILE:", upload_dir / photo_name)
            shutil.copyfileobj(photo.file, buffer)


    employee = EmployeeCreate(
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        phone=phone,
        birthday=birthday,
        gender=gender,
        photo=photo_name
    )


    # print("UPLOAD DIR:", upload_dir)
    # print("ABS PATH:", upload_dir.resolve())
    # print("EMPLOYEE MODEL:", employee)

    new_employee = create_employee(session, employee)
    return EmployeeResponse.from_employee(new_employee)

@app.get(
    "/employees/{employee_id}",
    response_model=EmployeeResponse,
    summary="Получение сотрудника по id"
)
def get_employee(
    employee_id: int,
    session: Session = Depends(get_session),
):
    employee = session.get(Employee, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Сотрудник не найден"
        )

    return EmployeeResponse.from_employee(employee)

@app.get(
    "/edit-employee/{employee_id}",
    response_class=HTMLResponse,
    summary='Страница редактирования'
)
def edit_page(request: Request):
    return templates.TemplateResponse(request,"create_employee.html")



@app.put(
    '/employees/{employee_id}',
    response_model=EmployeeResponse,
    summary='Обновление данных сотрудника',
    status_code=status.HTTP_200_OK
)
def update(
        employee_id: int,
        first_name: str = Form(...),
        last_name: str = Form(...),
        middle_name: Optional[str] = Form(None),
        phone: Optional[str] = Form(None),
        birthday: Optional[date] = Form(None),
        gender: Gender = Form(...),
        photo: Optional[UploadFile] = File(None),
        session: Session = Depends(get_session),
):
    photo_name = None

    # Внимание!!!! Добавить uuid для фото

    if photo:
        upload_dir = Path("static/photos")
        upload_dir.mkdir(parents=True, exist_ok=True)

        photo_name = photo.filename

        with open(upload_dir / photo_name, "wb") as buffer:
            print("WRITING FILE:", upload_dir / photo_name)
            shutil.copyfileobj(photo.file, buffer)

    employee_update = EmployeeCreate(
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        phone=phone,
        birthday=birthday,
        gender=gender,
        photo=photo_name
    )

    result = update_employee(
        session=session,
        employee_id=employee_id,
        employee_update=employee_update)

    return EmployeeResponse.from_employee(result)


@app.delete(
    '/employees/{employee_id}',
    summary='Удаление сотрудника',
    status_code=status.HTTP_204_NO_CONTENT)
def delete(
        employee_id: int,
        session: Session = Depends(get_session)
):
    delete_employee(
        session=session,
        employee_id=employee_id
    )
    return {'message': 'Success'}



if __name__ == '__main__':
    pass