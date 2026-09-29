from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"; DATA.mkdir(parents=True, exist_ok=True)
RNG = np.random.default_rng(23)
n = 2000
df = pd.DataFrame({
    "claim_id": [f"CLM{i:06d}" for i in range(n)],
    "claim_type": ["MEDICAL"] * (n - 23) + ["REFUND"] * 23,
    "paid_amount": np.concatenate([RNG.uniform(10, 5000, n - 23), -RNG.uniform(10, 800, 23)]).round(2),
    "service_date": "2024-05-01",
})
df.to_csv(DATA / "claims_lines.csv", index=False)
print("claims", n, "negatives", 23)
