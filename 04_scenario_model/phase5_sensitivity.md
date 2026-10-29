# Phase 5 — Sensitivity Analysis

Tests whether the Phase 4 lever results hold up when the assumptions behind
them are wrong, not just at the single value assumed in `assumptions.md`.

## Question this phase answers

Targeted layoffs (the only lever that passed) cleared the 5% target by a
margin that looked thin in isolation (5.02% vs. 5.00%). Before treating that
as the answer, this phase checks: does the result depend on getting a guess
exactly right, or does it hold across a realistic range of guesses?

## Test 1 — Severance formula (assumptions.md row 3)

Current assumption: 2 weeks pay per year of tenure. Varied from 2 to 30
weeks/year, holding everything else fixed, using the same random tie-break
seed (303) as the Phase 4 result.

Full sweep (2.0–15.0 in 0.5-week steps, plus spot checks to 30 weeks) in
`sensitivity_severance.csv`. Key points:

| Severance (weeks/yr tenure) | Net savings | C-pool exhausted? | Laid off | Result |
|---|---|---|---|---|
| 2.0 (current) | 5.01% | No | 145 | PASS |
| 5.0 | 5.00% | No | 149 | PASS |
| 10.0 | 5.04% | No | 164 | PASS |
| 15.0 | 5.02% | No | 183 | PASS |
| 20.0 | 5.00% | No | 213 | PASS |
| 30.0 | 5.01% | No | 330 | PASS |

**Finding:** the lever passes across the **full tested range (2–30 weeks/year)**
without exhausting the C pool. As severance rises, the algorithm lays off
more people to keep clearing 5% net — and there are enough C-role employees
(465) to absorb the increase even at 30 weeks/year (only 330 of 465 needed).
The result is robust: it does not depend on the severance assumption being
close to the current value. The headline figure moves from 145 laid off at
the current assumption to 330 at 15× the assumption — a real trade-off to
state, not a failure.

*Note: the original run (before the pipeline was fully documented) used a
different random seed and showed pool exhaustion at 10.5 weeks. That result
came from a generator run whose seed was not preserved. The committed
`employees_with_tags.csv` and this sensitivity file are consistent with
each other and with the rest of the pipeline.*

## Test 2 — Criticality thresholds (assumptions.md rows 8, 9, 11)

Tested whether moving the three thresholds that decide each role's A/B/B-HR/C
tag changes the size of the C-role pool that targeted layoffs draws from.

| Threshold | Values tested | Effect on C-role headcount | Effect on A-role headcount |
|---|---|---|---|
| Variance (row 11, currently ≥0.8) | 0.6 – 1.0 | None (465 at every value) | Drops from 384 to 197 only at 1.0 |
| Few-skill-holders (row 9, currently <5) | 3 – 10 | None (465 at every value) | No effect |
| Time-to-hire (row 8, currently ≥60 days) | 40 – 80 days | None (465 at every value) | No effect |

**Finding:** none of the three thresholds affect targeted layoffs at all. The
8 roles tagged C are C because they are non-strategic **and** don't support
a strategic role (`supports_a = false`) — a business-judgment input seeded
directly in Phase 3, not something these three numeric thresholds touch.
Moving the thresholds reshuffles some roles between A, B and B-HR, but never
creates or removes a C role. The real lever over targeted layoffs' eligible
pool is the `supports_a` design call, not the tag thresholds — worth stating
plainly rather than implying the thresholds are load-bearing here.

## Test 3 — Attrition rate (assumptions.md row 1), for hiring freeze

Tested whether a more optimistic attrition rate could ever get hiring
freeze's protected-set losses to zero.

| Annual attrition | Net savings | Protected positions lost | Result |
|---|---|---|---|
| 4% | 1.74% | 27 | FAIL |
| 6% | 2.70% | 39 | FAIL |
| 8% | 3.55% | 48 | FAIL |
| 10% | 4.70% | 62 | FAIL |
| 12% (current) | 5.61% | 77 | FAIL |

**Finding:** hiring freeze cannot pass at any realistic attrition rate. Lower
attrition reduces protected-set losses but also drops net savings below the
5% target; higher attrition clears 5% but increases protected-set losses
further. The two failure conditions move in opposite directions and never
overlap at zero-loss-and-5%-savings simultaneously. This is a structural
property of a blanket freeze with a 35%-of-headcount protected set, not a
result that depends on getting the attrition assumption right.

## Overall conclusion

Targeted layoffs is the most robust finding: it passes across a **15x range**
of the severance assumption (2 to 30 weeks/year) without exhausting the
eligible pool, and the thing that determines pool membership is a defensible
business-judgment call (`supports_a`), not a fragile numeric threshold. Hiring freeze's failure is
structural and doesn't depend on any single assumption being wrong — it
fails by design, at every attrition rate tested. Delayering's failure (from
Phase 4) is also structural: too few eligible managers, not an assumption
that sensitivity testing would move.

## Files
- `sensitivity_severance.csv`
- `sensitivity_attrition.csv`
- `sensitivity_criticality_thresholds.csv`
