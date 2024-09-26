from fastapi import APIRouter,Depends,HTTPException,status
from schemas import *
from api.deps import *
from sqlalchemy.orm import Session
from typing import Annotated
from crud import *

router = APIRouter()

@router.post("/super_user/create_employee",response_model=Message)
async def create(
                 db: Annotated[Session, Depends(get_db)],
                 data_in: EmployeeIn,
                 current_user: Annotated[User ,Depends(get_current_active_superuser)]
):
    """
    Here , Admin can create a Employee (Admin, Service Head, Service Employee)
    
    - **Name**: Required
    - **Email**: Required/Unique
    - **Password**: Required
    - **Destination Id**: Required(1-> Admin, 2-> Service Head, 3-> Service Employee)
    - **phone number**: Required/ Should be 10 digit
    - **Report to**: Can be null/you can't give report to person destination to (the user you created) eg-report-to-person: **20IT001(ADMIN)**
    """
    # check email is unique
    user = getUserByEmail(db=db, email=data_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Email id is already exists"
        )
    # check destination id   
    if not checkDestinationId(db=db, id=data_in.destination_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Destination is not found"
        )
    # check report_to person is valid or not,
    # report to person value you should not be same and low
    if data_in.report_to:
        report_to_person = getEmpById(db=db,id=data_in.report_to)
        
        if not report_to_person:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= "Report to person not found"
            )
        if report_to_person.destination_id >= data_in.destination_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= "Report to value should be high or destination should be low"
            )
    else:
        data_in.report_to = None 
        
    # create_employee
    return createEmployee(db=db,obj_in=data_in)

@router.get("/super_user/all_employee",response_model=list[UserResponse] | str)
async def showAllEmployee(
                        db: Annotated[Session, Depends(get_db)],
                        current_user: Annotated[User ,Depends(get_current_active_superuser)] 
):
    """
    Here , Admin can see (admin,service head,service employee)all employee details
    """
    return getAllEmployee(db=db)

@router.put("/super_user/{employee_id}/update",response_model=Message)
async def updateAllDetails(
                           db: Annotated[Session, Depends(get_db)],
                           employee_id: str,
                           current_user: Annotated[User ,Depends(get_current_active_superuser)],
                           data_in: UpdateUserIn
                           
): 
    """
    **Here admin can edit already exists employee**
    
    - **name**:(Not required)
    - **email**:(Not required)
    - **password**:(Not required)
    - **Destination_id**:(Not required)
    - **phone number**:(Not required)
    - **report_to**:(Not required)
    - **is_active**:(Not required)
    """
    db_emp = getEmpById(db=db,id=employee_id)
    if not db_emp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "User not Found"
        )
    return updateUser(db=db,update_user_in=data_in,exists_user_data=db_emp)

@router.get("/super_user/all_service_head/",response_model=list[UserResponse] | str)
async def showAllServiceHead(
                        db: Annotated[Session, Depends(get_db)],
                        current_user: Annotated[User ,Depends(get_current_active_superuser)] 
):
    """
    **Here, Admin see all service head's**
    """
    return getAllEmployeeByDestination(db=db,destination_id_in=2)

@router.get("/super_user/{service_head_id}/under_him",response_model=list[EmployeeUnderHeadResponse] | str)
async def showEmployeeUnderServiceHead(
                        db: Annotated[Session, Depends(get_db)],
                        current_user: Annotated[User ,Depends(get_current_active_superuser)],
                        service_head_id: str
):
    """
    **Here admin, can see the all employee's under particular service head - By providing service head id eg: (20IT001)**
    """
    db_data = db.query(User).filter(User.report_to == service_head_id).all()
    if not db_data:
        return "No Data"
    return db_data

@router.get("/super_user/all_service_engineers/",response_model=list[UserResponse] | str)
async def showAllServiceEngineer(
                        db: Annotated[Session, Depends(get_db)],
                        current_user: Annotated[User ,Depends(get_current_active_superuser)] 
):
    """
    **Here, admin can see all service engineer**
    """
    return getAllEmployeeByDestination(db=db,destination_id_in=3)


