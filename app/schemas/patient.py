from pydantic import BaseModel


class PatientCreate(BaseModel):
    name: str
    phone: str
