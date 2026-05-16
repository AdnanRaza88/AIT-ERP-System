from pydantic import BaseModel, EmailStr
from typing import Optional


class TeacherCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    qualification: Optional[str] = None
    experience_years: int = 0
    department: Optional[str] = None
    courses_assigned: Optional[str] = None
    salary: int = 0


class TeacherOut(TeacherCreate):
    id: int
    teacher_id: str
    status: str

    class Config:
        from_attributes = True