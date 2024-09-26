from sqlalchemy.orm import *
from models import *
from fastapi import *
from sqlalchemy import *
"""
check ticket id and assigned or not
"""
def checkTicket(db: Session,ticket_id: int):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).one_or_none()
    if not db_ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found !!"
        )
    
    already_assign=db.query(AssigningTicket).filter(AssigningTicket.ticket_id == ticket_id).one_or_none()
    
    if already_assign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket already assigned !!"
        )
   
"""
check the id is belongs to current employee or not
""" 
def checkTicketBelongsToHim(db: Session, ticket_id: int, current_user: User):
    db_data = db.query(
        AssigningTicket
    ).filter(
        and_(AssigningTicket.ticket_id == ticket_id,
             AssigningTicket.assigned_to_emp_id == current_user.id
             )
    ).one_or_none()
    if not db_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket is not found"
        )
    return 


def getSingleTicketStatus(db: Session,ticket_id: int):
    
    data = db.query(Ticket).filter(Ticket.id == ticket_id).one_or_none()
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    response = {
        "ticket_id": data.id,
        "customer_name": data.customer_name,
        "company_name": data.company_name,
        "address": data.address,
        "ticket_created_date": data.created_at,
        "ticket_created_by": data.created_by.name if data.created_by else "customer",
        "ticket_assigned_by": data.assigned_ticket.assigned_by.name if data.assigned_ticket and data.assigned_ticket.assigned_by else "not assigned",
        "ticket_assigned_to": data.assigned_ticket.assigned_to.name if data.assigned_ticket and data.assigned_ticket.assigned_to else "not assigned",
        "expected_date_to_complete": data.status.expected_date_to_complete if data.status else "Engineer did not visit the place",
        "status_of_ticket": (
        "completed" if data.status and data.status.status_of_ticket else "not completed" 
        if data.status else "Engineer did not visit the place"
        ),
        "completed_date": data.status.completed_date if data.status else "Engineer did not visit the place",
        "priority": (
        "High" if data.status and data.status.priority == 1 else
        "Medium" if data.status and data.status.priority == 2 else
        "Low" if data.status and data.status.priority == 3 else 
        "Engineer did not visit the place"
         )
    }
    return response