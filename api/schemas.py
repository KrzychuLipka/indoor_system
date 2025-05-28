from pydantic import BaseModel, ConfigDict
from typing import Optional

class PersonBase(BaseModel):
    first_name: str
    last_name: str
    person_type_id: int
    position: Optional[str] # WKT format

class PersonCreate(PersonBase):
    pass

class PersonRead(PersonBase):
    id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)

class PositionUpdate(BaseModel):
    position: str
