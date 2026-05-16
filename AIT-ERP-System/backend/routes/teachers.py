from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.models.teacher import Teacher
from backend.schemas.teacher import TeacherCreate, TeacherOut
from backend.services.id_generator import next_teacher_id
from backend.auth.dependencies import current_user, require_roles

router = APIRouter(prefix="/api/teachers", tags=["teachers"])


@router.post("", response_model=TeacherOut)
def create(payload: TeacherCreate, db: Session = Depends(get_db),
           _=Depends(require_roles("admin", "super_admin", "hr_manager"))):
    t = Teacher(**payload.dict(), teacher_id=next_teacher_id(db))
    db.add(t); db.commit(); db.refresh(t)
    return t


@router.get("", response_model=list[TeacherOut])
def list_all(db: Session = Depends(get_db), _=Depends(current_user)):
    return db.query(Teacher).order_by(Teacher.id.desc()).all()


@router.delete("/{teacher_id}")
def delete(teacher_id: str, db: Session = Depends(get_db),
           _=Depends(require_roles("admin", "super_admin"))):
    t = db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()
    if not t: raise HTTPException(404, "Not found")
    db.delete(t); db.commit()
    return {"deleted": True}