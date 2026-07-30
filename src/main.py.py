from  src.routes.auth import app as auth_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(auth_router)