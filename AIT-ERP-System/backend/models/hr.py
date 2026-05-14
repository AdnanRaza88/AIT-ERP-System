from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from backend.database.session import Base


class JobPost(Base):
    __tablename__ = "job_posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    department = Column(String(120))
    position_type = Column(String(50))
    description = Column(String(1000))
    status = Column(String(20), default="open")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Applicant(Base):
    __tablename__ = "applicants"
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, nullable=False)
    full_name = Column(String(150), nullable=False)
    email = Column(String(120))
    phone = Column(String(20))
    qualification = Column(String(150))
    experience = Column(String(150))
    cv_url = Column(String(300))
    interview_status = Column(String(30), default="pending")
    hire_status = Column(String(30), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())