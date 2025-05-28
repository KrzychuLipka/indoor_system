from sqlalchemy.orm import Session
from models import Person
from schemas import PersonCreate, PositionUpdate
from utils import validate_wkt

def create_person(db: Session, person_data: PersonCreate) -> Person:
    validate_wkt(person_data.position)
    person = Person(
        first_name=person_data.first_name,
        last_name=person_data.last_name,
        person_type_id=person_data.person_type_id,
        position=f"SRID=2180;{person_data.position}"
    )
    db.add(person)
    db.commit()
    db.refresh(person)
    return person

def get_all_people(db: Session):
    return db.query(Person).all()

def get_person(db: Session, person_id: int):
    return db.query(Person).filter(Person.id == person_id).first()

def update_person_position(db: Session, person_id: int, position_update: PositionUpdate):
    person = get_person(db, person_id)
    if not person:
        return None
    validate_wkt(position_update.position)
    person.position = f"SRID=2180;{position_update.position}"
    db.commit()
    db.refresh(person)
    return person

def delete_person(db: Session, person_id: int):
    person = get_person(db, person_id)
    if person:
        db.delete(person)
        db.commit()
    return person
