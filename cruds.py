from sqlalchemy.orm import Session
from models import Jersey
from schemas import JerseyCreate

def get_jerseys(db: Session):
    return db.query(Jersey).all()

def create_jersey(db: Session, jersey: JerseyCreate):
    db_jersey = Jersey(**jersey.dict())
    db.add(db_jersey)
    db.commit()
    db.refresh(db_jersey)
    return db_jersey

def get_jersey(db: Session, jersey_id: int):
    return db.query(Jersey).filter(Jersey.id == jersey_id).first()

def update_jersey(db: Session, jersey_id: int, jersey_data: JerseyCreate):
    db.query(Jersey).filter(Jersey.id == jersey_id).update(jersey_data.dict())
    db.commit()
    return jersey_data

def delete_jersey(db: Session, jersey_id: int):
    db.query(Jersey).filter(Jersey.id == jersey_id).delete()
    db.commit()
    return {"message": "Jersey deleted successfully"}
