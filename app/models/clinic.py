# app/models/clinic.py
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Clinic(BaseModel):
    __tablename__ = "clinics"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    zip_code = Column(String(20), nullable=False)
    latitude = Column(Float, nullable=False)  # For location-based queries
    longitude = Column(Float, nullable=False)  # For location-based queries

    # Relationships
    appointments = relationship("Appointment", back_populates="clinic")
    vaccines = relationship("Vaccine", back_populates="clinic")

    def __repr__(self):
        return f"<Clinic {self.name}>"