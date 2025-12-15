from pathlib import Path
from typing import Any
from datetime import datetime
import json



def md_header(source: str) -> list[str]:
    """ يُعيد أسطر رأس التقرير (العنوان، المصدر، تاريخ التوليد). """
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
    
    rows = report["row_count"]
    lines: list[str] = []

   
    lines.extend(md_header("data/sample.csv")) 
    
    
    lines.append("## Summary")
    lines.append(f"- Rows: {report['row_count']:,}")
    lines.append(f"- Columns: {report['column_count']:,}")
    lines.append("")
    
    
    lines.append("## Column Profiles (Table)")
    lines.extend(md_table_header())
    
    for name, col_profile in report["column_profiles"].items():
        missing = col_profile["missing"]
        # تأكد من أن نسبة المفقودات تستخدم 'rows' من التقرير العام
        missing_pct = (missing / rows) if rows else 0.0 
        
        row_line = (
            f"| `{name}` | {col_profile['type']} | "
            f"{missing} ({missing_pct:.1%}) | {col_profile['unique']:,} |"
        )
        lines.append(row_line)
    lines.append("")
    
    lines.append("## Detailed Column Stats")
    
    for name, col_profile in report["column_profiles"].items():
        lines.append(f"### Column: `{name}`")
        lines.append(f"- **Type:** {col_profile['type']}")
        lines.append(f"- **Total Count:** {col_profile['count']:,}")
        
        if col_profile.get("missing") is not None and rows > 0:
             missing_pct_detail = col_profile["missing"] / rows
        else:
             missing_pct_detail = 0.0
             
        lines.append(f"- **Missing:** {col_profile['missing']:,} ({missing_pct_detail:.1%})")
        lines.append(f"- **Unique:** {col_profile['unique']:,}")
        
        
        if col_profile["type"] in ["integer", "float"]:
            stats = col_profile["stats"]
            lines.append("#### Numeric Statistics")
            lines.append(f"- **Min:** {stats.get('min'):.2f}" if stats.get('min') is not None else f"- **Min:** N/A")
            lines.append(f"- **Max:** {stats.get('max'):.2f}" if stats.get('max') is not None else f"- **Max:** N/A")
            lines.append(f"- **Mean:** {stats.get('mean'):.2f}" if stats.get('mean') is not None else f"- **Mean:** N/A")
            
        elif col_profile["type"] in ["string", "boolean"]:
            lines.append("#### Top Values")
            for value, count in col_profile['values']:
                lines.append(f"- `{value}`: {count:,} times")

        lines.append("") 
        
    text = "\n".join(lines) + "\n"
    path.write_text(text, encoding="utf-8")




def write_json(report: dict[str, Any], path: str | Path) -> None:
    """تكتب التقرير في ملف JSON مع تنسيق للقراءة."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n" 
    
    path.write_text(text, encoding="utf-8")