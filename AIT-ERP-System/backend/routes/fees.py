from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.models.fee import FeeRecord
from backend.schemas.fee import FeeCreate
from backend.services.id_generator import next_invoice
from backend.auth.dependencies import current_user, require_roles

router = APIRouter(prefix="/api/fees", tags=["fees"])


@router.post("")
def create_fee(payload: FeeCreate, db: Session = Depends(get_db),
               _=Depends(require_roles("admin", "super_admin"))):
    status = "paid" if payload.paid_amount >= payload.amount else ("partial" if payload.paid_amount > 0 else "unpaid")
    rec = FeeRecord(**payload.dict(), invoice_no=next_invoice(), status=status)
    db.add(rec); db.commit(); db.refresh(rec)
    return {"invoice_no": rec.invoice_no, "status": rec.status}


@router.get("")
def list_fees(student_id: str | None = None, db: Session = Depends(get_db), _=Depends(current_user)):
    q = db.query(FeeRecord)
    if student_id:
        q = q.filter(FeeRecord.student_id == student_id)
    return [{
        "invoice_no": r.invoice_no, "student_id": r.student_id, "month": r.month,
        "amount": r.amount, "paid": r.paid_amount, "status": r.status, "method": r.method
    } for r in q.all()]