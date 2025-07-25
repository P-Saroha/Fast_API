from pydantic import BaseModel,EmailStr,  Field, computed_field
from typing import Optional, List, Dict, Annotated


class Patient(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100,title = "pateint name", description="Full name of the patient")]
    age: int
    email: EmailStr
    height: Optional[float] = None
    weight: Optional[float] = Field(default=None, ge=0, description="Weight in kilograms, must be non-negative") 
    contact_info: Optional[Dict[str, str]] = None
    bmi = Optional[float] = None
    
    @computed_field
    @property
    def calculate_bmi(self) -> float:
        if self.height and self.weight:
            return round(self.weight / (self.height ** 2), 2)

# Example usage of the Patient model
def insert_patient(patient: Patient):
    # Here you would typically insert the patient into a database or perform some action
    print(f"Inserting patient: {patient.name}, Age: {patient.age}, Email: {patient.email}, Height: {patient.height}, Weight: {patient.weight}, Contact: {patient.contact_info}, BMI : {patient.calculate_bmi}") 

patient_info = { 'name': 'Parveen', 'age': 20, 'email': 'pks@iitm.com', 'height': 1.9, 'weight': 60.0,  'contact_info': {'phone': '123-456-7890', 'email':'abbb@iitm.com'} }

pateint1 = Patient(**patient_info)
insert_patient(pateint1)

