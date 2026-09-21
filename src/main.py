from  src.routes.auth import router as auth_router
from src.routes.attendance import router as attendance_router
from src.routes.leave import app as leave_router
from fastapi import FastAPI
import uvicorn
from src.core.ai_model import ai_model
from src.routes.ai_route import router as ai_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(attendance_router)
app.include_router(leave_router)
app.include_router(ai_router)

@app.get("/health")
def health():
    return "API is Healthy"

if __name__ == "__main__":
    uvicorn.run("src.main:app",host ="0.0.0.0",port =8000,reload = True)


@app.on_event("startup")
async def load_ai_model():
    """Load AI model when app starts"""
    try:
        ai_model.load()
        print("✅ AI Model startup completed")
    except Exception as e:
        print(f"❌ Error loading AI model: {e}")
