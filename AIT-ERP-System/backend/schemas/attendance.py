from pydantic import BaseModel
from datetime import date


class AttendanceMark(BaseModel):
    person_type: str
    person_id: str
    date: date
    status: str
    remarks: str | None = None