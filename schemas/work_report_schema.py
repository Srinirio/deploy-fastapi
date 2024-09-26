from pydantic import BaseModel
from datetime import *

class WorkReportIn(BaseModel):
    
    description: str
    ticket_id: int | None = None
    created_at: date | None = None
    
class WorkReportOut(BaseModel):
    
    created_at: datetime
    description: str
    