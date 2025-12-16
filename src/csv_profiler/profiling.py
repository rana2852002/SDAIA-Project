from __future__ import annotations 

def is_missing(value: Any | None) -> bool:
    if value is None:
        return True
    
    if not isinstance(value, str):
        return True
    
    
    cleaned = value.strip().casefold()
    return cleaned in {"", "n/a", "na", "null", "none", "nan"}

def try_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None

def infer_type(values: list[str]) -> str:
    usable = [v for v in values if not is_missing(v)]
    if not usable:
        return "text" 
    
    for v in usable:
        if try_float(v) is None:
            return "text"
            
    return "number"

from collections import Counter 

def profile_rows(rows: list[dict[str, str]]) -> dict:
    if not rows:
        return {"n_rows": 0, "n_cols": 0, "columns": []} 

    n_rows = len(rows)
    columns = list(rows[0].keys())
    col_profiles = []

    for col in columns:
        values = [r.get(col, "") for r in rows]
        usable = [v for v in values if not is_missing(v)]
        missing = len(values) - len(usable)
        inferred = infer_type(values)
        unique = len(set(usable))

        profile = {
            "name": col,
            "type": inferred,
            "missing": missing,
           
            "missing_pct": 100.0 * missing / n_rows if n_rows else 0.0,
            "unique": unique,
        }

       
        if inferred == "number":
            nums = [try_float(v) for v in usable]
            nums = [x for x in nums if x is not None] 
            
            if nums:
                profile.update({"min": min(nums), "max": max(nums), "mean": sum(nums) / len(nums)})

        col_profiles.append(profile)

    return {"n_rows": n_rows, "n_cols": len(columns), "columns": col_profiles}