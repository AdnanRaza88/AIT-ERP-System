import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from backend.models.student import Student
from backend.models.teacher import Teacher
from backend.models.fee import FeeRecord
from backend.models.attendance import Attendance
from backend.models.exam import ExamResult


def overview_metrics(db: Session) -> dict:
    total_students = db.query(Student).count()
    total_teachers = db.query(Teacher).count()
    revenue = db.query(FeeRecord).all()
    total_revenue = sum(f.paid_amount for f in revenue)
    pending_dues = sum((f.amount - f.paid_amount) for f in revenue if f.status != "paid")
    return {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_revenue": total_revenue,
        "pending_dues": pending_dues,
    }


def attendance_stats(db: Session) -> dict:
    rows = db.query(Attendance).all()
    if not rows:
        return {"present_pct": 0, "absent_pct": 0, "leave_pct": 0}
    df = pd.DataFrame([{"status": r.status} for r in rows])
    total = len(df)
    return {
        "present_pct": round(len(df[df.status == "present"]) / total * 100, 2),
        "absent_pct": round(len(df[df.status == "absent"]) / total * 100, 2),
        "leave_pct": round(len(df[df.status == "leave"]) / total * 100, 2),
    }


def course_distribution(db: Session) -> list[dict]:
    students = db.query(Student).all()
    if not students:
        return []
    df = pd.DataFrame([{"course": s.course or "Unassigned"} for s in students])
    counts = df["course"].value_counts().to_dict()
    return [{"course": k, "students": int(v)} for k, v in counts.items()]


def enrollment_growth(db: Session) -> list[dict]:
    students = db.query(Student).all()
    if not students:
        return []
    df = pd.DataFrame([{"date": s.created_at} for s in students if s.created_at])
    df["month"] = df["date"].dt.strftime("%Y-%m")
    counts = df.groupby("month").size().to_dict()
    return [{"month": k, "count": int(v)} for k, v in sorted(counts.items())]


def result_performance(db: Session) -> dict:
    rows = db.query(ExamResult).all()
    if not rows:
        return {"avg_score": 0, "pass_rate": 0}
    scores = np.array([r.obtained for r in rows])
    passed = np.sum(scores >= 50)
    return {
        "avg_score": float(round(scores.mean(), 2)),
        "pass_rate": float(round(passed / len(scores) * 100, 2)),
    }