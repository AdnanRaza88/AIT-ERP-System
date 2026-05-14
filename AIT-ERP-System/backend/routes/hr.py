from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.models.hr import JobPost, Applicant
from backend.schemas.hr import JobCreate, ApplicantCreate
from backend.auth.dependencies import current_user, require_roles

router = APIRouter(prefix="/api/hr", tags=["hr"])


@router.post("/jobs")
def create_job(payload: JobCreate, db: Session = Depends(get_db),
               _=Depends(require_roles("admin", "super_admin", "hr_manager"))):
    j = JobPost(**payload.dict()); db.add(j); db.commit(); db.refresh(j)
    return {"id": j.id, "title": j.title}


@router.get("/jobs")
def list_jobs(db: Session = Depends(get_db), _=Depends(current_user)):
    return [{"id": j.id, "title": j.title, "department": j.department,
             "position_type": j.position_type, "status": j.status} for j in db.query(JobPost).all()]


@router.post("/applicants")
def apply(payload: ApplicantCreate, db: Session = Depends(get_db)):
    a = Applicant(**payload.dict()); db.add(a); db.commit(); db.refresh(a)
    return {"id": a.id}


@router.get("/applicants")
def list_applicants(db: Session = Depends(get_db),
                    _=Depends(require_roles("admin", "super_admin", "hr_manager"))):
    return [{"id": a.id, "job_id": a.job_id, "full_name": a.full_name,
             "email": a.email, "phone": a.phone, "interview_status": a.interview_status,
             "hire_status": a.hire_status} for a in db.query(Applicant).all()]


@router.post("/applicants/{aid}/hire")
def hire(aid: int, db: Session = Depends(get_db),
         _=Depends(require_roles("admin", "super_admin", "hr_manager"))):
    a = db.query(Applicant).get(aid)
    if not a: raise HTTPException(404, "Not found")
    a.hire_status = "hired"; a.interview_status = "completed"
    db.commit(); return {"ok": True}