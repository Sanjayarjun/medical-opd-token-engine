from datetime import datetime
from pydantic import BaseModel


class TimeSlotCreate(BaseModel):
    start_time: datetime
    end_time: datetime
    capacity: int


class TimeSlotResponse(BaseModel):
    id: int
    doctor_id: int
    start_time: datetime
    end_time: datetime
    capacity: int
    created_at: datetime

    class Config:
        from_attributes = True
