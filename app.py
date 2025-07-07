from fastapi import FastAPI, HTTPException, Path, Query
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
