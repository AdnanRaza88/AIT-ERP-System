from pydantic import BaseModel
from typing import Optional


class StudentOut(BaseModel):
    id: int
    student_id: str
    roll_number: str
    full_name: str
    department: Optional[str]
    course: Optional[str]
    level: Optional[str]
    batch: Optional[str]
    shift: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    status: str

    class Config:
        from_attributes = True


class StudentUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    batch: Optional[str] = None
    shift: Optional[str] = None
    status: Optional[str] = None