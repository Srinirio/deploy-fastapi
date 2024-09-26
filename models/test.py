from sqlalchemy import Column,Integer
from db import Base

class Test(Base):
    __tablename__ = "test"
    
    id = Column(Integer,primary_key=True)
    num = Column(Integer)