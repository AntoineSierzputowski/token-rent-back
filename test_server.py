from fastapi.testclient import TestClient
from server import app
from unittest.mock import patch
from datetime import date
import json

client = TestClient(app)

def test_get_profile():
    with patch("core_routes.profile_service.get_profile") as mock_get:
        mock_get.return_value = {
            "last_name": "Doe",
            "first_name": "John",
            "date_of_birth": date(1990, 1, 1),
            "salary": 5000.0
        }
        response = client.get("/profile/1")
        assert response.status_code == 200
        data = response.json()
        assert data["last_name"] == "Doe"
        assert data["first_name"] == "John"

@patch("core_routes.profile_service.insert_profile")
@patch("core_routes.validation_service")
def test_create_profile_success(mock_validation, mock_db_insert):
    # Setup happy path mocks
    mock_validation.analyze_id_card.return_value = {
        "last_name": "Doe",
        "first_name": "John",
        "date_of_birth": "1990-01-01"
    }
    mock_validation.analyze_salary_slip.return_value = 5000.0
    mock_db_insert.return_value = None

    payload = {
        "profile_data": {
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
    mock_db_insert.assert_called_once()

@patch("core_routes.validation_service")
def test_create_profile_id_mismatch(mock_validation):
    # ID scan returns different name
    mock_validation.analyze_id_card.return_value = {
        "last_name": "Smith",
        "first_name": "John",
        "date_of_birth": "1990-01-01"
    }

    payload = {
        "profile_data": {
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

@patch("core_routes.validation_service")
def test_create_profile_salary_mismatch(mock_validation):
    # ID matches
    mock_validation.analyze_id_card.return_value = {
        "last_name": "Doe",
        "first_name": "John",
        "date_of_birth": "1990-01-01"
    }
    # Salary scan returns vastly different amount
    mock_validation.analyze_salary_slip.return_value = 1000.0

    payload = {
        "profile_data": {
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
