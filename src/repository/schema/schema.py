from sqlalchemy.orm import relationship,declarative_base
from sqlalchemy import Column,String,Integer,DateTime,Enum,ForeignKey,func,UUID
from uuid import uuid4

Base = declarative_base()

class Employee(Base):
    __tablename__="employee"
    emp_id = Column(UUID,primary_key=True,default=uuid4)
    email_id =Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)
    phone_number= Column(String,nullable=False)
    dep_id =Column(UUID,ForeignKey("department.dep_id"),default=None)
    role= Column(Enum('admin','manager','employee',name='employee_role_enum'))
    manager_id = Column(UUID,ForeignKey("employee.emp_id"),default=None)
    created_at = Column(DateTime,default=func.now(),nullable=False)
    updated_at = Column(DateTime,nullable=True)

    department = relationship("Department",back_populates="employees")

    manager =relationship("Employee",remote_side=[emp_id],foreign_keys=[manager_id])

    quote =relationship("LeaveQuote",back_populates="employee")

    attendance_log =relationship("LogAttendance",back_populates="employee")

    leaves =relationship("LeaveManagement",back_populates="employee")


class LogAttendance(Base):
    __tablename__ = "log_attendance"
    log_id = Column(UUID,primary_key=True,default=uuid4)
    emp_id = Column(UUID,ForeignKey("employee.emp_id"),default=uuid4)
    log_in_time = Column(DateTime,nullable=True)
    log_out_time = Column(DateTime,nullable=True)
    status = Column(Enum('present','absent','half-day',name='attendance_status_enum'))
    created_at = Column(DateTime,default=func.now())
    updated_at = Column(DateTime)

    employee =relationship("Employee",back_populates="attendance_log")

class Department(Base):
     __tablename__ = "department"
     dep_id = Column(UUID,primary_key=True,default=uuid4)
     dep_name= Column(String,nullable=False)
     created_at = Column(DateTime,default=func.now())
     updated_at = Column(DateTime)

     employees =relationship("Employee",back_populates="department")
 
class LeaveManagement(Base):
    __tablename__="leave_management" 
    leave_id = Column(UUID,primary_key=True,default=uuid4,nullable=False)
    emp_id = Column(UUID,ForeignKey("employee.emp_id"),default=uuid4)
    leave_type = Column(String,nullable=False)
    status= Column(Enum('pending','approved','rejected',name='leave_status_enum'))
    start_date = Column(DateTime)
    leave_reason= Column(String,nullable=False)
    end_date= Column(DateTime)
    created_at = Column(DateTime,default=func.now())
    updated_at = Column(DateTime)

    employee =relationship("Employee",back_populates="leaves")

class LeaveQuote(Base):
    __tablename__ ="leave_quote"
    quote_id= Column(UUID,primary_key =True,default=uuid4)
    emp_id = Column(UUID,ForeignKey("employee.emp_id"),default=uuid4)
    sick_leave_allocated = Column(Integer,nullable=False)
    casual_leave_allocated = Column(Integer,nullable=False)
    casual_leave_remaining = Column(Integer,nullable=False)
    year= Column(Integer,nullable=True)
    created_at = Column(DateTime,default=func.now())
    updated_at = Column(DateTime)

    employee =relationship("Employee",back_populates="quote")


class ErrorLog(Base):
    __tablename__ = "error_log"
    log_id = Column(UUID,primary_key = True,default= uuid4)
    file_name = Column(String,nullable= False)
    function_name = Column(String,nullable = False)
    status_code = Column(Integer,nullable= False)
    log_data = Column(String,nullable = False)
    error_details = Column(String,nullable = False)
    created_at = Column(DateTime,default=func.now())
    updated_at = Column(DateTime)



