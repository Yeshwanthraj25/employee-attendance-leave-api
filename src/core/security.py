from datetime import datetime,timedelta
from jose import JWTError,jwt
from src.setting import Settings

setting = Settings()

# encode the jwt 

def create_token(data:dict,expire_data:timedelta = None):
    '''
    creat jwt token with optional expiry
    input : data (payload to encode eg:{"sub":emp_id,"role":"admin"})
    expire_delta: how long untill token expire 
    '''
    to_encode = data.copy()

    if expire_data:
        expire = datetime.now() + expire_data
    else:
        expire = datetime.now() + timedelta(minutes = 15)

    to_encode.update({"exp":expire})

    encode_jwt = jwt.encode(to_encode,setting.JWT_SECRET_KEY,algorithm = setting.JWT_ALGORITHM)

    return encode_jwt

# decode and verify the code 

def verify_token(token:str):
    try :
        decode = jwt.decode(token,setting.JWT_SECRET_KEY,algorithms=[setting.JWT_ALGORITHM])
        return decode 
    except  JWTError :
        raise 

# create a shoet span token 

def create_token(emp_id: str,role:str):
    data ={"sub":str(emp_id),"role":role}
    expire = datetime.now() + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp":expire})
    jwt_encode = jwt.encode(data,setting.JWT_SECRET_KEY,algorithm= setting.JWT_ALGORITHM)
    return jwt_encode

# create a refresh token (long span)

def refresh_token(emp_id: str):
    data ={"sub":str(emp_id),"type": "refresh"}
    expire = datetime.now() + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES) 
    data.update({"exp":expire})
    encode_jwt = jwt.encode(data,setting.JWT_SECRET_KEY,algorithm= setting.JWT_ALGORITHM)
    return encode_jwt




    




