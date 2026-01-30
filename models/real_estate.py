from pydantic import BaseModel
from typing import Optional

class CreateRealEstateRequest(BaseModel):
    rent_price: float

class RealEstateResponse(BaseModel):
    id: str
    rent_price: float
    minimum_salary_eligibility: float
