-- Phase 3, Query 2: hard-to-replace test, independent of any seeded tag.
-- A role passes if it has few internal cross-trainable employees AND takes a long time to fill.

SELECT
    role_id,
    role_name,
    division,
    strategic_impact,
    adjacent_qualified_headcount,
    time_to_fill_days,
    CASE
        WHEN adjacent_qualified_headcount < 5 AND time_to_fill_days >= 60
        THEN true ELSE false
    END AS hard_to_replace
FROM raw.roles
ORDER BY hard_to_replace DESC, time_to_fill_days DESC;