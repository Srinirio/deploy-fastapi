from sqlalchemy.orm import *    
from models import *
from fastapi import *
from schemas import *
import os
import uuid


"""
Creating expense details in Db
"""
def createExpense(db: Session,
                  ticket_id: int,
                  description: int,
                  amount: float,
                  emp_id: User,
                  image: UploadFile
                  ):
    unique_filename = None
    if image:
       image_dir = "image"
       unique_filename = f"{uuid.uuid4()}.jpg"
       image_path = os.path.join(image_dir, unique_filename)
       with open(image_path, "wb") as buffer:
            buffer.write(image.file.read()) 
            
    expense = Expense(
        description = description,
        amount = amount,
        emp_id = emp_id.id,
        ticket_id = ticket_id,
        image = unique_filename
    )
    db.add(expense)
    db.commit()
    
    return {"message":"Successfully Added !!"}


def checkMaterial(db: Session,
                  material_id: int
):
    db_material = db.query(Material).filter(Material.id == material_id).one_or_none()
    if not db_material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found"
        )

"""
Material request data adding in DB
"""
def createMaterialRequest(db: Session,
                          current_user: User,
                          ticket_id: int,
                          material_id: int,
                          units: int
):
    checkMaterial(db=db,material_id=material_id)
    db_data = MaterialRequest(
        units = units,
        material_id = material_id,
        ticket_id = ticket_id,
        emp_id = current_user.id
    )
    db.add(db_data)
    db.commit()
    return {"message":"Successfully requested !!"}

"""
Create Work_report
"""
def createWorkReport(db: Session,
                    current_user: User,
                    data_in: WorkReportIn
):
    db_work = db.query(WorkReport).filter(WorkReport.emp_id == current_user.id).order_by(WorkReport.created_at).one_or_none()
    #first work report
    if not db_work:
        create_work_report = WorkReport(
            description = data_in.description,
            ticket_id = data_in.ticket_id,
            emp_id = current_user.id
        )
        db.add(create_work_report)
        db.commit()
        db.refresh(create_work_report)
        return {"message":"Successfully work report is added !!"}
   #second work report have check
    if db_work.created_at.date() + timedelta(days=1) != data_in.created_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Please missing work report :{db_work.created_at.date()+timedelta(days=1)}"
        )
    create_work_report = WorkReport(
            description = data_in.description,
            ticket_id = data_in.ticket_id,
            emp_id = current_user.id
        )
    db.add(create_work_report)
    db.commit()
    db.refresh(create_work_report)
    return {"message":"Successfully work report is added !!"}
    
    


    

    