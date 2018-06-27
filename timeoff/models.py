from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, DateTime, Enum
import enum

class RequestStatus(enum.Enum):
    pending = 0
    approved = 1
    denied = 2

class RequestType(enum.Enum):
    remote = 0
    sick = 1
    vacation = 2
    holiday = 3


Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True)

    # Fields from LDAP
    name_last = Column(String)
    name_first = Column(String)
    email = Column(String)

    # App Fields
    manager_id = Column(Integer, ForeignKey('employee.id'))
    manager = relationship('Employee', remote_side=[id], backref='reports')

    approval_level # 

    requests = relationship('Request')
    
    requests_pending = relationship('Request',
            primaryjoin="and_(Employee.id==Request.employee_id, "
            "Request.status=='pending')")

    requests_approved = relationship('Request',
            primaryjoin="and_(Employee.id==Request.employee_id, "
            "Request.status=='approved')")
    
    requests_denied = relationship('Request',
            primaryjoin="and_(Employee.id==Request.employee_id, "
            "Request.status=='denied')")

    def __repr__(self):
        return '<Employee: {}, {}>'.format(self.name_last, self.name_first)



class Request(Base):
    __tablename__ = 'request'

    id = Column(Integer, primary_key=True)

    employee_id = Column(Integer, ForeignKey('employee.id'))

    create_date = Column(DateTime)

    start_date = Column(Date)
    end_date = Column(Date)

    def total_days(self):
        pass

    #actioned_by = relationship('Employee') # Manager who approved/denied request
    action_date = Column(DateTime)

    status = Column(Enum(RequestStatus), default=RequestStatus.pending)

    request_type = Column(Enum(RequestType))


class ACL(Base):
    __tablename__ = 'acl'

    id = Column(Integer, primary_key=True)
    
    

