from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

students = {
    1: {
        "name": "John",
        "age": 17,
        "year": "12A"
    },
    2: {
        "name": "Tim",
        "age": 15,
        "year": "10D"
    },
}

class Student(BaseModel):
    name: str
    age: int
    year: str
    
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

@app.get("/")
def index():
    return {"name": "Hello world"}

# Get student by ID
@app.get("/get-student/{student_id}")
def get_student(student_id: int):
    return students[student_id]

# Get student by name
@app.get("/get-by-name")
async def get_student(name: str):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
        
# Create a Student object
@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student Exists"}
    
    students[student_id] = student
    return students[student_id]

# Update student info
@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    
    if student.name != None:
        students[student_id].name = student.name
        
    if student.age != None:
        students[student_id].age = student.age
        
    if student.year != None:
        students[student_id].year = student.year    
        
    return students[student_id]

# Delete a student
@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    
    del students[student_id]
    return {"Message": "Student deleted sucessfully"}