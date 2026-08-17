from src.models.output_model import APIResponse
from src.service.attendance_service import check_in_service,check_out_service,get_team_attendance_service,get_attendance_history_service
from fastapi import Depends,APIRouter
from fastapi.responses import JSONResponse
from  src.repository.Database import get_db
from src.models.dto.exception import AppException
from src.repository.error_repo import error_insert
from src.core.dependencies import get_current_user
from  src.utilize.response_helper import API_response
from src.models.error_model import ErrorCreation
from uuid import uuid4
from datetime import datetime,date

router = APIRouter(prefix ="/attendance",tags=["Auth"])


@router.post("/attendance/check_in")
async def check_in_route(db = Depends(get_db)):
    try:
        current_user = get_current_user()
        check_in = await check_in_service(db,current_user.emp_id)
        response_dict  = check_in.model_dump(mode='json')
        api_response = API_response(response_dict,200,"Succesful check in","success")
        return  JSONResponse(status_code =200,content = api_response.model_dump(mode='json'))
    except Exception as e :
        if isinstance(e,AppException):
            error_schema = ErrorCreation(
                                          log_id = uuid4(),
                                         file_name="attendance.py",
                                         function_name="check_in_route",
                                         status_code=e.status_code,
                                         log_data= str(e.log_data) if e.log_data else "No additional log data",
                                         error_details=e.error_details,
                                         created_at = datetime.now(),
                                         updated_at = datetime.now() )
                                   
            await error_insert(db, error_schema)
            api_response =  API_response(
                                                                    data={},
                                                                    status_code=e.status_code,
                                                                    message=e.error_details,
                                                                    status="error",
                                                                    errors=[{"error": str(e)}]  
                                                                        )
            return JSONResponse(status_code = e.status_code,content = api_response.model_dump(mode ='json'))
            
        else :
                                  
            raise


@router.patch("/attendance/check_out")
async def check_out_route(db = Depends(get_db)):
    try:
        current_user = get_current_user()
        check_out = await check_out_service(db,current_user.emp_id)
        response_dict  = check_out.model_dump(mode='json')
        api_response = API_response(response_dict,200,"Succesful check in","success")
        return  JSONResponse(status_code =200,content = api_response.model_dump(mode='json'))
    except Exception as e :
        if isinstance(e,AppException):
            error_schema = ErrorCreation(
                                          log_id = uuid4(),
                                         file_name="attendance.py",
                                         function_name="check_out_route",
                                         status_code=e.status_code,
                                         log_data= str(e.log_data) if e.log_data else "No additional log data",
                                         error_details=e.error_details,
                                         created_at = datetime.now(),
                                         updated_at = datetime.now() )
                                   
            await error_insert(db, error_schema)
            api_response =  API_response(
                                                                    data={},
                                                                    status_code=e.status_code,
                                                                    message=e.error_details,
                                                                    status="error",
                                                                    errors=[{"error": str(e)}]  
                                                                        )
            return JSONResponse(status_code = e.status_code,content = api_response.model_dump(mode ='json'))
            
        else :
                                  
            raise


@router.get("/attendance/me")
async def get_attendance(db = Depends(get_db),start_date : date = None,end_date: date = None):
    try:
        current_user = get_current_user()
        get_history = await get_attendance_history_service(db,current_user.emp_id,start_date,end_date)
        response_dict  = get_history.model_dump(mode='json')
        api_response = API_response(response_dict,200,"Succesful check in","success")
        return  JSONResponse(status_code =200,content = api_response.model_dump(mode='json'))
    except Exception as e :
        if isinstance(e,AppException):
            error_schema = ErrorCreation(
                                          log_id = uuid4(),
                                         file_name="attendance.py",
                                         function_name="check_route",
                                         status_code=e.status_code,
                                         log_data= str(e.log_data) if e.log_data else "No additional log data",
                                         error_details=e.error_details,
                                         created_at = datetime.now(),
                                         updated_at = datetime.now() )
                                   
            await error_insert(db, error_schema)
            api_response =  API_response(
                                                                    data={},
                                                                    status_code=e.status_code,
                                                                    message=e.error_details,
                                                                    status="error",
                                                                    errors=[{"error": str(e)}]  
                                                                        )
            return JSONResponse(status_code = e.status_code,content = api_response.model_dump(mode ='json'))
            
        else :
                                  
            raise


@router.get("/attendance/team")
async def team_attendance(db = Depends(get_db),start_date : date = None,end_date: date = None):
    try:
        current_user = get_current_user()
        get_team_history = await get_team_attendance_service(db,current_user.emp_id,start_date,end_date)
        response_dict  = get_team_history.model_dump(mode='json')
        api_response = API_response(response_dict,200,"Succesful check in","success")
        return  JSONResponse(status_code =200,content = api_response.model_dump(mode='json'))
    except Exception as e :
        if isinstance(e,AppException):
            error_schema = ErrorCreation(
                                          log_id = uuid4(),
                                         file_name="attendance.py",
                                         function_name="check_route",
                                         status_code=e.status_code,
                                         log_data= str(e.log_data) if e.log_data else "No additional log data",
                                         error_details=e.error_details,
                                         created_at = datetime.now(),
                                         updated_at = datetime.now() )
                                   
            await error_insert(db, error_schema)
            api_response =  API_response(
                                                                    data={},
                                                                    status_code=e.status_code,
                                                                    message=e.error_details,
                                                                    status="error",
                                                                    errors=[{"error": str(e)}]  
                                                                        )
            return JSONResponse(status_code = e.status_code,content = api_response.model_dump(mode ='json'))
            
        else :
                                  
            raise