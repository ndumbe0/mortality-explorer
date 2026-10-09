#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "backend"))
from app.database import SessionLocal
from app.utils.ingest import ingest_file
import argparse

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--file', required=True)
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()
    db = SessionLocal()
    try:
        print(ingest_file(db, args.file, dry_run=args.dry_run))
    finally:
        db.close()

if __name__ == '__main__':
    main()
