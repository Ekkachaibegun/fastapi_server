from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Employee, Base  # make sure to import your models and Base
from database import SessionLocal, engine

# Assuming DATABASE_URL and engine have been set up as before
DATABASE_URL = "sqlite:///./mydatabase.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def add_employee():
    db = SessionLocal()
    try:
        # Create an instance of the Employee
        new_employee = Employee(
            firstname="Alice",
            lastname="Johnson",
            address="7890 Pine Road",
            department="Research and Development",
            salary=65000,
            gender="Female",
            skill_language="English,German",
            skill_another="Data Analysis,Critical Thinking"
        )
        db.add(new_employee)
        db.commit()
        print("Employee added successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_employee()
