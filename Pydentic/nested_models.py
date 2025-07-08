from pydantic import BaseModel, Field

class Address(BaseModel):
    street: str = Field(..., description="The street address")
    city: str = Field(..., description="The city name")
    state: str = Field(..., description="The state or province")
    zip_code: str = Field(..., description="The postal code")

class Patient(BaseModel):
    name: str
    age: int
    address: Address

address_example = Address(
    street="123 Main St",
    city="rohtak",
    state="Hrayana",
    zip_code="12345"
)

patient_example = Patient(
    name="John Doe",
    age=30,
    address=address_example
)

print(patient_example)