from db import Base
from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Boolean
from datetime import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"
    
    id = Column(String(20),primary_key=True,autoincrement=False)
    name = Column(String(50),nullable=False)
    email = Column(String(50),nullable=False,unique=True)
    password = Column(String(200),nullable=False)
    phone_number = Column(String(10),nullable=False)
    is_active = Column(Boolean,default=True)
    created_at = Column(DateTime, default=datetime.now()) 
    updated_at = Column(DateTime,default=datetime.now())
    # ForeignKey
    destination_id = Column(Integer,ForeignKey("destination.id"))
    report_to = Column(String(20), ForeignKey("user.id"),nullable=True)
    
    # relationship
    under_me = relationship("User",remote_side=[id],backref="higher_official")
    destination = relationship("Destination",back_populates="users")
    created_tickets = relationship("Ticket", back_populates="created_by")
    assigned_tickets = relationship("AssigningTicket", back_populates="assigned_by", foreign_keys="AssigningTicket.assigned_by_emp_id")
    received_tickets = relationship("AssigningTicket", back_populates="assigned_to", foreign_keys="AssigningTicket.assigned_to_emp_id") 
    expenses = relationship("Expense", foreign_keys="Expense.emp_id", back_populates="employee")
    approved_expenses = relationship("Expense", foreign_keys="Expense.approved_by", back_populates="approver")
    requested_items = relationship("MaterialRequest",back_populates="employee")
    work_report = relationship("WorkReport",back_populates="employee")