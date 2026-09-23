import json
from src.core.ai_model import ai_model
from src.repository.leave_repo import LeaveRepo
from src.repository.attendance_repo import AttendanceRepo
from src.models.dto.exception import AppException
from typing import List, Dict, Any
from src.models.output_model import AIResponse,LeaveInsightResponse,AttendanceAnalysisResponse



class AIService:
    
    def __init__(self):
        self.leave_repo = LeaveRepo()
        self.attendance_repo = AttendanceRepo()
    
    def invoke_model(self, prompt: str, max_tokens: int = 150) -> str:
        """Invoke AI model with prompt"""
        try:
            response = ai_model.generate(prompt, max_tokens)
            return response
        except Exception as e:
            raise AppException(
                "ai_service",
                "invoke_model",
                500,
                f"Error invoking model: {str(e)}",
                None
            )
    
    async def generate_leave_insights(self, db, emp_id: str) -> Dict[str, Any]:
        try:
            leaves = await self.leave_repo.get_leave_history(db, emp_id)
            
            if not leaves:
                raise AppException(
                    "ai_service",
                    "generate_leave_insights",
                    404,
                    "No leave data found for this employee",
                    None
                )
            
            # Analyze leave data
            total_leaves = len(leaves)
            leave_types = {}
            leave_reasons = {}
            approved_count = 0
            pending_count = 0
            rejected_count = 0
            
            for leave in leaves:
                # Count by type
                leave_type = leave.leave_type if hasattr(leave, 'leave_type') else 'Unknown'
                leave_types[leave_type] = leave_types.get(leave_type, 0) + 1
                
                # Count by reason
                reason = leave.leave_reason if hasattr(leave, 'leave_reason') else 'No reason'
                leave_reasons[reason] = leave_reasons.get(reason, 0) + 1
                
                # Count by status - CASE INSENSITIVE
                if hasattr(leave, 'status'):
                    status = str(leave.status).lower().strip()  # Convert to lowercase
                    
                    if status == 'approved':
                        approved_count += 1
                    elif status == 'pending':
                        pending_count += 1
                    elif status == 'rejected':
                        rejected_count += 1
                else:
                    pending_count += 1  # Default to pending
            
            # SYSTEM PROMPT with OUTPUT STRUCTURE
            system_prompt = """You are an HR Analytics AI Assistant specialized in employee leave analysis.

ROLE: Provide detailed insights about employee leave patterns, health, and work-life balance.

INSTRUCTIONS:
1. Analyze total leaves and breakdown by type
2. Identify reasons for leaves
3. Detect patterns (health issues, burnout, work-life balance)
4. Provide specific recommendations

OUTPUT FORMAT (MUST FOLLOW EXACTLY - Valid JSON):
{
  "summary": "1-2 sentence overview of leave pattern",
  "health_analysis": "Analysis of health-related leaves if any",
  "work_life_balance": "Assessment of work-life balance based on leaves",
  "patterns": [
    "Pattern 1 identified",
    "Pattern 2 identified"
  ],
  "recommendations": [
    "Recommendation 1",
    "Recommendation 2"
  ]
}

CONSTRAINTS:
- Return ONLY valid JSON, nothing else
- Be data-driven and objective
- Keep each field concise but informative
- Be professional and supportive"""
        
            # USER PROMPT with detailed analysis
            user_prompt = f"""Analyze this employee's complete leave history:

EMPLOYEE ID: {emp_id}
TOTAL LEAVES TAKEN: {total_leaves}

BREAKDOWN BY TYPE:
{chr(10).join([f"  - {k}: {v} leaves" for k, v in leave_types.items()])}

BREAKDOWN BY REASON:
{chr(10).join([f"  - {k}: {v} times" for k, v in leave_reasons.items()])}

STATUS SUMMARY:
  - Approved: {approved_count}
  - Pending: {pending_count}
  - Rejected: {rejected_count}

LEAVE DETAILS:
{chr(10).join([f"  - {l.start_date} to {l.end_date}: {l.leave_type} ({l.status}) - Reason: {l.leave_reason}" for l in leaves[:10]])}

{"... and more" if len(leaves) > 10 else ""}

Provide detailed insights using the JSON format specified."""
        
            # Combine prompts
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            # Invoke model
            ai_response_text = self.invoke_model(full_prompt, max_tokens=500)
            

            try:
                ai_insights = json.loads(ai_response_text)
            except json.JSONDecodeError:
                # If parsing fails, wrap in default structure
                ai_insights = {
                    "summary": ai_response_text,
                    "health_analysis": "Unable to parse detailed analysis",
                    "work_life_balance": "See summary",
                    "patterns": [],
                    "recommendations": []
                }
            
            # Return structured response
            return {
                "employee_id": emp_id,
                "total_leaves": total_leaves,
                "breakdown_by_type": leave_types,
                "breakdown_by_reason": leave_reasons,
                "status_summary": {
                    "approved": approved_count,
                    "pending": pending_count,
                    "rejected": rejected_count
                },
                "ai_insights": ai_insights  
            }
        
        except AppException:
            raise
        except Exception as e:
            raise AppException(
                "ai_service",
                "generate_leave_insights",
                500,
                f"Error: {str(e)}",
                None
            )
    
    async def analyze_attendance(self, db, start_date: str, end_date: str) -> Dict[str, Any]:
        """Generate analysis using REAL attendance data"""
        try:
            # Fetch actual attendance data from DB
            attendance_data = await self.attendance_repo.get_attendance_range(
                db,
                start_date, 
                end_date
            )
            
            if not attendance_data:
                raise AppException(
                    "ai_service",
                    "analyze_attendance",
                    404,
                    "No attendance data found for this period",
                    None
                )
            
            # Calculate statistics
            total_records = len(attendance_data)
            present_count = sum(1 for record in attendance_data if hasattr(record, 'log_out_time') and record.log_out_time)
            absent_count = total_records - present_count
            attendance_percentage = (present_count / total_records * 100) if total_records > 0 else 0
            
            # SYSTEM PROMPT with OUTPUT STRUCTURE
            system_prompt = """You are an HR Analytics AI Assistant specialized in team attendance analysis.

ROLE: Analyze team attendance patterns and provide management insights.

INSTRUCTIONS:
1. Analyze attendance percentage and trends
2. Identify patterns or anomalies
3. Assess team productivity signals
4. Provide actionable recommendations

OUTPUT FORMAT (MUST FOLLOW EXACTLY - Valid JSON):
{
  "overview": "1-2 sentence overview of attendance",
  "trends": "Description of attendance trends observed",
  "patterns": [
    "Pattern 1",
    "Pattern 2"
  ],
  "concerns": [
    "Concern 1 if any",
    "Concern 2 if any"
  ],
  "recommendations": [
    "Recommendation 1",
    "Recommendation 2"
  ]
}

CONSTRAINTS:
- Return ONLY valid JSON, nothing else
- Be data-driven
- Focus on team level, not individuals
- Be constructive"""
        
            # USER PROMPT with data
            user_prompt = f"""Analyze this team attendance data from {start_date} to {end_date}:

TOTAL RECORDS: {total_records}
PRESENT: {present_count}
ABSENT: {absent_count}
ATTENDANCE PERCENTAGE: {attendance_percentage:.2f}%

TOP EMPLOYEES BY ATTENDANCE:
{chr(10).join([f"  - Employee: {str(record.emp_id if hasattr(record, 'emp_id') else 'Unknown')[:8]}... - Present" for record in attendance_data[:5]])}

Provide analysis using the JSON format specified."""
        
            # Combine prompts
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            # Invoke model
            ai_response_text = self.invoke_model(full_prompt, max_tokens=500)
            
            # Parse AI response as JSON
            try:
                ai_insights = json.loads(ai_response_text)
            except json.JSONDecodeError:
                # If parsing fails, wrap in default structure
                ai_insights = {
                    "overview": ai_response_text,
                    "trends": "See overview",
                    "patterns": [],
                    "concerns": [],
                    "recommendations": []
                }
            
            # Return structured response
            return {
                "period": f"{start_date} to {end_date}",
                "total_records": total_records,
                "present": present_count,
                "absent": absent_count,
                "attendance_percentage": round(attendance_percentage, 2),
                "ai_insights": ai_insights  # ← Returns as parsed JSON object
            }
        
        except AppException:
            raise
        except Exception as e:
            raise AppException(
                "ai_service",
                "analyze_attendance",
                500,
                f"Error: {str(e)}",
                None
            )
    
    async def answer_query(self, question: str) -> AIResponse:
        """Answer natural language question"""
        try:
            if not question:
                raise AppException(
                    "ai_service",
                    "answer_query",
                    400,
                    "Question cannot be empty",
                    None
                )
            
            # SYSTEM PROMPT
            system_prompt = """You are an HR System Assistant for an Employee Attendance & Leave Management System.

ROLE: Answer questions about attendance, leave management, and employee policies.

INSTRUCTIONS:
1. Answer questions clearly and concisely
2. Use relevant information
3. Provide helpful guidance

CONSTRAINTS:
- Keep responses to 3-4 sentences
- Be professional and helpful
- Only provide relevant information
- If you don't know, say so

EXAMPLES:
Q: "How do I apply for leave?"
A: "To apply for leave, log into the system, go to Leave section, click 'Apply Leave', 
select your dates, provide reason, and submit. Your manager will review and respond within 2 business days."

Q: "What is my leave balance?"
A: "Your leave balance is visible in the 'My Profile' section under 'Leave Balance'. 
It shows breakdown by leave type (Annual, Sick, Casual)."""
        
            # USER PROMPT
            user_prompt = f"Q: {question}"
            
            # Combine prompts
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            # Invoke model
            response = self.invoke_model(full_prompt, max_tokens=200)
            
            return AIResponse(response=response)
        
        except AppException:
            raise
        except Exception as e:
            raise AppException(
                "ai_service",
                "answer_query",
                500,
                f"Error: {str(e)}",
                None
            )

# Create singleton instance
ai_service = AIService()