from datetime import datetime
from pydantic import BaseModel


class QueueTokenItem(BaseModel):
    appointment_id: int
    patient_name: str
    patient_phone: str
    token_number: int
    created_at: datetime


class QueueResponse(BaseModel):
    doctor_id: int
    slot_id: int
    slot_start_time: datetime
    slot_end_time: datetime
    capacity: int
    booked: int
    next_token_number: int
    tokens: list[QueueTokenItem]
