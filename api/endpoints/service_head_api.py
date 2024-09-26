from fastapi import *
from schemas import *
from models import *
from sqlalchemy.orm import *
from typing import Annotated
from api.deps import *
from crud import *
from typing import *

router = APIRouter()

@router.post("/service_head/create/ticket",response_model=Message)
async def createTicketByHead(
                            db: Annotated[Session, Depends(get_db)],
                            current_user: Annotated[User, Depends(get_current_service_head)],
                            data_in: TicketIn  
):
    """
    Admin and Service head can create ticket
    """
    ticket_data = Ticket(
        **data_in.dict(),
        created_by_user_id = current_user.id
    )
    db.add(ticket_data)
    db.commit()
    db.refresh(ticket_data)
    return {"message": "Successfully created !!!"}

@router.post("/service_head/create_employee")
async def createEmployeeByHead(
                            db: Annotated[Session, Depends(get_db)],
                            current_user: Annotated[User, Depends(get_current_service_head)],
                            obj_in: EmployeeInUnderHead
):
    """
    Here service head can create service engineer
    
     - **Name**: Required
    - **Email**: Required/Unique
    - **Password**: Required
    - **phone number**: Required/ Should be 10 digit
    """
    user = getUserByEmail(db=db, email=obj_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Email id is already exists"
        )
    emp_id = createEmployeeId(db=db)
    create_emp = User(
        id = emp_id,
        name = obj_in.name,
        email = obj_in.email,
        password = get_password_hash(obj_in.password),
        phone_number = obj_in.phone_number,
        destination_id = 3,
        report_to = current_user.id
    )
    db.add(create_emp)
    db.commit()
    return {"message":f"Successfully created {create_emp.id}"}



@router.get("/service_head/view_all_tickets",response_model=list[TicketsOut])
async def showAllTicket(
                        db: Annotated[Session, Depends(get_db)],
                        current_user: Annotated[User, Depends(get_current_service_head)]
):
    """
    Here, Admin and Service head can see the ticket's 
    """
    db_data = db.query(Ticket).outerjoin(
        AssigningTicket,
        Ticket.id == AssigningTicket.ticket_id
    ).filter(
        AssigningTicket.ticket_id.is_(None)  
    ).order_by(Ticket.id.desc()).all()
    if not db_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tickets"
        )
    return db_data
    
@router.get("/service_head/employee_under_me",response_model=list[EmployeeUnderHeadResponse])
async def empUnderServiceHead(
                     db: Annotated[Session, Depends(get_db)],
                     current_user: Annotated[User, Depends(get_current_service_head)]
): 
    return db.query(User).filter(User.report_to == current_user.id).all()


@router.post("/service_head/assign/ticket",response_model=Message)
async def assignTicket(
                     db: Annotated[Session, Depends(get_db)],
                     current_user: Annotated[User, Depends(get_current_service_head)],
                     employee_id: Annotated[str, Query(...)],
                     ticket_id: Annotated[int, Query(...)]
):
    checkEmployeeUnderHead(db=db,employee_id=employee_id,service_head=current_user)
    checkTicket(db=db,ticket_id=ticket_id)
    return assignTicketToEmp(db=db,employee_id=employee_id,service_head=current_user,ticket_id=ticket_id)

@router.get("/service_head/status_under_my_ticket",response_model=list[TicketStatusResponse])
async def statusUnderMyTickets(
                     db: Annotated[Session, Depends(get_db)],
                     current_user: Annotated[User, Depends(get_current_service_head)]
):
    emp_ids = db.query(User.id).filter(User.report_to == current_user.id).all()
    list_of_employee_ids = [data[0] for data in emp_ids]

    ticket_data = (
        db.query(Ticket)
        .join(AssigningTicket, AssigningTicket.ticket_id == Ticket.id)
        .filter(AssigningTicket.assigned_to_emp_id.in_(list_of_employee_ids))
        .order_by(Ticket.id.desc()).all()
    )
    if not ticket_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="O tickets under you"
        )

    response = []
    
    for data in ticket_data:
        ticket_response = {
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
        response.append(ticket_response)

    return response

@router.get("/service_head/{ticket_id}/status",response_model=TicketStatusResponse)
async def showSingleTicketStatus(
                     db: Annotated[Session, Depends(get_db)],
                     current_user: Annotated[User, Depends(get_current_service_head)],
                     ticket_id: int
):
    checkTicketUnderHead(db=db,current_user=current_user,ticket_id=ticket_id)
    return getSingleTicketStatus(db=db,ticket_id=ticket_id)

@router.get("/service_head/{employee_id}/work_report/",response_model=list[WorkReportOut])
async def showWorkReportToHead(
                    db: Annotated[Session, Depends(get_db)],
                    current_user: Annotated[User, Depends(get_current_service_head)],
                    emp_id: str
):
    emp_data = db.query(User).filter(and_(User.id == emp_id,User.report_to == current_user.id)).first()
    if not emp_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found or this employee is not belongs to you"
        )
    report = getWorkReport(db=db,emp_in=emp_data)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No reports"
        )
    return report

