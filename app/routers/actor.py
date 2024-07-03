from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas import actor as schemas
from app.services import actor as services

from app.dependencies import get_db, Auth

router = APIRouter(prefix="/actors", tags=["Actor"], dependencies=[Depends(Auth())])

@router.get("/", response_model=list[schemas.Actor])
def get_actors(skip: int = 0, limit: int = 10, db = Depends(get_db)):
    return services.get_actors(db, skip, limit)

@router.get("/{actor_id}", response_model=schemas.Actor)
def get_actor(actor_id: int, db = Depends(get_db)):
    actor = services.get_actor(db, actor_id)
    if not actor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Actor not found.")
    return actor

@router.post("/", response_model=schemas.Actor)
def create_actor(actor: schemas.ActorCreate, db = Depends(get_db)):
    return services.create_actor(db, actor)

@router.put("/{actor_id}", response_model=schemas.Actor)
def update_actor(actor_id: int, actor: schemas.ActorCreate, db = Depends(get_db)):
    return services.update_actor(db, actor_id, actor)

@router.delete("/{actor_id}")
def delete_actor(actor_id: int, db = Depends(get_db)):
    services.delete_actor(db, actor_id)
    return JSONResponse({"detail": "Actor deleted successfully."})
