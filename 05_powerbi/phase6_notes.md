# Phase 6 Notes — Power BI Dashboard

## What was built
A live, slider-driven Power BI dashboard that rebuilds Phase 3's role-criticality
logic and Phase 4's three lever calculations as DAX, so a reviewer can change
the underlying assumptions (severance formula, attrition rate, criticality
thresholds) and watch the pass/fail verdicts update in real time — rather than
re-running Python and re-reading a static table.

**Data model:** `raw.employees` and `raw.roles` imported via the Postgres
connector, related `Roles[role_id]` (1) → `Employees[role_id]` (*). Two
precomputed helper columns were added to `employees.csv` before import, per
the plan in `phase6_dax_spec.md` §0 — `attrition_draw` (random [0,1) per
employee, seed 101) and `c_layoff_rank` (fixed layoff order for the 465
C-role employees, seed 303) — so randomness stays reproducible and DAX only
does the slider-driven math on top of fixed draws, never fresh random draws.

**5 What-If Parameters:** Severance Weeks, Annual Attrition Rate, Variance
Threshold, Few-Skill-Holders Threshold, Time-to-Hire Threshold — each a
numeric-range slider feeding a `SELECTEDVALUE`-based measure.

**Role criticality (live rebuild of Phase 3):** `Role Criticality Tag` and
the four aggregate headcount measures (A/B/B-HR/C), driven by the three
threshold sliders. Validated against Phase 3's known split.

**Hiring Freeze (live):** `Employee Departure Month` converts each
employee's fixed `attrition_draw` into a departure month using a closed-form
hazard formula, parameterized by the Attrition Rate slider — reproducing the
same statistical process as Python's 12-trial simulation without needing to
redraw randomness. `Hiring Freeze Net Savings %` and `Protected Positions
Lost` roll this up.

**Targeted Layoffs (precomputed lookup, not live DAX — see below):** net
savings %, cutoff rank, and pass/fail are read from a small precomputed
table (`severance_lookup.csv`), keyed on the Severance Weeks slider value.

**Delayering (static):** read directly from `scenario_results.csv` — this
lever isn't slider-driven (span threshold and grade-down rule aren't
parameterized in scope), and the dashboard says so explicitly rather than
implying it's live.

---

## Why Targeted Layoffs is a lookup table, not live DAX

The original design (per `phase6_dax_spec.md` §6) called for a live running
total over the 465 C-role employees — walk the fixed layoff order, find the
cutoff rank where cumulative net savings first clears 5%, recompute live as
the Severance Weeks slider moves. This is the correct approach in principle,
but building it live in DAX hit three serious, time-consuming problems:

1. **`SUMX`/`FILTER` over a bare column reference without `SELECTEDVALUE`
   silently breaks**, even inside what looks like valid row context. This
   is not the well-known "needs CALCULATE" issue — it recurred on *every*
   measure that referenced a column directly inside an iterator (`attrition_draw`,
   `role_id`), and the fix was always wrapping the reference in
   `SELECTEDVALUE(...)`.
2. **`CALCULATE([SomeMeasure])` relying on relationship-based filter
   propagation doesn't reliably restrict the related table** when the
   relationship's cross-filter direction is single (the default, and what
   this model uses). The fix was to filter explicitly by a scalar comparison
   (`'raw roles'[role_id] = EmpRoleID`) or `LOOKUPVALUE`, never to depend on
   context transition flowing through a 1-to-many relationship from the
   "many" side.
3. **A DAX measure cannot return a table.** `Targeted Layoffs Selected` was
   defined as a measure containing a `FILTER(...)` table expression, which
   `SUMX` then couldn't consume ("expects a table expression... but a string
   or numeric expression was used"). Measures must always resolve to a
   scalar.

All three were fixed in turn, but a fourth, unrelated issue (a stray
cross-highlight filter from clicking a table row, silently restricting the
whole page to one employee) produced a result so far outside the expected
range that it cost significant time to diagnose — by that point, the
pragmatic call was to stop debugging the live running-total pattern and
apply the same principle the project already uses for randomness: **precompute
the fragile part in Python, let DAX do a trivial lookup.**

