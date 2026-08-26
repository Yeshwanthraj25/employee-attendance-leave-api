from src.service.leave_service import get_team_leave_history,get_leave_balance_service,get_team_leaves_service,get_leave_history_service,apply_leave_service,approve_leave_service,insert_leave_quote_service,reject_leave_service
from src.repository.Database import get_db
from fastapi.responses import JSONResponse
from src.models.dto.exception import AppException
from src.repository.error_repo import error_insert
from src.core.dependencies import get_current_user
from  src.utilize.response_helper import API_response
from src.models.error_model import ErrorCreation
from uuid import uuid4 
from src.models.input_models import ApplyLeave,LeaveQuote
from fastapi import APIRouter,Depends
from datetime import datetime,date

app = APIRouter(prefix = "/leave",tags=['leave'])

@app.post("/apply")
async def apply_leave(apply:ApplyLeave, db = Depends(get_db),current =Depends( get_current_user)):
    try:
        apply_leave = await apply_leave_service(db,current.emp_id,apply.leave_type,apply.leave_reason,apply.start_date,apply.end_date)
        response_dict = apply_leave.model_dump(mode='json')
        api_response = API_response(response_dict,201,"Leave Appiled successfully","success")
        return JSONResponse(status_code =201,content = api_response.model_dump(mode='json'))
    except Exception as e :
            if isinstance(e,AppException):
                error_schema = ErrorCreation(
                                              log_id = uuid4(),
                                             file_name="attendance.py",
                                             function_name="check_route",
                                             status_code=e.status_code,
                                             log_data= str(e.log_data) if e.log_data else "No additional log data",
                                             error_details=e.error_details,
                                             created_at = datetime.now(),
                                             updated_at = datetime.now() )
                                       
                await error_insert(db, error_schema)
                api_response =  API_response(
                                                                        data={},
                                                                        status_code=e.status_code,
                                                                        message=e.error_details,
                                                                        status="error",
                                                                        errors=[{"error": str(e)}]  
                                                                            )
                return JSONResponse(status_code = e.status_code,content = api_response.model_dump(mode ='json'))
                
            else :
                api_response =  API_response(
                                                                                        data={},
                                                                                        status_code=e.status_code,
                                                                                        message=e.error_details,
                                                                                        status="error",
                                                                                        errors=[{"error": str(e)}]  
                                                                                            )
                return JSONResponse(status_code = e.status_code,content = api_response.model_dump(mode ='json'))

@app.patch("/{leave_id}/approve")
async def approve_leave(leave_id,db = Depends(get_db),current =Depends( get_current_user)):
    try:
        approve_leave = await approve_leave_service(db,leave_id,current.emp_id,current.role)
        response_dict = approve_leave.model_dump(mode='json')
        api_response = API_response(response_dict,200,"The leave application has been approved successfully","success")
        return JSONResponse(status_code =200,content = api_response.model_dump(mode='json'))
    except Exception as e :
            if isinstance(e,AppException):
                error_schema = ErrorCreation(
                                              log_id = uuid4(),
                                             file_name="attendance.py",
                                             function_name="check_route",
                                             status_code=e.status_code,
                                             log_data= str(e.log_data) if e.log_data else "No additional log data",
                                             error_details=e.error_details,
                                             created_at = datetime.now(),
                                             updated_at = datetime.now() )
                                       
                await error_insert(db, error_schema)
                api_response =  API_response(
                                                                        data={},
                                                                        status_code=e.status_code,
                                                                        message=e.error_details,
                                                                        status="error",
                                                                        errors=[{"error": str(e)}]  
                                                                            )
                return JSONResponse(status_code = e.status_code,content = api_response.model_dump(mode ='json'))
                
            else :
                    api_response =  API_response(
                                                                                          data={},
                                                                                          status_code=e.status_code,
                                                                                          message=e.error_details,
                                                                                          status="error",
                                                                                          errors=[{"error": str(e)}]  
                                                                                              )
                    return JSONResponse(status_code = e.status_code,content = api_response.model_dump(mode ='json'))
                

@app.patch("/{leave_id}/reject")
async def reject_leave(leave_id,db = Depends(get_db),current =Depends( get_current_user)):
    try:
        reject_leave = await reject_leave_service(db,leave_id,current.emp_id,current.role)
        response_dict = reject_leave.model_dump(mode='json')
        api_response = API_response(response_dict,200,"The leave application has been rejected successfully","success")
        return JSONResponse(status_code =200,content = api_response.model_dump(mode='json'))
    except Exception as e :
            if isinstance(e,AppException):
                error_schema = ErrorCreation(
                                              log_id = uuid4(),
                                             file_name="attendance.py",
                                             function_name="check_route",
                                             status_code=e.status_code,
                                             log_data= str(e.log_data) if e.log_data else "No additional log data",
                                             error_details=e.error_details,
                                             created_at = datetime.now(),
                                             updated_at = datetime.now() )
                                       
                await error_insert(db, error_schema)
                api_response =  API_response(
                                                                        data={},
                                                                        status_code=e.status_code,
                                                                        message=e.error_details,
                                                                        status="error",
                                                                        errors=[{"error": str(e)}]  
                                                                            )
                return JSONResponse(status_code = e.status_code,content = api_response.model_dump(mode ='json'))
                
            else :
                api_response =  API_response(
                                                                                        data={},
                                                                                        status_code=e.status_code,
                                                                                        message=e.error_details,
                                                                                        status="error",
                                                                                        errors=[{"error": str(e)}]  
                                                                                            )
                return JSONResponse(status_code = e.status_code,content = api_response.model_dump(mode ='json'))




