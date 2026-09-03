from functools import wraps
from fastapi.responses import JSONResponse
from src.models.dto.exception import AppException
from src.repository.error_repo import error_insert
from src.models.error_model import ErrorCreation
from src.utilize.response_helper import API_response
from uuid import uuid4
from datetime import datetime


def handle_errors(func):
    """Decorator to handle errors consistently across all routes"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            db = kwargs.get('db')
            
            if isinstance(e, AppException):
                if db:
                    error_schema = ErrorCreation(
                        log_id=uuid4(),
                        file_name=func.__module__.split('.')[-1],
                        function_name=func.__name__,
                        status_code=e.status_code,
                        log_data=str(e.log_data) if e.log_data else "No additional log data",
                        error_details=e.error_details,
                        created_at=datetime.now(),
                        updated_at=datetime.now()
                    )
                    await error_insert(db, error_schema)
                
                api_response = API_response(
                    {},
                    e.status_code,
                    e.error_details,
                    status="error"
                )
                return JSONResponse(status_code=e.status_code, content=api_response.model_dump(mode='json'))
            
            else:
                api_response = API_response(
                    {},
                    500,
                    str(e),
                    status="error"
                )
                return JSONResponse(status_code=500, content=api_response.model_dump(mode='json'))
    
    return wrapper