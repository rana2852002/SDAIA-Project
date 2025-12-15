from typing import Any

def basic_profile(rows: list) -> dict[str, Any]:
    """Compute row count, column names, and missing values per column."""
    if not rows:
        return {
            "row_count": 0,
            "column_count": 0,
            "columns": [],
            "missing_counts": {},
        }

    # إذا الصفوف dict
    if isinstance(rows[0], dict):
        headers = list(rows[0].keys())
    else:  # إذا الصفوف list
        headers = [f"Column {i+1}" for i in range(len(rows[0]))]

    column_count = len(headers)
    row_count = len(rows)
    missing_counts = {header: 0 for header in headers}

    for row in rows:
        for i, header in enumerate(headers):
            # خذ القيمة حسب النوع
            if isinstance(row, dict):
                value = row.get(header, "")
            else:
                value = row[i] if i < len(row) else ""
            if str(value).strip() == "":
                missing_counts[header] += 1

    return {
        "row_count": row_count,
        "column_count": column_count,
        "columns": headers,
        "missing_counts": missing_counts,
    }
