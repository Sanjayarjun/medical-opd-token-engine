from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class TokenSource(str, Enum):
    ONLINE = "ONLINE"
    WALK_IN = "WALK_IN"
    PRIORITY = "PRIORITY"
    FOLLOW_UP = "FOLLOW_UP"


class BookingRequest(BaseModel):
    doctor_id: int
    patient_name: str
    patient_phone: str
    source: TokenSource = TokenSource.ONLINE


class BookingResponse(BaseModel):
    appointment_id: int
    token_number: int
    slot_id: int
    estimated_time: datetime
