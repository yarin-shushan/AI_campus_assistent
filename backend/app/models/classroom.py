from sqlmodel import SQLModel, Field
from typing import Optional

class Classroom(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    building_name: str
    room_number: str
    availability_schedule: str
