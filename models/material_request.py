from db import Base
from sqlalchemy import *
from sqlalchemy.orm import *
from datetime import datetime

class MaterialRequest(Base):
    __tablename__ = "material_request"
    
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    create_at = Column(DateTime,default=datetime.now())
    units = Column(Integer,nullable=False)
    # ForeignKey
    material_id = Column(Integer,ForeignKey("material.id"),nullable=False)
    ticket_id = Column(Integer,ForeignKey("ticket.id"))
    emp_id = Column(String(20),ForeignKey("user.id"))
    # relationship
    material = relationship("Material",back_populates="requests")
    ticket = relationship("Ticket",back_populates="requested_items")
    employee = relationship("User",back_populates="requested_items")
    
class Material(Base):
    __tablename__ = "material"
    
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    material_name = Column(String(100))
    amount = Column(Float)
    # relationship
    requests = relationship("MaterialRequest",back_populates="material")
    
