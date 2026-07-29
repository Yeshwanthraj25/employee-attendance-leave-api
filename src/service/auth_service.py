from src.repository.auth_repo import get_user_by_email,create_user
from models.dto.exception import AppException
from src.core.security import create_token,refresh_token,verify_token
from src.repository.auth_repo import get_user
from passlib.context import CryptContext
from jose import JWTError
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")


async  def register_service(db,email_id,password,phone_number,dep_id,role):
    try:
        user_checked = await get_user_by_email(db,email_id)
        if user_checked is not None:
            raise AppException("auth_service","register_user",409,"User already exist",None)
        password = pwd_context.hash(password)
        registered = await create_user(db,email_id,password,phone_number,dep_id,role)
        return registered
    except Exception as e :
        raise AppException("auth_service","register_user",500,"InternalError",str(e))

async def login_service(db,email_id,password):
    user_checked = await get_user_by_email(db,email_id)
    if user_checked is None:
            raise AppException("auth_service","login_user",401,"Invalid creditial",None)
    if not pwd_context.verify(password,user_checked.password):
         raise AppException("auth_service","login_user",401,"Invalid Password",None)
    emp_id = user_checked.emp_id
    role = user_checked.role
    get_acess =  create_token(emp_id,role)
    get_refresh = refresh_token(emp_id,role)
    return get_acess,get_refresh,user_checked

async def refresh_token_service(db,token):
    try:
        verify = verify_token(token)
        emp_id = verify["sub"]
        role = await get_user(db,emp_id)
        role = role.role
        new_acesss = create_token(emp_id,role)
        return new_acesss
    except JWTError :
         raise AppException("auth_service","refresh_token_service",500,"JWTError",None)



    

