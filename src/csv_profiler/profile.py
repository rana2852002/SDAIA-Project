from typing import Any, Optional, List, Union
import math 
from collections import Counter 


MISSING: List[Union[str, None]] = ["", "na", "n/a", "null", "none", "nan", None]



def is_missing(value: str | None) -> bool:
    if value is None:
        return True
    
    str_value = str(value).strip().lower()
    return str_value in MISSING

def try_float(value: str | Any) -> Optional[float]:
    if is_missing(value):
        return None
        
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def infer_type(values: List[str | Any]) -> str:
    non_missing_values = set()
    for v in values:
        if not is_missing(v):
            non_missing_values.add(str(v).strip().lower())

    if not non_missing_values:
        return "string"

    boolean_values = {"true", "false", "0", "1"}
    is_boolean = all(v in boolean_values for v in non_missing_values)
    if is_boolean:
        return "boolean"
        
    can_be_integer = True
    can_be_float = True
    
    for v_str in non_missing_values:
        float_val = try_float(v_str)
        
        if float_val is None:
            can_be_float = False
            can_be_integer = False
            break
           
        if float_val != int(float_val):
            can_be_integer = False

    if can_be_integer:
        return "integer"
    elif can_be_float:
        return "float"
        
    return "string"


def column_values(rows: List[dict | list], col: str | int) -> List[str]:
    return [str(row.get(col, "")) for row in rows]



def numeric_stats(values: List[str | Any]) -> dict:
    
    usable_values = [v for v in values if not is_missing(v)]
    nums = [try_float(v) for v in usable_values]

    valid_nums = [n for n in nums if n is not None]
    
    missing_count = len(values) - len(valid_nums)
    
    if not valid_nums:
        return {
            "count": 0, "missing": missing_count, "unique": 0, 
            "min": None, "max": None, "mean": None,
        }

    count = len(valid_nums)
    unique_count = len(set(valid_nums))
    minimum = min(valid_nums)
    maximum = max(valid_nums)
    total_sum = sum(valid_nums)
    mean = total_sum / count
    
    return {
        "count": count, "missing": missing_count, "unique": unique_count,
        "min": minimum, "max": maximum, "mean": mean,
    }


def text_stats(values: List[str | Any], top_k: int = 5) -> dict:
    
    non_missing_values = [v for v in values if not is_missing(v)]
    total_count = len(values)
    valid_count = len(non_missing_values)
    missing_count = total_count - valid_count
    unique_count = len(set(non_missing_values))
    
    counter = Counter(non_missing_values)
    top_k_values = counter.most_common(top_k)
    
    return {
        "count": valid_count, "missing": missing_count, "unique": unique_count,
        "top_k": top_k_values,
    }



def column_profile(values: List[str | Any]) -> dict:
    
    inferred_type = infer_type(values)
    
    if inferred_type in ["integer", "float"]:
        stats = numeric_stats(values)
    else: 
        stats = text_stats(values)
        
    
    profile_result = stats.copy()
    profile_result["type"] = inferred_type
    
    if inferred_type in ["integer", "float"]:
        profile_result["stats"] = {
            "min": profile_result.pop("min"),
            "max": profile_result.pop("max"),
            "mean": profile_result.pop("mean"),
        }
    else:
       
        profile_result["values"] = profile_result.pop("top_k")
        
    return profile_result



def full_profile(rows: list) -> dict:
    
    if not rows:
        return {"row_count": 0, "column_count": 0, "columns": []}
    
    
    if isinstance(rows[0], dict):
        headers = list(rows[0].keys())
    else:
        headers = [f"Column {i+1}" for i in range(len(rows[0]))]

    column_results = {}
    for header in headers:
       
        values = column_values(rows, header) 
        
       
        column_results[header] = column_profile(values)
        
    
    return {
        "row_count": len(rows),
        "column_count": len(headers),
        "columns": headers,
        "column_profiles": column_results, 
    }


def basic_profile(rows: list) -> dict[str, Any]:
   
    if not rows:
        return {"row_count": 0, "column_count": 0, "columns": [], "missing_counts": {}}
    
    if isinstance(rows[0], dict):
        headers = list(rows[0].keys())
    else:  
        headers = [f"Column {i+1}" for i in range(len(rows[0]))]

    column_count = len(headers)
    row_count = len(rows)
    missing_counts = {header: 0 for header in headers}

    for row in rows:
        for i, header in enumerate(headers):
            value = row.get(header, None) if isinstance(row, dict) else (row[i] if i < len(row) else None)
            if is_missing(value):
                missing_counts[header] += 1

    return {"row_count": row_count, "column_count": column_count, "columns": headers, "missing_counts": missing_counts}