DROP TABLE IF EXISTS clean.role_criticality;

CREATE TABLE clean.role_criticality AS
WITH variance_check AS (
    SELECT role_id, COUNT(*) AS headcount, STDDEV(rating) AS rating_stdev,
           (COUNT(*) >= 30 AND STDDEV(rating) >= 0.8) AS clears_variance
    FROM raw.employees GROUP BY role_id
),
hard_to_replace_check AS (
    SELECT role_id, (adjacent_qualified_headcount < 5 AND time_to_fill_days >= 60) AS is_hard_to_replace
    FROM raw.roles
)
SELECT
    r.role_id, r.role_name, r.division, r.grade_min, r.grade_max, r.lever_eligible,
    v.headcount, ROUND(v.rating_stdev::numeric, 2) AS rating_stdev,
    CASE
        WHEN r.strategic_impact AND v.clears_variance THEN 'A'
        WHEN NOT r.strategic_impact AND h.is_hard_to_replace THEN 'B-HR'
        WHEN NOT r.strategic_impact AND r.supports_a THEN 'B'
        WHEN r.strategic_impact AND NOT v.clears_variance THEN 'B'
        ELSE 'C'
    END AS criticality_tag
FROM raw.roles r
JOIN variance_check v USING (role_id)
JOIN hard_to_replace_check h USING (role_id);

-- Verify: 47 rows, tag counts 5/30/9/8
SELECT criticality_tag, COUNT(*) FROM clean.role_criticality GROUP BY criticality_tag ORDER BY criticality_tag;