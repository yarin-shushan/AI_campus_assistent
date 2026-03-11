from sqlmodel import SQLModel, Field
from typing import Optional

class TechnicalFAQ(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    issue: str
    solution: str
