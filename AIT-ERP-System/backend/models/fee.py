from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from backend.database.session import Base


class FeeRecord(Base):
    __tablename__ = "fees"
    id = Column(Integer, primary_key=True)
    invoice_no = Column(String(40), unique=True, nullable=False)
    student_id = Column(String(30), nullable=False, index=True)
    month = Column(String(20))
    amount = Column(Integer, default=0)
    paid_amount = Column(Integer, default=0)
    status = Column(String(20), default="unpaid")  # paid/unpaid/partial
    method = Column(String(30))
    created_at = Column(DateTime(timezone=True), server_default=func.now())