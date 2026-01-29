from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.entities import Appointment
from app.schemas.appointment import AppointmentResponse

router = APIRouter()


@router.patch("/appointments/{appointment_id}/cancel", response_model=AppointmentResponse)
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if appt.status != "BOOKED":
        raise HTTPException(status_code=400, detail=f"Cannot cancel appointment in status {appt.status}")

    appt.status = "CANCELLED"
    db.commit()
    db.refresh(appt)
    return appt


@router.patch("/appointments/{appointment_id}/serve", response_model=AppointmentResponse)
def serve_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if appt.status != "BOOKED":
        raise HTTPException(status_code=400, detail=f"Cannot serve appointment in status {appt.status}")

    appt.status = "SERVED"
    db.commit()
    db.refresh(appt)
    return appt
