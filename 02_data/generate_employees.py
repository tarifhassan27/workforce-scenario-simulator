"""
Synthetic employee generator for the Workforce Scenario Simulator.

Produces employees.csv (2,004 rows) and roles.csv (47 rows) using the same
design rules as the original simulation.  Run from the repo root:

    python 02_data/generate_employees.py

NOTE: The committed employees.csv was generated before this script was written
and its exact original seed was not preserved.  Running this script will
produce a *structurally identical* dataset (same role counts, same pay bands,
same tag logic, same headcount totals) but will NOT reproduce the committed
file byte-for-byte.  If you need the canonical file, use the committed version;
run this script only to regenerate or extend the dataset from scratch.

Seed: 42 (numpy default_rng).  All design inputs are in company_design.md and
assumptions.md; no external data is required.

Output columns (employees.csv):
    employee_id, role_id, role_name, division, grade, base_salary_usd,
    tenure_years, rating, manager_id

Output columns (roles.csv):
    role_id, role_name, division, grade_min, grade_max, strategic_impact,
    adjacent_qualified_headcount, time_to_fill_days, lever_eligible
"""

import numpy as np
import pandas as pd

RNG_SEED = 42
rng = np.random.default_rng(RNG_SEED)

# ---------------------------------------------------------------------------
# 1. Role catalogue  (company_design.md §2)
# ---------------------------------------------------------------------------
# strategic_impact=True → A-eligible;  adjacent_qualified_headcount < 5
# and time_to_fill_days ≥ 60 → hard-to-replace (B-HR-eligible)
ROLES = [
    # role_id, role_name, division, grade_min, grade_max, strategic_impact, adjacent_qualified, ttf_days, lever_eligible, headcount
    ("R001", "ML/AI Engineer",                       "Engineering",      1, 3, True,  25,  95, True,   82),
    ("R002", "Senior Backend/Platform Engineer",     "Engineering",      1, 3, True,  30,  90, True,   82),
    ("R003", "Software Engineer (general)",          "Engineering",      1, 3, False, 40,  45, True,  191),
    ("R004", "SRE/DevOps Engineer",                  "Engineering",      1, 3, False,  3,  80, True,   82),
    ("R005", "QA/Test Engineer",                     "Engineering",      1, 3, False, 50,  30, True,   64),
    ("R006", "Engineering Manager",                  "Engineering",      4, 4, False, 45,  40, False,  84),
    ("R007", "Engineering Director",                 "Engineering",      5, 5, False, 20,  35, False,  14),
    ("R008", "Engineering VP",                       "Engineering",      6, 6, False, 10,  30, False,   1),
    ("R009", "Enterprise Account Executive",         "Sales",            2, 4, True,  60,  60, True,  115),
    ("R010", "Solutions Architect (Sales Eng.)",     "Sales",            2, 4, True,  10,  75, True,   57),
    ("R011", "Sales Development Rep",                "Sales",            1, 2, False, 80,  25, True,  162),
    ("R012", "Sales Manager",                        "Sales",            4, 4, False, 50,  35, False,  56),
    ("R013", "Sales Director",                       "Sales",            5, 5, False, 25,  40, False,   9),
    ("R014", "Sales VP",                             "Sales",            6, 6, False, 10,  30, False,   1),
    ("R015", "Enterprise CSM",                       "Customer Success", 2, 4, False,  2,  90, True,  118),
    ("R016", "Technical Support Engineer",           "Customer Success", 1, 3, False, 55,  30, True,  132),
    ("R017", "CS Manager",                           "Customer Success", 4, 4, False, 40,  35, False,  42),
    ("R018", "CS Director",                          "Customer Success", 5, 5, False, 20,  30, False,   7),
    ("R019", "CS VP",                                "Customer Success", 6, 6, False, 10,  25, False,   1),
    ("R020", "Senior Product Manager",               "Product",          3, 4, True,  20,  70, True,   48),
    ("R021", "Product Designer",                     "Product",          2, 3, False, 35,  45, True,   85),
    ("R022", "Product Team Lead",                    "Product",          4, 4, False, 30,  40, False,  22),
    ("R023", "Product Director",                     "Product",          5, 5, False, 15,  35, False,   4),
    ("R024", "Product VP",                           "Product",          6, 6, False, 10,  25, False,   1),
    ("R025", "Product Marketing Manager",            "Marketing",        3, 4, False, 45,  40, True,   66),
    ("R026", "Marketing Generalist / Content",       "Marketing",        1, 3, False, 60,  25, True,   51),
    ("R027", "Marketing Manager",                    "Marketing",        4, 4, False, 40,  35, False,  19),
    ("R028", "Marketing Director",                   "Marketing",        5, 5, False, 20,  30, False,   3),
    ("R029", "Marketing VP",                         "Marketing",        6, 6, False, 10,  25, False,   1),
    ("R030", "Legal Counsel",                        "G&A",              3, 5, False,  2, 120, True,   20),
    ("R031", "Technical Recruiter",                  "G&A",              2, 4, False,  3,  90, True,   20),
    ("R032", "Finance Analyst",                      "G&A",              1, 3, False, 45,  30, True,   50),
    ("R033", "HR Generalist",                        "G&A",              1, 3, False, 50,  25, True,   40),
    ("R034", "IT Support",                           "G&A",              1, 2, False, 55,  20, True,   30),
    ("R035", "Executive Assistant",                  "G&A",              1, 3, False, 35,  30, True,   40),
    ("R036", "G&A Manager",                          "G&A",              4, 4, False, 30,  35, False,  33),
    ("R037", "G&A Director",                         "G&A",              5, 5, False, 15,  30, False,   6),
    ("R038", "G&A VP",                               "G&A",              6, 6, False, 10,  25, False,   1),
    ("R039", "Infrastructure/Data Center Engineer",  "Operations",       2, 4, False,  3,  80, True,   75),
    ("R040", "Program Manager (Ops)",                "Operations",       3, 4, False, 40,  35, True,   58),
    ("R041", "Ops Manager",                          "Operations",       4, 4, False, 35,  35, False,  22),
    ("R042", "Ops Director",                         "Operations",       5, 5, False, 15,  30, False,   4),
    ("R043", "Ops VP",                               "Operations",       6, 6, False, 10,  25, False,   1),
    ("R044", "SVP Engineering & Product",            "Corporate",        7, 7, False, 10,  25, False,   1),
    ("R045", "SVP G&A & Operations",                 "Corporate",        7, 7, False, 10,  25, False,   1),
    ("R046", "SVP Go-to-Market",                     "Corporate",        7, 7, False, 10,  25, False,   1),
    ("R047", "CEO",                                  "Corporate",        7, 7, False, 10,  25, False,   1),
]

