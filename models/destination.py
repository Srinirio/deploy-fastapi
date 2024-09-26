from db import Base
from sqlalchemy import Integer,String,Column
from sqlalchemy.orm import relationship

class Destination(Base):
    __tablename__ = "destination"
    
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    destination_name = Column(String(40), nullable=False)
    
    # relationship
    users = relationship("User",back_populates="destination")

