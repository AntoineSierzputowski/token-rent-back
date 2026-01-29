from utils.database import db
from datetime import date

class ProfileService:
    def get_profile(self, profile_id: int):
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True) 
        
        sql = "SELECT last_name, first_name, date_of_birth, salary FROM profiles WHERE id = %s"
        cursor.execute(sql, (profile_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result
        else:
            return None

    def insert_profile(self, data: dict):
        conn = db.get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO profiles (last_name, first_name, date_of_birth, salary)
            VALUES (%s, %s, %s, %s)
        """
        val = (
            data["last_name"], 
            data["first_name"], 
            data["date_of_birth"], 
            data["salary"]
        )
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()

profile_service = ProfileService()
