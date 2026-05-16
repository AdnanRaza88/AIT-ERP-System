from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.models.course import Course, Batch
from backend.auth.dependencies import current_user

router = APIRouter(prefix="/api/courses", tags=["courses"])


@router.get("")
def list_courses(db: Session = Depends(get_db), _=Depends(current_user)):
    return [{
        "id": c.id, "department": c.department, "level": c.level,
        "title": c.title, "duration_months": c.duration_months, "fee": c.fee
    } for c in db.query(Course).all()]


@router.get("/batches")
def list_batches(db: Session = Depends(get_db), _=Depends(current_user)):
    return [{"id": b.id, "code": b.code, "course_id": b.course_id, "shift": b.shift,
             "start_date": b.start_date, "end_date": b.end_date} for b in db.query(Batch).all()]