from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.entities import Doctor, TimeSlot
from app.schemas.doctor import DoctorCreate, DoctorResponse
from app.schemas.slot import TimeSlotResponse, TimeSlotCreate

# routers
from app.api.v1.booking import router as booking_router
from app.api.v1.queue import router as queue_router
from app.api.v1.appointments import router as appointment_router

router = APIRouter()

# include sub routers FIRST
router.include_router(booking_router, tags=["Booking"])
router.include_router(queue_router, tags=["Queue"])
router.include_router(appointment_router, tags=["Appointments"])


@router.get("/test")
def test_api():
    return {"message": "API working ✅"}


# ---------------- DOCTORS ----------------

@router.get("/doctors", response_model=list[DoctorResponse])
def list_doctors(db: Session = Depends(get_db)):
    return db.query(Doctor).order_by(Doctor.id.asc()).all()


@router.post("/doctors", response_model=DoctorResponse)
def create_doctor(payload: DoctorCreate, db: Session = Depends(get_db)):
    existing = db.query(Doctor).filter(Doctor.doctor_code == payload.doctor_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="doctor_code already exists")

    doctor = Doctor(
        name=payload.name,
        specialization=payload.specialization,
        doctor_code=payload.doctor_code,
        is_active=True,
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


# ---------------- SLOTS ----------------

@router.get("/doctors/{doctor_id}/slots", response_model=list[TimeSlotResponse])
def get_doctor_slots(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return (
        db.query(TimeSlot)
        .filter(TimeSlot.doctor_id == doctor_id)
        .order_by(TimeSlot.start_time.asc())
        .all()
    )


@router.post("/doctors/{doctor_id}/slots", response_model=TimeSlotResponse)
def create_slot(doctor_id: int, payload: TimeSlotCreate, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    slot = TimeSlot(
        doctor_id=doctor_id,
        start_time=payload.start_time,
        end_time=payload.end_time,
        capacity=payload.capacity,
    )
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot
