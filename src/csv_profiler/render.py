
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

def write_json(report: dict[str, Any], path: str | Path) -> None:
    path_obj = Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)
    path_obj.write_text(
        json.dumps(report, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

def write_markdown(report: dict[str, Any], path: str | Path) -> None:
    path_obj = Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)

    lines = ["# CSV Profile Report\n"]
    lines.append("| Statistic | Value |")
    lines.append("|:---|---:|")
    lines.append(f"| Rows | {report.get('row_count', 0)} |")
    lines.append(f"| Columns | {report.get('column_count', 0)} |\n")

    lines.append("## Missing Values\n")
    lines.append("| Column | Missing Count |")
    lines.append("|:---|---:|")
    missing_counts = report.get("missing_counts", {})
    for column, count in missing_counts.items():
        lines.append(f"| {column} | {count} |")

    path_obj.write_text("\n".join(lines), encoding="utf-8")
    