@router.get("/service_head/{ticket_id}/material_request",response_model=list[MaterialResponse])
async def showMaterialForTicket(
                    db: Annotated[Session, Depends(get_db)],
                    current_user: Annotated[User, Depends(get_current_service_head)],
                    ticket_id: int
):
    checkTicketUnderHead(db=db,current_user=current_user,ticket_id=ticket_id)

    db_ticket = db.query(
        Ticket.id,
        Material.material_name,
        func.sum(MaterialRequest.units)  
    ).join(
        MaterialRequest,
        MaterialRequest.ticket_id == Ticket.id,
    ).join(
        Material,
        Material.id == MaterialRequest.material_id
    ).group_by(Material.material_name, Ticket.id).filter(Ticket.id == ticket_id).all() 

    if not db_ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No items requested"
        )
    
    list_of_items = []
    for data in db_ticket:
        ticket_data = {
            "material_name":data[1],
            "material_count":data[2]
        }
        list_of_items.append(ticket_data)
    return list_of_items

# @router.get("/service_head/show_travel_expense")
# async def showTravelExpense(
#                     db: Annotated[Session, Depends(get_db)],
#                     current_user: Annotated[User, Depends(get_current_service_head)],
# ):
#     emp_ids = db.query(User.id).filter(User.report_to == current_user.id).all()
#     list_of_employee_ids = [data[0] for data in emp_ids]
    
#     expense = db.query(
#         Expense.description,
#         Expense.amount,
#         Expense.ticket_id
#     ).all()

@router.get("/service_head/tickets/travel_expenses",response_model=list[ExpenseDetailsOut])
async def show_expenses_for_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_service_head)
):
   
    emp_ids = db.query(User.id).filter(User.report_to == current_user.id).all()
    list_of_employee_ids = [data[0] for data in emp_ids]
    
    if len(list_of_employee_ids) <= 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No employees under you"
        )
    
    employee_user = aliased(User)
    approver_user = aliased(User)

    db_expenses = db.query(
        Expense.id.label("expense_id"),
        Expense.ticket_id,
        Expense.description,
        Expense.amount,
        Expense.approved_status,
        approver_user.name.label("approved_by"),  
        employee_user.name.label("employee_name")  
    ).join(
        employee_user, employee_user.id == Expense.emp_id  
    ).outerjoin(
        approver_user, approver_user.id == Expense.approved_by  
    ).filter(
        Expense.emp_id.in_(list_of_employee_ids)
    ).all()

    if not db_expenses:
        raise HTTPException(status_code=404, detail="No expense details found")

    
    ticket_expenses = {}

    for exp in db_expenses:
        ticket_id = exp[1]

        if ticket_id not in ticket_expenses:
            ticket_expenses[ticket_id] = {
                "ticket_id": ticket_id,
                "expenses": [],
                "total_amount": 0,
                "total_amount_approved": 0
            }

        ticket_expenses[ticket_id]["total_amount"] += exp[3]
        if exp[4]:  
            ticket_expenses[ticket_id]["total_amount_approved"] += exp[3]

        ticket_expenses[ticket_id]["expenses"].append(ExpenseDetails(
            expense_id=exp[0],
            description=exp[2],
            amount=exp[3],
            approved_status=exp[4],
            approved_by=exp[5] if exp[4] else None,
            employee_name=exp[6]
        ))

    return list(ticket_expenses.values())



@router.put("/service_head/tickets/travel_expenses/{expense_id}/approve")
async def show_expenses_for_tickets(*,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_service_head),
    expense_id: int
):
    emp_ids = db.query(User.id).filter(User.report_to == current_user.id).all()
    list_of_employee_ids = [data[0] for data in emp_ids]
    
    if len(list_of_employee_ids) <= 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No employees under you"
        )
    db_expense = db.query(Expense).filter(
        and_(
            Expense.id == expense_id,
            Expense.emp_id.in_(list_of_employee_ids)
        )
    ).one_or_none()
    
    if not db_expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Id not found")
    if db_expense.approved_status:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Already approved")
    
    return updateExpense(db=db,expense_in=db_expense,updater=current_user)
    




    
    
    