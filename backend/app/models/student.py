from sqlmodel import SQLModel, Field
from typing import Optional, TYPE_CHECKING
from sqlmodel import Relationship

if TYPE_CHECKING:
    from .user import User

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    identity_number: str
    department: str
    
    user: Optional["User"] = Relationship(back_populates="student_profile")
