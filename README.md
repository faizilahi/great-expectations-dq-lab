# One Suite, One Failed Expectation

[Faiz Elahi](https://www.linkedin.com/in/faizilahi) — [pendataco.com](https://pendataco.com) — [github.com/faizilahi](https://github.com/faizilahi)

Synthetic data only. No vendor-customer employment claim.

A Great-Expectations-style suite on synthetic claims lines expects
`paid_amount >= 0`. One run failed with **23** negative paid rows from a refund
sign convention the suite had not yet allowed.

## The suite

`suites/claims_suite.json` — expect columns, null rates, and `paid_amount >= 0`.

## The failure

Expectation `expect_column_values_to_be_between` on `paid_amount` failed:
unexpected count **23**.

## The rows

`output/bad_rows.csv` lists the 23 refund lines (negative paid). After updating
the suite to allow negatives when `claim_type='REFUND'`, the suite passes.

```powershell
pip install -r requirements.txt
python scripts/generate_synthetic_data.py
python src/run_suite.py
```
