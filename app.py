from fastapi import FastAPI

app = FastAPI()

def get_json():
    with open('patients.json', 'r') as file:
        data = file.read()
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