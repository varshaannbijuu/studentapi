from pydantic import BaseModel
from typing import Optional
from datetime import date

class StudentCreate(BaseModel):
    firstname: str
    lastname: str
    middlename: Optional[str] = None
    age: int
    city: str

class ClassCreate(BaseModel):
    classname: str
    description: str
    start_date: date
    end_date: date
    hours: int




