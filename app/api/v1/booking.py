from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.models.entities import Doctor, TimeSlot, Patient, Appointment, Token
from app.schemas.booking import BookingRequest, BookingResponse

router = APIRouter()


@router.post("/book", response_model=BookingResponse)
def book_token(payload: BookingRequest, db: Session = Depends(get_db)):
    # 1) doctor exists
    doctor = db.query(Doctor).filter(Doctor.id == payload.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # 2) doctor active
    if not doctor.is_active:
        raise HTTPException(status_code=400, detail="Doctor is not active")

    now = datetime.now(timezone.utc)

    # 3) pick earliest slot that is NOT ended
    slot = (
        db.query(TimeSlot)
        .filter(TimeSlot.doctor_id == doctor.id)
        .order_by(TimeSlot.start_time.asc())
        .all()
    )

    if not slot:
        raise HTTPException(status_code=400, detail="No slots available for this doctor")

    # choose first slot that hasn't ended
    active_slot = None
    for s in slot:
        end_time = s.end_time
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=timezone.utc)

        if end_time > now:
            active_slot = s
            break

    if not active_slot:
        raise HTTPException(status_code=400, detail="All doctor slots already ended")

    slot = active_slot

    # normalize slot times
    slot_start = slot.start_time
    if slot_start.tzinfo is None:
        slot_start = slot_start.replace(tzinfo=timezone.utc)

    slot_end = slot.end_time
    if slot_end.tzinfo is None:
        slot_end = slot_end.replace(tzinfo=timezone.utc)

    # 4) Get or create patient by phone
    patient = db.query(Patient).filter(Patient.phone == payload.patient_phone).first()
    if not patient:
        patient = Patient(name=payload.patient_name, phone=payload.patient_phone)
        db.add(patient)
        db.commit()
        db.refresh(patient)

    # 5) Prevent duplicate booking (same patient + same slot)
    existing_appt = (
        db.query(Appointment)
        .filter(
            Appointment.patient_id == patient.id,
            Appointment.slot_id == slot.id,
            Appointment.status == "BOOKED",
        )
        .first()
    )
    if existing_appt:
        raise HTTPException(status_code=400, detail="Patient already has a booking in this slot")

    # 6) Capacity check (count only BOOKED)
    booked_count = (
        db.query(func.count(Appointment.id))
        .filter(Appointment.slot_id == slot.id, Appointment.status == "BOOKED")
        .scalar()
    )
    if booked_count >= slot.capacity:
        raise HTTPException(status_code=400, detail="Slot is full")

    # 7) Create appointment
    appointment = Appointment(
        doctor_id=doctor.id,
        patient_id=patient.id,
        slot_id=slot.id,
        status="BOOKED",
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    # 8) Allocate token number safely (retry once if conflict)
    for _ in range(2):
        try:
            last_token = (
                db.query(func.max(Token.token_number))
                .filter(Token.slot_id == slot.id)
                .scalar()
            )
            token_number = (last_token or 0) + 1

            token = Token(
                appointment_id=appointment.id,
                slot_id=slot.id,
                token_number=token_number,
                source=payload.source,
            )

            db.add(token)
            db.commit()
            db.refresh(token)
            break

        except IntegrityError:
            db.rollback()
            continue
    else:
        raise HTTPException(status_code=500, detail="Token allocation failed. Try again.")

    # 9) Estimated time
    slot_duration = slot_end - slot_start
    per_patient = slot_duration / slot.capacity
    estimated_time = slot_start + (token.token_number - 1) * per_patient

    return BookingResponse(
        appointment_id=appointment.id,
        token_number=token.token_number,
        slot_id=slot.id,
        estimated_time=estimated_time,
    )
