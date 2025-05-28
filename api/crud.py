from sqlalchemy.orm import Session
from models import Person
from schemas import PersonCreate, PositionUpdate

def create_person(db: Session, person_data: PersonCreate) -> Person:
    person = Person(
        first_name=person_data.first_name,
        last_name=person_data.last_name,
        person_type_id=person_data.person_type_id,
        lat=person_data.lat,
        lon=person_data.lon
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
    person.lat = position_update.lat
    person.lon = position_update.lon
    db.commit()
    db.refresh(person)
    return person

def delete_person(db: Session, person_id: int):
    person = get_person(db, person_id)
    if person:
        db.delete(person)
        db.commit()
    return person