# ---------------------------------------------------------------------------
# 2. Pay bands (company_design.md §3) — base salary, USD
# ---------------------------------------------------------------------------
PAY_BANDS = {
    1: (70_000,  90_000),
    2: (90_000, 115_000),
    3: (115_000, 150_000),
    4: (150_000, 190_000),
    5: (190_000, 240_000),
    6: (240_000, 320_000),
    7: (320_000, 450_000),
}

# ---------------------------------------------------------------------------
# 3. Rating distribution — normal-ish, skewed toward 3 (company_design.md §2)
# ---------------------------------------------------------------------------
# Weight: 1→~1.5%, 2→~18.5%, 3→~60.5%, 4→~18%, 5→~1.5%
RATING_WEIGHTS = [0.015, 0.185, 0.605, 0.180, 0.015]

# ---------------------------------------------------------------------------
# 4. Build roles.csv
# ---------------------------------------------------------------------------
roles_rows = []
for r in ROLES:
    rid, rname, div, gmin, gmax, si, aq, ttf, le, _hc = r
    roles_rows.append({
        "role_id": rid,
        "role_name": rname,
        "division": div,
        "grade_min": gmin,
        "grade_max": gmax,
        "strategic_impact": si,
        "adjacent_qualified_headcount": aq,
        "time_to_fill_days": ttf,
        "lever_eligible": le,
    })
roles_df = pd.DataFrame(roles_rows)

# ---------------------------------------------------------------------------
# 5. Build employees.csv
# ---------------------------------------------------------------------------
employees = []
emp_counter = 1

for r in ROLES:
    rid, rname, div, gmin, gmax, si, aq, ttf, le, headcount = r

    for _ in range(headcount):
        eid = f"E{emp_counter:05d}"
        emp_counter += 1

        # Grade: uniform across the role's grade range
        grade = int(rng.integers(gmin, gmax + 1))

        # Base salary: uniform within grade band, rounded to integer
        lo, hi = PAY_BANDS[grade]
        base_salary = int(rng.integers(lo, hi + 1))

        # Tenure: exponential with mean ~3 years, capped at 15, 1 d.p.
        tenure = round(min(float(rng.exponential(3.0)), 15.0), 1)

        # Rating: 1–5 drawn from weighted distribution
        rating = int(rng.choice([1, 2, 3, 4, 5], p=RATING_WEIGHTS))

        employees.append({
            "employee_id": eid,
            "role_id": rid,
            "role_name": rname,
            "division": div,
            "grade": grade,
            "base_salary_usd": base_salary,
            "tenure_years": tenure,
            "rating": rating,
            "manager_id": None,  # assigned in pass 2
        })

emp_df = pd.DataFrame(employees)

# ---------------------------------------------------------------------------
# 6. Assign manager_ids (pass 2)
#    Rule: each non-exec employee reports to a random manager in grade gmin+1
#    within the same division.  Execs (G6+) and the CEO report upward through
#    the Corporate SVPs and CEO rows.
# ---------------------------------------------------------------------------
def assign_managers(df):
    df = df.copy()
    # Build a lookup: division → list of manager employee_ids (G4+)
    mgr_lookup = {}
    for div in df["division"].unique():
        sub = df[(df["division"] == div) & (df["grade"] >= 4)]
        mgr_lookup[div] = sub["employee_id"].tolist()

    # Corporate SVPs manage VPs across divisions
    corp_svps = df[df["division"] == "Corporate"]["employee_id"].tolist()

    for idx, row in df.iterrows():
        if row["role_id"] == "R047":          # CEO has no manager
            df.at[idx, "manager_id"] = row["employee_id"]
            continue
        if row["grade"] >= 6:                 # VPs report to Corporate SVPs
            choices = corp_svps if corp_svps else [row["employee_id"]]
        else:
            div_mgrs = [m for m in mgr_lookup.get(row["division"], [])
                        if m != row["employee_id"]]
            choices = div_mgrs if div_mgrs else corp_svps
        if choices:
            df.at[idx, "manager_id"] = rng.choice(choices)
        else:
            df.at[idx, "manager_id"] = row["employee_id"]
    return df

emp_df = assign_managers(emp_df)

# ---------------------------------------------------------------------------
# 7. Write outputs
# ---------------------------------------------------------------------------
roles_df.to_csv("02_data/roles.csv", index=False)
emp_df.to_csv("02_data/employees.csv", index=False)

print(f"employees.csv: {len(emp_df):,} rows")
print(f"roles.csv:     {len(roles_df):,} rows")
print(f"Baseline fully-loaded cost: ${(emp_df['base_salary_usd'] * 1.3).astype(int).sum():,}")
print("\nHeadcount by tag (will match after tagging step):")
print("Run 02_data/build_employees_with_tags.py next.")
