from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'

    # Handle UUID as a string for SQLite compatibility
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    address = Column(String)
    department = Column(String)
    salary = Column(Integer)
    gender = Column(String)
    # Skill fields will be stored as comma-separated strings
    skill_language = Column(String)
    skill_another = Column(String)

    def __repr__(self):
        return f"<Employee(name={self.firstname} {self.lastname})>"

DATABASE_URL = "sqlite:///./mydatabase.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)  # echo set to False for non-debug mode

# Create tables
Base.metadata.create_all(engine)
