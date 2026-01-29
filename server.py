from fastapi import FastAPI
from core_routes import router
from utils.database import db

app = FastAPI(title="Token Rent Back API", version="0.1")

# Initialize DB
try:
    db.init_db()
except Exception as e:
    print(f"Warning: Could not initialize database: {e}")

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(router)
