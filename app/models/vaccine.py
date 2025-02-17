# app/models/vaccine.py
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Vaccine(BaseModel):
    __tablename__ = "vaccines"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    clinic_id = Column(Integer, ForeignKey("clinics.id"), nullable=False)

    # Relationship back to Clinic
    clinic = relationship("Clinic", back_populates="vaccines")

    def __repr__(self):
        return f"<Vaccine {self.name}>"