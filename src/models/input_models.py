from pydantic import BaseModel

class  RegisterRequest(BaseModel):
    email_id : str
    password: str
    phone_number: str
    dep_id : int
    role : str

class LoginRequest(BaseModel):
    email_id : str
    password : str

class RefreshToken(BaseModel):
    refresh_token:str


