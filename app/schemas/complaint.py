from pydantic import BaseModel


class ComplaintCreate(BaseModel):
    title: str
    description: str
    category: str
    urgency: str
    preferred_lawyer_id: int | None = None


class ComplaintOut(BaseModel):
    id: int
    client_id: int
    title: str
    description: str
    category: str
    urgency: str
    status: str

    class Config:
        from_attributes = True