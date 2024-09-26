from db import Base
from sqlalchemy import *
from sqlalchemy.orm import *
from datetime import datetime

class Expense(Base):
    __tablename__ = "expense"
    
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    description = Column(String(100))
    amount = Column(Float)
    approved_status = Column(Boolean,default=False)
    approved_date = Column(DateTime,nullable=True)
    create_at = Column(DateTime,default=datetime.now())
    image = Column(String(200))
    # ForeignKey
    emp_id = Column(String(20),ForeignKey("user.id"),nullable=False)
    approved_by = Column(String(20),ForeignKey("user.id"),nullable=True)
    ticket_id = Column(Integer,ForeignKey("ticket.id"),nullable=True)
    # relationships
    ticket = relationship("Ticket",back_populates="expenses")
    employee = relationship("User", foreign_keys=[emp_id], back_populates="expenses")
    approver = relationship("User", foreign_keys=[approved_by], back_populates="approved_expenses")
    
    
    
    