from models import *
from fastapi import *
from sqlalchemy.orm import Session
from datetime import datetime

def updateExpense(db: Session, expense_in: Expense, updater: User):
    expense_in.approved_status = True
    expense_in.approved_date = datetime.now()
    expense_in.approved_by = updater.id
    
    db.add(expense_in)
    db.commit()
    return {"message":"Successfully approved"}