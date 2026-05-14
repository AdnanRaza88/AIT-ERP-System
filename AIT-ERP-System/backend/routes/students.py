from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.models.student import Student
from backend.schemas.student import StudentOut, StudentUpdate
from backend.auth.dependencies import current_user, require_roles

router = APIRouter(prefix="/api/students", tags=["students"])


@router.get("", response_model=list[StudentOut])
def list_students(search: str | None = Query(None), department: str | None = None,
                  db: Session = Depends(get_db), _=Depends(current_user)):
    q = db.query(Student)
    if search:
        q = q.filter(Student.full_name.ilike(f"%{search}%"))
    if department:
        q = q.filter(Student.department == department)
    return q.order_by(Student.id.desc()).limit(500).all()


@router.get("/{student_id}", response_model=StudentOut)
def detail(student_id: str, db: Session = Depends(get_db), _=Depends(current_user)):
    s = db.query(Student).filter(Student.student_id == student_id).first()
    if not s: raise HTTPException(404, "Not found")
    return s


@router.put("/{student_id}", response_model=StudentOut)
def update(student_id: str, payload: StudentUpdate, db: Session = Depends(get_db),
           _=Depends(require_roles("admin", "super_admin"))):
    s = db.query(Student).filter(Student.student_id == student_id).first()
    if not s: raise HTTPException(404, "Not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(s, k, v)
    db.commit(); db.refresh(s)
    return s