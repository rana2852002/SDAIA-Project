from pathlib import Path
import csv
import json
from typing import Any, Dict, List, Optional
from datetime import datetime


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


def md_header(source: str) -> List[str]:
    ts = datetime.now().isoformat(timespec="seconds") 
    return [
        "# CSV Profile Report",
        "",
        f"- **Source:** `{source}`", 
        f"- **Generated:** `{ts}`",
        "",
    ]

def write_markdown(report: Dict[str, Any], path: Optional[Path | str] = None) -> str:
    rows_count = report["n_rows"] 
    lines: List[str] = []

    lines.extend(md_header("Uploaded File")) 
    
    lines.append("## Summary")
    lines.append(f"- Rows: {report['n_rows']:,}")
    lines.append(f"- Columns: {report['n_cols']:,}")
    lines.append("")
    
    lines.append("## Column Profiles")
    lines.append("| Column | Type | Missing | Unique |")
    lines.append("|---|---:|---:|---:|")
    
    for col in report["columns"]:
        lines.append(
            f"| `{col['name']}` | {col['type']} | "
            f"{col['missing']} ({col['missing_pct']:.1f}%) | {col['unique']:,} |"
        )
    
    text = "\n".join(lines) + "\n"
    
    if path:
        save_path = Path(path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text(text, encoding="utf-8")
    
    return text

def write_json(report: Dict[str, Any], path: Path | str) -> None:
    
    save_path = Path(path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    save_path.write_text(text, encoding="utf-8")