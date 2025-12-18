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
    return [
        "| Column | Type | Missing | Unique |",
        "|---|---:|---:|---:|", 
    ]


def render_markdown(report: dict[str, Any]) -> None:
 
    
    # فحص أمان للمفاتيح الأساسية
    rows = report.get("n_rows", report.get("num_rows", 0))
    cols = report.get("n_cols", report.get("num_cols", 0))
    
    lines: list[str] = []

    lines.extend(md_header("data/sample.csv")) 
    
    lines.append("## Summary")
    lines.append(f"- Rows: {rows:,}")
    lines.append(f"- Columns: {cols:,}")
    lines.append("")
    
    lines.append("## Column Profiles (Table)")
    lines.extend(md_table_header())
    
    for col_profile in report.get("columns", []):
        if col_profile is None: 
            continue
            
        missing = col_profile.get("missing", 0)
        missing_pct = col_profile.get("missing_pct", 0.0) 
        
        row_line = (
            f"| `{col_profile.get('name', 'Unknown')}` | {col_profile.get('type', 'N/A')} | "
            f"{missing} ({missing_pct:.1f}%) | {col_profile.get('unique', 0):,} |"
        )
        lines.append(row_line)
        
    lines.append("")
    lines.append("## Detailed Column Stats")
    
    for col_profile in report.get("columns", []):
        if col_profile is None: # تجاهل العناصر الفارغة هنا أيضاً
            continue
            
        name = col_profile.get("name", "Unknown")
        col_type = col_profile.get("type", "N/A")
        
        lines.append(f"### Column: `{name}`")
        lines.append(f"- **Type:** {col_type}")
        lines.append(f"- **Total Count:** {rows:,}")
        
        m_val = col_profile.get("missing", 0)
        m_pct = col_profile.get("missing_pct", 0) / 100.0 
             
        lines.append(f"- **Missing:** {m_val:,} ({m_pct:.1%})")
        lines.append(f"- **Unique:** {col_profile.get('unique', 0):,}")
        
        if col_type == "number":
            lines.append("#### Numeric Statistics")
            lines.append(f"- **Min:** {col_profile.get('min'):.2f}" if col_profile.get('min') is not None else f"- **Min:** N/A")
            lines.append(f"- **Max:** {col_profile.get('max'):.2f}" if col_profile.get('max') is not None else f"- **Max:** N/A")
            lines.append(f"- **Mean:** {col_profile.get('mean'):.2f}" if col_profile.get('mean') is not None else f"- **Mean:** N/A")
            
        elif col_type == "text":
            lines.append("#### Top Values")
            lines.append("*(Top values are not calculated in the current profiling baseline)*")

        lines.append("") 
        
    text = "\n".join(lines) + "\n"
    return text


def write_json(report: dict[str, Any], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n" 
    path.write_text(text, encoding="utf-8")
