from datetime import datetime
from uuid import uuid4
from src.models.output_model import APIResponse


def API_response(data,status_code=200,message="",status="success",errors = None):
    return APIResponse(status = status,code = status_code,message=message,data =data,errors =[],timestamp =datetime.now(),request_id= str(uuid4()))