@app.get("/me")
async def get_mine_history(status = None , year = None,db = Depends(get_db),current =Depends(get_current_user)):
        try:
            leave_history = await get_leave_history_service(db,current.emp_id,status,year)
            api_response = API_response(leave_history,200,"Retrieve the mine leave history successfully","success")
            return JSONResponse(status_code =200,content = api_response.model_dump(mode='json'))
        except Exception as e :
                       if isinstance(e,AppException):
                           error_schema = ErrorCreation(
                                                         log_id = uuid4(),
                                                        file_name="attendance.py",
                                                        function_name="check_route",
                                                        status_code=e.status_code,
                                                        log_data= str(e.log_data) if e.log_data else "No additional log data",
                                                        error_details=e.error_details,
                                                        created_at = datetime.now(),
                                                        updated_at = datetime.now() )
                                                  
                           await error_insert(db, error_schema)
                           api_response =  API_response(
                                                                                   data={},
                                                                                   status_code=e.status_code,
                                                                                   message=e.error_details,
                                                                                   status="error",
                                                                                   errors=[{"error": str(e)}]  
                                                                                       )
                           return JSONResponse(status_code = e.status_code,content = api_response.model_dump(mode ='json'))
                           
                       else :
                           raise


@app.get("/team")
async def get_team_history(status = None , year = None,db = Depends(get_db),current =Depends( get_current_user)):
        try:
            
            leave_history = await get_team_leaves_service(db,current.emp_id,current.role,status,year)
            api_response = API_response(leave_history,200,"Retrieve the team leave history successfully","success")
            return JSONResponse(status_code =200,content = api_response.model_dump(mode='json'))
        except Exception as e :
                       if isinstance(e,AppException):
                           error_schema = ErrorCreation(
                                                         log_id = uuid4(),
                                                        file_name="attendance.py",
                                                        function_name="check_route",
                                                        status_code=e.status_code,
                                                        log_data= str(e.log_data) if e.log_data else "No additional log data",
                                                        error_details=e.error_details,
                                                        created_at = datetime.now(),
                                                        updated_at = datetime.now() )
                                                  
                           await error_insert(db, error_schema)
                           api_response =  API_response(
                                                                                   data={},
                                                                                   status_code=e.status_code,
                                                                                   message=e.error_details,
                                                                                   status="error",
                                                                                   errors=[{"error": str(e)}]  
                                                                                       )
                           return JSONResponse(status_code = e.status_code,content = api_response.model_dump(mode ='json'))
                           
                       else :
                            api_response =  API_response(
                                                                                                     data={},
                                                                                                     status_code=e.status_code,
                                                                                                     message=e.error_details,
                                                                                                     status="error",
                                                                                                     errors=[{"error": str(e)}]  
                                                                                                         )
                            return JSONResponse(status_code = e.status_code,content = api_response.model_dump(mode ='json'))

@app.get("/balance")
async def get_mine_history( year: int = None,db = Depends(get_db),current =Depends( get_current_user)):
        try:
            if year is None :
                  year = date.today().year
            leave_balance = await  get_leave_balance_service(db,current.emp_id,year)
            response_dict = leave_balance.model_dump(mode='json')
            api_response = API_response(response_dict,200,"The leave balance has been retrieve successfully","success")
            return JSONResponse(status_code =200,content = api_response.model_dump(mode='json'))
        except Exception as e :
                       if isinstance(e,AppException):
                           error_schema = ErrorCreation(
                                                         log_id = uuid4(),
                                                        file_name="attendance.py",
                                                        function_name="check_route",
                                                        status_code=e.status_code,
                                                        log_data= str(e.log_data) if e.log_data else "No additional log data",
                                                        error_details=e.error_details,
                                                        created_at = datetime.now(),
                                                        updated_at = datetime.now() )
                                                  
                           await error_insert(db, error_schema)
                           api_response =  API_response(
                                                                                   data={},
                                                                                   status_code=e.status_code,
                                                                                   message=e.error_details,
                                                                                   status="error",
                                                                                   errors=[{"error": str(e)}]  
                                                                                       )
                           return JSONResponse(status_code = e.status_code,content = api_response.model_dump(mode ='json'))
                           
                       else :
                            api_response =  API_response(
                                                                                                      data={},
                                                                                                      status_code=500,
                                                                                                      message="Internal error ",
                                                                                                      status="error",
                                                                                                      errors=[{"error": str(e)}]  
                                                                                                          )
                            return JSONResponse(status_code = e.status_code,content = api_response.model_dump(mode ='json'))

@app.post("/leave-quote")
async def leave_quote_route(quote: LeaveQuote, db=Depends(get_db), current_user=Depends(get_current_user)):
    try:
        leave_quote = await insert_leave_quote_service(
            db,
            quote.emp_id,
            quote.year,
            quote.sick_leave_allotted,
            quote.sick_leave_remaining,
            quote.casual_leave_allotted,
            quote.casual_leave_remaining
        )
        
        api_response = API_response(leave_quote, 201, "Allocation successfully inserted", "success")
        
        return JSONResponse(status_code=201, content=api_response.model_dump(mode='json'))
        
    except Exception as e:
        if isinstance(e, AppException):
            error_schema = ErrorCreation(
                log_id=uuid4(),
                file_name="leave.py",
                function_name="leave_quote_route",
                status_code=e.status_code,
                log_data=str(e.log_data) if e.log_data else "No additional log data",
                error_details=e.error_details,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            await error_insert(db, error_schema)
            api_response = API_response({}, e.status_code, e.error_details, status="error")
            return JSONResponse(status_code=e.status_code, content=api_response.model_dump(mode='json'))
        
        else:
            api_response = API_response({}, 500, str(e), status="error")
            return JSONResponse(status_code=500, content=api_response.model_dump(mode='json'))