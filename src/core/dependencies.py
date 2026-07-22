from src.core.security import verify_token
from jose import JWTError,jwt
from fastapi import HTTPException,status,Depends
from pydantic import BaseModel
from src.repository.auth_repo import get_user

from fastapi.security import OAuth2PasswordBearer
from src.repository.Database import get_db

oauth_schema = OAuth2PasswordBearer(tokenUrl= "token")



async def get_current_user(token:str = Depends(oauth_schema),db = Depends(get_db)):
    try:
        decode = verify_token(token)
        employee_id = decode["sub"]
        role = decode["role"]
        result = await  get_user(db,employee_id)
        return result 
    except JWTError:
         raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")
    
def required_role(require_role:str):
        async def role_checker(current_user = Depends(get_current_user)):
            if current_user["role"] != require_role:
                raise HTTPException(status_code= 403,detail = "Acess denied")
            return current_user
        return role_checker
  





         
         


