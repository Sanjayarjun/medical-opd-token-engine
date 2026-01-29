from enum import Enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class TokenSource(str, Enum):
    PRIORITY = "PRIORITY"
    FOLLOW_UP = "FOLLOW_UP"
    ONLINE = "ONLINE"
    WALK_IN = "WALK_IN"


def source_to_rank(source: str) -> int:
    mapping = {
        "PRIORITY": 1,
        "FOLLOW_UP": 2,
        "ONLINE": 3,
        "WALK_IN": 4,
    }
    return mapping.get(source, 3)


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=True)

    doctor_code = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    slots = relationship("TimeSlot", back_populates="doctor", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="doctor", cascade="all, delete-orphan")


class TimeSlot(Base):
    __tablename__ = "time_slots"

    id = Column(Integer, primary_key=True, index=True)

    doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)

    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)

    capacity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    doctor = relationship("Doctor", back_populates="slots")

    appointments = relationship("Appointment", back_populates="slot", cascade="all, delete-orphan")
    tokens = relationship("Token", back_populates="slot", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("doctor_id", "start_time", "end_time", name="uq_doctor_slot"),
    )


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    phone = Column(String, nullable=False, unique=True, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    slot_id = Column(Integer, ForeignKey("time_slots.id", ondelete="CASCADE"), nullable=False)

    status = Column(String, nullable=False, default="BOOKED")

    # ✅ REQUIRED FOR PRIORITY ENGINE
    source = Column(String, nullable=False, default="ONLINE")
    priority_rank = Column(Integer, nullable=False, default=3)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")
    slot = relationship("TimeSlot", back_populates="appointments")

    token = relationship("Token", back_populates="appointment", uselist=False, cascade="all, delete-orphan")


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)

    appointment_id = Column(Integer, ForeignKey("appointments.id", ondelete="CASCADE"), nullable=False, unique=True)
    slot_id = Column(Integer, ForeignKey("time_slots.id", ondelete="CASCADE"), nullable=False)

    token_number = Column(Integer, nullable=False)
    source = Column(String, nullable=False, default="ONLINE")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    appointment = relationship("Appointment", back_populates="token")
    slot = relationship("TimeSlot", back_populates="tokens")

    __table_args__ = (
        UniqueConstraint("slot_id", "token_number", name="uq_slot_token_number"),
    )
