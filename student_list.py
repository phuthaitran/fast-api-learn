from typing import Any, Annotated
from datetime import date
from enum import Enum

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field

app = FastAPI(
    title="Student Database"
)

class Major(Enum):
    ICT = "ict"
    MATH = "math"
    DATA_SCIENCE = "ds"
    CYBER_SECURITY = "cyber"
    COMPUTER_SCIENCE = "cs"

class Student(BaseModel):
    name: str
    dob: date
    group: Major
    
class Mark(BaseModel):
    attendance: Annotated[float, Field(ge=0, le=20)]
    mid_term: Annotated[float, Field(ge=0, le=20)]
    final: Annotated[float, Field(ge=0, le=20)]
    is_passed: bool
    
students = [
    {
        "student_id": 1,
        "student": Student(name="Nam", dob=date(2005, 7, 30), group=Major.ICT),
        "mark": Mark(attendance=20, mid_term=17.5, final=15, is_passed=True)
    },
    {
        "student_id": 2,
        "student": Student(name="Long", dob=date(2005, 12, 1), group=Major.COMPUTER_SCIENCE),
        "mark": Mark(attendance=18, mid_term=10, final=10.5, is_passed=True)
    }
]

# Homepage
@app.get("/")
def index():
    return {"list of students": students}


# Get student by ID 
@app.get(
    "/get-student/{student_id}",
    responses={
        404: {"description": "Not found"},
    },
)
def get_student(student_id: int):
    for student in students:
        if student["student_id"] == student_id:
            return student
    raise HTTPException(status_code=404, detail=f"Student with ID {student_id} does not exist")


# Get student by name
@app.get(
    "/get-by-name",
    responses={
        404: {"description": "Not found"},
    },
)
def get_student_by_name(name: Annotated[str | None, Query(description="Enter first name of the student")] = None):
    if name is None:
        return {"students": students}
    
    matched_students = []
    for student in students:
        # Check if the student has 'student' key and if that student has a name that matches
        if "student" in student and isinstance(student["student"], Student) and student["student"].name.lower() == name.lower():
            matched_students.append(student)      
            
    if not matched_students:
        raise HTTPException(status_code=404, detail=f"Student with name {name} does not exist")  
    
    return {"student": matched_students}

# Get student whether they're passed or not
@app.get(
    "/get-by-status",
    responses={
        404: {"description": "Not found"},
    },
)
def get_student_by_status(passed: bool):
    matched_students = []
    for student in students:
        if "mark" in student and isinstance(student["mark"], Mark) and student["mark"].is_passed == passed:
            matched_students.append(student)
            
    if not matched_students:
        raise HTTPException(status_code=404, detail="No students found in this query.")
    
    return {"student": matched_students}

# Get student by their group
@app.get(
    "/get-by-group",
    responses={
        404: {"description": "Not found"},
    }
)
def get_student_by_group(group: Major):
    matched_students = []
    for student in students:
        if "student" in student and isinstance(student["student"], Student) and student["student"].group == group:
            matched_students.append(student)
            
    if not matched_students:
        raise HTTPException(status_code=404, detail="No students found in this group")
    
    return {group: matched_students}

@app.get(
    "/students",
    responses={
        404: {"description": "Not Found"}
    }
)
def query_student_by_parameters(
    name: str | None = None,
    passed: bool | None = None,
    group: Major | None = None
):
    matched_students = []
    for student in students:
        if all(
            (
                name is None or ("student" in student and isinstance(student["student"], Student) and student["student"].name.lower() == name.lower()),
                passed is None or ("mark" in student and isinstance(student["mark"], Mark) and student["mark"].is_passed == passed),
                group is None or ("student" in student and isinstance(student["student"], Student) and student["student"].group == group)
            )
        ):
            matched_students.append(student)
            
    if not matched_students:
        raise HTTPException(status_code=404, detail="No students found in this query.")
    
    return {"student": matched_students}

# Create a Student object
@app.post(
    "/create-student/{student_id}",
    responses={
        400: {"description": "Duplicate ID"},
    },
)
def create_student(student_id: int, student: Student, mark: Mark):
    for existing_student in students:
        if existing_student["student_id"] == student_id:
            raise HTTPException(status_code=400, detail=f"Student with ID {student_id} already exists.")
        
    new_student = {"student_id": student_id}
    if student:
        new_student.update({"student": student})
    if mark:
        new_student.update({"mark": mark})
        
    students.append(new_student)
    return new_student


# Update student info
@app.put(
    "/update-student/{student_id}",
    responses={
        404: {"description": "Not found"},
        400: {"description": "No arguments specified"},
    },
)
def update_student(
    student_id: Annotated[int, Path(gt=0)],
    student: Student | None = None,
    mark: Mark | None = None
):
    result = None
    for student_ in students:
        if student_["student_id"] == student_id:
            result = student_
            break
        
    if result is None:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} does not exist.")
    
    
    if student is not None:
        result["student"] = student
    if mark is not None:
        result["mark"] = mark
        
    return {"updated": result}


# Delete a student
@app.delete(
    "/delete-student/{student_id}",
    responses={
        404: {"description": "Not found"},
    },
)
def delete_student(student_id: int):
    result = None
    for student_ in students:
        if student_["student_id"] == student_id:
            result = student_
            break
        
    if result is None:
            raise HTTPException(status_code=404, detail=f"Student with ID {student_id} does not exist.")
        
    students.remove(result)
    return {"removed": result}