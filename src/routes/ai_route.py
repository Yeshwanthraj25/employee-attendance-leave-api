from fastapi import APIRouter, Depends
from src.core.dependencies import get_current_user
from src.service.ai_service import ai_service
from src.utilize.response_helper import API_response
from fastapi.responses import JSONResponse
from src.core.error_handler import handle_errors

router = APIRouter(prefix="/api/ai", tags=["AI"])

@router.post("/query")
@handle_errors
async def query(question: str, current_user=Depends(get_current_user)):
    """Answer natural language question using AI"""
    # Call service method
    answer = await ai_service.answer_query(question)
    
    api_response = API_response(
        {"answer": answer},
        200,
        "Query answered successfully",
        "success"
    )
    return JSONResponse(status_code=200, content=api_response.model_dump(mode='json'))

@router.post("/leave-insights")
@handle_errors
async def leave_insights(emp_id: str, current_user=Depends(get_current_user)):
    """Generate AI insights about employee's leaves"""
    # Call service method
    insights = await ai_service.generate_leave_insights(emp_id)
    
    api_response = API_response(
        {"insights": insights},
        200,
        "Leave insights generated successfully",
        "success"
    )
    return JSONResponse(status_code=200, content=api_response.model_dump(mode='json'))

@router.post("/attendance-analysis")
@handle_errors
async def attendance_analysis(
    start_date: str,
    end_date: str,
    current_user=Depends(get_current_user)
):
    """Analyze team attendance using AI"""
    
    # Check role - only managers and admins
    if current_user.role not in ['manager', 'admin']:
        api_response = API_response(
            {},
            403,
            "Only managers and admins can access this endpoint",
            "error"
        )
        return JSONResponse(status_code=403, content=api_response.model_dump(mode='json'))
    
    # Call service method
    analysis = await ai_service.analyze_attendance(start_date, end_date)
    
    api_response = API_response(
        {"analysis": analysis},
        200,
        "Attendance analysis generated successfully",
        "success"
    )
    return JSONResponse(status_code=200, content=api_response.model_dump(mode='json'))