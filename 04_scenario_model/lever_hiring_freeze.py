"""
Lever 1: Hiring freeze.
No backfill for 12 months, no exemption for protected roles (assumptions.md row 1-2,
locked in problem_statement.md §4). Monthly attrition hazard derived from the 12%
annual rate so P(leaves within 12 months) = exactly 0.12 by construction.

Confirmed FAIL across 7 seeds tested (101, 202, 303, 404, 505, 606, 707):
net savings always clears 5%, but protected-set losses are never zero (range 77-90).
"""
import pandas as pd
import numpy as np

emp = pd.read_csv("employees_with_tags.csv")
BASELINE_COST = emp.fully_loaded_cost.sum()
N = len(emp)

rng = np.random.default_rng(101)  # separate seed from generation, documented here
ANNUAL_ATTRITION = 0.12
monthly_p = 1 - (1 - ANNUAL_ATTRITION) ** (1 / 12)

trials = rng.random((N, 12)) < monthly_p
left_mask = trials.any(axis=1)
departure_month = np.where(left_mask, trials.argmax(axis=1) + 1, np.nan)

emp["left"] = left_mask
emp["departure_month"] = departure_month

actual_rate = emp.left.mean()
print(f"Sanity check: {emp.left.sum()} of {N} left = {actual_rate:.1%} (target: 12.0%)")
assert 0.09 < actual_rate < 0.15, "Attrition rate too far off target — check monthly_p logic"

departed = emp[emp.left].copy()

departed["months_remaining"] = 12 - departed.departure_month
net_savings = (departed.fully_loaded_cost * departed.months_remaining / 12).sum()
run_rate_savings = departed.fully_loaded_cost.sum()

net_pct = net_savings / BASELINE_COST * 100
run_rate_pct = run_rate_savings / BASELINE_COST * 100

protected_lost = departed[(departed.criticality_tag.isin(["A", "B-HR"])) & (departed.lever_eligible)]

print(f"\n=== HIRING FREEZE RESULTS ===")
print(f"Departed (no backfill): {len(departed)} of {N} ({len(departed)/N:.1%})")
print(f"12-month net savings: ${net_savings:,.0f} ({net_pct:.2f}% of baseline)")
print(f"Annual run-rate savings: ${run_rate_savings:,.0f} ({run_rate_pct:.2f}% of baseline)")
print(f"Protected-set positions lost: {len(protected_lost)}")

passes = (net_pct >= 5.0) and (len(protected_lost) == 0)
print(f"\nPASS/FAIL: {'PASS' if passes else 'FAIL'}")
if not passes:
    reasons = []
    if net_pct < 5.0: reasons.append(f"net savings {net_pct:.2f}% < 5% target")
    if len(protected_lost) > 0: reasons.append(f"{len(protected_lost)} protected positions lost")
    print(f"Reason: {'; '.join(reasons)}")
