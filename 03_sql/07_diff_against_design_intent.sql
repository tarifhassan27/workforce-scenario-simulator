-- Diffs the derived A/B/C/B-HR tag against company_design.md's stated intent.
-- Only the 24 originally-designed roles have a documented intent to diff against;
-- the 23 auto-added leadership roles never had one, flagged as n/a rather than pass/fail.
-- Result: 24/24 match, 0 mismatches.

WITH intended AS (
    SELECT * FROM (VALUES
        ('R001','A'), ('R002','A'), ('R009','A'), ('R010','A'), ('R020','A'),
        ('R003','B'), ('R006','B'), ('R011','B'), ('R012','B'), ('R021','B'), ('R025','B'),
        ('R004','B-HR'), ('R015','B-HR'), ('R030','B-HR'), ('R031','B-HR'), ('R039','B-HR'),
        ('R005','C'), ('R016','C'), ('R026','C'), ('R032','C'), ('R033','C'), ('R034','C'), ('R035','C'), ('R040','C')
    ) AS t(role_id, intended_tag)
),
derived AS (
    WITH variance_check AS (
        SELECT role_id, COUNT(*) AS headcount, STDDEV(rating) AS rating_stdev,
               (COUNT(*) >= 30 AND STDDEV(rating) >= 0.8) AS clears_variance
        FROM raw.employees GROUP BY role_id
    ),
    hard_to_replace_check AS (
        SELECT role_id, (adjacent_qualified_headcount < 5 AND time_to_fill_days >= 60) AS is_hard_to_replace
        FROM raw.roles
    )
    SELECT r.role_id, r.role_name,
        CASE
            WHEN r.strategic_impact AND v.clears_variance THEN 'A'
            WHEN NOT r.strategic_impact AND h.is_hard_to_replace THEN 'B-HR'
            WHEN NOT r.strategic_impact AND r.supports_a THEN 'B'
            WHEN r.strategic_impact AND NOT v.clears_variance THEN 'B'
            ELSE 'C'
        END AS derived_tag
    FROM raw.roles r
    JOIN variance_check v USING (role_id)
    JOIN hard_to_replace_check h USING (role_id)
)
SELECT
    d.role_id, d.role_name,
    COALESCE(i.intended_tag, 'not designed — auto-added role') AS intended_tag,
    d.derived_tag,
    CASE
        WHEN i.intended_tag IS NULL THEN 'n/a'
        WHEN i.intended_tag = d.derived_tag THEN 'match'
        ELSE 'MISMATCH'
    END AS diff_result
FROM derived d
LEFT JOIN intended i USING (role_id)
ORDER BY diff_result DESC, d.role_id;