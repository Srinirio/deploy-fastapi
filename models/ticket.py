from db import Base
from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Boolean
from datetime import datetime
from sqlalchemy.orm import relationship

class Ticket(Base):
    __tablename__ = "ticket"
    
    id = Column(Integer,primary_key=True,index=True)
    customer_name = Column(String(100),nullable=False)
    address = Column(String(100),nullable=False)
    company_name = Column(String(100),nullable=False)
    created_at = Column(DateTime,default=datetime.now())
    update_at = Column(DateTime,default=datetime.now())
    description = Column(String(1000))
    # ForeignKey
    created_by_user_id = Column(String(20), ForeignKey("user.id"), nullable=True)
    # relationship
    created_by = relationship("User",back_populates="created_tickets")
    assigned_ticket = relationship("AssigningTicket", back_populates="ticket",uselist=False)
    status = relationship("TicketStatus",back_populates="ticket", uselist=False)
    expenses = relationship("Expense", back_populates="ticket")
    requested_items = relationship("MaterialRequest",back_populates="ticket")
    work_report = relationship("WorkReport",back_populates="ticket")    
    
class AssigningTicket(Base):
    __tablename__ = "assigning_ticket"
    
    id = Column(Integer,primary_key=True,index=True)
    created_at = Column(DateTime,default=datetime.now())
    update_at = Column(DateTime,default=datetime.now())
    # ForeignKey
    ticket_id = Column(Integer,ForeignKey("ticket.id"))
    assigned_by_emp_id = Column(String(20),ForeignKey("user.id"))
    assigned_to_emp_id = Column(String(20),ForeignKey("user.id"))
    # relationship
    assigned_by = relationship("User", back_populates="assigned_tickets", foreign_keys=[assigned_by_emp_id])  
    assigned_to = relationship("User", back_populates="received_tickets", foreign_keys=[assigned_to_emp_id])  
    ticket = relationship("Ticket", back_populates="assigned_ticket")
    
class TicketStatus(Base):
    __tablename__ = "ticket_status"
    
    id = Column(Integer,primary_key=True,index=True)
    created_at = Column(DateTime,default=datetime.now())
    update_at = Column(DateTime,default=datetime.now())
    expected_date_to_complete = Column(DateTime)
    status_of_ticket = Column(Boolean, default=False)
    completed_date = Column(DateTime)
    priority = Column(Integer)
    # ForeignKey
    ticket_id = Column(Integer,ForeignKey("ticket.id"))
    # relationship
    ticket = relationship("Ticket", back_populates="status")
    

     
    
    
    
    
