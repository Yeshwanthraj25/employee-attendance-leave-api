from src.repository.attendance_repo import get_today_log,create_check_in,get_attendance_history,get_team_attendance,update_attendance_log
from src.models.dto.exception import AppException


async def check_in_service(db,emp_id):
    try:
        log_check = await get_today_log(db,emp_id) 
        if log_check is not None:
            raise AppException("attendance_service","check_in_service",400,"Today attendance already exist",None)
        else :
            check_in = await  create_check_in(db,emp_id)  
            return {
                 "log_id":str(check_in.log_id),
                 "emp_id": str(check_in.emp_id),
                 "log_in_time":check_in.log_in_time,
                 "log_out_time":check_in.log_out_time

            }
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
                return {
            "log_id": str(updated_log.log_id),
            "emp_id": str(updated_log.emp_id),
            "log_in_time": updated_log.log_in_time,
            "log_out_time": updated_log.log_out_time,
            "status": updated_log.status
        }
        except AppException:
            raise
        except Exception as e :
            raise AppException("attendance_service","check_out_service",500,"Internal Error",str(e))

async def get_attendance_history_service(db,emp_id,start_date,end_date):
        try:
            attendance_history = await  get_team_attendance(db,emp_id,start_date,end_date)
            return [
            {
                "log_id": str(log.log_id),
                "emp_id": str(log.emp_id),
                "log_in_time": log.log_in_time,
                "log_out_time": log.log_out_time,
                "status": log.status
            }
            for log in attendance_history
        ]
        except Exception as e :
            raise AppException("attendance_service","get_attendance_history",500,"Internal Error",str(e))

async def get_team_attendance_service(db,manager_id,role,start_date,end_date):
        try:
            if role not in ['manager','admin']:
                 raise AppException("attendance_service","get_team_attendance",403,"only manager can view team attendance")
            team_attendance = await  get_attendance_history(db,manager_id,start_date,end_date)
            return [{
                 "log_id": str(log.log_id )
            }
            for log in team_attendance
            ]
        except Exception as e :
            raise AppException("attendance_service","get_attendance_history",500,"Internal Error",str(e))



