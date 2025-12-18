from __future__ import annotations 
from typing import Any
from collections import Counter 

def is_missing(value: Any | None) -> bool:
    """يحدد ما إذا كانت القيمة مفقودة بناءً على النص أو النوع."""
    if value is None:
        return True
    
    # إذا كانت القيمة أصلاً رقم (int/float) فهي ليست مفقودة
    if isinstance(value, (int, float)): 
        return False
        
    if not isinstance(value, str):
        return True
        
    cleaned = value.strip().casefold()
    # التحقق من الكلمات الشائعة للقيم الفارغة
    return cleaned in {"", "n/a", "na", "null", "none", "nan"}

def try_float(value: Any) -> float | None:
    """يحاول تحويل القيمة إلى رقم عشري."""
    try:
        if value is None: return None
        return float(value)
    except (ValueError, TypeError):
        return None

def infer_type(values: list[Any]) -> str:
    """يستنتج ما إذا كان العمود نصياً أم رقمياً."""
    usable = [v for v in values if not is_missing(v)]
    if not usable:
        return "text" 
    
    for v in usable:
        if try_float(v) is None:
            return "text"
            
    return "number"

def profile_rows(rows: list[dict[str, Any]]) -> dict:
    """يقوم بتحليل قائمة الصفوف واستخراج الإحصائيات."""
    # التأكد من أن القائمة ليست فارغة
    if not rows:
        return {"n_rows": 0, "n_cols": 0, "columns": []} 

    n_rows = len(rows)
    columns = list(rows[0].keys())
    col_profiles = []

    for col in columns:
        # جمع كافة القيم في العمود الحالي
        values = [r.get(col) for r in rows]
        usable_values = [v for v in values if not is_missing(v)]
        
        missing_count = n_rows - len(usable_values)
        col_type = infer_type(values)
        unique_count = len(set(usable_values))

        profile = {
            "name": col,
            "type": col_type,
            "missing": missing_count,
            "missing_pct": (missing_count / n_rows) * 100 if n_rows > 0 else 0.0,
            "unique": unique_count,
        }

        # حساب الإحصائيات الإضافية للأعمدة الرقمية
        if col_type == "number":
            nums = [try_float(v) for v in usable_values]
            # تصفية أي قيم None متبقية
            valid_nums = [n for n in nums if n is not None]
            
            if valid_nums:
                profile.update({
                    "min": float(min(valid_nums)), 
                    "max": float(max(valid_nums)), 
                    "mean": float(sum(valid_nums) / len(valid_nums))
                })

        col_profiles.append(profile)

    return {
        "n_rows": n_rows, 
        "n_cols": len(columns), 
        "columns": col_profiles
    }