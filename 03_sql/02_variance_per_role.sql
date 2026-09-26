-- Phase 3, Query 1: rating variance per role, independent of any seeded tag.
-- Flags roles below the n=30 floor (assumptions.md row 17) as unreliable for the variance test.

SELECT
    r.role_id,
    r.role_name,
    r.division,
    r.strategic_impact,
    COUNT(*) AS headcount,
    ROUND(STDDEV(e.rating)::numeric, 2) AS rating_stdev,
    ROUND(AVG(e.rating)::numeric, 2) AS rating_mean,
    CASE WHEN COUNT(*) >= 30 THEN 'reliable' ELSE 'below n=30 floor' END AS sample_reliability,
    CASE WHEN STDDEV(e.rating) >= 0.8 THEN true ELSE false END AS clears_variance_threshold
FROM raw.employees e
JOIN raw.roles r USING (role_id)
GROUP BY r.role_id, r.role_name, r.division, r.strategic_impact
ORDER BY rating_stdev DESC;