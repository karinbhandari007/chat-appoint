from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import init_db
from app.models.clinic import Clinic
from app.models.patient import Patient
from app.models.vaccine import Vaccine
from app.models.appointment import Appointment
from app.core.config import settings
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

DATABASE_URL = "postgresql://postgres:root@localhost/signetic_ai_scheduler"

# Function to generate random clinics
def generate_clinics(num):
    clinics = []
    for _ in range(num):
        clinic = {
            "name": fake.company() + " Clinic",
            "address": fake.street_address(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "zip_code": fake.zipcode(),
            "latitude": fake.latitude(),
            "longitude": fake.longitude(),
        }
        clinics.append(clinic)
    return clinics

# Function to generate random patients
def generate_patients(num):
    patients = []
    for _ in range(num):
        patient = {
            "name": fake.name(),
            "email": fake.unique.email(),
        }
        patients.append(patient)
    return patients

# Function to generate random vaccines
def generate_vaccines(num, clinic_ids):
    vaccines = []
    for _ in range(num):
        vaccine = {
            "clinic_id": random.choice(clinic_ids),
            "name": random.choice(["Pfizer", "Moderna", "Johnson & Johnson"]),
            # "manufacturer": random.choice(["Pfizer Inc.", "Moderna Inc.", "Johnson & Johnson"]),
            # "lot_number": fake.bothify(text='LOT#####'),
            # "quantity": random.randint(1, 200),
            # "expiration_date": fake.date_between(start_date='today', end_date='+2y'),
            # "storage_temperature": random.uniform(-20.0, 8.0),  # Example temperature range
            # "minimum_age": random.randint(12, 65),
            # "dose_number": random.choice([1, 2]),
            # "status": random.choice(["available", "reserved", "depleted"]),
        }
        vaccines.append(vaccine)
    return vaccines

# Function to generate random appointments
def generate_appointments(num, clinic_ids, patient_ids):
    appointments = []
    for _ in range(num):
        appointment = {
            "clinic_id": random.choice(clinic_ids),
            "patient_id": random.choice(patient_ids),
            "appointment_time": fake.date_time_between(start_date='now', end_date='+30d'),  # Appointments within the next 30 days
            "status": random.choice(["scheduled", "completed", "canceled"]),
        }
        appointments.append(appointment)
    return appointments

def seed_data():
    # Create a database engine
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Generate and seed clinics
    clinics_data = generate_clinics(150)  # Generate 150 clinics
    for clinic in clinics_data:
        clinic_instance = Clinic(**clinic)
        session.add(clinic_instance)

    session.commit()  # Commit to get clinic IDs
    clinic_ids = [clinic.id for clinic in session.query(Clinic).all()]  # Get generated clinic IDs

    # Generate and seed patients
    patients_data = generate_patients(100)  # Generate 100 patients
    for patient in patients_data:
        patient_instance = Patient(**patient)
        session.add(patient_instance)

    session.commit()  # Commit to get patient IDs
    patient_ids = [patient.id for patient in session.query(Patient).all()]  # Get generated patient IDs

    # Generate and seed vaccines
    vaccines_data = generate_vaccines(200, clinic_ids)  # Generate 200 vaccines
    for vaccine in vaccines_data:
        vaccine_instance = Vaccine(**vaccine)
        session.add(vaccine_instance)

    session.commit()  # Commit vaccines

    # Generate and seed appointments
    appointments_data = generate_appointments(100, clinic_ids, patient_ids)  # Generate 100 appointments
    for appointment in appointments_data:
        appointment_instance = Appointment(**appointment)
        session.add(appointment_instance)

    session.commit()  # Commit appointments
    session.close()
    print("Seeding completed!")

if __name__ == "__main__":
    init_db()  # Ensure the database tables are created
    seed_data()