from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .token import Token
    from .student import Student
    from .lecturer import Lecturer

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    role: str = Field(default="student")
    student_id: Optional[int] = Field(default=None, foreign_key="student.id")
    lecturer_id: Optional[int] = Field(default=None, foreign_key="lecturer.id")
    
    tokens: List["Token"] = Relationship(back_populates="user")
    student_profile: Optional["Student"] = Relationship(back_populates="user")
    lecturer_profile: Optional["Lecturer"] = Relationship(back_populates="user")
