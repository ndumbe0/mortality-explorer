from pathlib import Path
from typing import Dict
import pandas as pd
from sqlalchemy.orm import Session

from app.models.mortality import Mortality
from app.utils.parsers import clean_number, clean_rate

def get_natkey(row) -> str:
    cc = str(row.get('Country Code') or row.get('country_code') or '').strip()
    yr = str(int(row.get('Year') or row.get('year') or 0))
    ag = str(row.get('Age Group') or row.get('age_group') or '').strip().lower()
    sx = str(row.get('Sex') or row.get('sex') or '').strip().lower()
    return f"{cc}|{yr}|{ag}|{sx}"

def ingest_file(db: Session, file_path: str, dry_run: bool = False) -> Dict:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(file_path)
    df = pd.read_csv(path) if path.suffix.lower() == '.csv' else pd.read_excel(path)
    df.columns = [str(c).strip() for c in df.columns]
    
    results = {
        "rows_read": len(df),
        "rows_valid": 0,
        "rows_added": 0,
        "rows_skipped": 0,
        "rows_failed": 0,
        "errors_sample": []
    }
    
    existing = set()
    if not dry_run:
        for r in db.query(Mortality.country_code, Mortality.year, Mortality.age_group, Mortality.sex).all():
            existing.add(f"{r[0]}|{r[1]}|{r[2].lower()}|{r[3].lower()}")
    
    for idx, row in df.iterrows():
        try:
            cc = str(row.get('Country Code') or row.get('country_code') or '').strip()
            cn = str(row.get('Country Name') or row.get('country_name') or '').strip()
            yr = row.get('Year') or row.get('year')
            ag = str(row.get('Age Group') or row.get('age_group') or '').strip()
            sx = str(row.get('Sex') or row.get('sex') or '').strip()
            nd = row.get('Number of Deaths') or row.get('number of deaths') or row.get('Number of deaths')
            dr = row.get('Death Rate Per 100,000') or row.get('death rate per 100000') or row.get('Death rate per 100,000')
            if not cc or yr is None:
                results["rows_failed"] += 1
                if len(results["errors_sample"]) < 3:
                    results["errors_sample"].append({"idx": int(idx), "err": "missing key"})
                continue
            k = f"{cc}|{int(yr)}|{ag.lower()}|{sx.lower()}"
            if not dry_run and k in existing:
                results["rows_skipped"] += 1
                continue
            results["rows_valid"] += 1
            if dry_run:
                results["rows_added"] += 1
                continue
            obj = Mortality(
                country_code=cc,
                country_name=cn,
                year=int(yr),
                age_group=ag,
                sex=sx,
                number_of_deaths=clean_number(nd),
                death_rate_per_100000=clean_rate(dr),
                source_file=Path(file_path).name
            )
            db.add(obj)
            existing.add(k)
            results["rows_added"] += 1
        except Exception as e:
            results["rows_failed"] += 1
            if len(results["errors_sample"]) < 5:
                results["errors_sample"].append({"idx": int(idx), "err": str(e)})
    if not dry_run:
        db.commit()
    return results
