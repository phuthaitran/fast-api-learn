from typing import Any, Annotated

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel

app = FastAPI(
    title="Student Database"
)

class Student(BaseModel):
    name: str
    age: int
    year: str
    
students = {
    1: Student(
        name="John", age=17, year="12A"
    ),
    2: Student(
        name="Tim", age=15, year="10D"
    )
}

@app.get("/")
def index():
    return {"list of students": students}

# Get student by ID
@app.get("/get-student/{student_id}")
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail=f"There is no student with ID {student_id}")
    return students[student_id]

# Get student by name
@app.get("/get-by-name")
def get_student_by_name(name: str) -> dict[str, Any]:
    def check_name(student: Student) -> bool:
        return student.name == name
    
    selection = [student for student in students.values() if check_name(student)]  # Fixed: pass student instead of name
    
    return {"selection": selection}
        
# Create a Student object
@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student Exists"}
    
    students[student_id] = student
    return students[student_id]

# Update student info
@app.put("/update-student/{student_id}")
def update_student(
    student_id: Annotated[int, Path(gt=0)],
    name: str | None = None,
    age: Annotated[int | None, Query(gt=0)] = None,
    year: str | None = None
):
    if student_id not in students:
        raise HTTPException(status_code=404, detail=f"Student with id {student_id} does not exist")
    if all(info is None for info in (name, age, year)):
        raise HTTPException(status_code=400, detail="No parameters provided for update")
    
    student = students[student_id]
    if name is not None:
        student.name = name
    if age is not None:
        student.age = age
    if year is not None:
        student.year = year
        
    return {"updated": student}

# Delete a student
@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    
    student = students.pop(student_id)
    return {"deleted": student}