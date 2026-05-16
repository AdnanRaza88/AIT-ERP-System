from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.models.exam import ExamResult
from backend.schemas.exam import ExamCreate
from backend.auth.dependencies import current_user, require_roles


def grade_from_score(pct: float) -> tuple[str, str]:
    if pct >= 90: return "A+", "4.0"
    if pct >= 80: return "A", "3.7"
    if pct >= 70: return "B", "3.3"
    if pct >= 60: return "C", "2.7"
    if pct >= 50: return "D", "2.0"
    return "F", "0.0"


router = APIRouter(prefix="/api/exams", tags=["exams"])


@router.post("")
def add_result(payload: ExamCreate, db: Session = Depends(get_db),
               _=Depends(require_roles("admin", "super_admin", "teacher"))):
    pct = (payload.obtained / payload.total) * 100
    grade, gpa = grade_from_score(pct)
    rec = ExamResult(**payload.dict(), grade=grade, gpa=gpa)
    db.add(rec); db.commit(); db.refresh(rec)
    return {"id": rec.id, "grade": grade, "gpa": gpa}


@router.get("")
def list_results(student_id: str | None = None, db: Session = Depends(get_db), _=Depends(current_user)):
    q = db.query(ExamResult)
    if student_id:
        q = q.filter(ExamResult.student_id == student_id)
    return [{
        "student_id": r.student_id, "exam_type": r.exam_type, "course": r.course,
        "level": r.level, "total": r.total, "obtained": r.obtained,
        "grade": r.grade, "gpa": r.gpa
    } for r in q.all()]