# models.py
from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

student_class = Table(
    "student_class",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("class_id", Integer, ForeignKey("classes.id")),
)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    middlename = Column(String)
    age = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    classes = relationship("Course", secondary=student_class, back_populates="students")

class Course(Base):  # ✅ not Class!
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True, index=True)
    classname = Column(String, nullable=False)
    description = Column(String)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    hours = Column(Integer, nullable=False)
    students = relationship("Student", secondary=student_class, back_populates="classes")


