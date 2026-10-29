# Phase 6 — DAX Specification

Documents the measures and data model used in `workforce_scenario_simulator.pbix`.
The pbix uses a **precomputed lookup** approach: scenario outputs are calculated
in Python and loaded as tables; DAX reads the right row via LOOKUPVALUE() based
on the active What-If parameter value.

---

## Tables loaded

| Table | Source file | Rows |
|---|---|---|
| raw employees | `02_data/employees_with_tags.csv` | 2,004 |
| raw roles | `02_data/roles.csv` | 47 |
| scenario_results | `04_scenario_model/scenario_results.csv` | 3 |
| severance_lookup | `05_powerbi/severance_lookup.csv` | 27 |

---

## What-If parameters (sliders)

| Parameter | Range | Step | Default | Used by |
|---|---|---|---|---|
| Severance Weeks | 2.0 – 15.0 | 0.5 | 4.0 | Targeted Layoffs |
| Attrition Rate | 0% – 20% | 0.5% | 5% | Hiring Freeze |
| Time To Hire | 30 – 180 days | 5 | 90 | Hiring Freeze |
| Few Skill Holders | 1 – 10 | 1 | 3 | tag derivation display |
| Variance Threshold | 0.5 – 1.5 | 0.05 | 0.8 | tag derivation display |

---

## Key measures

### Targeted Layoffs — Cutoff Rank
```dax
Targeted Layoffs Cutoff Rank =
LOOKUPVALUE(
    severance_lookup[cutoff_rank],
    severance_lookup[severance_weeks], [Severance Weeks Value]
)
```

### Targeted Layoffs — Net Savings %
```dax
Targeted Layoffs Net Savings % =
LOOKUPVALUE(
    severance_lookup[net_savings_pct],
    severance_lookup[severance_weeks], [Severance Weeks Value]
)
```

### Targeted Layoffs — Pass/Fail
```dax
Targeted Layoffs Pass Fail =
LOOKUPVALUE(
    severance_lookup[pass_fail],
    severance_lookup[severance_weeks], [Severance Weeks Value]
)
```

### Hiring Freeze — Projected Attrition
Counts employees whose `attrition_draw` falls below the slider value:
```dax
Hiring Freeze Projected Attrition =
CALCULATE(
    COUNTROWS('raw employees'),
    'raw employees'[attrition_draw] <= [Attrition Rate Value]
)
```

### Headcount by tag
```dax
Headcount A   = CALCULATE(COUNTROWS('raw employees'), 'raw employees'[criticality_tag] = "A")
Headcount B   = CALCULATE(COUNTROWS('raw employees'), 'raw employees'[criticality_tag] = "B")
Headcount BHR = CALCULATE(COUNTROWS('raw employees'), 'raw employees'[criticality_tag] = "B-HR")
Headcount C   = CALCULATE(COUNTROWS('raw employees'), 'raw employees'[criticality_tag] = "C")
```

---

## Lookup approach — rationale

The Targeted Layoffs lever requires sorting the C pool, computing cumulative net
savings, and stopping at a threshold — logic that cannot be expressed in DAX
without row-by-row iteration.  The precomputed lookup (`severance_lookup.csv`,
built by `05_powerbi/build_severance_lookup.py`) covers all 27 slider positions
and is exact to 4 decimal places.  The slider drives a LOOKUPVALUE() call;
no DAX iteration is needed.

To regenerate the lookup after changing the employee data:
```
python 02_data/build_employees_with_tags.py
python 05_powerbi/build_severance_lookup.py
```
Then reload the table in Power BI Desktop (Home → Refresh).