@router.get("/super_user/{employee_id}/details",response_model=UserResponse)
async def getEmpDetails(
                       db: Annotated[Session, Depends(get_db)],
                       employee_id: str,
                       current_user: Annotated[User ,Depends(get_current_active_superuser)],
):
    """
    **Here admin can see particular employee details** 
    """
    db_emp = getDetailsOfSingleEmp(db=db,id=employee_id)
    if not db_emp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "User not Found"
        )
    return db_emp

@router.get("/super_user/{employee_id}/work_report/",response_model=list[WorkReportOut])
async def showWorkReportToHead(
                    db: Annotated[Session, Depends(get_db)],
                    current_user: Annotated[User, Depends(get_current_active_superuser)],
                    emp_id: str
):
    emp_data = getEmpById(db=db,id=emp_id)
    if not emp_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    report = getWorkReport(db=db,emp_in=emp_data)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No reports"
        )
    return report

@router.post("/super_user/create_material",response_model=Message)
async def createMaterial(
                        db: Annotated[Session, Depends(get_db)],
                        current_user: Annotated[User ,Depends(get_current_active_superuser)],
                        material_in: MaterialIn 
):
    material_create = Material(**material_in.dict())
    db.add(material_create)
    db.commit()
    return {"message":"Successfully added"}

@router.get("/super_user/all_materials",response_model=list[MaterialAdminResponse])
async def getMaterialsAdmin(
                       db: Annotated[Session, Depends(get_db)],
                       current_user: Annotated[User, Depends(get_current_active_superuser)],
):
    db_material = db.query(Material.id,Material.material_name,Material.amount).all()
    if not db_material:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No materials")
    return db_material

@router.put("/super_user/{material_id}/update",response_model=Message)
async def updateMaterialAdmin(
                       db: Annotated[Session, Depends(get_db)],
                       current_user: Annotated[User, Depends(get_current_active_superuser)],
                       material_id: int,
                       material_in: MaterialUpdateIn 
):
    db_material = db.query(Material).filter(Material.id == material_id).one_or_none()
    if not db_material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material id not found"
        )
    if material_in.material_name != None:
        db_material.material_name = material_in.material_name
    if material_in.amount != None:
        db_material.amount = material_in.amount
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return {"message":"Successfully updated !!"}
    

@router.post("/super_user/create/ticket",response_model=Message)
async def createTicketByHead(
                            db: Annotated[Session, Depends(get_db)],
                            current_user: Annotated[User, Depends(get_current_active_superuser)],
                            data_in: TicketIn  
):
    """
    Admin can create ticket
    """
    ticket_data = Ticket(
        **data_in.dict(),
        created_by_user_id = current_user.id
    )
    db.add(ticket_data)
    db.commit()
    db.refresh(ticket_data)
    return {"message": "Successfully created !!!"}

@router.get("/super_user/view_all_tickets",response_model=list[TicketsOut])
async def adminViewTickets(
                           db: Annotated[Session, Depends(get_db)],
                           current_user: Annotated[User, Depends(get_current_active_superuser)]
):
    """
    Here, Admin an see all tickets, newly created tickets first. 
    """
    db_ticket = db.query(Ticket).order_by(Ticket.id.desc()).all()
    if not db_ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tickets"
        )
    return db_ticket

@router.post("/super_user/assign_ticket/",response_model=Message)
async def adminAssignTicket(
                            db: Annotated[Session, Depends(get_db)],
                            current_user: Annotated[User, Depends(get_current_active_superuser)],
                            employee_id: str,
                            ticket_id: int
):
    checkValidEmpAndServiceEngineerOrNot(db=db, emp_id=employee_id)
    checkTicket(db=db,ticket_id=ticket_id)
    return assignTicketToEmp(db=db,employee_id=employee_id,service_head=current_user,ticket_id=ticket_id)


