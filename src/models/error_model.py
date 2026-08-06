from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class ErrorCreation(BaseModel):
    log_id: UUID  
    file_name: str
    function_name: str
    status_code: int 
    log_data : str = "no log data" 
    error_details: str
    created_at : datetime
    updated_at : datetime

class ErrorResponse(BaseModel):
    log_id: UUID
    file_name: str
    function_name: str
    status_code: int
    log_data : str
    error_details: str
    created_at : datetime
    updated_at : datetime

    class Config:
        from_attributes = True
