from pathlib import Path
import json,re,csv
from .normalize import normalize_fa, slug
ROOT=Path(__file__).resolve().parents[1]
PAGES=ROOT/"data/processed/jobvision_pages"
OUT=ROOT/"site/data"
# Canonical schema: fields are populated only when a header/value mapping is explicit.
SCHEMA=[
"course_name","university_name","degree","entrants","confidence","salary_year1_million_toman",
"rank_region1","rank_region2","rank_region3","related_employment_percent","capacity",
"overall_satisfaction_5","satisfaction_job_market_5","satisfaction_job_type_5",
"satisfaction_income_5","satisfaction_skill_match_5","rank_trend","salary_by_degree",
"graduate_job_groups","job_opportunities","interest_match","income_level"
]
ALIASES={
"رشته":"course_name","دانشگاه":"university_name","رشته تحصیلی":"course_name",
"تعداد ورودی کارشناسی":"entrants","ضریب اطمینان":"confidence","ظرفیت":"capacity",
"میزان اشتغال مرتبط با رشته":"related_employment_percent","میزان اشتغال مرتبط":"related_employment_percent",
"رضایت کلی فارغ التحصیلان":"overall_satisfaction_5","رضایت فارغ التحصیلان":"overall_satisfaction_5",
"منطقه ۱":"rank_region1","منطقه ۲":"rank_region2","منطقه ۳":"rank_region3",
"حقوق فارغ التحصیلان کارشناسی در سال اول":"salary_year1_million_toman",
}
def header_key(x): return normalize_fa(x).replace(" ","")
def map_header(x):
    n=normalize_fa(x)
    for a,b in ALIASES.items():
        if normalize_fa(a)==n:return b
    return None
records=[]; issues=[]
for fp in sorted(PAGES.glob("page-*.json")):
    obj=json.loads(fp.read_text(encoding="utf-8"))
    for table in obj.get("tables",[]):
        rows=table.get("rows",[])
        if not rows: continue
        # Detect a header row; do not infer values without headers.
        hdr=None
        for ri,row in enumerate(rows[:5]):
            mapped=[map_header(c) for c in row]
            if sum(x is not None for x in mapped)>=2:
                hdr=(ri,mapped); break
        if not hdr:
            issues.append({"page":obj["page"],"table":table["table"],"reason":"header_not_resolved"})
            continue
        ri,mapped=hdr
        for row in rows[ri+1:]:
            rec={"source":"jobvision","source_year":1405,"source_page":obj["page"],"source_table":table["table"]}
            for idx,key in enumerate(mapped):
                if key and idx<len(row): rec[key]=row[idx]
            if rec.get("course_name") or rec.get("university_name"):
                records.append(rec)
(OUT/"jobvision_metrics.json").write_text(json.dumps({"schema_version":"1.0","records":records},ensure_ascii=False,indent=2),encoding="utf-8")
(OUT/"jobvision_mapping_issues.json").write_text(json.dumps(issues,ensure_ascii=False,indent=2),encoding="utf-8")
print("Mapped records:",len(records),"unresolved tables:",len(issues))
