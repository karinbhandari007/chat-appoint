from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import ConversationChain
from app.core.config import settings
from sqlalchemy.orm import Session #DB-QUERY
from app.models.clinic import Clinic #DB-QUERY
from app.models.vaccine import Vaccine #DB-QUERY
from app.models.appointment import Appointment #DB-QUERY
from typing import Dict, Any
import re  # Import regex for extraction
from .location_coordinates import location_coordinates

class AIService:
    def __init__(self, db_session: Session):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",  
            temperature=0.7,
            api_key=settings.OPENAI_API_KEY
        )
        self.prompt = PromptTemplate.from_template("{input}")
        self.chain = self.prompt | self.llm | StrOutputParser()
        self.db_session = db_session  #DB-QUERY  # Inject the database session
        self.conversation_chain = ConversationChain(llm=self.llm)  #DB-QUERY


    async def process_query(self, message: str, context: Dict[str, Any]) -> Dict[Any, Any]:
        """Process user messages and extract appointment-related information"""
        context['last_message'] = message
            # Combine system prompt with user message
        # full_prompt = f"You are a helpful AI assistant for a vaccination scheduling system. {message}"

        system_prompt = """
        You are a helpful AI assistant for a vaccination scheduling system. 
        Extract the following information from the user's message if present:
        - Vaccine type (e.g., Pfizer, Moderna, J&J)
        - Preferred location or area
        - Preferred date/time
        - Any special requirements
        
        If the information is not complete, ask follow-up questions.
        If all information is present, proceed with scheduling suggestions.
        """
        
        try:
            # Combine system prompt with user message
            full_prompt = f"{system_prompt}\nUser: {message}"

            # response = self.chain.invoke(full_prompt)

            response = self.conversation_chain.invoke(full_prompt, context=context)

            # # Extract information from the response
            # extracted_info = self.extract_information(response)

            # Parse the response to extract vaccine type and location
            vaccine_type = self.extract_vaccine_type(message)  #DB-QUERY
            location = self.extract_location(message)  #DB-QUERY

            extracted_info = {
                "vaccine_type": vaccine_type,  #DB-QUERY - previously none
                "location": location,  #DB-QUERY - previously none
                "datetime": None,
                "special_requirements": None
            }
            # # Update context with extracted information
            context.update(extracted_info)

            # Check if we have enough information to query the database
            if vaccine_type and location:
                # Query the database for available clinics
                available_clinics = self.find_available_clinics(vaccine_type, location)  #DB-QUERY
            else:
                available_clinics = []  # No need to query if we don't have enough info

            # Prepare the response based on the availability of clinics
            if not available_clinics:
                message = f"Sorry, I couldn't find any clinics that offer {vaccine_type} in {location}."
            else:
                message = response  # Use the original response if clinics are found

            # Parse the response and try to extract structured data
            parsed_data = {
                "type": "ai_response",
                "message": response,
                "available_clinics": available_clinics,  #DB-QUERY - previously none 
                "extracted_info": extracted_info,
                "requires_followup": not (vaccine_type and location),  # Set to True if we need more info
                "context": context 
            }

            return parsed_data
            
        except Exception as e:
            return {
                "type": "error",
                "message": f"Error processing message: {str(e)}"
            }
        
    def extract_vaccine_type(self, response: str) -> str:
        """
        Extract the vaccine type from the response using regex.
        
        :param response: The response string from the AI model
        :return: The extracted vaccine type or None if not found
        """
        # Example regex pattern to find vaccine types
        vaccine_pattern = r"(Pfizer|Moderna|Johnson & Johnson)"
        match = re.search(vaccine_pattern, response, re.IGNORECASE)
        return match.group(0) if match else None  # Return the matched vaccine type or None

    def extract_location(self, response: str) -> str:
        """
        Extract the location from the response using regex.
        
        :param response: The response string from the AI model
        :return: The extracted location or None if not found
        """
        # Example regex pattern to find locations (this can be refined)
        location_pattern = r"(in|at|near)\s+([A-Za-z\s]+)"
        match = re.search(location_pattern, response, re.IGNORECASE)
        return match.group(2).strip() if match else None  # Return the matched location or None


    def find_available_clinics(self, vaccine_type: str, location: str):
        """
        Query the database for available clinics based on the vaccine type and location.
        
        :param vaccine_type: The type of vaccine requested
        :param location: The location where the patient wants to find clinics
        :return: List of available clinics
        """
        # Convert location to coordinates (this is a placeholder; you may want to use a geocoding service)
        # For example, you can use a dictionary or a geocoding API to get coordinates
        patient_location = location_coordinates.get(location)

        if not patient_location:
            return []  # Return an empty list if location is not found

        # Query the database for available clinics
        return self.get_available_clinics(vaccine_type, patient_location)

    def get_available_clinics(self, vaccine_type: str, patient_location: tuple):
        """
        Query the database for available clinics based on the vaccine type and patient location.
        
        :param vaccine_type: The type of vaccine requested
        :param patient_location: A tuple containing the patient's latitude and longitude
        :return: List of available clinics with their details
        """


        patient_latitude, patient_longitude = patient_location


        # Query to find clinics that provide the desired vaccine
        clinics_with_vaccine = (
            self.db_session.query(Clinic)
            .join(Vaccine)
            .filter(Vaccine.name == vaccine_type)
            .all()
        )

        available_clinics = []

        for clinic in clinics_with_vaccine:
            # Check for available appointments
            available_appointments = (
                self.db_session.query(Appointment)
                .filter(
                    Appointment.clinic_id == clinic.id,
                    Appointment.status == "scheduled"  # Assuming 'scheduled' means available
                )
                .all()
            )

            if available_appointments:
                # Calculate distance to the clinic (you can use Haversine formula or similar)
                distance = self.calculate_distance(patient_latitude, patient_longitude, clinic.latitude, clinic.longitude)
                available_clinics.append({
                    "clinic": self.serialize_clinic(clinic),  # Serialize the clinic object
                    "appointments": [self.serialize_appointment(appointment) for appointment in available_appointments],  # Serialize appointments
                    "distance": distance
                })

        # Sort clinics by distance
        available_clinics.sort(key=lambda x: x["distance"])  # Sort by distance


        return available_clinics

    def serialize_clinic(self, clinic):
        """Convert a Clinic object to a dictionary."""
        return {
            "id": clinic.id,
            "name": clinic.name,
            "address": clinic.address,
            "city": clinic.city,
            "state": clinic.state,
            "zip_code": clinic.zip_code,
            "latitude": clinic.latitude,
            "longitude": clinic.longitude,
            "vaccines": [vaccine.name for vaccine in clinic.vaccines],  # List of vaccine names offered by the clinic
            # Add more fields as necessary
        }

    def serialize_appointment(self, appointment):
        """Convert an Appointment object to a dictionary."""
        return {
            "id": appointment.id,
            "clinic_id": appointment.clinic_id,
            "patient_id": appointment.patient_id,
            "appointment_time": appointment.appointment_time.isoformat(),  # Convert datetime to string
            "status": appointment.status,  # Status of the appointment (e.g., scheduled, completed, canceled)
            "created_at": appointment.created_at.isoformat(),  # When the appointment was created
            "updated_at": appointment.updated_at.isoformat(),  # When the appointment was last updated
            # Add more fields as necessary
        }

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate the distance between two geographical points using the Haversine formula.
        
        :param lat1: Latitude of the first point
        :param lon1: Longitude of the first point
        :param lat2: Latitude of the second point
        :param lon2: Longitude of the second point
        :return: Distance in kilometers
        """
        from math import radians, sin, cos, sqrt, atan2

        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        r = 6371  # Radius of Earth in kilometers
        return r * c  # Return distance in kilometers

    async def get_response(self, message: str) -> str:
        response = await self.chain.ainvoke({"input": message})
        return response