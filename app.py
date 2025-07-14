from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json


app = FastAPI()

def get_json():
    with open('patients.json', 'r') as file:
        data = json.load(file)  # Use json.load() instead of file.read()
    return data

@app.get("/")
async def root():
    return {"message": "Patient Management System API"}

@app.get('/about')
async def about():
    return {
        "name": "Patient Management System API",
        "version": "1.0.0",
        "description": "API for managing patient records, appointments, and medical history."
    }

@app.get("/view-patients")
async def view_patients():
    data = get_json()
    return {"patients": data}

@app.get('/patient/{patient_id}')
async def view_patient(patient_id: str = Path(..., description="The ID of the patient to view")):
    data = get_json()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort')
def sort_patients(
    sort_by: str = Query("name", description="Field to sort by", enum=["name", "age","bmi", "height", "weight"]), 
    order: str = Query("asc", description="Sort order", enum=["asc", "desc"])):
    valid_sort_fields = ["name", "age", "bmi", "height", "weight"]
    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort_by}. Valid fields are: {', '.join(valid_sort_fields)}")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Use 'asc' or 'desc'.")
    data = get_json()
    patients = list(data.values())  
    reverse = order == "desc"
    sorted_patients = sorted(patients, key=lambda x: x[sort_by], reverse=reverse)
    return {"sorted_patients": sorted_patients} 



def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)
        

## Models for Patient and PatientUpdate which will be used for creating and updating patient records and also for validation
class Patient(BaseModel):

    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]

## Computed fields for BMI and Verdict @computed_field decorator is used to define fields that are computed based on other fields in the model.
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'

# Model for updating patient information and it allows partial updates to the patient information.
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

## Endpoint for editing the patient information.
@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = get_json()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    #existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pydandic_obj = Patient(**existing_patient_info)
    #-> pydantic object -> dict
    existing_patient_info = patient_pydandic_obj.model_dump(exclude='id')

    # add this dict to data
    data[patient_id] = existing_patient_info

    # save data
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated'})

# Endpoint for deleting a patient record.
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    # load data
    data = get_json()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient deleted'})

