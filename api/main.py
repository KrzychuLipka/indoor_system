from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from db_config import get_db_session, db_engine
from schemas import PersonCreate, PersonRead, PositionUpdate
from models import ORMBaseModel
from crud import (
    create_person,
    get_all_people,
    get_person,
    update_person_position,
    delete_person,
)

app = FastAPI()

ORMBaseModel.metadata.create_all(bind=db_engine)

@app.post("/users", response_model=PersonRead, status_code=201)
def create_user(person_data: PersonCreate, db: Session = Depends(get_db_session)):
    person = create_person(db, person_data)
    return person

@app.get("/users", response_model=list[PersonRead])
def read_users(db: Session = Depends(get_db_session)):
    return get_all_people(db)

@app.get("/users/{person_id}", response_model=PersonRead)
def read_user(person_id: int, db: Session = Depends(get_db_session)):
    person = get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="User not found")
    return person

@app.put("/users/{person_id}/position", response_model=PersonRead)
def update_position(person_id: int, position: PositionUpdate, db: Session = Depends(get_db_session)):
    person = update_person_position(db, person_id, position)
    if not person:
        raise HTTPException(status_code=404, detail="User not found")
    return person

@app.delete("/users/{person_id}")
def remove_user(person_id: int, db: Session = Depends(get_db_session)):
    deleted = delete_person(db, person_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
