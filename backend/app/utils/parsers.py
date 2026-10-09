import re
from typing import Any, Optional

def clean_number(s: Any) -> Optional[int]:
    if s is None or s == "":
        return None
    if isinstance(s, bool):
        return int(s)
    if isinstance(s, int):
        return s
    if isinstance(s, float):
        return int(round(s))
    t = str(s).strip()
    if t in ("—", "-", "NA", "N/A", "n/a", "NULL", "null"):
        return None
    t = re.sub(r'[,]', '', t)
    m = re.search(r'[-\d]+', t)
    if m:
        try:
            return int(m.group(0))
        except:
            return None
    return None

def clean_rate(s: Any) -> Optional[float]:
    if s is None or s == "":
        return None
    if isinstance(s, bool):
        return float(s)
    if isinstance(s, (int, float)):
        return float(s)
    t = str(s).strip()
    if t in ("—", "-", "NA", "N/A", "n/a", "NULL", "null"):
        return None
    t = re.sub(r'[,]', '', t)
    m = re.search(r'[-\d.]+', t)
    if m:
        try:
            return float(m.group(0))
        except:
            return None
    return None

def normalize_text(s: Any) -> str:
    if s is None:
        return ""
    t = str(s).strip()
    return re.sub(r'\s+', ' ', t).lower()
