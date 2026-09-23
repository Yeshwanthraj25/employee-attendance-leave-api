from src.service.attendance_service import attendance_service
from fastapi import Depends,APIRouter
from fastapi.responses import JSONResponse
from  src.repository.Database import get_db
from src.core.dependencies import OAuth
from  src.utilize.response_helper import API_response
from src.core.error_handler import handle_errors
from datetime import date

router = APIRouter(prefix ="/attendance",tags=["Attendance"])

oauth = OAuth()
@router.post("/check-in")
@handle_errors
async def check_in_route(db = Depends(get_db),current_user=Depends(oauth.get_current_user)):
        check_in = await attendance_service.check_in_service(db,current_user.emp_id)
        print(f" got the output {check_in}")
        response_dict = check_in.model_dump(mode='json')
        api_response = API_response(response_dict,200,"Succesful check in","success")
        return  JSONResponse(status_code =200,content = api_response.model_dump(mode='json'))

@router.patch("/check-out")
@handle_errors
async def check_out_route(db = Depends(get_db),current_user=Depends(oauth.get_current_user)):
        check_out = await attendance_service.check_out_service(db,current_user.emp_id)
        response_dict = check_out.model_dump(mode='json')
        api_response = API_response(response_dict,200,"Succesful check  out","success")
        return  JSONResponse(status_code =200,content = api_response.model_dump(mode='json'))
  
@router.get("/me")
@handle_errors
async def get_attendance(db = Depends(get_db),start_date : date = None,end_date: date = None,current_user=Depends(oauth.get_current_user)):
        get_history = await attendance_service.get_attendance_history_service(db,current_user.emp_id,start_date,end_date)
        api_response = API_response(get_history,200,"Retrieve the attendance history","success")
        return  JSONResponse(status_code =200,content = api_response.model_dump(mode='json'))

 
@router.get("/team")
@handle_errors
async def team_attendance(db = Depends(get_db),start_date : date = None,end_date: date = None,current_user=Depends(oauth.get_current_user)):
        get_team_history = await attendance_service.get_team_attendance_service(db,current_user.emp_id,current_user.role, start_date,end_date)
        api_response = API_response(get_team_history,200,"Succesful retrieve the team attendance history","success")
        return  JSONResponse(status_code =200,content = api_response.model_dump(mode='json'))