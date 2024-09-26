from sqlalchemy.orm import Session
from fpdf import FPDF
from models import *
from fastapi import *

def createReport(db: Session, ticket_id: int, engineer_charge: int):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).one_or_none()
    
    
    if not db_ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
        
    if not db_ticket.assigned_ticket:
          raise HTTPException(
              status_code=status.HTTP_403_FORBIDDEN,
              detail="Ticket not assigned"
          )
    if not db_ticket.status:
        raise HTTPException(
              status_code=status.HTTP_403_FORBIDDEN,
              detail="Engineer not visited the place"
          )
    
    ticket_created_by = db_ticket.customer_name
    ticket_engineer = db_ticket.assigned_ticket.assigned_to.name 
    ticket_address = db_ticket.address
    ticket_assigned_by = db_ticket.assigned_ticket.assigned_by.name
    
    ticket_status = "Completed" if db_ticket.status.status_of_ticket else "In Progress"

    
    list_of_materials = []

    for requested_item in db_ticket.requested_items:
        material_name = requested_item.material.material_name
        material_amount = requested_item.material.amount
        material_units = requested_item.units
        total_cost = material_amount * material_units

        list_of_materials.append({
            'name': material_name,
            'amount': material_amount,
            'units': material_units,
            'total': total_cost
        })
    

    travel_charge = sum(expense.amount for expense in db_ticket.expenses if expense.approved_status)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Ticket Report", ln=True, align='C')
    pdf.set_font("Arial","B", size=12)
    pdf.cell(200, 7, txt=f"Customer: {ticket_created_by}", ln=True)
    pdf.cell(200, 7, txt=f"Ticket Id: {ticket_id}", ln=True)
    pdf.cell(200, 7, txt=f"Address: {ticket_address}", ln=True)
    pdf.cell(200, 7, txt=f"Engineer: {ticket_engineer}", ln=True)
    pdf.cell(200, 7, txt=f"Assigned_by: {ticket_assigned_by}", ln=True)
    pdf.cell(200, 7, txt=f"Ticket Status: {ticket_status}", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(90, 10, txt="Item", border=1, align='C')
    pdf.cell(30, 10, txt="Amount", border=1, align='C')
    pdf.cell(30, 10, txt="Unit", border=1, align='C')
    pdf.cell(40, 10, txt="Total", border=1, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    for material in list_of_materials:
        pdf.cell(90, 10, txt=material['name'], border=1)
        pdf.cell(30, 10, txt=f"{material['amount']}", border=1, align='C')
        pdf.cell(30, 10, txt=f"{material['units']}", border=1, align='C')
        pdf.cell(40, 10, txt=f"{material['total']}", border=1, align='C')
        pdf.ln(10)

    pdf.cell(90, 10, txt="Travel Charges", border=1)
    pdf.cell(30, 10, txt=f"{travel_charge}", border=1, align='C')
    pdf.cell(30, 10, txt="", border=1)
    pdf.cell(40, 10, txt=f"{travel_charge}", border=1, align='C')
    pdf.ln(10)

    pdf.cell(90, 10, txt="Engineer Charges", border=1)
    pdf.cell(30, 10, txt=f"{engineer_charge}", border=1, align='C')
    pdf.cell(30, 10, txt="", border=1)
    pdf.cell(40, 10, txt=f"{engineer_charge}", border=1, align='C')
    pdf.ln(10)

    total_charge = travel_charge + engineer_charge + sum(item['total'] for item in list_of_materials)
    
    pdf.cell(150, 10, txt="Total", border=1, align='R')
    pdf.cell(40, 10, txt=f"{total_charge}", border=1, align='C')

    pdf_output_path = f"Ticket_Report_{ticket_id}.pdf"
    pdf.output(pdf_output_path)
    print(f"PDF created: {pdf_output_path}")
    
    return {"message":"Report sended"}


