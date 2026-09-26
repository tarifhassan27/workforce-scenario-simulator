-- Phase 3, Query 4: adds the one missing design input.
-- strategic_impact and the hard-to-replace inputs are seeded, but nothing yet
-- distinguishes B (support) from C (surplus) — that's a business judgment call
-- from company_design.md, not something the numbers reveal. Seeding it here,
-- same status as strategic_impact.

ALTER TABLE raw.roles ADD COLUMN supports_a BOOLEAN;

UPDATE raw.roles SET supports_a = true
WHERE role_name IN (
    'Software Engineer (general)', 'Product Designer', 'Sales Development Rep',
    'Sales Manager', 'Product Marketing Manager', 'Engineering Manager',
    'CS Manager', 'Product Team Lead', 'Marketing Manager', 'G&A Manager', 'Ops Manager',
    'Engineering Director', 'Sales Director', 'CS Director', 'Product Director',
    'Marketing Director', 'G&A Director', 'Ops Director',
    'Engineering VP', 'Sales VP', 'CS VP', 'Product VP', 'Marketing VP', 'G&A VP', 'Ops VP',
    'SVP Engineering & Product', 'SVP Go-to-Market', 'SVP G&A & Operations', 'CEO',
    'SRE/DevOps Engineer', 'Enterprise CSM', 'Legal Counsel', 'Technical Recruiter',
    'Infrastructure/Data Center Engineer'
);

UPDATE raw.roles SET supports_a = false WHERE supports_a IS NULL AND strategic_impact = false;