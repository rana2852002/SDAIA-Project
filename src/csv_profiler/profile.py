from typing import Any, Optional, List, Union



MISSING: List[Union[str, None]] = ["", "na", "n/a", "null", "none", "nan", None]

def is_missing(value: str | None) -> bool:
    # ... (الدالة كما هي)
    if value is None:
        return True
    
    
    str_value = str(value).strip().lower()
    
    return str_value in MISSING

def try_float(value: str | Any) -> Optional[float]:
    # ... (الدالة كما هي)
    if is_missing(value):
        return None
        
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def infer_type(values: List[str | Any]) -> str:
    # ... (الدالة كما هي)
    
   
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


# =================================================================
# الدالة الجديدة المطلوبة (Task 2)
# =================================================================

def column_values(rows: List[dict | list], col: str | int) -> List[str]:
    """
    تستخرج جميع القيم من عمود محدد (باستخدام مفتاح/فهرس العمود).
    """
    # الحل المقترح من الصورة باستخدام فهم القائمة (List Comprehension):
    return [str(row.get(col, "")) for row in rows]



def basic_profile(rows: list) -> dict[str, Any]:
    # ... (الدالة كما هي)
    if not rows:
        return {
            "row_count": 0,
            "column_count": 0,
            "columns": [],
            "missing_counts": {},
        }

    
    if isinstance(rows[0], dict):
        headers = list(rows[0].keys())
    else:  
        headers = [f"Column {i+1}" for i in range(len(rows[0]))]

    column_count = len(headers)
    row_count = len(rows)
    missing_counts = {header: 0 for header in headers}

    for row in rows:
        for i, header in enumerate(headers):
          
            if isinstance(row, dict):
              
                value = row.get(header, None)
            else:
               
                value = row[i] if i < len(row) else None
            
          
            if is_missing(value):
                missing_counts[header] += 1

    return {
        "row_count": row_count,
        "column_count": column_count,
        "columns": headers,
        "missing_counts": missing_counts,
    }