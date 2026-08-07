from src.repository.auth_repo import get_user_by_email,create_user
from src.models.dto.exception import AppException
from src.core.security import create_token,refresh_token,verify_token
from src.repository.auth_repo import get_user
import bcrypt
from jose import JWTError
from src.models.output_model import RegisterResponse,LoginResponse,RefreshToken



async  def register_service(db,email_id,password,phone_number,dep_id,role):
    try:
        user_checked = await get_user_by_email(db,email_id)
        if user_checked is not None:
              raise AppException("auth_service","register_user",409,"User already exist",None)
        gen_pass = bcrypt.gensalt(rounds=12)
        password = bcrypt.hashpw(password.encode(),gen_pass).decode()
        
        registered = await create_user(db,email_id,password,phone_number,dep_id,role)
        return RegisterResponse(emp_id=str(registered.emp_id),
                    email_id=registered.email_id,
                    phone_number=registered.phone_number,
                    role=registered.role,
                    dep_id=str(registered.dep_id))
    except AppException:
        raise 
    except Exception as e :
        raise AppException("auth_service","register_user",500,"InternalError",str(e))

async def login_service(db,email_id,password):
    try:
        user_checked = await get_user_by_email(db,email_id)
        if user_checked is None:
                raise AppException("auth_service","login_user",401,"Invalid creditial",None)
        if not bcrypt.checkpw(password.encode(),user_checked.password.encode()):
            raise AppException("auth_service","login_user",401,"Invalid Password",None)
        emp_id = user_checked.emp_id
        role = user_checked.role
        get_access =  create_token(emp_id,role)
        get_refresh = refresh_token(emp_id)
        return  LoginResponse(access_token = get_access,refresh_token = get_refresh,user_id = str(emp_id) , role = role)
    except AppException:
            raise 
    except Exception as e :
            raise AppException("auth_service","login_user",500,"InternalError",str(e))

async def refresh_token_service(db,token):
    try:
        verify = verify_token(token)
        emp_id = verify["sub"]
        role = await get_user(db,emp_id)
        role = role.role
        new_acess = create_token(emp_id,role)
        return  RefreshToken(refresh_token = new_acess)
    except JWTError :
         raise AppException("auth_service","refresh_token_service",500,"JWTError",None)



    

