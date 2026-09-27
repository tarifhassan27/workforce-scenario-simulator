"""
Lever 3: Targeted layoffs.
Removes headcount from C roles only, lowest performance rating first, until the
5% net-savings target is hit or C roles are exhausted (problem_statement.md §4).
Tie-break among equal ratings: random (not tenure-based) — avoids a systematic
bias toward or against longer-serving employees, and keeps the outcome from
depending on a modeling choice that wasn't specified in Phase 0.
Severance: 2 weeks pay per year of tenure, 4-week minimum (assumptions.md row 3).
Notice/transition cost: 4 weeks pay flat (row 4).
"""
import pandas as pd
import numpy as np

emp = pd.read_csv("employees_with_tags.csv")
BASELINE_COST = emp.fully_loaded_cost.sum()
TARGET_NET_SAVINGS = BASELINE_COST * 0.05

c_pool = emp[emp.criticality_tag == "C"].copy()
print(f"Sanity check: {len(c_pool)} employees in C roles, total cost ${c_pool.fully_loaded_cost.sum():,.0f} "
      f"({c_pool.fully_loaded_cost.sum()/BASELINE_COST*100:.1f}% of baseline)")

rng = np.random.default_rng(303)  # separate seed, documented here, for the random tie-break only
c_pool["tiebreak"] = rng.random(len(c_pool))
c_pool = c_pool.sort_values(["rating", "tiebreak"], ascending=[True, True]).reset_index(drop=True)

def severance_cost(row):
    weekly_pay = row.fully_loaded_cost / 52
    weeks = max(2 * row.tenure_years, 4)
    return weekly_pay * weeks

def notice_cost(row):
    weekly_pay = row.fully_loaded_cost / 52
    return weekly_pay * 4

c_pool["severance"] = c_pool.apply(severance_cost, axis=1)
c_pool["notice_cost"] = c_pool.apply(notice_cost, axis=1)
c_pool["one_time_cost"] = c_pool.severance + c_pool.notice_cost
c_pool["annual_saving"] = c_pool.fully_loaded_cost
c_pool["net_contribution"] = c_pool.annual_saving - c_pool.one_time_cost
c_pool["cum_net"] = c_pool.net_contribution.cumsum()

hit_idx = c_pool[c_pool.cum_net >= TARGET_NET_SAVINGS].index.min()
if pd.isna(hit_idx):
    selected = c_pool
    exhausted = True
else:
    selected = c_pool.iloc[:hit_idx + 1]
    exhausted = False

net_savings = selected.net_contribution.sum()
run_rate_savings = selected.annual_saving.sum()
net_pct = net_savings / BASELINE_COST * 100
run_rate_pct = run_rate_savings / BASELINE_COST * 100

protected_lost = selected[selected.criticality_tag.isin(["A", "B-HR"])]

print(f"\n=== TARGETED LAYOFFS RESULTS (random tie-break) ===")
print(f"Target reached without exhausting C roles: {not exhausted}")
print(f"Employees laid off: {len(selected)} of {len(c_pool)} C-role employees ({len(selected)/len(c_pool):.1%})")
print(f"Total severance + notice cost: ${selected.one_time_cost.sum():,.0f}")
print(f"12-month net savings: ${net_savings:,.0f} ({net_pct:.2f}% of baseline)")
print(f"Annual run-rate savings: ${run_rate_savings:,.0f} ({run_rate_pct:.2f}% of baseline)")
print(f"Protected-set positions lost: {len(protected_lost)}")

passes = (net_pct >= 5.0) and (len(protected_lost) == 0)
print(f"\nPASS/FAIL: {'PASS' if passes else 'FAIL'}")

selected.to_csv("targeted_layoffs_detail.csv", index=False)
