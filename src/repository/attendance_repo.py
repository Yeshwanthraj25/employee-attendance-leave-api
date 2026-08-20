from sqlalchemy import select,update,func
from src.repository.schema.schema import Employee,LogAttendance,Department,LeaveManagement,LeaveQuote,ErrorLog
from src.models.dto.exception  import AppException
from datetime import datetime,date


async def create_check_in(db,emp_id):
    try:
        check_in =  LogAttendance(emp_id = emp_id,log_in_time = datetime.now(),log_out_time = None , status = 'present' )
        db.add(check_in)
        await db.flush()
        await db.commit()
        return check_in 
    except  Exception as e :
        raise AppException("attendance_repo","create_check_in",500,"Failed to check in user",str(e))
    
async def get_today_log(db,emp_id):
        try:
            log_data = select(LogAttendance).where((LogAttendance.emp_id == emp_id) & (func.date(LogAttendance.log_in_time )== date.today()))
            result = await db.execute(log_data)
            today_log = result.scalars().first()
            if today_log  is not None:
                 return today_log
        except  Exception as e :
                raise AppException("attendance_repo","get_today_in",500,"Failed to Today log",str(e))

async def get_attendance_history_repo(db,emp_id,start_date,end_date):
    try:
            query = select(LogAttendance).where((LogAttendance.emp_id == emp_id) & (func.date(LogAttendance.log_in_time).between(start_date,end_date)))
            result = await db.execute(query)
            history = result.scalars().all()
            return history
    except Exception as e :
                         raise AppException("attendance_repo","get_attendance_history",500,"Failed to get the attendance history",str(e)

                         )
         
         

async def get_team_attendance_repo(db,manager_id,start_date,end_date):
        try:
            log_data = select(LogAttendance,Employee.email_id).join(Employee).where((Employee.manager_id == manager_id) & (func.date(LogAttendance.log_in_time).between(start_date,end_date)))
            result = await db.execute(log_data)
            today_log = result.all()
            return today_log
             
        except  Exception as e :
                raise AppException("attendance_repo","get_team_attandance",500,"Failed to retreive team attendance",str(e))

async def update_attendance_log(db,log_id):
    try:
           
            query = update(LogAttendance).where(LogAttendance.log_id == log_id).values(log_out_time=datetime.now(),status ='present')
            await db.execute(query)
            await db.commit()
        
            fetched = select(LogAttendance).where(LogAttendance.log_id == log_id)
            fetch_result = await db.execute(fetched)
            fetched_history = fetch_result.scalars().first()
           
            return fetched_history

    except Exception as e :
                         print(f"DEBUG - Exception: {type(e).__name__} - {str(e)}")
                         raise AppException("attendance_repo","get_attendance_history",500,"Failed to get the attendance history",str(e)

                         )

