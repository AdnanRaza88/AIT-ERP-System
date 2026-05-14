from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.models.attendance import Attendance
from backend.schemas.attendance import AttendanceMark
from backend.auth.dependencies import current_user, require_roles

router = APIRouter(prefix="/api/attendance", tags=["attendance"])


@router.post("")
def mark(payload: AttendanceMark, db: Session = Depends(get_db),
         _=Depends(require_roles("admin", "super_admin", "teacher"))):
    record = Attendance(**payload.dict())
    db.add(record); db.commit(); db.refresh(record)
    return {"id": record.id}


@router.get("/{person_id}")
def history(person_id: str, db: Session = Depends(get_db), _=Depends(current_user)):
    rows = db.query(Attendance).filter(Attendance.person_id == person_id).all()
    return [{"date": str(r.date), "status": r.status, "remarks": r.remarks} for r in rows]