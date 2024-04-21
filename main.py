from fastapi import FastAPI, HTTPException, Depends,Response, File, UploadFile
from pydantic import BaseModel,Field
import models 
from database import engine,Sessionlocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import csv
from io import StringIO
import io
app = FastAPI()


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Specify the origin of the frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db=Sessionlocal()
        yield db
    finally:
            db.close()

class Employee(BaseModel):
    id: str
    firstname :str =Field(min_length=1)
    lastname :str =Field(min_length=1)
    address :str =Field(min_length=1)
    department :str =Field(min_length=1)
    salary :int =Field
    gender :str =Field(min_length=1)
    skill_language:str =Field(min_length=1)
    skill_another :str =Field(min_length=1)

employee=[]

@app.get("/employees/")
def read_employees(db: Session = Depends(get_db)):
    employees=db.query(models.Employee).all()
    return employees



@app.get("/employees/{employee_id}")
def find_employee(employee_id: str, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee




@app.post("/create/")
def create_employee(employee:Employee, db: Session = Depends(get_db)):
    print("Received employee data:")
    print(f"ID: {employee.id}")
    print(f"First Name: {employee.firstname}")
    print(f"Last Name: {employee.lastname}")
    print(f"Address: {employee.address}")
    print(f"Department: {employee.department}")
    print(f"Salary: {employee.salary}")
    print(f"Gender: {employee.gender}")
    print(f"Skill Language: {employee.skill_language}")
    print(f"Skill Another: {employee.skill_another}")
    employee_model = models.Employee()
    employee_model.id = employee.id
    employee_model.firstname = employee.firstname
    employee_model.lastname = employee.lastname
    employee_model.address = employee.address
    employee_model.department = employee.department
    employee_model.salary = employee.salary
    employee_model.gender = employee.gender
    employee_model.skill_language = employee.skill_language
    employee_model.skill_another = employee.skill_another
    db.add(employee_model)
    db.commit()
  
    return employee

@app.put("/edit/{employee_id}")
def edit_employee(employee_id:str, employee:Employee, db: Session = Depends(get_db) ):
    employee_model = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if employee_model is None:
        print(f"No employee found with ID: {employee_id}")
        raise HTTPException(
            status_code=404,
            detail=f"ID {employee_id} : Does not exist"
        )

    print(f"Found employee: {employee_model}")
    employee_model.id = employee.id
    employee_model.firstname = employee.firstname
    employee_model.lastname = employee.lastname
    employee_model.address = employee.address
    employee_model.department = employee.department
    employee_model.salary = employee.salary
    employee_model.gender = employee.gender
    employee_model.skill_language = employee.skill_language
    employee_model.skill_another = employee.skill_another

    db.add(employee_model)
    db.commit()
  
    return employee


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: str, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.query(models.Employee).filter(models.Employee.id == employee_id).delete()
    db.commit()


@app.get("/export/employees/csv", response_class=Response)
def export_employees_csv(db: Session = Depends(get_db)):
    employees = db.query(models.Employee).all()

    # Create an in-memory text stream to hold the CSV data
    stream = StringIO()
    csv_writer = csv.writer(stream)

    # Write the header row
    csv_writer.writerow(['ID', 'First Name', 'Last Name', 'Address', 'Department', 'Salary', 'Gender', 'Skill Language', 'Other Skills'])

    # Write the employee data rows
    for employee in employees:
        csv_writer.writerow([
            employee.id, 
            employee.firstname, 
            employee.lastname, 
            employee.address, 
            employee.department, 
            employee.salary, 
            employee.gender, 
            employee.skill_language, 
            employee.skill_another
        ])
    
    # Set the file position to the beginning
    stream.seek(0)
    response = Response(stream.getvalue(), media_type="text/csv")

    # Set a header that tells the browser to download the file
    response.headers["Content-Disposition"] = "attachment; filename=employees.csv"
    return response



@app.post("/import/employees/csv")
async def upload_employees_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Check file format
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")
    
    # Read the contents of the file
    contents = await file.read()
    stream = io.StringIO(contents.decode('utf-8'))
    csv_reader = csv.reader(stream)
    
    # Optional: skip header if your CSV file includes header row
    next(csv_reader)
    
    # Process CSV data
    for index, row in enumerate(csv_reader):
        if len(row) == 9:  # Ensure row has the right number of columns
            employee_data = models.Employee(
                id=row[0],
                firstname=row[1],
                lastname=row[2],
                address=row[3],
                department=row[4],
                salary=int(row[5]),
                gender=row[6],
                skill_language=row[7],
                skill_another=row[8]
            )
            db.add(employee_data)
        else:
            raise HTTPException(status_code=400, detail=f"Row {index+1} has incorrect data format.")

    # Commit the transaction
    db.commit()

    return {"message": "Employees imported successfully."}
