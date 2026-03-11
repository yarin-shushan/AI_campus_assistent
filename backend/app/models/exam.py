from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, time

class Exam(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    course_name: str
    classroom_name: str
    date: date
    hours: time
