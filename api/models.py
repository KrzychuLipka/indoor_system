from sqlalchemy import Column, Integer, String
# from geoalchemy2 import Geometry
from db_config import ORMBaseModel
from pydantic import BaseModel

class Person(ORMBaseModel):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    person_type_id = Column(Integer, index=True, nullable=False)
    # position = Column(Geometry(geometry_type='POINT', srid=2180))

class PersonCreate(BaseModel):
    first_name: str
    last_name: str
    person_type_id: int
    # position: str  # WKT string, e.g. "POINT(123 456)"

# class PositionUpdate(BaseModel):
#     position: str  # WKT string
