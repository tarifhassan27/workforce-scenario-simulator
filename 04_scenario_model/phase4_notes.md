# Phase 4 Notes — Scenario Engine

## What was built
Three levers, each as a standalone Python script (not one flexible function),
matching the binary pass/fail framing locked in Phase 0:
- `lever_hiring_freeze.py`
- `lever_delayering.py`
- `lever_targeted_layoffs.py`

Each reads `employees_with_tags.csv` (built from `clean.role_criticality` +
`raw.employees`), applies its lever logic, and scores against the pass/fail
rule from `problem_statement.md` §5: 12-month net savings ≥5% of baseline
AND zero protected-set (A + B-HR, lever-eligible) positions lost.

**Baseline:** 2,004 employees, $292,255,445 total 12-month fully loaded cost.
Target: $14,612,772 (5%).

## Results

| Lever | Net savings | Run-rate | Protected lost | Result |
|---|---|---|---|---|
| Hiring freeze (no exemption) | 5.6% (range 5.0–6.4% across 7 seeds) | 11–13% | 77–90 (never zero) | **FAIL** — protection |
| Delayering (redeploy, no severance) | 0.61% | 0.61% | 0 | **FAIL** — savings |
| Targeted layoffs (C-role only, lowest rating first, random tie-break) | 5.0–5.02% (range across 7 seeds) | 6.4–6.6% | 0 | **PASS** |

## What each hand-check caught
- **Hiring freeze:** confirmed the FAIL is reliable, not a single unlucky draw —
  ran 7 seeds, protected-set losses never zero (77–90 range), net savings always
  clears 5%. This is the sharpest finding: a naive read of "5.6% net savings"
  would call this a win; the model catches what that reading misses.
- **Delayering:** initial run found zero candidates — the generator's original
  round-robin manager assignment produced an artificially even 5–7 span, with
  no manager ever falling under the span=4 threshold. Traced to Phase 2, fixed
  there (manager assignment now uses random assignment with replacement, giving
  genuine variance: mean span 6.0, range 1–14, 34 of 256 managers now under-span).
  Phase 3's tags were re-verified unaffected by the fix (5/25/9/8, unchanged).
- **Targeted layoffs:** passes, but the margin is thin by construction — the
  C-role pool ($60M, 20.5% of baseline cost) is only just large enough to
  supply a 5% net cut once severance and notice costs are subtracted. The
  tie-break rule among equal ratings (random, not tenure-based, per explicit
  decision) moved the result from 5.03% to 5.02% — a small modeling choice
  visibly moves a result sitting this close to the line. Passed all 7 seeds
  tested (5.00–5.02%), but with no headroom against a stricter severance
  assumption.

## Known limitations, carried into Phase 5
- All three results depend on random seeds (attrition draws, tie-breaks). What's
  reported here is a representative run plus a multi-seed range — Phase 5's
  sensitivity analysis should test whether these seeds are structurally reliable
  or whether a bad draw could flip Targeted Layoffs to FAIL.
- Targeted layoffs' pass margin (~0.02–0.03 percentage points above target) is
  the single most fragile number in this project. A ~30% increase in the
  severance assumption (row 3) would plausibly flip it.
- Delayering can never fail on protection by construction (redeployment, not
  termination) — this was a Phase 0/1 design choice, not something the data
  discovered.

## Output
`scenario_results.csv` — one row per lever, columns: lever, net_savings_pct,
run_rate_savings_pct, protected_positions_lost, passes, fail_reason. This is
what Phase 6's Power BI dashboard reads directly — no scenario logic in DAX.