@router.get("/super_user/view_all_tickets/{ticket_id}/",response_model=TicketStatusResponse)
async def getDetailsOfSingleTicket(
                           db: Annotated[Session, Depends(get_db)],
                           current_user: Annotated[User, Depends(get_current_active_superuser)],
                           ticket_id: Annotated[int, Path(...)]
):
    
    return getSingleTicketStatus(db=db,ticket_id=ticket_id)
        

@router.get("/super_user/{ticket_id}/material_request",response_model=list[MaterialResponse])
async def showMaterialForTicket(
                    db: Annotated[Session, Depends(get_db)],
                    current_user: Annotated[User, Depends(get_current_active_superuser)],
                    ticket_id: int
):

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
            detail="Ticket not found"
        )
    
    list_of_items = []
    for data in db_ticket:
        ticket_data = {
            "material_name":data[1],
            "material_count":data[2]
        }
        list_of_items.append(ticket_data)
    return list_of_items

@router.get("/super_user/tickets/travel_expenses",response_model=list   [ExpenseDetailsOut])
async def showTravelExpenses(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_superuser)]
):
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

@router.put("/super_user/tickets/travel_expenses/{expense_id}/approve",response_model=Message)
async def approveExpense(
                       db: Annotated[Session, Depends(get_db)],
                       current_user: Annotated[User, Depends(get_current_active_superuser)],
                       expense_id: int
):
    db_expense_status = db.query(Expense).filter(Expense.id == expense_id).one_or_none()
    
    if not db_expense_status:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Id not found")
    if db_expense_status.approved_status:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Already approved")
    return updateExpense(db=db,expense_in=db_expense_status,updater=current_user)

@router.get("/super_user/{ticket_id}/report",response_model=Message)
async def ticketReport(
                     db: Annotated[Session, Depends(get_db)],
                     current_user: Annotated[User, Depends(get_current_active_superuser)],
                     ticket_id: int,
                     engineer_price: Annotated[int , Query(...)]
):
    return createReport(db=db,ticket_id=ticket_id,engineer_charge=engineer_price)

@router.get("/super_user/admin/dashboard",response_model=DashboardResponse)
async def adminDashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser)
):
    current_year = datetime.now().year
    current_month = datetime.now().month
    total_tickets = db.query(
        extract('month', Ticket.created_at).label('month'),
        func.count(Ticket.id).label('total_tickets')
    ).filter(
        extract('year', Ticket.created_at) == current_year,
        extract('month', Ticket.created_at) <= current_month  
    ).group_by(
        extract('month', Ticket.created_at)
    ).all()

    completed_tickets = db.query(
        extract('month', Ticket.created_at).label('month'),
        func.count(Ticket.id).label('completed_tickets')
    ).join(TicketStatus).filter(
        TicketStatus.status_of_ticket == True,
        extract('year', Ticket.created_at) == current_year,
        extract('month', Ticket.created_at) <= current_month  
    ).group_by(
        extract('month', Ticket.created_at)
    ).all()
    
    in_process_tickets = []
    for i in range(len(completed_tickets)):
        this_tuple = (completed_tickets[i][0],total_tickets[i][1]-completed_tickets[i][1])
        in_process_tickets.append(this_tuple)

    dummy_data = {}
    for month in range(1, current_month + 1):
        dummy_data[month] = {
            "total_tickets": 0,
            "completed_tickets": 0,
            "in_process_tickets": 0
        }            

    for row in total_tickets:
        dummy_data[row[0]]["total_tickets"] = row[1]

    for row in completed_tickets:
        dummy_data[row[0]]["completed_tickets"] = row[1]  
   
    for row in in_process_tickets:
        dummy_data[row[0]]["in_process_tickets"] = row[1]

    return DashboardResponse(month_wise_report=dummy_data)  


        
    






