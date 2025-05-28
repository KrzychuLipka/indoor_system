from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from db_config import ORMBaseModel, db_engine, get_db_session
from schemas import PersonCreate, PersonRead, PositionUpdate
from fastapi.logger import logger
from utils import wkb_to_xy, wkb_to_wkt, validate_wkt
from crud import *
import time

app = FastAPI()

# Retry DB connection
for i in range(10):
    try:
        ORMBaseModel.metadata.create_all(bind=db_engine)
        print("✅ Database connected and tables created.")
        break
    except OperationalError:
        print(f"⏳ Retry {i+1}/10...")
        time.sleep(2)
else:
    raise RuntimeError("❌ Could not connect to the database.")

@app.post("/users", response_model=PersonRead, status_code=201)
def create_user(person_create: PersonCreate, db_session: Session = Depends(get_db_session)):
    try:
        validate_wkt(person_create.position)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid position WKT format")
    new_person = Person(
        first_name=person_create.first_name,
        last_name=person_create.last_name,
        person_type_id=person_create.person_type_id,
        position=f"SRID=2180;{person_create.position}"
    )
    db_session.add(new_person)
    db_session.commit()
    db_session.refresh(new_person)
    return PersonRead(
        id=new_person.id,
        first_name=new_person.first_name,
        last_name=new_person.last_name,
        person_type_id=new_person.person_type_id,
        position=person_create.position
    )

@app.get("/users", response_model=list[PersonRead])
def get_all_users(db_session: Session = Depends(get_db_session)):
    users = db_session.query(Person).all()
    result = []
    for person in users:
        try:
            position_str = wkb_to_wkt(person.position.data) if person.position else None
            result.append(PersonRead.model_validate({
                "id": person.id,
                "first_name": person.first_name,
                "last_name": person.last_name,
                "person_type_id": person.person_type_id,
                "position": position_str
            }))
        except Exception as e:
            logger.error(f"Error processing person ID {person.id}: {e}")
    return result

@app.put("/users/{person_id}/position")
def update_position(person_id: int, position: PositionUpdate, db=Depends(get_db_session)):
    try:
        updated = update_person_position(db, person_id, position)
        if not updated:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "message": "Position updated",
            "id": updated.id,
            "position": position.position
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid WKT format")
    except Exception as e:
        logger.error(f"❌ Unexpected error while updating position: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/users/{person_id}")
def delete_user(person_id: int, db=Depends(get_db_session)):
    deleted = delete_person(db, person_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
