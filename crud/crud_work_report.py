from sqlalchemy.orm import *
from models import *
from schemas import *
from crud import *

def getWorkReport(db: Session,emp_in: User):
    return db.query(WorkReport).filter(WorkReport.emp_id == emp_in.id).all()