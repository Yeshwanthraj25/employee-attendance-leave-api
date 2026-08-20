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

router = APIRouter(prefix ="/attendance",tags=["Attendance"])


@router.post("/check-in")
async def check_in_route(db = Depends(get_db),current_user=Depends(get_current_user)):
    try:
        check_in = await check_in_service(db,current_user.emp_id)
        api_response = API_response(check_in,200,"Succesful check in","success")
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
                api_response = API_response({}, 500, str(e), status="error")
                return JSONResponse(status_code=500, content=api_response.model_dump(mode='json')) 


@router.patch("/check-out")
async def check_out_route(db = Depends(get_db),current_user=Depends(get_current_user)):
    try:
        check_out = await check_out_service(db,current_user.emp_id)
        api_response = API_response(check_out,200,"Succesful check  out","success")
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
                api_response = API_response({}, 500, str(e), status="error")
                return JSONResponse(status_code=500, content=api_response.model_dump(mode='json')) 


@router.get("/me")
async def get_attendance(db = Depends(get_db),start_date : date = None,end_date: date = None,current_user=Depends(get_current_user)):
    try:
        get_history = await get_attendance_history_service(db,current_user.emp_id,start_date,end_date)
        api_response = API_response(get_history,200,"Retrieve the attendance history","success")
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
                                  
            api_response = API_response({}, 500, str(e), status="error")
            return JSONResponse(status_code=500, content=api_response.model_dump(mode='json')) 


@router.get("/team")
async def team_attendance(db = Depends(get_db),start_date : date = None,end_date: date = None,current_user=Depends(get_current_user)):
    try:
        get_team_history = await get_team_attendance_service(db,current_user.emp_id,current_user.role, start_date,end_date)
        api_response = API_response(get_team_history,200,"Succesful retrieve the team attendance history","success")
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
                api_response = API_response({}, 500, str(e), status="error")
                return JSONResponse(status_code=500, content=api_response.model_dump(mode='json'))                
        