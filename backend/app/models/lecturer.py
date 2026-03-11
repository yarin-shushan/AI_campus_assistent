from sqlmodel import SQLModel, Field
from typing import Optional, TYPE_CHECKING
from sqlmodel import Relationship

if TYPE_CHECKING:
    from .user import User

class Lecturer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    identity_number: str
    department: str
    reception_day: str
    reception_hours: str
    location: str
    
    user: Optional["User"] = Relationship(back_populates="lecturer_profile")
