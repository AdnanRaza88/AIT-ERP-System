from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from backend.database.session import Base


class Admission(Base):
    __tablename__ = "admissions"

    id = Column(Integer, primary_key=True)
    admission_id = Column(String(30), unique=True, nullable=False, index=True)
    full_name = Column(String(150), nullable=False)
    father_name = Column(String(150))
    gender = Column(String(10))
    dob = Column(String(20))
    cnic = Column(String(20))
    phone = Column(String(20))
    whatsapp = Column(String(20))
    email = Column(String(120))
    address = Column(String(300))
    city = Column(String(80))
    previous_qualification = Column(String(120))
    department = Column(String(120))
    course = Column(String(150))
    level = Column(String(40))
    shift = Column(String(30))
    test_required = Column(Boolean, default=True)
    test_marks = Column(Integer, default=0)
    test_status = Column(String(20), default="pending")  # pending/passed/failed
    approval_status = Column(String(20), default="pending")  # pending/approved/rejected
    recommended_level = Column(String(40))
    created_at = Column(DateTime(timezone=True), server_default=func.now())