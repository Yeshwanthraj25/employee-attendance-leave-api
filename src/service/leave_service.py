from src.repository.leave_repo import get_leave_by_id,get_leave_history,get_leave_quote,update_leave_quote,update_leave_status,create_leave_request,get_team_leave_history
from src.models.dto.exception import AppException





async def apply_leave_service(db, emp_id, leave_type, leave_reason, start_date, end_date):
    try:
        if end_date < start_date:
            raise AppException("leave_service", "apply_leave_service", 400, "End date must be after start date", None)
        
        days_requested = (end_date - start_date).days + 1
        year = start_date.year
        
        
        quota = await get_leave_quote(db, emp_id, year)
        if quota is None:
            raise AppException("leave_service", "apply_leave_service", 404, "Leave quota not found for this year", None)
        
        remaining = quota.sick_leave_remaining if leave_type == 'sick' else quota.casual_leave_remaining
        if remaining < days_requested:
            raise AppException("leave_service", "apply_leave_service", 400, "Insufficient leave balance", None)
        
        
        leave = await create_leave_request(db, emp_id, leave_type, leave_reason, start_date, end_date)
        
        return {
            "leave_id": str(leave.leave_id),
            "emp_id": str(leave.emp_id),
            "leave_type": leave.leave_type,
            "status": "pending",
            "start_date": leave.start_date,
            "end_date": leave.end_date
        }
    except AppException:
        raise
    except Exception as e:
        raise AppException("leave_service", "apply_leave_service", 500, "Internal error", str(e))




async def approve_leave_service(db,leave_id,manager_id,role):
    try:
        if role not in ['manager', 'admin']:
            raise AppException("leave_rep","approve_leave_service",403,"unauthorization access",None)
        leave = await get_leave_by_id(db,leave_id)
        if leave is None :
            raise AppException("leave_rep","approve_leave_service",404,"user not found",None)
        if leave.status != 'pending':
            raise AppException("leave_rep","approve_leave_service",409,"Request already process",None)
        days_approved = (leave.end_date-leave.start_date).days +  1
        update_status = await update_leave_status(db,leave_id,'approved')
        emp_id,leave_type,start_date = leave.emp_id,leave.leave_type,leave.start_date
        year = start_date.year
        update_balance = await update_leave_quote(db,emp_id,leave_type,days_approved,year)
        return {
            "leave_id" :str(leave.leave_id),
            "emp_id": str(leave.emp_id),
            "leave_type":leave.leave_type,
            "status":"approved",
            "start_date":leave.start_date,
            "end_date":leave.end_date
        }
    except AppException:
            raise
    except Exception as e:
            raise AppException("leave_service", "approve_leave_service", 500, "Internal error", str(e))

async def reject_leave_service(db,leave_id,manager_id,role):
    try:
        if role not in ['manager','admin']:
            raise AppException("leave_rep","reject_leave_service",403,"unauthorization access",None)
        leave = await get_leave_by_id(db,leave_id)
        if leave is None :
                raise AppException("leave_rep","reject_leave_service",404,"user not found",None)
        if leave.status != 'pending':
                raise AppException("leave_rep","reject_leave_service",409,"Request already process",None)
        update_status = await update_leave_status(db,leave_id,'rejected')
        return {
                "leave_id" :str(leave.leave_id),
                "emp_id": str(leave.emp_id),
                "leave_type":leave.leave_type,
                "status":"rejected",
                "start_date":leave.start_date,
                "end_date":leave.end_date
            }
    except AppException:
            raise
    except Exception as e:
            raise AppException("leave_service", "reject_leave_service", 500, "Internal error", str(e))



async def get_leave_history_service(db, emp_id, status=None, year=None) :
    try:
        leave_history  = await get_leave_history(db,emp_id,status,year)
        return [{
                "leave_id" :str(leave.leave_id),
                "emp_id": str(leave.emp_id),
                "leave_type":leave.leave_type,
                "status":leave.status,
                "start_date":leave.start_date,
                "end_date":leave.end_date,
                "leave_reason" : leave.leave_reason}

            for leave in leave_history]
    except Exception as e:
            raise AppException("leave_service", "get_leave_history_service", 500, "Internal error", str(e))

async def get_team_leaves_service(db, manager_id, role, status=None, year=None):
    try:
        if role  not in ['manager','admin']:
                raise AppException("leave_rep","get_team_leaves_service",403,"unauthorization access",None)
        leave_history  = await get_team_leave_history(db,manager_id,status,year)
        return [{
                    "leave_id" :str(leave.leave_id),
                    "emp_id": str(leave.emp_id),
                    "leave_type":leave.leave_type,
                    "status":leave.status,
                    "start_date":leave.start_date,
                    "end_date":leave.end_date,
                    "leave_reason" : leave.leave_reason}
        
                for leave in leave_history]
    except AppException:
            raise
    except Exception as e:
            raise AppException("leave_service", "get_team_leaves_service", 500, "Internal error", str(e))

async def get_leave_balance_service(db, emp_id, year):
    try:
        leave_quote = await get_leave_quote(db,emp_id,year)
        return {
            "sick_leave_remaining":leave_quote.sick_leave_remaining,
            "casual_leave_remaining": leave_quote.casual_leave_remaining,
            "year":leave_quote.year
        }
    
    except Exception as e:
            raise AppException("leave_service", "get_leave_balance_service", 500, "Internal error", str(e))


    
    
     
    




