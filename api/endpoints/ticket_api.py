from fastapi import *
from schemas import *
from models import *
from api.deps import *
from sqlalchemy.orm import *
from typing import *

router = APIRouter()

@router.post("/create/ticket",response_model=Message)
async def createTicket(data_in: TicketIn, db: Annotated[Session, Depends(get_db)]):
    ticket_data = Ticket(
        **data_in.dict()
    )
    db.add(ticket_data)
    db.commit()
    db.refresh(ticket_data)
    
    return {"message": "Successfully created !!!"}
    
    