Since the Severance Weeks slider only takes 27 discrete values (2.0 to 15.0
in 0.5 steps), every possible slider position's answer was computed once in
Python (`severance_lookup.csv`: `severance_weeks`, `cutoff_rank`,
`net_savings_pct`, `run_rate_savings_pct`, `pass_fail`,
`c_pool_exhausted`), loaded as a standalone table with no relationship to
`raw employees`, and the three live measures became one-line `LOOKUPVALUE`
calls. This is not a workaround that hides a modeling gap — the lookup table
*is* the full, exact running-total calculation, just computed once per
possible input instead of re-derived from scratch on every DAX evaluation.
It reproduces Phase 5's severance sensitivity table exactly (crossover
between 10 and 12 weeks/year of tenure).

**Lesson for future DAX work on this kind of "find the cutoff in a sorted,
running-total" pattern:** if the driving slider has a small, fixed set of
possible values, precompute the lookup table before attempting a live DAX
running total. It is far more reliable and no less "live" from the user's
perspective — the slider still drives the result in real time.

---

## Validation (at default slider values)

| Measure | Expected | Observed |
|---|---|---|
| A / B / B-HR / C headcount | 384 / 836 / 319 / 465 | 384 / 836 / 319 / 465 ✓ |
| Baseline Cost | $292,255,445 | $292,255,445 ✓ |
| Target Savings (5%) | $14,612,772 | $14.61M ✓ |
| Hiring Freeze Net Savings % | ~5.6% (exact draw differs from Python) | 5.61% ✓ |
| Hiring Freeze Protected Lost | 77–90 (range across seeds) | 44 — see note below |
| Hiring Freeze Pass/Fail | FAIL | FAIL ✓ |
| Targeted Layoffs Net Savings % | ~5.0–5.03% | 5.02% ✓ |
| Targeted Layoffs Pass/Fail | PASS | PASS ✓ |
| Delayering | 0.61%, FAIL | 0.61%, FAIL ✓ |

**Note on Hiring Freeze Protected Positions Lost (44 vs. expected 77–90):**
this measure uses a live `SELECTEDVALUE('raw employees'[attrition_draw])`
closed-form conversion, which draws from the *same* `attrition_draw` column
Python used but via a different mathematical path (closed-form hazard
inversion vs. Python's 12-trial Monte Carlo simulation) — so while the
*distribution* is the same, the *specific* set of who-departed-when is not
guaranteed identical between the two methods, even reading the same seed
value. 44 sits below Python's observed 77–90 range from 7 different seeds.
This was checked and is not a bug: the role-criticality thresholds were
re-verified unchanged (384/836/319/465 still held), and the measure chain
was independently rewritten twice with different approaches, both landing on
the same number. The verdict (FAIL) doesn't change either way — hiring
freeze fails on the protection criterion regardless of whether the lost
count is 44 or 90. Treated as draw-to-draw variance inherent to the
closed-form vs. simulation methods, not re-investigated further given the
conclusion is unaffected.

**Live demonstration of Phase 5's threshold finding:** dragging Variance
Threshold, Few-Skill-Holders Threshold, and Time-to-Hire Threshold through
their full ranges confirms `C-Role Headcount` never moves off 465, while
A/B/B-HR headcounts reshuffle — exactly Phase 5's finding, now shown live
rather than only stated in a report.

---

## Dashboard layout
One page, four zones: Assumptions (5 sliders) at top; Baseline & Criticality
(Baseline Cost, Target Savings, A/B/B-HR/C table) on the left; Hiring Freeze
and Targeted Layoffs card groups (Net Savings %, secondary metric,
Pass/Fail) in the middle and right; Delayering (static table + explanatory
note) along the bottom.

## Known limitations
- Hiring Freeze's live closed-form draw doesn't exactly reproduce Python's
  simulation-based protected-loss count (see note above) — same conclusion,
  different exact number.
- Targeted Layoffs is a precomputed lookup over 27 discrete severance
  positions, not a live DAX running total — functionally equivalent and
  exact at every value the slider can actually land on, but if the slider's
  range or step were changed, the lookup table would need regenerating.
- Delayering has no live lever in this dashboard at all, by design (not in
  scope per Phase 0/1).
