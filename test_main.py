from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
from datetime import date
import json

client = TestClient(app)

def test_get_profile():
    response = client.get("/profile")
    assert response.status_code == 200
    data = response.json()
    assert data["last_name"] == "Doe"
    assert data["first_name"] == "John"

@patch("main.ocr_service")
def test_create_profile_success(mock_ocr):
    # Setup happy path mocks
    mock_ocr.analyze_id_card.return_value = {
        "last_name": "Doe",
        "first_name": "John",
        "date_of_birth": "1990-01-01"
    }
    mock_ocr.analyze_salary_slip.return_value = 5000.0

    payload = {
        "text_data": {
            "last_name": "Doe",
            "first_name": "John",
            "date_of_birth": "1990-01-01",
            "salary": 5000.0
        },
        "image1": "mock_base64_id",
        "image2": "mock_base64_salary"
    }

    response = client.post("/create-profile", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_create_profile_text_mismatch():
    payload = {
        "text_data": {
            "last_name": "Smith", # Mismatch with DB (Doe)
            "first_name": "John",
            "date_of_birth": "1990-01-01",
            "salary": 5000.0
        },
        "image1": "mock_base64_id",
        "image2": "mock_base64_salary"
    }
    response = client.post("/create-profile", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Text data mismatch"

@patch("main.ocr_service")
def test_create_profile_id_mismatch(mock_ocr):
    # ID scan returns different name
    mock_ocr.analyze_id_card.return_value = {
        "last_name": "Smith",
        "first_name": "John",
        "date_of_birth": "1990-01-01"
    }

    payload = {
        "text_data": {
            "last_name": "Doe",
            "first_name": "John",
            "date_of_birth": "1990-01-01",
            "salary": 5000.0
        },
        "image1": "mock_base64_id",
        "image2": "mock_base64_salary"
    }
    
    response = client.post("/create-profile", json=payload)
    assert response.status_code == 400
    assert "ID data mismatch" in response.json()["detail"]

@patch("main.ocr_service")
def test_create_profile_salary_mismatch(mock_ocr):
    # ID matches
    mock_ocr.analyze_id_card.return_value = {
        "last_name": "Doe",
        "first_name": "John",
        "date_of_birth": "1990-01-01"
    }
    # Salary scan returns vastly different amount
    mock_ocr.analyze_salary_slip.return_value = 1000.0

    payload = {
        "text_data": {
            "last_name": "Doe",
            "first_name": "John",
            "date_of_birth": "1990-01-01",
            "salary": 5000.0
        },
        "image1": "mock_base64_id",
        "image2": "mock_base64_salary"
    }
    
    response = client.post("/create-profile", json=payload)
    assert response.status_code == 400
    assert "Salary data mismatch" in response.json()["detail"]
