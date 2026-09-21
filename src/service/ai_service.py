from src.core.ai_model import ai_model
from src.repository.leave_repo import LeaveRepository
from src.repository.attendance_repo import AttendanceRepository

class AIService:
    
    def __init__(self):
        self.leave_repo = LeaveRepository()
        self.attendance_repo = AttendanceRepository()
    
    def invoke_model(self, prompt: str, max_tokens: int = 150) -> str:
        """Invoke AI model with prompt
        
        Args:
            prompt: Full prompt (system + user)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated response from model
        """
        try:
            response = ai_model.generate(prompt, max_tokens)
            return response
        except Exception as e:
            raise Exception(f"Error invoking model: {str(e)}")
    
    async def generate_leave_insights(self, emp_id: str) -> str:
        """Generate insights using REAL employee leave data"""
        try:
            # Fetch employee's actual leave data from DB
            leaves = await self.leave_repo.get_employee_leaves(emp_id)
            
            if not leaves:
                return "No leave data found for this employee"
            
            # SYSTEM PROMPT with Role, Instructions, Constraints
            system_prompt = """You are an HR Analytics AI Assistant specialized in employee leave analysis.

ROLE: Analyze employee leave patterns and provide actionable insights.

CONSTRAINTS:
- Keep response concise (2-3 sentences)
- Focus on patterns and recommendations
- Be professional and objective
- Only use provided data

EXAMPLES:
Input: Employee took 5 sick leaves in Q2
Output: "Pattern detected: High sick leave usage in monsoon season. Recommendation: Schedule health check-ups."

Input: Employee took leaves on Mondays
Output: "Pattern: Extended weekends preferred. Recommendation: Monitor for potential scheduling issues."
"""
            
            # USER PROMPT with data
            user_prompt = f"""Analyze this employee's leave data:
Employee ID: {emp_id}
Total Leaves Taken: {len(leaves)}
Leave Details: {leaves}

Provide 2-3 key insights about their leave patterns and recommendations."""
            
            # Combine prompts
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            # Invoke model using invoke_model()
            insights = self.invoke_model(full_prompt, max_tokens=200)
            return insights
        
        except Exception as e:
            raise Exception(f"Error generating leave insights: {str(e)}")
    
    async def analyze_attendance(self, start_date: str, end_date: str) -> str:
        """Generate analysis using REAL attendance data"""
        try:
            # Fetch actual attendance data from DB
            attendance_data = await self.attendance_repo.get_attendance_range(
                start_date, 
                end_date
            )
            
            if not attendance_data:
                return "No attendance data found for this period"
            
            # SYSTEM PROMPT with Role, Instructions, Constraints
            system_prompt = """You are an HR Analytics AI Assistant specialized in team attendance analysis.

ROLE: Analyze team attendance patterns and provide management insights.

INSTRUCTIONS:
1. Calculate overall attendance percentage
2. Identify attendance patterns or anomalies
3. Provide actionable recommendations

CONSTRAINTS:
- Keep response to 3-4 sentences
- Be data-driven and objective
- Focus on trends not individuals
- Provide specific recommendations

EXAMPLES:
Input: 90% attendance with Monday absences
Output: "Team attendance is strong at 90%. Pattern: Elevated absences on Mondays suggest potential scheduling conflicts. Recommendation: Review Monday schedules."

Input: 85% with increasing trend
Output: "Attendance improving month-over-month (85% current). Positive trend detected. Recommend continuing current initiatives."
"""
            
            # USER PROMPT with data
            user_prompt = f"""Analyze this team attendance data from {start_date} to {end_date}:
Total Records: {len(attendance_data)}
Data: {attendance_data}

Provide insights about overall attendance percentage, patterns, and recommendations."""
            
            # Combine prompts
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            # Invoke model using invoke_model()
            analysis = self.invoke_model(full_prompt, max_tokens=250)
            return analysis
        
        except Exception as e:
            raise Exception(f"Error analyzing attendance: {str(e)}")
    
    async def answer_query(self, question: str) -> str:
        """Answer natural language question"""
        try:
            # SYSTEM PROMPT with Role, Instructions, Constraints
            system_prompt = """You are an HR System Assistant for an Employee Attendance & Leave Management System.

ROLE: Answer questions about attendance, leave management, and employee policies.

INSTRUCTIONS:
1. Answer questions clearly and concisely
2. Use data when available
3. Provide helpful guidance

CONSTRAINTS:
- Keep responses to 2-3 sentences
- Be professional and helpful
- Only provide relevant information
- Acknowledge if data is not available

EXAMPLES:
Q: "How do I apply for leave?"
A: "To apply for leave, navigate to the Leave section, click 'Apply Leave', select dates, provide reason, and submit. Your manager will review and approve/reject within 2 business days."

Q: "What is my leave balance?"
A: "Please check the 'My Profile' section under 'Leave Balance' to view your current leave balance by type."
"""
            
            # USER PROMPT with question
            user_prompt = f"Q: {question}"
            
            # Combine prompts
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            # Invoke model using invoke_model()
            response = self.invoke_model(full_prompt, max_tokens=150)
            return response
        
        except Exception as e:
            raise Exception(f"Error answering query: {str(e)}")

# Create singleton instance
ai_service = AIService()