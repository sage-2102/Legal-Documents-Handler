from pydantic import BaseModel
from datetime import date


class CaseCreate(BaseModel):
    complaint_id: int
    lawyer_id: int
    hearing_date: date | None = None


class CaseOut(BaseModel):
    id: int
    complaint_id: int
    client_id: int
    lawyer_id: int
    status: str

    class Config:
        from_attributes = True