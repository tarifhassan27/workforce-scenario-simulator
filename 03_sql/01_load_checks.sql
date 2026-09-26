-- Phase 2: Load verification queries
-- Confirms the raw.employees / raw.roles import matches the Python generator's output
-- (see 02_data/phase2_notes.md for the source numbers)

-- Expect: 2,004
SELECT COUNT(*) FROM raw.employees;

-- Expect: 47
SELECT COUNT(*) FROM raw.roles;

-- Expect: 5 rows summing to 384 (19.2% of 2,004) — the A-role headcount share
SELECT
    role_id,
    strategic_impact,
    COUNT(*)
FROM raw.employees e
JOIN raw.roles r USING (role_id)
WHERE r.strategic_impact = true
GROUP BY role_id, strategic_impact;