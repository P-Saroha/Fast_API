from pydantic import BaseModel,EmailStr,  Field, field_validator, model_validator
from typing import Optional, List, Dict, Annotated


class Patient(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100,title = "pateint name", description="Full name of the patient")]
    age: int
    email: EmailStr
    height: Optional[float] = None
    weight: Optional[float] = Field(default=None, ge=0, description="Weight in kilograms, must be non-negative") 
    bmi: Optional[float] = None
    contact_info: Optional[Dict[str, str]] = None
    
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

    @field_validator('age', mode='before')
    @classmethod
    def age_validator(cls, value):
        if value < 0 or value > 100:
            raise ValueError("Age must be between 0 and 100.")
        return value
    

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model: 'Patient'):
        if model.age > 60 and 'emergency_contact' not in model.contact_info:
            raise ValueError("Emergency contact is required for patients over 60 years old.")
        return model





# Example usage of the Patient model
def insert_patient(patient: Patient):
    # Here you would typically insert the patient into a database or perform some action
    print(f"Inserting patient: {patient.name}, Age: {patient.age}, Email: {patient.email}, Height: {patient.height}, Weight: {patient.weight}, BMI: {patient.bmi} ,Contact: {patient.contact_info}" )

patient_info = { 'name': 'Parveen', 'age': 20, 'email': 'pks@iitm.com', 'height': 5.5, 'weight': 60.0, 'bmi': 22.0, 'contact_info': {'phone': '123-456-7890', 'email':'abbb@iitm.com'} }

pateint1 = Patient(**patient_info)
insert_patient(pateint1)

