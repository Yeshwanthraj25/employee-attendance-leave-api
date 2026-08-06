from pydantic import BaseModel,ConfigDict
from datetime import datetime


class APIResponse(BaseModel):
    status: str
    code : int 
    message : str
    data : dict | list | None = {}
    errors : list = []
    timestamp : datetime
    request_id : str


class RegisterResponse(BaseModel):
    emp_id : str
    email_id : str
    phone_number : str
    role : str
    dep_id : str 


