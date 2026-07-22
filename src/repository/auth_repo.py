from src.repository.Database import get_db
from sqlalchemy import select
from src.repository.schema import Employee
from fastapi import HTTPException,status


async def get_user(emp_id,get_db):
    try:
        with get_db as session:
            get_user = session.execute(Employee.emp_id,Employee.role).filter(Employee.emp_id == emp_id).one()
        return {"data":{"emp_id":get_user["emp_id"],"role":get_user["role"]}}
    except  Exception as e:
        raise HTTPException(status_code=404,detail =f"get_user is faild({e})"