from sqlalchemy.orm import Session,joinedload
from sqlalchemy import and_,or_
from sqlalchemy.orm import aliased
from models import *
from schemas import *
from utils import createEmployeeId
from core.security import get_password_hash
from fastapi import *
from datetime import datetime
"""
get user by ID
"""
def getEmpById(db: Session,id: str):
    return db.query(User).filter(and_(User.id == id,User.is_active == True)).one_or_none()
"""
get user by email
"""
def getUserByEmail(db: Session, email: str):
    return db.query(User).filter(and_(User.email == email,User.is_active == True)).one_or_none()

"""
Check destination id is valid
"""
def checkDestinationId(db: Session, id: int):
    return db.query(Destination).filter(Destination.id == id).one_or_none()

"""
Create Employee in DB
"""
def createEmployee(db: Session,obj_in: EmployeeIn):
    emp_id = createEmployeeId(db=db)
    print(emp_id)
    
    db_obj = User(
        id = emp_id,
        name = obj_in.name,
        email = obj_in.email,
        password = get_password_hash(obj_in.password),
        phone_number = obj_in.phone_number,
        destination_id = obj_in.destination_id,
        report_to = None if obj_in.report_to == None else obj_in.report_to
    )
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return {"message": "Successfully Added !!"}

"""
get all employee
"""
def getAllEmployee(db: Session):
    
    report_to_user = aliased(User)

    all_employee = db.query(
        User.id,
        User.name,
        User.email,
        User.phone_number,
        Destination.destination_name.label("destination_name"), 
        report_to_user.name.label("report_to_name") 
    ).join(
        Destination, User.destination_id == Destination.id
    ).outerjoin(
        report_to_user, User.report_to == report_to_user.id 
    ).filter(
        User.is_active == True
    ).order_by(User.created_at.desc()).all()
    
    if not all_employee:
        return "No data"
    
    return all_employee

"""
Update User
"""
def updateUser(db: Session, update_user_in: UpdateUserIn, exists_user_data: User):

    if update_user_in.name is not None:
        exists_user_data.name = update_user_in.name
    if update_user_in.email is not None:
        user_email = getUserByEmail(db=db, email=update_user_in.email)
        if user_email:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Email id is already exists" 
            )
        exists_user_data.email = update_user_in.email
    if update_user_in.destination_id is not None:
        if not checkDestinationId(db=db, id=update_user_in.destination_id):
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Destination is not found"
            )
        exists_user_data.destination_id = update_user_in.destination_id
    if update_user_in.password is not None:
        print(update_user_in.password)
        exists_user_data.password = get_password_hash(update_user_in.password)
    
    if update_user_in.phone_number is not None:
        exists_user_data.phone_number = update_user_in.phone_number
    if update_user_in.report_to is not None:

        report_to_person = getEmpById(db=db,id=update_user_in.report_to)
        
        if not report_to_person:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= "Report to person not found"
            )
        if report_to_person.destination_id >= update_user_in.destination_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= "Report to value should be high or destination should be low"
            )
        
        exists_user_data.report_to = update_user_in.report_to
    if update_user_in.is_active is not None:
        exists_user_data.is_active = update_user_in.is_active
    
    exists_user_data.updated_at = datetime.now()
    db.add(exists_user_data)
    db.commit()
    db.refresh(exists_user_data)  
    return {"message": "Successfully Updated !!"}

"""
get particular employee by id
"""
def getDetailsOfSingleEmp(db: Session,id: str):
    report_to_user = aliased(User)

    emp = db.query(
        User.id,
        User.name,
        User.email,
        User.phone_number,
        Destination.destination_name.label("destination_name"), 
        report_to_user.name.label("report_to_name") 
    ).join(
        Destination, User.destination_id == Destination.id
    ).outerjoin(
        report_to_user, User.report_to == report_to_user.id 
    ).filter(
        User.is_active == True,
        User.id == id
    ).first()
    return emp

def checkValidEmpAndServiceEngineerOrNot(db: Session,emp_id: str):
    db_emp = db.query(User).filter(
        and_(User.id == emp_id,User.destination_id == 3)
        ).one_or_none()
    if not db_emp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Invalid User"
        )
    

"""
get all employee by their destination
"""
def getAllEmployeeByDestination(db: Session,destination_id_in: int):
    
    report_to_user = aliased(User)

    all_employee = db.query(
        User.id,
        User.name,
        User.email,
        User.phone_number,
        Destination.destination_name.label("destination_name"), 
        report_to_user.name.label("report_to_name") 
    ).join(
        Destination, User.destination_id == Destination.id
    ).outerjoin(
        report_to_user, User.report_to == report_to_user.id 
    ).filter(
        and_(
            User.is_active == True,
            Destination.id == destination_id_in
        )
    ).order_by(User.created_at.desc()).all()
    
    if not all_employee:
        return "No data"
     
    return all_employee

"""

"""
