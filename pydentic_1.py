from pydantic import BaseModel
class Patient(BaseModel):
    name: str
    age: int

# Example usage of the Patient model
def insert_patient(patient: Patient):
    # Here you would typically insert the patient into a database or perform some action
    print(f"Inserting patient: {patient.name}, Age: {patient.age}")

patient_info = { 'name': 'Parveen', 'age': 20}

pateint1 = Patient(**patient_info)

