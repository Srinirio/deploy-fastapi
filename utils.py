from sqlalchemy.orm import Session
from models import *
from sqlalchemy import desc,asc
# from api.deps import get_db
from fastapi import *

def createEmployeeId(db: Session):
    user = db.query(User).order_by(User.created_at.desc(),User.id.desc()).first()
    if not user:
        return "20IT001"

    prefix = "20IT"
    roll_no = int(user.id[4:])+1
    
    if len(str(roll_no))==1:
        return prefix +"00"+str(roll_no)
        print(roll_no)
        
    elif len(str(roll_no))==2:
        return prefix +"0"+str(roll_no)
        print(roll_no)
        
    else:
        return prefix+str(roll_no)
    
def createReport(db: Session,ticket_id: int):

    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).one_or_none()
    
    print(db_ticket.status)
          

    

    

    

    
    