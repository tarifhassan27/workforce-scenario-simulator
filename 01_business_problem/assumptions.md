# Assumptions Register

*One row per number not derived from the generated data itself. Every scenario result should be traceable back to a row here. Values marked "assumption" are candidates for the Phase 5 sensitivity analysis first.*

| # | Assumption | Value | Basis | Used by |
|---|---|---|---|---|
| 1 | Annual voluntary attrition rate | 12%, applied evenly per month | Assumption (typical mid-range tech attrition) | Hiring freeze |
| 2 | Attrition is random across roles (not concentrated in any tag) | — | Assumption, deliberately simple for v1 | Hiring freeze |
| 3 | Severance formula | 2 weeks pay per year of tenure, 4-week minimum | Assumption (common US private-sector norm) | Targeted layoffs |
| 4 | Notice/transition cost per layoff | 4 weeks pay, flat | Assumption | Targeted layoffs |
| 5 | Time to fill — A roles | 90 days | Assumption | Hard-to-replace check, hiring freeze savings timing |
| 6 | Time to fill — B roles | 60 days | Assumption | Hard-to-replace check |
| 7 | Time to fill — C roles | 30 days | Assumption | Hard-to-replace check |
| 8 | "Long time to hire" threshold (hard-to-replace test) | ≥60 days | Assumption — sets the B vs B-HR line | Role tagging |
| 9 | Internal skill holders — "few" threshold (hard-to-replace test) | <5 employees in adjacent roles (same division, one grade above/below) who could realistically cross-train into the role within 90 days | Assumption — sets the B vs B-HR line. Scoped to adjacent roles, not company-wide, so the test isn't trivially true for every small/niche role | Role tagging |
| 10 | Performance rating scale | 1–5, discrete | Assumption | Role variance check, layoff selection |
| 11 | "High variance" threshold (A-role test) | Role-level rating stdev ≥ 0.8 | Assumption — sets the A vs B line | Role tagging |
| 12 | Rating distribution shape by role | Mean rating equal across A/B/C (~3.0/5 for all); spread differs by tier — **A: stdev 0.9–1.1** (only tier crossing the row-11 threshold); **B (incl. B-HR): stdev 0.5–0.7**; **C: stdev 0.3–0.5** | Assumption, seeded into generator for the blind-analysis check (see Phase 3). Mean is held constant deliberately — if C roles also had a lower mean, "lowest rating first" in targeted layoffs would just be re-selecting the tag rather than performance. **Fixed during Phase 2 build:** original draft gave A and B the same spread, which would have made every B role clear the A threshold too — corrected so only A crosses 0.8 | Role tagging, layoff selection |
| 13 | Minimum span of control (delayering threshold) | 4 direct reports | From company design (§4), not independently sourced | Delayering |
| 14 | Fully loaded cost multiplier on base salary | 1.30× | Assumption (typical US benefits/tax load range) | All cost calculations |
| 15 | Baseline headcount | ~2,000 | Design choice (§1) | All levers |
| 16 | Delayered manager's new IC grade | One grade below their manager grade (e.g. G5 Director → G4 Staff IC) | Assumption | Delayering |
| 17 | Minimum role headcount before trusting the variance test | n ≥ 30 | Caught during Phase 2 validation: small roles (e.g. a 3-person Marketing Director population) can clear the row-11 variance threshold by chance alone, producing a false A-signal. Roles below n=30 are excluded from the empirical variance test in Phase 3 and tagged by strategic_impact + support logic only | Role tagging (Phase 3 SQL) |

## Notes

- Rows 8, 9 and 11 are the three thresholds that decide every role's A/B/C tag. If the sensitivity analysis is going to move any needle, it's these three — flag them for Phase 5 first.
- Row 12 is intentionally seeded rather than left to chance, so Phase 3's SQL can be checked blind against it (same pattern as Project 3).
- **Workflow rule (avoids circularity):** the A/B/C tags in `company_design.md` §2 are the sealed answer key, not an input to the generator. Two things are allowed to be seeded directly, because they're not statistical properties — they're business judgment: (1) `strategic_impact` (true/false per role) — whether the role executes part of the fictional strategy, a design call, not something data can discover; (2) `adjacent_qualified_headcount` and `time_to_fill_days` per role — raw, role-level numbers reflecting how scarce that skill genuinely is, seeded independently of any tag. What is NOT seeded directly: performance variance (computed in Phase 3 from actual generated ratings) and the final A/B/C tag itself (derived in Phase 3 by combining strategic_impact + empirical variance + the replaceability threshold test on rows 1–2's seeded numbers). Only then is the result diffed against `company_design.md` §2.
- Nothing here is sourced from a real dataset or a real company — deliberately, since this is a decision-support tool, not a claim about how real cost-cutting behaves.
