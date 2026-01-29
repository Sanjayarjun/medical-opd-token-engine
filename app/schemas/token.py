from datetime import datetime
from pydantic import BaseModel


class TokenResponse(BaseModel):
    id: int
    appointment_id: int
    slot_id: int
    token_number: int
    created_at: datetime

    class Config:
        from_attributes = True
