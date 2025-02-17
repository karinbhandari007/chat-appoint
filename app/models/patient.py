# app/models/patient.py
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Patient(BaseModel):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    # Relationships
    appointments = relationship("Appointment", back_populates="patient")

    def __repr__(self):
        return f"<Patient id={self.id}, name={self.name}>"