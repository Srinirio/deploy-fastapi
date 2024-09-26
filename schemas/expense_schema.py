from pydantic import BaseModel
from fastapi import *

class ExpenseDetails(BaseModel):
    expense_id: int  
    description: str
    amount: float
    approved_status: bool
    approved_by: str | None = None
    employee_name: str | None = None

    class Config:
        orm_mode = True


class ExpenseDetailsOut(BaseModel):
    ticket_id: int
    expenses: list[ExpenseDetails]
    total_amount: float
    total_amount_approved: float

    class Config:
        orm_mode = True