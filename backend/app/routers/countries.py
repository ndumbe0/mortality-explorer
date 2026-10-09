from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal

router = APIRouter(prefix="/api/countries", tags=["countries"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_countries(db: Session = Depends(get_db)):
    rows = db.execute(text("SELECT DISTINCT country_code, country_name FROM mortality ORDER BY country_name")).fetchall()
    return [{"code": r[0], "name": r[1]} for r in rows]
