from pydantic import BaseModel, EmailStr
from typing import Optional


class AdmissionCreate(BaseModel):
    full_name: str
    father_name: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[str] = None
    cnic: Optional[str] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    previous_qualification: Optional[str] = None
    department: str
    course: str
    level: str
    shift: str
    test_required: bool = True


class AdmissionOut(AdmissionCreate):
    id: int
    admission_id: str
    test_marks: int
    test_status: str
    approval_status: str
    recommended_level: Optional[str] = None

    class Config:
        from_attributes = True


class TestResultUpdate(BaseModel):
    admission_id: str
    test_marks: int