from pydantic import BaseModel
from uuid import UUID
from datetime import date

class  RegisterRequest(BaseModel):
    email_id : str
    password: str
    phone_number: str
    dep_id : UUID
    role : str

class LoginRequest(BaseModel):
    email_id : str
    password : str

class RefreshToken(BaseModel):
    refresh_token:str

class ApplyLeave(BaseModel):
    leave_type : str
    leave_reason : str
    start_date : date
    end_date : date

