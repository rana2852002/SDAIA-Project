from pathlib import Path
from typing import Any
from datetime import datetime
import json
import os 


def md_header(source: str) -> list[str]:
    ts = datetime.now().isoformat(timespec="seconds") 
    return [
        "# CSV Profile Report",
        "",
        f"- **Source:** `{source}`", 
        f"- **Generated:** `{ts}`",
        "",
    ]
    
def md_table_header() -> list[str]:
    """ يُعيد أسطر رأس جدول الأعمدة مع فواصل التنسيق. """
    return [
        "| Column | Type | Missing | Unique |",
        "|---|---:|---:|---:|", 
    ]


def write_markdown(report: dict[str, Any], path: str | Path) -> None:
    path = Path(path)
   
    path.parent.mkdir(parents=True, exist_ok=True)
    
    rows = report["n_rows"] 
    lines: list[str] = []

   
    lines.extend(md_header("data/sample.csv")) 
    
    
    lines.append("## Summary")
    lines.append(f"- Rows: {report['n_rows']:,}")
    lines.append(f"- Columns: {report['n_cols']:,}")
    lines.append("")
    
    
    lines.append("## Column Profiles (Table)")
    lines.extend(md_table_header())
    
    for col_profile in report["columns"]:
        missing = col_profile["missing"]
        missing_pct = col_profile["missing_pct"] 
        
        row_line = (
            f"| `{col_profile['name']}` | {col_profile['type']} | "
            f"{missing} ({missing_pct:.1f}%) | {col_profile['unique']:,} |"
        )
        lines.append(row_line)
    lines.append("")
    
    lines.append("## Detailed Column Stats")
    
    for col_profile in report["columns"]:
        name = col_profile["name"]
        lines.append(f"### Column: `{name}`")
        lines.append(f"- **Type:** {col_profile['type']}")
        
        lines.append(f"- **Total Count:** {rows:,}")
        
        missing_pct_detail = col_profile["missing_pct"] / 100.0 
             
        lines.append(f"- **Missing:** {col_profile['missing']:,} ({missing_pct_detail:.1%})")
        lines.append(f"- **Unique:** {col_profile['unique']:,}")
        
        
        if col_profile["type"] == "number":
            lines.append("#### Numeric Statistics")
            lines.append(f"- **Min:** {col_profile.get('min'):.2f}" if col_profile.get('min') is not None else f"- **Min:** N/A")
            lines.append(f"- **Max:** {col_profile.get('max'):.2f}" if col_profile.get('max') is not None else f"- **Max:** N/A")
            lines.append(f"- **Mean:** {col_profile.get('mean'):.2f}" if col_profile.get('mean') is not None else f"- **Mean:** N/A")
            
        elif col_profile["type"] == "text":
            lines.append("#### Top Values")
            lines.append("*(Top values are not calculated in the current profiling baseline)*")

        lines.append("") 
        
    text = "\n".join(lines) + "\n"
    path.write_text(text, encoding="utf-8")


def write_json(report: dict[str, Any], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n" 
    
    path.write_text(text, encoding="utf-8")