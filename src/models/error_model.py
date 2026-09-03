from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from pydantic import ConfigDict


class ErrorCreation(BaseModel):
    log_id: UUID  
    file_name: str
    function_name: str
    status_code: int 
    log_data : str = "no log data" 
    error_details: str
    created_at : datetime
    updated_at : datetime

    model_config = ConfigDict(from_attributes=True)

class ErrorResponse(BaseModel):
    log_id: UUID
    file_name: str
    function_name: str
    status_code: int
    log_data : str
    error_details: str
    created_at : datetime
    updated_at : datetime

    model_config = ConfigDict(from_attributes=True)
