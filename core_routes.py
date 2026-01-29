from fastapi import APIRouter, HTTPException
from models.user import CreateProfileRequest, ProfileResponse, SuccessResponse
from services.profile_service import profile_service
from services.validation_service import validation_service

router = APIRouter()

@router.get("/profile/{profile_id}", response_model=ProfileResponse)
def get_profile(profile_id: int):
    profile = profile_service.get_profile(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
        
    return {
        "last_name": profile["last_name"],
        "first_name": profile["first_name"],
        "date_of_birth": profile["date_of_birth"]
    }

@router.post("/create-profile", response_model=SuccessResponse)
async def create_profile(request: CreateProfileRequest):
    # extraction of Profile Data
    profile_data = request.profile_data
    
    # image analysis - ID card   
    try:
        extracted_id_data = validation_service.analyze_id_card(request.image1)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed for ID: {str(e)}")

    # compare extracted ID data
    id_last_name = extracted_id_data.get("last_name", "")
    id_first_name = extracted_id_data.get("first_name", "")
    id_dob_str = extracted_id_data.get("date_of_birth", "")
    
    if (id_last_name.lower() != profile_data.last_name.lower() or
        id_first_name.lower() != profile_data.first_name.lower()):
        if str(profile_data.date_of_birth) != id_dob_str:
             raise HTTPException(status_code=400, detail="ID data mismatch")

    # image analysis - salary slip
    try:
        extracted_salary = validation_service.analyze_salary_slip(request.image2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed for Salary Slip: {str(e)}")

    # check salary match
    if abs(extracted_salary - profile_data.salary) > 50.0: 
        raise HTTPException(status_code=400, detail="Salary data mismatch")

    # save to database
    try:
        profile_service.insert_profile({
            "last_name": profile_data.last_name,
            "first_name": profile_data.first_name,
            "date_of_birth": profile_data.date_of_birth,
            "salary": extracted_salary
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return {
        "status": "success",
        "salary": extracted_salary
    }
