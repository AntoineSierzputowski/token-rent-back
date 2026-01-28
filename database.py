from datetime import date

class MockDB:
    def __init__(self):
        # Initial mock state
        self.profile = {
            "last_name": "Doe",
            "first_name": "John",
            "date_of_birth": date(1990, 1, 1),
            "salary": 5000.0  # Optional, but useful for validation if needed
        }

    def get_profile(self):
        return self.profile

    def update_profile(self, data: dict):
        self.profile.update(data)

db = MockDB()
