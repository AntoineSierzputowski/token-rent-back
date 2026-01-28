from pydantic import BaseModel
from datetime import date

class TextData(BaseModel):
    last_name: str
    first_name: str
    date_of_birth: date
    salary: float

class CreateProfileRequest(BaseModel):
    text_data: TextData
    image1: str  # Base64 encoded ID image
    image2: str  # Base64 encoded Salary Slip image

class ProfileResponse(BaseModel):
    last_name: str
    first_name: str
    date_of_birth: date

class SuccessResponse(BaseModel):
    status: str
    salary: float
