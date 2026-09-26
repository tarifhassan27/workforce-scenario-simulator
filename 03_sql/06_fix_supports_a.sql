-- Fixes 04_add_supports_a.sql: its role_name-based UPDATE matched 0 rows for an
-- unclear reason. Re-done here on role_id, which is safer against text mismatches.

UPDATE raw.roles SET supports_a = true
WHERE role_id IN (
    'R003','R004','R006','R007','R008','R011','R012','R013','R014','R015',
    'R017','R018','R019','R021','R022','R023','R024','R025','R027','R028',
    'R029','R030','R031','R036','R037','R038','R039','R041','R042','R043',
    'R044','R045','R046','R047'
);

UPDATE raw.roles SET supports_a = false
WHERE role_id IN ('R005','R016','R026','R032','R033','R034','R035','R040');

-- Verify: null_count=5 (the A roles), true_count=34, false_count=8
SELECT
    COUNT(*) FILTER (WHERE supports_a IS NULL) AS null_count,
    COUNT(*) FILTER (WHERE supports_a = true) AS true_count,
    COUNT(*) FILTER (WHERE supports_a = false) AS false_count
FROM raw.roles;