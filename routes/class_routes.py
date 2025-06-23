from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Course, Student
from schemas import ClassCreate

router = APIRouter()

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Create a class
@router.post("/classes/")
def create_class(new_data: ClassCreate, db: Session = Depends(get_db)):
    new_class = Course(**new_data.dict())
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return {"message": "Class created", "id": new_class.id}

# ✅ Update a class
@router.put("/classes/{class_id}")
def update_class(class_id: int, updated_data: ClassCreate, db: Session = Depends(get_db)):
    class_obj = db.query(Course).filter(Course.id == class_id).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    for key, value in updated_data.dict().items():
        setattr(class_obj, key, value)
    db.commit()
    return {"message": "Class updated"}

# ✅ Delete a class
@router.delete("/classes/{class_id}")
def delete_class(class_id: int, db: Session = Depends(get_db)):
    class_obj = db.query(Course).filter(Course.id == class_id).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    db.delete(class_obj)
    db.commit()
    return {"message": "Class deleted"}

# ✅ Register a student to a class
@router.post("/classes/{class_id}/register/{student_id}")
def register_student(class_id: int, student_id: int, db: Session = Depends(get_db)):
    class_obj = db.query(Course).filter(Course.id == class_id).first()
    student = db.query(Student).filter(Student.id == student_id).first()

    if not class_obj or not student:
        raise HTTPException(status_code=404, detail="Student or class not found")

    class_obj.students.append(student)
    db.commit()
    return {"message": f"Student {student_id} registered to class {class_id}"}

# ✅ Get all students in a class
@router.get("/classes/{class_id}/students")
def get_class_students(class_id: int, db: Session = Depends(get_db)):
    class_obj = db.query(Course).filter(Course.id == class_id).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")

    return {
        "class": class_obj.classname,
        "students": [
            {
                "id": s.id,
                "firstname": s.firstname,
                "lastname": s.lastname,
                "age": s.age,
                "city": s.city
            }
            for s in class_obj.students
        ]
    }

# ✅ Get all classes
@router.get("/classes/")
def get_all_classes(db: Session = Depends(get_db)):
    classes = db.query(Course).all()
    return [
        {
            "id": c.id,
            "classname": c.classname,
            "description": c.description,
            "start_date": c.start_date,
            "end_date": c.end_date,
            "hours": c.hours
        }
        for c in classes
    ]



