from sqlalchemy.orm import *
from models import *
from fastapi import *
from sqlalchemy import *

"""
check the employee is under the particular service head
"""
def checkEmployeeUnderHead(db: Session,employee_id: str,service_head: User):
    emp = db.query(User).filter(and_(
        User.id == employee_id, User.report_to == service_head.id
        )).first()
    if not emp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
        
def assignTicketToEmp(db: Session,employee_id: str,service_head: User,ticket_id: int):
    assign_ticket = AssigningTicket(
        ticket_id = ticket_id,
        assigned_by_emp_id  = service_head.id,
        assigned_to_emp_id = employee_id
    )
    db.add(assign_ticket)
    db.commit()
    db.refresh(assign_ticket)
    return {"message": "Assigned Successfully"}

def checkTicketUnderHead(db: Session,current_user: User,ticket_id: int):
    emp_ids = db.query(User.id).filter(User.report_to == current_user.id).all()
    list_of_employee_ids = [data[0] for data in emp_ids]
    ticket_data = (
        db.query(Ticket.id)
        .join(AssigningTicket, AssigningTicket.ticket_id == Ticket.id)
        .filter(AssigningTicket.assigned_to_emp_id.in_(list_of_employee_ids)).all()
    )
    list_of_ticket_ids = [data[0] for data in ticket_data]

    if ticket_id not in list_of_ticket_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This ticket is not belongs to you"
        )
    return


        
    