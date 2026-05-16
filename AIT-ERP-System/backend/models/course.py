from sqlalchemy import Column, Integer, String
from backend.database.session import Base


class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, nullable=False)
    code = Column(String(20), unique=True, nullable=False)


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    department = Column(String(120), nullable=False)
    level = Column(String(40), nullable=False)
    title = Column(String(160), nullable=False)
    duration_months = Column(Integer, default=6)
    fee = Column(Integer, default=0)


class Batch(Base):
    __tablename__ = "batches"
    id = Column(Integer, primary_key=True)
    code = Column(String(40), unique=True, nullable=False)
    course_id = Column(Integer, nullable=False)
    shift = Column(String(30), nullable=False)
    start_date = Column(String(20))
    end_date = Column(String(20))