# Data Dictionary — Enttekhab Reshte 1405

## JobVision 1405
Canonical fields:
- `course_name`
- `university_name`
- `degree`
- `entrants`
- `confidence`
- `salary_year1_million_toman`
- `rank_region1`, `rank_region2`, `rank_region3`
- `related_employment_percent`
- `capacity`
- `overall_satisfaction_5`
- `satisfaction_job_market_5`
- `satisfaction_job_type_5`
- `satisfaction_income_5`
- `satisfaction_skill_match_5`
- `rank_trend`
- `salary_by_degree`
- `graduate_job_groups`
- `job_opportunities`
- `interest_match`
- `income_level`

Every mapped record must contain `source`, `source_year`, `source_page`, and `source_table`.

## Sanjesh 1404
The project consumes the 37-column audited dataset from the reference project. The full raw records are downloaded at build time from the reference repository; this repository does not invent or duplicate a synthetic schema.

## Match
A JobVision course/university record is:
- `matched`: both course and university fuzzy scores >= 96
- `ambiguous`: both >= 88 but at least one < 96
- `unmatched`: otherwise

Only `matched` records enter the final joined analytical dataset.
