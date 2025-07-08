from pydantic import BaseModel
from typing import Optional, List, Dict, EmailStr, Field


class Patient(BaseModel):
    name: str
    age: int
    email: Optional[EmailStr] = None
    height: Optional[float] = None
    weight: Optional[float] = Field(default=None, ge=0, description="Weight in kilograms, must be non-negative") 
    bmi: Optional[float] = None
    medical_history: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    medications: Optional[List[str]] = None
    contact_info: Optional[Dict[str, str]] = None
    emergency_contact: Optional[Dict[str, str]] = None
     

# Example usage of the Patient model
def insert_patient(patient: Patient):
    # Here you would typically insert the patient into a database or perform some action
    print(f"Inserting patient: {patient.name}, Age: {patient.age}")

patient_info = { 'name': 'Parveen', 'age': 20, 'emal': 'pks@gmail.com', 'height': 5.5, 'weight': 60.0, 'bmi': 22.0,
                 'medical_history': ['asthma'], 'allergies': ['pollen'], 'medications': ['inhaler'],
                 'contact_info': {'phone': '123-456-7890', 'email': 'abc@gmail.com'},
                 'emergency_contact': {'name': 'ABBA', 'phone': '987-654-3210'} }

pateint1 = Patient(**patient_info)

