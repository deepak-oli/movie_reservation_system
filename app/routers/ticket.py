from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse


from app.dependencies import get_db, Auth

from app.services import ticket as service
from app.schemas import ticket as schema
from app.schemas.user import  AuthUser


router = APIRouter(prefix="/tickets", tags=["Ticket"], dependencies=[Depends(Auth())])


@router.post("/", response_model=schema.Ticket)
def create_ticket(ticket: schema.TicketCreate, db: Session = Depends(get_db), user: AuthUser = Depends(Auth())):
    return service.create_ticket(db, ticket, user.id)

@router.get("/{ticket_id}", response_model=schema.Ticket)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    return service.get_ticket(db, ticket_id)

# @router.get("/", response_model=list[schema.Ticket])
# def get_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return service.get_tickets(db, skip, limit)

@router.put("/{ticket_id}", response_model=schema.Ticket,)
def update_ticket(ticket_id: int, ticket: schema.TicketUpdate, db: Session = Depends(get_db)):
    return service.update_ticket(db, ticket_id, ticket)

@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    service.delete_ticket(db, ticket_id)
    return JSONResponse({
        "detail": "Ticket deleted successfully."
    })

@router.get("/show/{show_id}", response_model=list[schema.Ticket])
def get_ticket_by_show_id(show_id: int, db: Session = Depends(get_db)):
    return service.get_ticket_by_show_id(db, show_id)

@router.get("/user/{user_id}", response_model=list[schema.Ticket])
def get_ticket_by_user_id(user_id: int, db: Session = Depends(get_db)):
    return service.get_ticket_by_user_id(db, user_id)


