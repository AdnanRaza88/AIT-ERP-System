import random
from datetime import datetime
from sqlalchemy.orm import Session


def next_admission_id(db: Session) -> str:
    from backend.models.admission import Admission
    year = datetime.now().year
    count = db.query(Admission).count() + 1
    return f"AIT-ADM-{year}-{count:05d}"


def next_student_id(db: Session) -> str:
    from backend.models.student import Student
    year = datetime.now().year
    count = db.query(Student).count() + 1
    return f"AIT-STD-{year}-{count:05d}"


def next_roll_number(db: Session, department: str) -> str:
    from backend.models.student import Student
    code = "".join([w[0] for w in department.split()][:3]).upper() or "GEN"
    count = db.query(Student).filter(Student.department == department).count() + 1
    return f"{code}-{count:04d}"


def next_teacher_id(db: Session) -> str:
    from backend.models.teacher import Teacher
    count = db.query(Teacher).count() + 1
    return f"AIT-TCH-{count:05d}"


def next_invoice() -> str:
    return f"INV-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"