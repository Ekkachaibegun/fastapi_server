from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.types import JSON
import uuid
from typing import List

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    address = Column(String)
    department = Column(String)
    salary = Column(Integer)
    gender = Column(String)
    skill_language = Column(String)
    skill_another = Column(String)

    def __repr__(self):
        return f"<Employee(name={self.firstname} {self.lastname})>"
