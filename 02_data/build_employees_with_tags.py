"""
Builds employees_with_tags.csv from the committed employees.csv and roles.csv.

This replicates the tag derivation from 03_sql/05_derive_tags.sql and
03_sql/06_fix_supports_a.sql in Python, so the pipeline runs without PostgreSQL.

Tag logic (company_design.md §2, assumptions.md):
    A   : strategic_impact=True AND rating_stdev >= 0.8 (n≥30) for the role
    B-HR: NOT A, hard_to_replace (adjacent_qualified<5 AND time_to_fill≥60)
    B   : NOT A, NOT B-HR, supports_a=True (or management layer)
    C   : everything else

Also adds:
    fully_loaded_cost = round(base_salary_usd * 1.3)   (assumptions.md row 2)
    attrition_draw    = uniform [0,1), seed 99          (lever_hiring_freeze.py)
    c_layoff_rank     = within-C rank by (rating, tiebreak), seed 303
                        (lever_targeted_layoffs.py)

Run from repo root:
    python 02_data/build_employees_with_tags.py

Outputs:
    02_data/employees_with_tags.csv
    02_data/employees_with_helpers.csv   (legacy name, same content minus tag)
"""

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# 1. Load raw data
# ---------------------------------------------------------------------------
emp   = pd.read_csv("02_data/employees.csv")
roles = pd.read_csv("02_data/roles.csv")

# ---------------------------------------------------------------------------
# 2. Compute per-role variance (replicates 03_sql/02_variance_per_role.sql)
# ---------------------------------------------------------------------------
variance = (
    emp.groupby("role_id")["rating"]
    .agg(headcount="count", rating_stdev="std")
    .reset_index()
)
variance["clears_variance"] = (
    (variance["headcount"] >= 30) & (variance["rating_stdev"] >= 0.8)
)

# ---------------------------------------------------------------------------
# 3. Hard-to-replace flag (replicates 03_sql/03_hard_to_replace.sql)
# ---------------------------------------------------------------------------
roles["hard_to_replace"] = (
    (roles["adjacent_qualified_headcount"] < 5) &
    (roles["time_to_fill_days"] >= 60)
)

# ---------------------------------------------------------------------------
# 4. supports_a flag (replicates 03_sql/06_fix_supports_a.sql)
# ---------------------------------------------------------------------------
SUPPORTS_A_ROLES = {
    "R003","R004","R006","R007","R008","R011","R012","R013","R014","R015",
    "R017","R018","R019","R021","R022","R023","R024","R025","R027","R028",
    "R029","R030","R031","R036","R037","R038","R039","R041","R042","R043",
    "R044","R045","R046","R047",
}
NOT_SUPPORTS_A = {"R005","R016","R026","R032","R033","R034","R035","R040"}
# A-roles (strategic_impact=True) get NULL — handled by tag logic below

roles["supports_a"] = roles["role_id"].apply(
    lambda x: True if x in SUPPORTS_A_ROLES else (False if x in NOT_SUPPORTS_A else None)
)

# ---------------------------------------------------------------------------
# 5. Derive criticality tag (replicates 03_sql/05_derive_tags.sql)
# ---------------------------------------------------------------------------
merged = (
    emp
    .merge(roles[["role_id","strategic_impact","hard_to_replace","supports_a"]], on="role_id")
    .merge(variance[["role_id","clears_variance"]], on="role_id")
)

def assign_tag(row):
    if row["strategic_impact"] and row["clears_variance"]:
        return "A"
    if row["hard_to_replace"]:
        return "B-HR"
    if row["supports_a"]:
        return "B"
    return "C"

merged["criticality_tag"] = merged.apply(assign_tag, axis=1)

# ---------------------------------------------------------------------------
# 6. fully_loaded_cost (assumptions.md row 2: base × 1.3, rounded to integer)
# ---------------------------------------------------------------------------
merged["fully_loaded_cost"] = (merged["base_salary_usd"] * 1.3).round(0).astype(int)

# ---------------------------------------------------------------------------
# 7. attrition_draw (lever_hiring_freeze.py seed 99)
# ---------------------------------------------------------------------------
rng_attr = np.random.default_rng(99)
merged["attrition_draw"] = rng_attr.random(len(merged))

# ---------------------------------------------------------------------------
# 8. c_layoff_rank (lever_targeted_layoffs.py seed 303)
# ---------------------------------------------------------------------------
rng_lay = np.random.default_rng(303)
c_mask = merged["criticality_tag"] == "C"
merged.loc[c_mask, "tiebreak_tmp"] = rng_lay.random(c_mask.sum())
c_sorted = (
    merged[c_mask]
    .sort_values(["rating", "tiebreak_tmp"], ascending=[True, True])
    .index
)
merged["c_layoff_rank"] = np.nan
merged.loc[c_sorted, "c_layoff_rank"] = range(1, c_mask.sum() + 1)
# Convert to nullable int (blank for non-C rows)
merged["c_layoff_rank"] = pd.array(
    merged["c_layoff_rank"].where(c_mask).values, dtype="Int64"
)
merged = merged.drop(columns=["tiebreak_tmp"], errors="ignore")

# ---------------------------------------------------------------------------
# 9. Sanity checks
# ---------------------------------------------------------------------------
tag_counts = merged["criticality_tag"].value_counts().to_dict()
baseline   = merged["fully_loaded_cost"].sum()

print("=== build_employees_with_tags.py ===")
print(f"Total employees : {len(merged):,}")
print(f"Tag counts      : A={tag_counts.get('A',0)}  B={tag_counts.get('B',0)}  "
      f"B-HR={tag_counts.get('B-HR',0)}  C={tag_counts.get('C',0)}")
print(f"Baseline cost   : ${baseline:,}")
print(f"Expected        : A=384  B=836  B-HR=319  C=465  baseline=$292,255,445")

# ---------------------------------------------------------------------------
# 10. Write outputs
# ---------------------------------------------------------------------------
tag_cols = [
    "employee_id","role_id","role_name","division","grade",
    "base_salary_usd","tenure_years","rating","manager_id",
    "criticality_tag","fully_loaded_cost","attrition_draw","c_layoff_rank",
]
merged[tag_cols].to_csv("02_data/employees_with_tags.csv", index=False)

# employees_with_helpers.csv: legacy format without criticality_tag/fully_loaded_cost
helper_cols = [
    "employee_id","role_id","role_name","division","grade",
    "base_salary_usd","tenure_years","rating","manager_id",
    "attrition_draw","c_layoff_rank",
]
merged[helper_cols].to_csv("02_data/employees_with_helpers.csv", index=False)

print("\nWrote: 02_data/employees_with_tags.csv")
print("Wrote: 02_data/employees_with_helpers.csv")
