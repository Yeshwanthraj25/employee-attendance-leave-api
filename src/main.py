from  src.routes.auth import router as auth_router
from fastapi import FastAPI
import uvicorn

app = FastAPI()

app.include_router(auth_router)

@app.get("/health")
def health():
    return "API is Healthy"

if __name__ == "__main__":
    uvicorn.run("src.main:app",host ="0.0.0.0",port =8000,reload = True)
