from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from pathlib import Path
from typing import List, Optional
import pandas as pd

from app.database import SessionLocal
from app.models.mortality import Mortality
from app.utils.ingest import ingest_file

router = APIRouter(prefix="/api/mortality", tags=["mortality"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/countries")
def countries(db: Session = Depends(get_db)):
    res = db.query(Mortality.country_code, Mortality.country_name).distinct().all()
    return [{"code": r[0], "name": r[1]} for r in res]

@router.get("/time-series")
def time_series(
    country_code: str,
    metric: str = Query("deaths", pattern="^(deaths|rate)$"),
    db: Session = Depends(get_db)
):
    rows = db.query(Mortality.year, Mortality.number_of_deaths, Mortality.death_rate_per_100000, Mortality.age_group, Mortality.sex).filter(Mortality.country_code == country_code).all()
    data = []
    for y, nd, dr, ag, sx in rows:
        val = float(nd) if metric == "deaths" and nd is not None else (float(dr) if dr is not None else 0)
        data.append({"year": y, "value": val, "age_group": ag, "sex": sx})
    return data

@router.get("/age-distribution")
def age_dist(country_code: str, year: int, sex: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Mortality.age_group, Mortality.number_of_deaths).filter(Mortality.country_code == country_code, Mortality.year == year)
    if sex:
        q = q.filter(Mortality.sex == sex)
    rows = q.all()
    return [{"age_group": ag, "deaths": float(nd) if nd is not None else 0} for ag, nd in rows]

@router.get("/aggregates")
def aggregates(db: Session = Depends(get_db)):
    total = db.query(Mortality).count()
    return {"total": total}

@router.post("/ingest")
def ingest(file: UploadFile = File(...), dry_run: bool = False, db: Session = Depends(get_db)):
    up = Path(__file__).parent.parent.parent.parent / "data" / "uploads"
    up.mkdir(parents=True, exist_ok=True)
    p = up / file.filename
    with open(p, "wb") as f:
        f.write(file.file.read())
    try:
        res = ingest_file(db, str(p), dry_run=dry_run)
        return res
    except Exception as e:
        raise HTTPException(400, str(e))

@router.post("/ingest/cli")
def ingest_cli(path: str = Query(...), dry_run: bool = False, db: Session = Depends(get_db)):
    try:
        res = ingest_file(db, path, dry_run=dry_run)
        return res
    except Exception as e:
        raise HTTPException(400, str(e))
