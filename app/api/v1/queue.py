from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import asc, func

from app.core.database import get_db
from app.models.entities import Doctor, TimeSlot, Appointment, Token, Patient
from app.schemas.queue import QueueResponse, QueueTokenItem

router = APIRouter()


@router.get("/doctors/{doctor_id}/queue", response_model=QueueResponse)
def get_queue(doctor_id: int, db: Session = Depends(get_db)):
    # 1) Check doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # 2) Get earliest slot for doctor
    slot = (
        db.query(TimeSlot)
        .filter(TimeSlot.doctor_id == doctor_id)
        .order_by(TimeSlot.start_time.asc())
        .first()
    )
    if not slot:
        raise HTTPException(status_code=404, detail="No slot found for this doctor")

    # 3) Join tokens -> appointment -> patient
    rows = (
        db.query(Token, Appointment, Patient)
        .join(Appointment, Appointment.id == Token.appointment_id)
        .join(Patient, Patient.id == Appointment.patient_id)
        .filter(Token.slot_id == slot.id)
        .order_by(asc(Token.token_number))
        .all()
    )

    # 4) Build queue list (only BOOKED)
    tokens = []
    for token, appt, patient in rows:
        if appt.status != "BOOKED":
            continue

        tokens.append(
            QueueTokenItem(
                appointment_id=appt.id,
                patient_name=patient.name,
                patient_phone=patient.phone,
                token_number=token.token_number,
                created_at=token.created_at,
            )
        )

    # 5) booked means number of currently waiting patients (BOOKED)
    booked = len(tokens)

    # ✅ Correct next token logic: max token_number + 1
    last_token = (
        db.query(func.max(Token.token_number))
        .filter(Token.slot_id == slot.id)
        .scalar()
    )
    next_token = (last_token or 0) + 1

    return QueueResponse(
        doctor_id=doctor_id,
        slot_id=slot.id,
        slot_start_time=slot.start_time,
        slot_end_time=slot.end_time,
        capacity=slot.capacity,
        booked=booked,
        next_token_number=next_token,
        tokens=tokens,
    )
