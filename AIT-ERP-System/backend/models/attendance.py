from sqlalchemy import Column, Integer, String, Date
from backend.database.session import Base


class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True)
    person_type = Column(String(20))  # student/teacher
    person_id = Column(String(30), nullable=False, index=True)
    date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)  # present/absent/leave
    remarks = Column(String(200))