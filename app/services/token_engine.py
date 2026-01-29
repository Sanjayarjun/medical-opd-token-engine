from datetime import timedelta

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.entities import Doctor, TimeSlot, Patient, Appointment, Token, TokenSource


def allocate_token(db: Session, doctor_id: int, patient_name: str, patient_phone: str, source: TokenSource):
    # 1) doctor check
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        return None, "Doctor not found"
    if not doctor.is_active:
        return None, "Doctor is inactive"

    # 2) find first active slot (earliest upcoming)
    slot = (
        db.query(TimeSlot)
        .filter(TimeSlot.doctor_id == doctor_id)
        .order_by(TimeSlot.start_time.asc())
        .first()
    )

    if not slot:
        return None, "No slots available for this doctor"

    # 3) capacity check
    booked_count = db.query(Appointment).filter(
        Appointment.slot_id == slot.id,
        Appointment.status == "BOOKED"
    ).count()

    if booked_count >= slot.capacity:
        return None, "Slot is full"

    # 4) patient upsert
    patient = db.query(Patient).filter(Patient.phone == patient_phone).first()
    if not patient:
        patient = Patient(name=patient_name, phone=patient_phone)
        db.add(patient)
        db.commit()
        db.refresh(patient)

    # 5) create appointment
    appointment = Appointment(
        doctor_id=doctor_id,
        patient_id=patient.id,
        slot_id=slot.id,
        status="BOOKED",
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    # 6) token_number = max + 1 (SAFE)
    max_token = db.query(func.max(Token.token_number)).filter(Token.slot_id == slot.id).scalar()
    next_token = (max_token or 0) + 1

    token = Token(
        appointment_id=appointment.id,
        slot_id=slot.id,
        token_number=next_token,
        source=source.value if hasattr(source, "value") else str(source),
    )
    db.add(token)
    db.commit()
    db.refresh(token)

    # 7) estimated_time
    per_patient_minutes = 10
    estimated_time = slot.start_time + timedelta(minutes=(next_token - 1) * per_patient_minutes)

    return {
        "appointment_id": appointment.id,
        "token_number": token.token_number,
        "slot_id": slot.id,
        "estimated_time": estimated_time,
    }, None
