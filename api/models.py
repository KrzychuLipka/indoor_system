from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from db_config import ORMBaseModel

class Person(ORMBaseModel):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    person_type_id = Column(Integer, index=True, nullable=False)
    position = Column(Geometry(geometry_type='POINT', srid=2180))
