from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from backend.database.session import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    student_id = Column(String(30), unique=True, nullable=False, index=True)
    roll_number = Column(String(30), unique=True, nullable=False)
    full_name = Column(String(150), nullable=False)
    father_name = Column(String(150))
    gender = Column(String(10))
    dob = Column(Date)
    cnic = Column(String(20))
    phone = Column(String(20))
    whatsapp = Column(String(20))
    email = Column(String(120))
    address = Column(String(300))
    city = Column(String(80))
    previous_qualification = Column(String(120))
    previous_institute = Column(String(150))
    marks = Column(String(30))
    department = Column(String(120))
    course = Column(String(150))
    level = Column(String(40))
    batch = Column(String(40))
    shift = Column(String(30))
    guardian_name = Column(String(150))
    guardian_phone = Column(String(20))
    status = Column(String(30), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())