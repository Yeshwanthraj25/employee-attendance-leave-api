from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.dependencies import OAuth
from  src.repository.Database import get_db
from src.service.ai_service import ai_service
from src.utilize.response_helper import API_response
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api/ai", tags=["AI"])
oauth = OAuth()

@router.post("/query")
async def query(
    question: str,
    current_user=Depends(oauth.get_current_user)
):
    """Answer natural language question using AI"""
    result = await ai_service.answer_query(question)
    
    api_response = API_response(
        {"answer": result.response},
        200,
        "Query answered successfully",
        "success"
    )
    return JSONResponse(status_code=200, content=api_response.model_dump(mode='json'))

@router.post("/leave-insights")
async def leave_insights(
    emp_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(oauth.get_current_user)
):
    """Generate detailed AI insights about employee's leaves"""
    result = await ai_service.generate_leave_insights(db, emp_id)
    
    api_response = API_response(
        result,  # ← Returns structured dict
        200,
        "Leave insights generated successfully",
        "success"
    )
    return JSONResponse(status_code=200, content=api_response.model_dump(mode='json'))

@router.post("/attendance-analysis")
async def attendance_analysis(
    start_date: str,
    end_date: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(oauth.get_current_user)
):
    """Analyze team attendance using AI"""
    
    # Check role
    if current_user.role not in ['manager', 'admin']:
        api_response = API_response(
            {},
            403,
            "Only managers and admins can access this endpoint",
            "error"
        )
        return JSONResponse(status_code=403, content=api_response.model_dump(mode='json'))
    
    result = await ai_service.analyze_attendance(db, start_date, end_date)
    
    api_response = API_response(
        result,  # ← Returns structured dict
        200,
        "Attendance analysis generated successfully",
        "success"
    )
    return JSONResponse(status_code=200, content=api_response.model_dump(mode='json'))