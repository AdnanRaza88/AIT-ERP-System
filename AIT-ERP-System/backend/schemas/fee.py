from pydantic import BaseModel


class FeeCreate(BaseModel):
    student_id: str
    month: str
    amount: int
    paid_amount: int = 0
    method: str | None = None