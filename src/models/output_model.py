from pydantic import BaseModel
from datetime import datetime

class APIResponse(BaseModel):
    status: str
    code : int 
    message : str
    data : dict | list | None = {}
    error : list = []
    timestamps : datetime
    request_id : str

