from db import Base
from sqlalchemy import *
from sqlalchemy.orm import *
from datetime import datetime

class WorkReport(Base):
    __tablename__ = "work_report"
    
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    description = Column(String(500),nullable=False)
    created_at = Column(DateTime,default=datetime.now())
    # ForeignKey
    ticket_id = Column(Integer,ForeignKey("ticket.id"),nullable=True)
    emp_id = Column(String(20),ForeignKey("user.id"),nullable=False)
    # relationship
    employee = relationship("User",back_populates="work_report")
    ticket = relationship("Ticket",back_populates="work_report")