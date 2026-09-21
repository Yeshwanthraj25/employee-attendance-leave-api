from src.repository.leave_repo import LeaveRepo
from src.models.dto.exception import AppException
from src.models.output_model import LeaveBalance,LeaveHistory,ApplyLeave,ApplyApproved,ApplyRejected,TeamHistory



class LeaveService:
        def __init__(self):
             self.leave_repo = LeaveRepo()

        async def apply_leave_service(self,db, emp_id, leave_type, leave_reason, start_date, end_date):
            try:
                if end_date < start_date:
                    raise AppException("leave_service", "apply_leave_service", 400, "End date must be after start date", None)
                
                days_requested = (end_date - start_date).days + 1
                year = start_date.year
                quota = await self.leave_repo.get_leave_quote(db, emp_id, year)
                if quota is None:
                    raise AppException("leave_service", "apply_leave_service", 404, "Leave quota not found for this year", None)
                
                remaining = quota.sick_leave_remaining if leave_type == 'sick' else quota.casual_leave_remaining
                if remaining < days_requested:
                    raise AppException("leave_service", "apply_leave_service", 400, "Insufficient leave balance", None)
                
                
                leave = await self.leave_repo.create_leave_request(db, emp_id, leave_type, leave_reason, start_date, end_date)
                
                response = ApplyLeave(
                    leave_id = str(leave.leave_id),
                    emp_id = str(leave.emp_id),
                    leave_type = leave.leave_type,
                    status= "pending",
                    start_date = leave.start_date,
                    end_date = leave.end_date
                )
                return response 
            except AppException:
                raise
            except Exception as e:
                raise AppException("leave_service", "apply_leave_service", 500, "Internal error", str(e))




        async def approve_leave_service(self,db,leave_id,manager_id,role):
            try:
                if role not in ['manager', 'admin']:
                    raise AppException("leave_rep","approve_leave_service",403,"unauthorization access",None)
                leave = await self.leave_repo.get_leave_by_id(db,leave_id)
                if leave is None :
                    raise AppException("leave_rep","approve_leave_service",404,"user not found",None)
                if leave.status != 'pending':
                    raise AppException("leave_rep","approve_leave_service",409,"Request already process",None)
                days_approved = (leave.end_date-leave.start_date).days +  1
                update_status = await self.leave_repo.update_leave_status(db,leave_id,'approved')
                emp_id,leave_type,start_date = leave.emp_id,leave.leave_type,leave.start_date
                year = start_date.year
                update_balance = await self.leave_repo.update_leave_quote(db,emp_id,leave_type,days_approved,year)
                response = ApplyApproved(
                    leave_id = str(leave.leave_id),
                    emp_id = str(leave.emp_id),
                    leave_type = leave.leave_type,
                    status= "pending",
                    start_date = leave.start_date,
                    end_date = leave.end_date
                )
                return response 
            except AppException:
                    raise
            except Exception as e:
                    raise AppException("leave_service", "approve_leave_service", 500, "Internal error", str(e))

        async def reject_leave_service(self,db,leave_id,manager_id,role):
            try:
                if role not in ['manager','admin']:
                    raise AppException("leave_rep","reject_leave_service",403,"unauthorization access",None)
                leave = await self.leave_repo.get_leave_by_id(db,leave_id)
                if leave is None :
                        raise AppException("leave_rep","reject_leave_service",404,"user not found",None)
                if leave.status != 'pending':
                        raise AppException("leave_rep","reject_leave_service",409,"Request already process",None)
                update_status = await self.leave_repo.update_leave_status(db,leave_id,'rejected')
                response = ApplyRejected(
                    leave_id = str(leave.leave_id),
                    emp_id = str(leave.emp_id),
                    leave_type = leave.leave_type,
                    status= "pending",
                    start_date = leave.start_date,
                    end_date = leave.end_date
                )
                return response
            except AppException:
                    raise
            except Exception as e:
                    raise AppException("leave_service", "reject_leave_service", 500, "Internal error", str(e))



        async def get_leave_history_service(self,db, emp_id, status=None, year=None) :
            try:
                leave_history  = await self.leave_repo.get_leave_history(db,emp_id,status,year)
                return [ LeaveHistory.model_validate(leave)
                    for leave in leave_history]
            except Exception as e:
                    raise AppException("leave_service", "get_leave_history_service", 500, "Internal error", str(e))

        async def get_team_leaves_service(self,db, manager_id, role, status=None, year=None):
            try:
                if role  not in ['manager','admin']:
                        raise AppException("leave_rep","get_team_leaves_service",403,"unauthorization access",None)
                leave_history  = await self.leave_repo.get_team_leave_history(db,manager_id,status,year)
                return [ TeamHistory.model_validate(leave)
                        for leave in leave_history]
            except AppException:
                    raise
            except Exception as e:
                    raise AppException("leave_service", "get_team_leaves_service", 500, "Internal error", str(e))

        async def get_leave_balance_service(self,db, emp_id, year):
            try:
                leave_quote = await self.leave_repo.get_leave_quote(db,emp_id,year)
                response = LeaveBalance(
                    sick_leave_remaining =leave_quote.sick_leave_remaining,
                    casual_leave_remaining = leave_quote.casual_leave_remaining,
                    year = leave_quote.year
                )
                return response
            
            except Exception as e:
                    raise AppException("leave_service", "get_leave_balance_service", 500, "Internal error", str(e))

        async def insert_leave_quote_service(self, db,
                    emp_id,
                    year,
                    sick_leave_allotted,
                    sick_leave_remaining,
                    casual_leave_allotted,
                    casual_leave_remaining):
            try:
                # ...
                leave_quote = await self.leave_repo.insert_leave_quote(db, emp_id, year, sick_leave_allotted,sick_leave_remaining, casual_leave_allotted, casual_leave_remaining)
                print(f"DEBUG - Inserted: {leave_quote}")
                
                return {
                    "quote_id": str(leave_quote.quote_id),
                    "emp_id": str(leave_quote.emp_id),
                    "year": leave_quote.year,
                    "sick_leave_allotted": leave_quote.sick_leave_allotted,
                    "sick_leave_remaining": leave_quote.sick_leave_remaining,
                    "casual_leave_allotted": leave_quote.casual_leave_allotted,
                    "casual_leave_remaining": leave_quote.casual_leave_remaining
                }
            except Exception as e:
                raise AppException("leave_service", "insert_leave_quote_service", 500, "Internal error", str(e))

leave_service  = LeaveService()

