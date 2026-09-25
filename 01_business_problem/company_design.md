# Company Design — "Meridian Cloud" (fictional)

*Fictional company built for this simulation only. No resemblance to any real employer intended.*

## 1. Company shape

- **Profile:** Enterprise SaaS company, AI-powered platform, sold to large enterprise customers
- **Strategic capabilities:** ship AI/ML features fast, keep enterprise customers running without downtime, close large complex deals, retain differentiated engineering talent
- **Headcount:** ~2,000
- **Divisions (7):** Engineering, Product, Sales, Customer Success, Marketing, G&A, Operations
- **Org layers (6):** CEO → SVP/EVP → VP → Director → Manager → IC / Senior IC
- **Grades (7):** G1 (entry IC) → G7 (executive)

## 2. Role list and criticality tags

Tag legend: **A** = strategic impact + high performance variance · **B** = support, or strategic with low variance · **B-HR** = B role that also clears the hard-to-replace bar (few internal skill holders + long time to hire) · **C** = neither

| Division | Role | Tag | Why |
|---|---|---|---|
| Engineering | ML/AI Engineer | **A** | Builds the AI differentiator; wide skill/output variance |
| Engineering | Senior Backend/Platform Engineer | **A** | Platform reliability is the product; wide variance |
| Engineering | Software Engineer (general) | B | Supports A engineers; more standardized output |
| Engineering | SRE / DevOps Engineer | **B-HR** | Supports uptime; scarce skill, slow to backfill |
| Engineering | QA/Test Engineer | C | Standardized, low strategic differentiation |
| Engineering | Engineering Manager | B | Coordinates A talent, doesn't create the differentiation itself |
| Product | Senior Product Manager | **A** | Owns roadmap prioritization; wide variance in execution quality |
| Product | Product Designer | B | Supports product, more standardized craft |
| Sales | Enterprise Account Executive | **A** | Direct revenue driver; classic wide sales variance |
| Sales | Solutions Architect (Sales Eng.) | **A** | Technical deal-closer; wide variance |
| Sales | Sales Development Rep | B | Feeds pipeline; process-standardized |
| Sales | Sales Manager | B | Supports A sellers |
| Customer Success | Enterprise CSM | **B-HR** | Relationship/account knowledge; slow to rebuild, real downside if lost |
| Customer Success | Technical Support Engineer | C | Standardized, replaceable |
| Marketing | Product Marketing Manager | B | Supports Sales/Product |
| Marketing | Marketing Generalist / Content | C | Standardized, low strategic differentiation |
| G&A | Legal Counsel | **B-HR** | Specialized, scarce, asymmetric downside if absent |
| G&A | Technical Recruiter | **B-HR** | Scarce skill in a tight market; cost of a bad hire is high |
| G&A | Finance Analyst | C | Standardized |
| G&A | HR Generalist | C | Standardized |
| G&A | IT Support | C | Standardized |
| G&A | Executive Assistant | C | Standardized |
| Operations | Infrastructure/Data Center Engineer | **B-HR** | Uptime-critical, scarce skill |
| Operations | Program Manager (Ops) | C | Standardized coordination |

**A-role share check:** 5 of 24 roles = ~21% of role *types* — close to Huselid's "under 20% of the workforce" guideline, which is measured in headcount, not role count. Headcount-weighted A share will be checked once the generator assigns employees to roles, and role counts adjusted if it drifts too far above ~20%.

## 3. Grades and pay bands (fully loaded, USD)

| Grade | Level | Base salary range | Fully loaded (×1.3) |
|---|---|---|---|
| G1 | Entry IC | $70,000–$90,000 | $91,000–$117,000 |
| G2 | IC | $90,000–$115,000 | $117,000–$149,500 |
| G3 | Senior IC | $115,000–$150,000 | $149,500–$195,000 |
| G4 | Staff IC / Manager | $150,000–$190,000 | $195,000–$247,000 |
| G5 | Senior Manager / Director | $190,000–$240,000 | $247,000–$312,000 |
| G6 | VP | $240,000–$320,000 | $312,000–$416,000 |
| G7 | SVP/EVP | $320,000–$450,000 | $416,000–$585,000 |

## 4. Org structure rules

- **Span of control:** managers (G4+) target 5–8 direct reports; below 4 is flagged as under-span (delayering candidate)
- **Reporting depth:** max 6 layers, CEO to IC
- **Grade-to-layer mapping:** IC/Senior IC → G1–G3, Manager → G4, Director → G5, VP → G6, SVP/EVP → G7
