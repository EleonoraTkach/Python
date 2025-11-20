from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from models import Student
from DataBase import DataBase
import uvicorn

class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    faculty: str
    course: int
    grade: float

class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    faculty: Optional[str] = None
    course: Optional[int] = None
    grade: Optional[float] = None

def get_db():
    return database

app = FastAPI(title="Student Management API")
database = DataBase()

@app.on_event("startup")
async def startup_event():
    database.create_db_and_tables()

@app.post("/students/", response_model=StudentCreate)
async def create_student(student: StudentCreate, db: DataBase = Depends(get_db)):
    db_student = Student(
        first_name=student.first_name,
        last_name=student.last_name,
        faculty=student.faculty,
        course=student.course,
        grade=student.grade
    )
    created_student = db.create_student(db_student)
    return created_student

@app.get("/students/", response_model=List[StudentCreate])
async def read_all_students(db: DataBase = Depends(get_db)):
    return db.get_all_students()

@app.get("/students/{student_id}")
async def read_student(student_id: int, db: DataBase = Depends(get_db)):
    student = db.get_student_by_id(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}")
async def update_student(student_id: int, student_update: StudentUpdate, db: DataBase = Depends(get_db)):
    # Убираем None значения
    update_data = student_update.dict(exclude_unset=True)

    updated_student = db.update_student(student_id, update_data)
    if updated_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return updated_student

@app.delete("/students/{student_id}")
async def delete_student(student_id: int, db: DataBase = Depends(get_db)):
    success = db.delete_student(student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student deleted successfully"}


@app.get("/students/faculty/{faculty}")
async def get_students_by_faculty(faculty: str, db: DataBase = Depends(get_db)):
    return db.get_by_faculty(faculty)


@app.get("/courses/unique/")
async def get_unique_courses(db: DataBase = Depends(get_db)):
    return db.get_unic_course()


@app.get("/faculty/average-grades/")
async def get_faculty_average_grades(db: DataBase = Depends(get_db)):
    return db.get_facult_grade_avg()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)