from datetime import datetime
from pydantic import BaseModel


class AppointmentResponse(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    slot_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
