from src.models.input_models import RegisterRequest,LoginRequest,RefreshToken
from src.models.output_model import APIResponse
from src.service.auth_service import register_service,login_service,refresh_token_service
from fastapi import Depends,APIRouter
from fastapi.responses import JSONResponse
from  src.repository.Database import get_db
from src.models.dto.exception import AppException
from src.repository.error_repo import error_insert
from src.core.dependencies import get_current_user
from  src.utilize.response_helper import API_response
from src.models.error_model import ErrorCreation
from uuid import uuid4
from datetime import datetime
from src.core.error_handler import handle_errors

router = APIRouter(prefix ="/auth",tags=["Auth"])


@router.post("/register" )
@handle_errors
async def register(request:RegisterRequest,db = Depends(get_db)) :
                register_user = await register_service(db,request.email_id,request.password,request.phone_number,request.dep_id,request.role)
                user_dict = register_user.model_dump(mode='json')
                api_response = API_response(user_dict,201,"User sucessfully created")
                return JSONResponse(status_code = 201,content = api_response.model_dump(mode ='json'))
               

    
@router.post("/login",response_model = APIResponse )
@handle_errors
async def login(request: LoginRequest,db = Depends(get_db)) :
                login_user = await login_service(db,request.email_id,request.password)
                login_dict = login_user.model_dump(mode='json')
                api_response =  API_response(login_dict,200,"Sucessfully Login")
                return JSONResponse(status_code = 200,content = api_response.model_dump(mode ='json') )
      

@router.post("/refresh",response_model =  APIResponse)
@handle_errors
async def refresh_token(request:RefreshToken ,db = Depends(get_db)) :
                token_refresh = await refresh_token_service(db,request.refresh_token)
                refresh_dict = token_refresh.model_dump(mode='json')
                return API_response(refresh_dict,200,"Refresh token")
        

@router.get("/me")
@handle_errors
async def auth(db = Depends(get_db),current_user = Depends(get_current_user)):
                user_dict = {
                                "emp_id": str(current_user.emp_id),
                                "email_id": current_user.email_id,
                                "phone_number": current_user.phone_number,
                                "role": current_user.role,
                                "dep_id": str(current_user.dep_id)
                        }
                response  =  API_response(user_dict,200,"API is healthy")
                return JSONResponse(status_code = 200 , content = response.model_dump(mode ='json'))
     