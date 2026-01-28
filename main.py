from fastapi import FastAPI, HTTPException
from schemas import CreateProfileRequest, ProfileResponse, SuccessResponse
from database import db
from ocr import ocr_service
from datetime import date

app = FastAPI(title="Profile Validation API", version="0.1")

@app.get("/profile", response_model=ProfileResponse)
def get_profile():
    profile = db.get_profile()
    return {
        "last_name": profile["last_name"],
        "first_name": profile["first_name"],
        "date_of_birth": profile["date_of_birth"]
    }

@app.post("/create-profile", response_model=SuccessResponse)
async def create_profile(request: CreateProfileRequest):
    # 1. Text Validation
    stored_profile = db.get_profile()
    
    if (request.text_data.last_name != stored_profile["last_name"] or
        request.text_data.first_name != stored_profile["first_name"] or
        request.text_data.date_of_birth != stored_profile["date_of_birth"]):
        
        raise HTTPException(status_code=400, detail="Text data mismatch")

    # 2. Image Analysis - ID Card
    try:
        extracted_id_data = ocr_service.analyze_id_card(request.image1)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed for ID: {str(e)}")

    # Sanitize and compare extracted ID data
    id_last_name = extracted_id_data.get("last_name", "")
    id_first_name = extracted_id_data.get("first_name", "")
    id_dob_str = extracted_id_data.get("date_of_birth", "")
    
    if (id_last_name.lower() != request.text_data.last_name.lower() or
        id_first_name.lower() != request.text_data.first_name.lower()):
        if str(request.text_data.date_of_birth) != id_dob_str:
             raise HTTPException(status_code=400, detail="ID data mismatch")

    # 3. Image Analysis - Salary Slip
    try:
        extracted_salary = ocr_service.analyze_salary_slip(request.image2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed for Salary Slip: {str(e)}")

    # Check salary match
    if abs(extracted_salary - request.text_data.salary) > 50.0: 
        raise HTTPException(status_code=400, detail="Salary data mismatch")

    return {
        "status": "success",
        "salary": extracted_salary
    }
