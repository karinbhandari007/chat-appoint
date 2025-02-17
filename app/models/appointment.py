# app/models/appointment.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Appointment(BaseModel):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    clinic_id = Column(Integer, ForeignKey("clinics.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)  # Foreign key to Patient
    appointment_time = Column(DateTime, nullable=False)
    status = Column(String(20), default="scheduled")  # e.g., scheduled, completed, canceled

    # Relationships
    clinic = relationship("Clinic", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")  # Link to Patient

    def __repr__(self):
        return f"<Appointment id={self.id}, clinic_id={self.clinic_id}, patient_id={self.patient_id}, time={self.appointment_time}>"