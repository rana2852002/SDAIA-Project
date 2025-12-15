# src/csv_profiler/io.py
from pathlib import Path
import csv
from typing import Any

def read_csv_rows(path: str | Path) -> list[dict[str, str]]:
    """Reads a CSV as a list of rows (each row is a dict of strings)."""
    path_obj = Path(path)
    with path_obj.open(mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)
