from pydantic import BaseModel
from typing import Optional


class JobCreate(BaseModel):
    title: str
    department: Optional[str] = None
    position_type: str
    description: Optional[str] = None


class ApplicantCreate(BaseModel):
    job_id: int
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    qualification: Optional[str] = None
    experience: Optional[str] = None
    cv_url: Optional[str] = None