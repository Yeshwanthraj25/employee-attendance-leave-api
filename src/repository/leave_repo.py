from sqlalchemy import select,update,func
from src.repository.schema.schema import Employee,LogAttendance,Department,LeaveManagement,LeaveQuote,ErrorLog
from src.models.dto.exception  import AppException



async def create_leave_request(db,emp_id,leave_type,leave_reason,start_date,end_date):
    try :
        request = LeaveManagement(emp_id = emp_id , leave_type = leave_type,leave_reason = leave_reason, start_date =start_date,end_date = end_date,status = 'pending')
        db.add(request)
        await db.flush()
        await db.commit()
        return  request
    except Exception as e:
        raise AppException("leave_repo","create_leave_request",500,"Internal error",str(e))


async def get_leave_by_id(db, leave_id):
    try :
        query = select(LeaveManagement).where(LeaveManagement.leave_id == leave_id)
        result = await db.execute(query)
        get_details = result.scalars().first() 
        if get_details is not None:     
             return  get_details
    except Exception as e:
        raise AppException("leave_repo","get_leave_by_id",500,"Internal error",str(e))

async def get_leave_history(db, emp_id, status=None, year=None):
    try :
        condition =(LeaveManagement.emp_id == emp_id) 
        if status:
            condition = condition &(LeaveManagement.status == status)
        if year:
            condition = condition & (func.extract('year',LeaveManagement.start_date) == year)
        query = select(LeaveManagement).where(condition)
        result = await db.execute(query)
        get_details = result.scalars().all() 
        return list(get_details)
    except Exception as e:
        raise AppException("leave_repo","get_leave_history",500,"Internal error",str(e))

async def update_leave_status(db, leave_id, status):
    try :
        query = update(LeaveManagement).where(LeaveManagement.leave_id == leave_id).values(status = status )
        await db.execute(query)
        await db.commit()
        return query
    except Exception as e:
        raise AppException("leave_repo","update_leave_status",500,"Internal error",str(e))

async def update_leave_quote(db, emp_id, leave_type, days_to_deduct, year):
    try :
        if leave_type =='sick':
            column_to_update = LeaveQuote.sick_leave_remaining
        elif leave_type =='casual':
            column_to_update = LeaveQuote.casual_leave_remaining 
        query = update(LeaveQuote).where((LeaveQuote.emp_id ==emp_id) & (LeaveQuote.year ==year)).values({column_to_update: column_to_update - days_to_deduct})
        await db.execute(query)
        await db.commit()        
    
        return query
    except Exception as e:
        raise AppException("leave_repo","update_leave_status",500,"Internal error",str(e))


async def get_leave_quote(db,emp_id,year):
    try:
        query = select(LeaveQuote).where(LeaveQuote.emp_id == emp_id) & (LeaveQuote.year ==year)
        result = await db.execute(query)
        leave_quote = result.scalars().all()
        return leave_quote
    except Exception as e:
            raise AppException("leave_repo","get_leave_quote",500,"Internal error",str(e))

async def get_team_leave_history(db,manager_id,status=None,year = None ):
    try:
       
        condition = (Employee.manager_id == manager_id) 
        if status != None:
            condition = condition & (LeaveManagement.status ==status) 
        if year != None:
            condition = condition & (func.extract('year',LeaveManagement.start_date) == year)
        query = select(LeaveManagement).join(Employee).where(condition)
        result = await db.execute(query)
        team_leaves = result.scalars().all()
        return team_leaves
        
    except Exception as e:
            raise AppException("leave_repo","get_team_leave_history",500,"Internal error",str(e))
    



