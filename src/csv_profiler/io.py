from pathlib import Path
import csv
from typing import Any, Dict, List

def read_csv_rows(path: Path | str) -> List[Dict[str, str]]:
 
    csv_path = Path(path)
    
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    rows: List[Dict[str, str]] = []

    with csv_path.open(mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            processed_row = {key: str(value) for key, value in row.items()}
            rows.append(processed_row)

    if not rows:
        raise ValueError("CSV has no data rows")

    return rows
