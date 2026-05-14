from pydantic import BaseModel


class ExamCreate(BaseModel):
    student_id: str
    exam_type: str
    course: str
    level: str
    total: int = 100
    obtained: int
    remarks: str | None = None