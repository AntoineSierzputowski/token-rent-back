import random
import string
from utils.database import db

class RealEstateService:
    def _generate_id(self, length=8):
        """Generate a random alphanumeric ID."""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def create_real_estate(self, rent_price: float):
        """
        Create a new real estate entry.
        Calculates minimum_salary_eligibility as 34% of rent_price.
        """
        real_estate_id = self._generate_id()
        minimum_salary_eligibility = rent_price * 0.34
        
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO real_estates (id, rent_price, minimum_salary_eligibility) VALUES (%s, %s, %s)",
                (real_estate_id, rent_price, minimum_salary_eligibility)
            )
            conn.commit()
            
            return {
                "id": real_estate_id,
                "rent_price": rent_price,
                "minimum_salary_eligibility": minimum_salary_eligibility
            }
        finally:
            cursor.close()

real_estate_service = RealEstateService()
