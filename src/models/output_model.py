from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID

# Define ALL models here, in order

class APIResponse(BaseModel):
    status: str
    code: int 
    message: str
    data: dict | list | None = {}
    errors: list = []
    timestamp: datetime
    request_id: str
    
    model_config = ConfigDict(from_attributes=True)


class RegisterResponse(BaseModel):
    emp_id: str
    email_id: str
    phone_number: str
    role: str
    dep_id: str
    
    model_config = ConfigDict(from_attributes=True)


class LoginResponse(BaseModel):
    access_token: str 
    refresh_token: str
    user_id: str
    role: str
    
    model_config = ConfigDict(from_attributes=True)


class RefreshToken(BaseModel):
    refresh_token: str


class CheckIn(BaseModel):
    log_id: str
    emp_id: str
    log_in_time: datetime
    
    
    model_config = ConfigDict(from_attributes=True)


class CheckOut(BaseModel):
    log_id: str
    emp_id: str
    log_in_time: datetime 
    log_out_time: Optional[datetime] = None
    status: str
    
    model_config = ConfigDict(from_attributes=True)


class AttendanceHistory(BaseModel):
    log_id: UUID
    emp_id: UUID
    log_in_time: datetime
    log_out_time: Optional[datetime] = None
    status: str
    
    model_config = ConfigDict(from_attributes=True)


class TeamHistory(BaseModel):
    email_id: UUID
    log_id: UUID
    emp_id: UUID                                        
    log_in_time: datetime
    log_out_time: Optional[datetime] = None
    status: str
    
    model_config = ConfigDict(from_attributes=True)

class ApplyLeave(BaseModel):
    leave_id :UUID
    emp_id :UUID 
    leave_type : str
    status : str
    start_date : datetime
    end_date : datetime

class ApplyApproved(BaseModel):
    leave_id :UUID
    emp_id :UUID 
    leave_type : str
    status : str
    start_date : datetime
    end_date : datetime

class ApplyRejected(BaseModel):
    leave_id :UUID
    emp_id :UUID 
    leave_type : str
    status : str
    start_date : datetime
    end_date : datetime

class LeaveHistory(BaseModel):
    leave_id :UUID
    emp_id :UUID 
    leave_type : str
    status : str
    start_date : datetime
    end_date : datetime
    leave_reason : str

class TeamLeaveHistory(BaseModel):
    leave_id :UUID
    emp_id :UUID 
    leave_type : str
    status : str
    start_date : datetime
    end_date : datetime
    leave_reason : str

class LeaveBalance(BaseModel):
    sick_leave_remaining: int
    casual_leave_remaining: int 
    year: datetime


CheckIn.model_rebuild()
CheckOut.model_rebuild()
AttendanceHistory.model_rebuild()
TeamHistory.model_rebuild()