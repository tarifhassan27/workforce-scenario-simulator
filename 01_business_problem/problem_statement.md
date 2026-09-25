# Problem Statement — Workforce Scenario Simulator

*Locked before any data was generated. Definitions in this file do not change after Phase 1 begins; any change is logged with a date and reason.*

## 1. Business problem

The CHRO has been asked to reduce workforce costs by 5% over the next 12 months without losing the capabilities the business depends on. Several cost levers are on the table, each with different speed, one-time cost and risk to critical roles. Today these options are debated on intuition. This project builds a simulator that tests each option against the same definitions, so the choice is made on evidence rather than on who argues best.

## 2. The decision

- **Decision owner:** CHRO, with CFO sign-off
- **Decision:** which cost lever to pursue, or whether none meets the target on its own
- **Question the model answers:** *Which lever reaches a 5% cost reduction within 12 months while losing zero critical positions — and how sensitive is that answer to our assumptions?*

## 3. Definitions

**Organisation.** A fictional, generic company of ~2,000 employees. No legal jurisdiction is modelled; severance and notice rules are set as explicit assumptions in `assumptions.md`.

**Workforce cost.** Fully loaded cost: base salary plus employer-side costs (benefits, taxes, allowances), as one combined figure per employee.

**Baseline.** Fully loaded workforce cost for the next 12 months if nothing changes.

**Time horizon.** 12 months from the decision date.

**Savings — two measures, reported side by side:**
- **12-month net savings** = cost avoided within the 12 months − one-time costs incurred within the 12 months (e.g. severance), as % of baseline. **This measure decides pass/fail.**
- **Annual run-rate savings** = annualised workforce cost at month 12 vs baseline, as %. Reported for context only; shows where each lever ends up once one-time costs are behind it.

**Criticality — two layers (after Huselid, Beatty & Becker, HBR 2005):**

*Role layer* — every role is classified once:
- **A (strategic):** direct impact on executing the company's strategy **and** wide spread in performance ratings among the people in that role.
- **B (support):** supports A roles, **or** is strategic but shows little performance spread.
  - **Hard-to-replace B:** a B role that crosses the thresholds for *both* few internal skill holders *and* long time to hire. Thresholds are set in `assumptions.md`.
- **C (surplus):** neither strategic nor supporting A roles.

*Person layer* — each employee's year-on-year performance rating. Used to select individuals within a lever (see §4), not to decide criticality.

**Protected set.** All positions in A roles plus all positions in hard-to-replace B roles.

## 4. Levers (v1)

1. **Hiring freeze.** Departures from natural attrition are not backfilled for the 12-month horizon, with no exemption for the protected set. If a critical position empties out through attrition, it stays empty — this is a deliberate test of the blanket-freeze default many companies reach for first.
2. **Delayering.** Managers below a minimum span of control are removed; their direct reports move to the next manager up. Span threshold set in `assumptions.md`.
3. **Targeted layoffs.** Headcount is reduced in C roles first, lowest performance ratings first, until the target is reached or C roles are exhausted.

Each lever is tested **on its own**. If no single lever passes, that is a valid finding, not a failure of the model.

## 5. Pass / fail rule

A scenario **passes** only if both are true:
1. 12-month net savings ≥ 5% of baseline, **and**
2. Zero positions in the protected set are lost — "lost" means eliminated, or vacated and left unfilled at month 12.

## 6. Out of scope (v1)

- Grade-mix change, redeployment and reskilling (planned for v2)
- Combinations of levers
- Knock-on effects: productivity loss, survivor attrition, morale
- Jurisdiction-specific labour law
- Any real company's data

## 7. Deliverable

A dashboard where the CHRO selects a lever and sees, in one view: net savings %, run-rate savings %, protected positions lost, and pass/fail — plus a sensitivity view showing which assumptions would change the answer. Supported by a short executive brief.
