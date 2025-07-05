from fastapi import FastAPI

app = FastAPI()

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

 