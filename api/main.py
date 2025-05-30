from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
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
import json

app = FastAPI()
active_connections: list[WebSocket] = []

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
async def update_position(person_id: int, position: PositionUpdate, db: Session = Depends(get_db_session)):
    person = update_person_position(db, person_id, position)
    if not person:
        raise HTTPException(status_code=404, detail="User not found")
    message = json.dumps({
        "id": person.id,
        "lat": person.lat,
        "lon": person.lon,
        "first_name": person.first_name,
        "last_name": person.last_name,
        "person_type_id": person.person_type_id
    })
    print(f"Sending message to {len(active_connections)} clients")
    for connection in active_connections:
        await connection.send_text(message)
    return person

@app.delete("/users/{person_id}")
def remove_user(person_id: int, db: Session = Depends(get_db_session)):
    deleted = delete_person(db, person_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@app.websocket("/ws/positions")
async def positions(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text() # Utrzymywanie poołączenia
    except WebSocketDisconnect:
        active_connections.remove(websocket)