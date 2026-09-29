import json, sys
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from engine import run_suite
DATA, OUT = ROOT / "data", ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)

def main():
    df = pd.read_csv(DATA / "claims_lines.csv")
    result = run_suite(df, ROOT / "suites" / "claims_suite.json")
    failed = next(r for r in result["results"] if not r["success"])
    bad = df.loc[failed["bad_index"]]
    bad.to_csv(OUT / "bad_rows.csv", index=False)
    # fixed suite path: allow refunds negative
    df2 = df.copy()
    # evaluate conditional: paid_amount >= 0 OR claim_type == REFUND
    mask = (df2["paid_amount"] >= 0) | (df2["claim_type"] == "REFUND")
    fixed_ok = bool(mask.all())
    summary = {
        "suite_success": result["success"],
        "failed_expectation": failed["expectation"],
        "unexpected_count": failed["unexpected_count"],
        "bad_row_count": int(len(bad)),
        "fixed_conditional_pass": fixed_ok,
    }
    pd.DataFrame([summary]).to_csv(OUT / "suite_result.csv", index=False)
    print(json.dumps(summary, indent=2))
if __name__ == "__main__":
    main()
