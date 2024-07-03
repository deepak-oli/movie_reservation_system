from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import actor as models
from app.schemas import actor as schemas

def get_actor(db:Session, actor_id:int):
    return db.query(models.Actor).filter(models.Actor.id == actor_id).first()

def get_actors(db:Session, skip:int=0, limit:int=10):
    return db.query(models.Actor).offset(skip).limit(limit).all()

def create_actor(db:Session, actor:schemas.ActorCreate):
    db_actor = db.query(models.Actor).filter(models.Actor.name.ilike(actor.name)).first()
    if db_actor:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Actor already registered.")
    
    new_actor = models.Actor(
        name=actor.name,
        image=actor.image
    )
    db.add(new_actor)
    db.commit()
    db.refresh(new_actor)
    return new_actor

def update_actor(db:Session, actor_id:int, actor:schemas.ActorCreate):
    db_actor = get_actor(db, actor_id)
    if not db_actor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Actor not found.")
    
    db_actor.name = actor.name
    db_actor.image = actor.image
    db.commit()
    db.refresh(db_actor)
    return db_actor

def delete_actor(db:Session, actor_id:int):
    db_actor = get_actor(db, actor_id)
    if not db_actor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Actor not found.")
    
    db.delete(db_actor)
    db.commit()
    return db_actor
