"""
Lever 2: Delayering.
Managers (grade 4) below the span-of-control threshold (assumptions.md row 13:
minimum 4 direct reports) are redeployed into an IC role one grade down
(row 16). No severance, no notice cost, not counted as lost — this lever can
never fail the protection rule by construction (locked in Phase 0/1), since
nobody is terminated. Its pass/fail hinges entirely on whether it clears 5% net.
"""
import pandas as pd
import numpy as np

emp = pd.read_csv("employees_with_tags.csv")
BASELINE_COST = emp.fully_loaded_cost.sum()

# Identify grade-4 managers and their span (direct report count)
managers = emp[(emp.grade == 4) & (emp.role_name.str.contains("Manager"))].copy()
spans = emp[emp.manager_id.notna()].groupby("manager_id").size().rename("span")
managers = managers.merge(spans, left_on="employee_id", right_index=True, how="left")
managers["span"] = managers["span"].fillna(0)

SPAN_THRESHOLD = 4  # assumptions.md row 13
under_span = managers[managers.span < SPAN_THRESHOLD].copy()

print(f"Sanity check: {len(managers)} grade-4 managers total, {len(under_span)} under span={SPAN_THRESHOLD}")
assert len(under_span) > 0, "No delayering candidates — check span data before proceeding"

# Redeploy: new grade = 3 (one grade down from 4), new IC-level pay.
# Cost saving = old manager salary - new IC salary, fully loaded, for the full 12 months
# (redeployment is treated as immediate, so this is a full-year saving from day one —
# unlike the hiring freeze, which only saves as attrition actually occurs).
GRADE_BANDS = {3: (115_000, 150_000)}  # matches company_design.md grade bands
rng = np.random.default_rng(202)  # separate seed, documented here
new_ic_salary = rng.integers(GRADE_BANDS[3][0], GRADE_BANDS[3][1] + 1, size=len(under_span))
under_span["new_grade"] = 3
under_span["new_base_salary"] = new_ic_salary
under_span["new_fully_loaded_cost"] = under_span.new_base_salary * 1.30
under_span["savings"] = under_span.fully_loaded_cost - under_span.new_fully_loaded_cost

net_savings = under_span.savings.sum()   # no severance/notice cost for this lever
run_rate_savings = net_savings           # same number — saving is realized immediately, holds all 12 months

net_pct = net_savings / BASELINE_COST * 100
run_rate_pct = run_rate_savings / BASELINE_COST * 100

# Protection check: nobody is terminated, so by definition nobody in the protected
# set is "lost" — but confirm none of the delayered managers were themselves
# tagged A or B-HR, since that would be a modeling inconsistency worth flagging.
protected_among_delayered = under_span[under_span.criticality_tag.isin(["A", "B-HR"])]

print(f"\n=== DELAYERING RESULTS ===")
print(f"Managers redeployed: {len(under_span)} of {len(managers)} grade-4 managers ({len(under_span)/len(managers):.1%})")
print(f"12-month net savings: ${net_savings:,.0f} ({net_pct:.2f}% of baseline)")
print(f"Annual run-rate savings: ${run_rate_savings:,.0f} ({run_rate_pct:.2f}% of baseline)")
print(f"Protected-set positions lost: 0 (redeployment never counts as lost, by design)")
print(f"Delayered managers who were themselves A/B-HR tagged: {len(protected_among_delayered)} (informational only, doesn't affect pass/fail)")

passes = net_pct >= 5.0  # protection clause is automatically satisfied
print(f"\nPASS/FAIL: {'PASS' if passes else 'FAIL'}")
if not passes:
    print(f"Reason: net savings {net_pct:.2f}% < 5% target")

under_span.to_csv("delayering_detail.csv", index=False)
