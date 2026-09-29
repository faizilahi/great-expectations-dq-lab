import pandas as pd, numpy as np
from pathlib import Path
RNG=np.random.default_rng(12)
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"; DATA.mkdir(parents=True, exist_ok=True)
rows=[{"member_id":f"M{i:04d}","status":RNG.choice(["active","inactive"]),"age":int(RNG.integers(18,90))} for i in range(1,201)]
rows.append({"member_id":"M0001","status":"active","age":40})  # duplicate for fail demo
rows.append({"member_id":"M9999","status":"unknown","age":30})
pd.DataFrame(rows).to_csv(DATA/"members.csv",index=False)
print("Wrote DQ dataset")

