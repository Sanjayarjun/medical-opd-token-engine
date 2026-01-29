from datetime import datetime
from pydantic import BaseModel


class DoctorCreate(BaseModel):
    name: str
    specialization: str | None = None
    doctor_code: str


class DoctorResponse(BaseModel):
    id: int
    name: str
    specialization: str | None
    doctor_code: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
