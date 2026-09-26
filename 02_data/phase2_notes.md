# Phase 2 Notes — Data Generation

## Files
- `employees.csv` — 2,004 employees. Columns: employee_id, role_id, role_name, division, grade, base_salary_usd, tenure_years, rating, manager_id
- `roles.csv` — 47 role types. Columns: role_id, role_name, division, grade_min, grade_max, strategic_impact, adjacent_qualified_headcount, time_to_fill_days, lever_eligible

## What was seeded vs. what Phase 3 must derive
Per the workflow rule in `assumptions.md`:
- **Seeded directly (business judgment, not data-derivable):** `strategic_impact` per role.
- **Seeded directly (role-level scarcity, independent of any tag):** `adjacent_qualified_headcount`, `time_to_fill_days`.
- **NOT seeded — must be computed in Phase 3 from raw data:** performance-rating variance per role, the hard-to-replace test result, and the final A/B/C tag.
- Random seed: 7 (chosen after seed 42 produced two small-sample false positives on the variance test — see below).

## Role list
24 roles came from `company_design.md` §2. 23 more were auto-added to complete the org hierarchy (a generic Manager/Director/VP per division that lacked one, plus a 4-person corporate exec tier: 3 SVPs + CEO). All 23 are `strategic_impact = False` — the additions only build reporting lines, they never touch the A designation. The corporate exec tier is `lever_eligible = False`, excluded from all three levers.

## Validation (run blind, against the generated data only)
| Check | Result |
|---|---|
| Total headcount | 2,004 (target ~2,000) |
| A-role headcount share | 19.2% (Huselid guideline: under ~20%) |
| A roles failing the variance test | 0 |
| Non-A roles falsely passing the variance test | 0 (at seed 7 — see limitation below) |
| B-HR roles recovered by the replaceability threshold | 5 operational roles (SRE/DevOps, Enterprise CSM, Legal Counsel, Technical Recruiter, Infrastructure/Data Center Engineer) — matches `company_design.md`'s stated intent |
| Manager span of control (grade 4) | mean 6.0, range 5–7, 0 under-span |
| Orphaned reporting lines | 0 |
| Employees with no manager | 1 (CEO only, as expected) |

## Known limitation — carried forward as assumptions.md row 17
Small role populations (e.g. Marketing Director, n=3–14) can clear the ≥0.8 variance threshold by chance alone, independent of any real strategic signal. At seed 42 this produced 2 false positives; at seed 7, 0. This is a property of small samples, not something a seed change fixes structurally — a future regeneration could re-trigger it. **Fix applied:** Phase 3's SQL excludes any role with n<30 from the empirical variance test and relies on `strategic_impact` + support logic alone for those roles.
