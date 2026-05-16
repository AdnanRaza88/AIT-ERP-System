from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.services import analytics_engine
from backend.auth.dependencies import current_user

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/overview")
def overview(db: Session = Depends(get_db), _=Depends(current_user)):
    return analytics_engine.overview_metrics(db)


@router.get("/attendance")
def attendance(db: Session = Depends(get_db), _=Depends(current_user)):
    return analytics_engine.attendance_stats(db)


@router.get("/courses")
def courses(db: Session = Depends(get_db), _=Depends(current_user)):
    return analytics_engine.course_distribution(db)


@router.get("/enrollment")
def enrollment(db: Session = Depends(get_db), _=Depends(current_user)):
    return analytics_engine.enrollment_growth(db)


@router.get("/results")
def results(db: Session = Depends(get_db), _=Depends(current_user)):
    return analytics_engine.result_performance(db)