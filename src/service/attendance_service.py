from src.repository.attendance_repo import get_today_log,create_check_in,update_attendance_log,get_attendance_history_repo,get_team_attendance_repo
from src.models.dto.exception import AppException
from  src.models.output_model import CheckIn,CheckOut,AttendanceHistory,TeamHistory

async def check_in_service(db,emp_id):
    try:
        log_check = await get_today_log(db,emp_id) 
        if log_check is not None:
            raise AppException("attendance_service","check_in_service",400,"Today attendance already exist",None)
        else :
            check_in = await  create_check_in(db,emp_id)  
            response = CheckIn(
                log_id= str(check_in.log_id),
                emp_id= str(check_in.emp_id),
                log_in_time=check_in.log_in_time
                )
            return response
    except AppException:
        raise
    except Exception as e :
        raise AppException("attendance_service","check_in_service",500,"Internal Error",str(e))

async def check_out_service(db,emp_id):
        try:
            today_log = await get_today_log(db,emp_id) 
            if today_log is  None:
                raise AppException("attendance_service","check_out_service",404,"No check in  found",None)
            elif today_log.log_out_time is not None:
                raise AppException("attendance_service","check_out_service",409,"user already check out",None)
            else :
                log_id = today_log.log_id
                updated = await  update_attendance_log(db,log_id)  
            response = CheckOut(
            log_id = str(updated.log_id),
            emp_id =  str(updated.emp_id),
            log_in_time = updated.log_in_time,
            log_out_time = updated.log_out_time,
            status = updated.status)
            return response
        
        except AppException:
            raise
        except Exception as e :
            raise AppException("attendance_service","check_out_service",500,"Internal Error",str(e))

async def get_attendance_history_service(db,emp_id,start_date,end_date):
        try:
            attendance_history = await  get_attendance_history_repo(db,emp_id,start_date,end_date)
            print(f'the result from {attendance_history}')
            return [ AttendanceHistory.model_validate(log) for log in attendance_history
        ]
        except AppException:
            raise
        except Exception as e :
            print(f'the error is str{e}')
            raise AppException("attendance_service","get_attendance_history_service",500,"Internal Error",str(e))


async def get_team_attendance_service(db, manager_id, role, start_date, end_date):
    try:
        if role not in ['manager', 'admin']:
            raise AppException("attendance_service", "get_team_attendance_service", 403, "Only managers can view team attendance", None)
        
        team_attendance = await get_team_attendance_repo(db, manager_id, start_date, end_date)
        
        return [
            TeamHistory.model_validate(log,email_id)
            for log ,email_id in team_attendance
        ]
    except AppException:
        raise
    except Exception as e:
        raise AppException("attendance_service", "get_team_attendance_service", 500, "Internal error", str(e))



