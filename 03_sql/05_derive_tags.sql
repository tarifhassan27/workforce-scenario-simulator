-- Phase 3, Query 5: derives the final tag per role, combining everything computed so far.
-- Nothing here reads a pre-assigned tag — it's built from strategic_impact, supports_a
-- (both seeded design inputs), the variance test (Query 1, computed from raw ratings),
-- and the hard-to-replace test (Query 2, computed from raw scarcity inputs).

WITH variance_check AS (
    SELECT
        role_id,
        COUNT(*) AS headcount,
        STDDEV(rating) AS rating_stdev,
        (COUNT(*) >= 30 AND STDDEV(rating) >= 0.8) AS clears_variance
    FROM raw.employees
    GROUP BY role_id
),
hard_to_replace_check AS (
    SELECT
        role_id,
        (adjacent_qualified_headcount < 5 AND time_to_fill_days >= 60) AS is_hard_to_replace
    FROM raw.roles
)
SELECT
    r.role_id,
    r.role_name,
    r.division,
    v.headcount,
    ROUND(v.rating_stdev::numeric, 2) AS rating_stdev,
    r.strategic_impact,
    v.clears_variance,
    h.is_hard_to_replace,
    CASE
        WHEN r.strategic_impact AND v.clears_variance THEN 'A'
        WHEN NOT r.strategic_impact AND h.is_hard_to_replace THEN 'B-HR'
        WHEN NOT r.strategic_impact AND r.supports_a THEN 'B'
        WHEN r.strategic_impact AND NOT v.clears_variance THEN 'B'  -- strategic but low variance, per §3 role-layer rule
        ELSE 'C'
    END AS derived_tag
FROM raw.roles r
JOIN variance_check v USING (role_id)
JOIN hard_to_replace_check h USING (role_id)
ORDER BY derived_tag, r.division, r.role_name;