from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from backend.database.session import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)
    teacher_id = Column(String(30), unique=True, nullable=False, index=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(120), unique=True)
    phone = Column(String(20))
    qualification = Column(String(150))
    experience_years = Column(Integer, default=0)
    department = Column(String(120))
    courses_assigned = Column(String(500))
    salary = Column(Integer, default=0)
    status = Column(String(30), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())