from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from shapely import wkb, wkt
from fastapi.encoders import jsonable_encoder
from models import Person, PersonCreate, PositionUpdate
from db_config import ORMBaseModel, db_engine, get_db_session
from encoders import to_dict
import time

max_retries = 10
for i in range(max_retries):
    try:
        ORMBaseModel.metadata.create_all(bind=db_engine)
        print("✅ Database connected and tables created.")
        break
    except OperationalError:
        print(f"⏳ Database not ready (attempt {i+1}/{max_retries}), retrying in 2s...")
        time.sleep(2)
else:
    print("❌ Could not connect to the database. Exiting.")
    raise RuntimeError("Database not available")

app = FastAPI()

@app.post("/users")
def create_user(person_create: PersonCreate, db_session: Session = Depends(get_db_session)):
    try:
        position_geom = wkt.loads(person_create.position)
    except Exception:
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
    return jsonable_encoder({
        "id": new_person.id,
        "first_name": new_person.first_name,
        "last_name": new_person.last_name,
        "person_type_id": new_person.person_type_id,
        "position": {
            "x": position_geom.x,
            "y": position_geom.y
        }
    })

@app.get("/users")
def get_all_users(db_session: Session = Depends(get_db_session)):
    people = db_session.query(Person).all()
    result = []
    for person in people:
        person_dict = to_dict(person)
        if person.position:
            position_geom = wkb.loads(bytes(person.position.data))
            person_dict['position'] = {
                "x": position_geom.x,
                "y": position_geom.y
            }
        result.append(person_dict)
    return jsonable_encoder(result)

@app.get("/users/{person_id}/position")
def get_user_position(person_id: int, db_session: Session = Depends(get_db_session)):
    person = db_session.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="User not found")
    if not person.position:
        raise HTTPException(status_code=404, detail="Position not available")
    position_geom = wkb.loads(bytes(person.position.data))
    return jsonable_encoder({
        "position": {
            "x": position_geom.x,
            "y": position_geom.y
        }
    })

@app.put("/users/{person_id}/position")
def update_position(person_id: int, position_update: PositionUpdate, db_session: Session = Depends(get_db_session)):
    person = db_session.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="User not found")    
    try:
        _ = wkt.loads(position_update.position)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid position WKT format")
    person.position = f"SRID=2180;{position_update.position}"
    db_session.commit()
    db_session.refresh(person)
    return jsonable_encoder({
        "message": "Position updated",
        "id": person.id,
        "position": position_update.position
    })

@app.delete("/users/{person_id}")
def delete_user(person_id: int, db_session: Session = Depends(get_db_session)):
    person = db_session.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="User not found")
    db_session.delete(person)
    db_session.commit()
    return jsonable_encoder({"message": "User deleted"})
