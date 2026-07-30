from src.models.input_models import RegisterRequest,LoginRequest,RefreshToken
from src.models.output_model import APIResponse
from src.service.auth_service import register_service,login_service,refresh_token_service
from fastapi import Depends,APIRouter
from  src.repository.Database import get_db
from src.models.dto.exception import AppException
from src.repository.auth_repo import get_user
from src.core.dependencies import get_current_user
from  src.utilize.response_helper import API_response

app = APIRouter(prefix ="/auth",tags=["Auth"])


@app.post("/register",response_model =  APIResponse )
async def register(request:RegisterRequest,db = Depends(get_db)) :
    register_user = await register_service(db,request.email_id,request.password,request.phone_number,request.dep_id,request.role)
    return API_response(register_user,201,"User sucessfully created")
    
@app.post("/login",response_model = APIResponse )
async def login(request: LoginRequest,db = Depends(get_db)) :
        login_user = await login_service(db,request.email_id,request.password)
        return API_response(login_user,200,"Sucessfully Login")



@app.post("/refresh",response_model =  APIResponse)
async def refresh_token(request:RefreshToken ,db = Depends(get_db)) :

        token_refresh = await refresh_token_service(db,request.refresh_token)
        return API_response(token_refresh,200,"Refresh token")

@app.get("/me")
async def auth(current_user = Depends(get_current_user)):
    return API_response(current_user,200,"API is healthy")
