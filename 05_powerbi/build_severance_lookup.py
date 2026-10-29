"""
Builds severance_lookup.csv — the precomputed table the Power BI What-If
parameter reads via LOOKUPVALUE().

Sweeps severance_weeks from 2.0 to 15.0 in 0.5-week steps (27 values) and
records the cutoff rank, net savings %, run-rate savings %, pass/fail flag,
and whether the C pool was exhausted.

Must be run AFTER 02_data/build_employees_with_tags.py has produced
02_data/employees_with_tags.csv.

Run from repo root:
    python 05_powerbi/build_severance_lookup.py

Output:
    05_powerbi/severance_lookup.csv
"""

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# 1. Load tagged data
# ---------------------------------------------------------------------------
emp = pd.read_csv("02_data/employees_with_tags.csv")
BASELINE = emp["fully_loaded_cost"].sum()
TARGET   = BASELINE * 0.05

# ---------------------------------------------------------------------------
# 2. Sort C pool exactly as lever_targeted_layoffs.py does
# ---------------------------------------------------------------------------
c_pool = emp[emp["criticality_tag"] == "C"].copy()
rng = np.random.default_rng(303)          # same seed as the lever script
c_pool["tiebreak"] = rng.random(len(c_pool))
c_pool = c_pool.sort_values(["rating", "tiebreak"], ascending=[True, True]).reset_index(drop=True)

# ---------------------------------------------------------------------------
# 3. Sweep severance weeks
# ---------------------------------------------------------------------------
SEVERANCE_VALUES = [round(v * 0.5, 1) for v in range(4, 31)]   # 2.0 … 15.0

rows = []
for sw in SEVERANCE_VALUES:
    c = c_pool.copy()

    weekly_pay   = c["fully_loaded_cost"] / 52
    sev_weeks    = c["tenure_years"].apply(lambda t: max(sw * t / sw, sw)).copy()
    # Correct formula: severance = max(2 * tenure_years, sw) weeks × weekly_pay
    # (The default lever uses 2 wks/yr of tenure; here we sweep the minimum floor sw)
    sev_weeks    = c["tenure_years"].apply(lambda t: max(2 * t, sw))
    c["severance"]     = weekly_pay * sev_weeks
    c["notice_cost"]   = weekly_pay * 4
    c["one_time_cost"] = c["severance"] + c["notice_cost"]
    c["net_contribution"] = c["fully_loaded_cost"] - c["one_time_cost"]
    c["cum_net"]          = c["net_contribution"].cumsum()

    hit = c[c["cum_net"] >= TARGET].index.min()
    if pd.isna(hit):
        sel       = c
        exhausted = True
    else:
        sel       = c.iloc[: hit + 1]
        exhausted = False

    net_savings     = sel["net_contribution"].sum()
    run_rate_savings = sel["fully_loaded_cost"].sum()
    net_pct         = round(net_savings / BASELINE * 100, 4)
    rr_pct          = round(run_rate_savings / BASELINE * 100, 4)
    passes          = net_pct >= 5.0

    rows.append({
        "severance_weeks":     sw,
        "cutoff_rank":         len(sel),
        "net_savings_pct":     net_pct,
        "run_rate_savings_pct": rr_pct,
        "pass_fail":           "PASS" if passes else "FAIL",
        "c_pool_exhausted":    exhausted,
    })

lookup = pd.DataFrame(rows)

# ---------------------------------------------------------------------------
# 4. Sanity check against known values
# ---------------------------------------------------------------------------
print("=== build_severance_lookup.py ===")
print(f"C pool size : {len(c_pool)}")
print(f"Baseline    : ${BASELINE:,}")
print()
print(lookup.to_string(index=False))
print()

# Spot-check key rows against values produced by committed employees_with_tags.csv.
# Note: the pbix was built from the original (unpreserved) generator run and will
# show different cutoff_ranks; these checks validate the committed-data pipeline only.
checks = {
    2.0:  (145, "PASS"),
    10.0: (164, "PASS"),
    10.5: (165, "PASS"),   # committed data never exhausts the pool within 2–15 wk range
    15.0: (183, "PASS"),
}
ok = True
for sw, (expected_rank, expected_pf) in checks.items():
    row = lookup[lookup["severance_weeks"] == sw].iloc[0]
    match = (row["cutoff_rank"] == expected_rank) and (row["pass_fail"] == expected_pf)
    status = "OK" if match else f"MISMATCH (got rank={row['cutoff_rank']} {row['pass_fail']})"
    print(f"  sw={sw:4.1f}: {status}")
    if not match:
        ok = False

print()
print("All checks passed." if ok else "SOME CHECKS FAILED — review output above.")

# ---------------------------------------------------------------------------
# 5. Write
# ---------------------------------------------------------------------------
lookup.to_csv("05_powerbi/severance_lookup.csv", index=False)
print("\nWrote: 05_powerbi/severance_lookup.csv")
