from datetime import datetime
from uuid import uuid4
from src.models.output_model import APIResponse


async def API_response(data,status_code=200,message=""):
    return APIResponse(status = "sucess",code = status_code,message=message,data =data.error =[],timestamp =datetime.now(),request_id= str(uuid4()))