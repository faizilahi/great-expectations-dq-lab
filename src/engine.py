import json
from pathlib import Path
import pandas as pd

def run_expectation(df: pd.DataFrame, exp: dict) -> dict:
    t, kw = exp["type"], exp["kwargs"]
    col = kw.get("column")
    if t == "expect_column_to_exist":
        ok = col in df.columns
        return {"expectation": t, "success": ok, "unexpected_count": 0 if ok else 1}
    if t == "expect_column_values_to_not_be_null":
        bad = int(df[col].isna().sum())
        return {"expectation": t, "success": bad == 0, "unexpected_count": bad}
    if t == "expect_column_values_to_be_between":
        mn, mx = kw.get("min_value"), kw.get("max_value")
        s = df[col]
        mask = pd.Series([True] * len(df))
        if mn is not None:
            mask &= s >= mn
        if mx is not None:
            mask &= s <= mx
        bad = int((~mask).sum())
        return {"expectation": t, "column": col, "success": bad == 0, "unexpected_count": bad,
                "bad_index": df.index[~mask].tolist()}
    return {"expectation": t, "success": False, "unexpected_count": -1}

def run_suite(df: pd.DataFrame, suite_path: Path) -> dict:
    suite = json.loads(suite_path.read_text(encoding="utf-8"))
    results = [run_expectation(df, e) for e in suite["expectations"]]
    return {"suite_name": suite["suite_name"], "results": results, "success": all(r["success"] for r in results)}
