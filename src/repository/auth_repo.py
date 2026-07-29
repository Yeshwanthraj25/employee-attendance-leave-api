
from sqlalchemy import select
from src.repository.schema.schema import Employee,LogAttendance,Department,LeaveManagement,LeaveQuote,ErrorLog
from fastapi import HTTPException,status
from src.models.dto.exception  import AppException


async def get_user(db,emp_id):
    try:
        query = select(Employee).where(Employee.emp_id ==  emp_id)
        result  = await db.execute(query)
        user = result.scalars().first()
        if not user:
            raise AppException("auth_repo","get_user",404,"user not found",None)
        return user
    except  Exception as e:
        raise AppException("auth_repo","get_user",500,"DB error ",str(e)
                           )

async def get_user_by_email(db,email):
    try :
        query = select(Employee).where (Employee.email_id == email )
        result = await db.execute(query)
        user = result.scalars().first()
        if not user:
            raise   AppException("auth_repo","get_user_by_email",404,"user not found",None)
        return user
    except Exception as e :
        raise AppException("auth_repo","get_user_by_email",500,"DB error ",str(e))

async def create_user(db,email_id,password,phone_number,dep_id,role):
    try:
        insert = Employee(email_id=email_id,password=password,phone_number =phone_number,dep_id=dep_id,role=role)
        db.add(insert)
        await db.flush()
        return insert
    except Exception as e :
        raise AppException("auth_repo","create_user",500,"DB error ",str(e))


    