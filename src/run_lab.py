from pathlib import Path
import yaml, pandas as pd
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"output"; OUT.mkdir(parents=True, exist_ok=True)
df=pd.read_csv(ROOT/"data"/"members.csv")
suite=yaml.safe_load((ROOT/"expectations"/"suite.yml").read_text(encoding="utf-8"))
results=[]
for exp in suite["expectations"]:
  t=exp["type"]; ok=True; detail=""
  if t=="unique":
    col=exp["column"]; ok=df[col].is_unique; detail=f"dupes={int(df[col].duplicated().sum())}"
  elif t=="accepted_values":
    col=exp["column"]; bad=~df[col].isin(exp["values"]); ok=not bad.any(); detail=f"bad={int(bad.sum())}"
  elif t=="not_null":
    col=exp["column"]; ok=df[col].notna().all(); detail=f"nulls={int(df[col].isna().sum())}"
  results.append({"expectation":t,"column":exp.get("column"),"success":ok,"detail":detail})
res=pd.DataFrame(results); res.to_csv(OUT/"summary.csv",index=False)
print(res)

