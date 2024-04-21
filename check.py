from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./mydatabase.db"
engine = create_engine(DATABASE_URL, echo=True)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Try to fetch all entries from the employees table
try:
    result = session.execute("SELECT * FROM employees")
    for row in result:
        print(row)
except Exception as e:
    print("Error:", e)

session.close()
