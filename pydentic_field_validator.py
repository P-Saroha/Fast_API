from pydantic import BaseModel,EmailStr,  Field, field_validator
from typing import Optional, List, Dict, Annotated


class Patient(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100,title = "pateint name", description="Full name of the patient")]
    age: int
    email: EmailStr
    height: Optional[float] = None
    weight: Optional[float] = Field(default=None, ge=0, description="Weight in kilograms, must be non-negative") 
    bmi: Optional[float] = None
    
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_email_domains = ['iitm.com', 'hdfc.com', 'pu.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_email_domains:
            raise ValueError(f"Email domain '{domain_name}' is not allowed. Allowed domains are: {', '.join(valid_email_domains)}")
        
    @field_validator('name')
    @classmethod
    def name_validator(cls, value):
        if not value.isalpha():
            raise ValueError("Name must contain only alphabetic characters.")
        return value

# Example usage of the Patient model
def insert_patient(patient: Patient):
    # Here you would typically insert the patient into a database or perform some action
    print(f"Inserting patient: {patient.name}, Age: {patient.age}, Email: {patient.email}, Height: {patient.height}, Weight: {patient.weight}, BMI: {patient.bmi}")

patient_info = { 'name': 'Parveen', 'age': 20, 'email': 'pks@iitm.com', 'height': 5.5, 'weight': 60.0, 'bmi': 22.0}

pateint1 = Patient(**patient_info)
insert_patient(pateint1)

