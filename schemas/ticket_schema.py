from pydantic import BaseModel
from datetime import datetime

class TicketIn(BaseModel):
    customer_name: str
    address: str
    description: str
    company_name: str
    
    
class TicketsOut(TicketIn):
    id: int
    created_at: datetime
    
class TicketStatusResponse(BaseModel):
    ticket_id: int
    customer_name: str
    company_name: str
    address: str
    ticket_created_date: datetime
    ticket_created_by: str | None = None
    ticket_assigned_by: str | None = None
    ticket_assigned_to: str | None = None
    expected_date_to_complete: str | datetime | None = None
    status_of_ticket: bool | str | None = None
    completed_date: datetime | str | None = None
    priority: int | str | None = None

    class Config:
        orm_mode = True 

class TicketCounts(BaseModel):
    total_tickets: int
    completed_tickets: int
    in_process_tickets: int

class DashboardResponse(BaseModel):
    month_wise_report: dict[int, TicketCounts]
