from pydantic import BaseModel, ConfigDict

class PersonBase(BaseModel):
    first_name: str
    last_name: str
    person_type_id: int
    lat: float
    lon: float

class PersonCreate(PersonBase):
    pass

class PersonRead(PersonBase):
    id: int
    class Config:
        model_config = ConfigDict(from_attributes=True)

class PositionUpdate(BaseModel):
    lat: float
    lon: float
