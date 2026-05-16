from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from backend.database.session import Base


class ExamResult(Base):
    __tablename__ = "exam_results"
    id = Column(Integer, primary_key=True)
    student_id = Column(String(30), nullable=False, index=True)
    exam_type = Column(String(30))  # entry/mid/final
    course = Column(String(150))
    level = Column(String(40))
    total = Column(Integer, default=100)
    obtained = Column(Integer, default=0)
    grade = Column(String(5))
    gpa = Column(String(10))
    remarks = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())