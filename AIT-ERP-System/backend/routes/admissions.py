from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.models.admission import Admission
from backend.models.student import Student
from backend.schemas.admission import AdmissionCreate, AdmissionOut, TestResultUpdate
from backend.services.id_generator import next_admission_id, next_student_id, next_roll_number
from backend.auth.dependencies import current_user, require_roles

router = APIRouter(prefix="/api/admissions", tags=["admissions"])


@router.post("", response_model=AdmissionOut)
def create_admission(payload: AdmissionCreate, db: Session = Depends(get_db)):
    adm = Admission(**payload.dict(), admission_id=next_admission_id(db))
    if not payload.test_required:
        adm.approval_status = "approved"
        adm.test_status = "n/a"
    db.add(adm); db.commit(); db.refresh(adm)
    return adm


@router.get("", response_model=list[AdmissionOut])
def list_admissions(db: Session = Depends(get_db), _=Depends(current_user)):
    return db.query(Admission).order_by(Admission.id.desc()).all()


@router.post("/test-result", response_model=AdmissionOut)
def submit_test_result(payload: TestResultUpdate, db: Session = Depends(get_db),
                       _=Depends(require_roles("admin", "super_admin", "teacher"))):
    adm = db.query(Admission).filter(Admission.admission_id == payload.admission_id).first()
    if not adm:
        raise HTTPException(404, "Admission not found")
    adm.test_marks = payload.test_marks
    if payload.test_marks >= 50:
        adm.test_status = "passed"
        adm.recommended_level = adm.level
    else:
        adm.test_status = "failed"
        adm.recommended_level = "IT Level 0"
    db.commit(); db.refresh(adm)
    return adm


@router.post("/{admission_id}/approve", response_model=AdmissionOut)
def approve(admission_id: str, db: Session = Depends(get_db),
            _=Depends(require_roles("admin", "super_admin"))):
    adm = db.query(Admission).filter(Admission.admission_id == admission_id).first()
    if not adm:
        raise HTTPException(404, "Not found")
    adm.approval_status = "approved"

    sid = next_student_id(db)
    roll = next_roll_number(db, adm.department)
    student = Student(
        student_id=sid, roll_number=roll, full_name=adm.full_name,
        father_name=adm.father_name, gender=adm.gender,
        cnic=adm.cnic, phone=adm.phone, whatsapp=adm.whatsapp, email=adm.email,
        address=adm.address, city=adm.city,
        previous_qualification=adm.previous_qualification,
        department=adm.department, course=adm.course,
        level=adm.recommended_level or adm.level,
        shift=adm.shift, status="active",
    )
    db.add(student); db.commit(); db.refresh(adm)
    return adm


@router.post("/{admission_id}/reject", response_model=AdmissionOut)
def reject(admission_id: str, db: Session = Depends(get_db),
           _=Depends(require_roles("admin", "super_admin"))):
    adm = db.query(Admission).filter(Admission.admission_id == admission_id).first()
    if not adm:
        raise HTTPException(404, "Not found")
    adm.approval_status = "rejected"
    db.commit(); db.refresh(adm)
    return adm