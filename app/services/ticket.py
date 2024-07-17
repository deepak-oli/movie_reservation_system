from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import ticket as models
from app.schemas import ticket as schemas

def create_ticket(db: Session, ticket: schemas.TicketCreate, user_id: int):
    new_ticket = models.Ticket(**ticket.model_dump(), user_id=user_id)
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

def get_ticket(db: Session, ticket_id: int):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found.")
    return ticket

def get_tickets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ticket).offset(skip).limit(limit).all()

def update_ticket(db: Session, ticket_id: int, ticket: schemas.TicketUpdate):
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found.")
    for key, value in vars(ticket).items():
        setattr(db_ticket, key, value)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def delete_ticket(db: Session, ticket_id: int):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found.")
    db.delete(ticket)
    db.commit()
    return ticket

def get_ticket_by_show_id(db: Session, show_id: int):
    tickets = db.query(models.Ticket).filter(models.Ticket.show_id == show_id).all()
    return tickets

def get_ticket_by_user_id(db: Session, user_id: int):
    tickets = db.query(models.Ticket).filter(models.Ticket.user_id == user_id).all()
    return tickets
