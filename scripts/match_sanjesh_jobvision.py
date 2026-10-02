from pathlib import Path
import gzip,json,re,csv
from rapidfuzz import fuzz,process
from normalize import normalize_fa,slug
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/"data/raw/sanjesh/sanjesh_records.ndjson.gz"
J=ROOT/"site/data/jobvision_metrics.json"
OUT=ROOT/"site/data"
def find_key(d,cands):
    for c in cands:
        if c in d:return d[c]
    return ""
def sample_sanjesh():
    # Read all records but keep only normalized course/university names for matching.
    out=[]
    with gzip.open(S,"rt",encoding="utf-8") as f:
        for line in f:
            try:d=json.loads(line)
            except:continue
            course=find_key(d,["field","course","رشته","رشته/گرایش","عنوان رشته/گرایش"])
            uni=find_key(d,["university","institution","دانشگاه/مؤسسه","نام دانشگاه/مؤسسه"])
            if course or uni:
                out.append({"course_name":course,"university_name":uni,"record":d})
    return out
job=json.loads(J.read_text(encoding="utf-8")).get("records",[])
s=sample_sanjesh()
courses=sorted({normalize_fa(x["course_name"]) for x in s if x["course_name"]})
unis=sorted({normalize_fa(x["university_name"]) for x in s if x["university_name"]})
matches=[]; ambiguous=[]
for r in job:
    jc=normalize_fa(r.get("course_name","")); ju=normalize_fa(r.get("university_name",""))
    mc=process.extract(jc,courses,scorer=fuzz.ratio,limit=2) if jc else []
    mu=process.extract(ju,unis,scorer=fuzz.ratio,limit=2) if ju else []
    c1=mc[0] if mc else ("",0,None); c2=mc[1] if len(mc)>1 else ("",0,None)
    u1=mu[0] if mu else ("",0,None); u2=mu[1] if len(mu)>1 else ("",0,None)
    status="matched" if c1[1]>=96 and u1[1]>=96 else "ambiguous" if c1[1]>=88 and u1[1]>=88 else "unmatched"
    rec={**r,"normalized_course":jc,"normalized_university":ju,"course_match":c1[0],"course_score":c1[1],"university_match":u1[0],"university_score":u1[1],"match_status":status}
    if status=="ambiguous":
        rec["alternatives"]={"course":c2[0],"course_score":c2[1],"university":u2[0],"university_score":u2[1]}
        ambiguous.append(rec)
    elif status=="matched": matches.append(rec)
# Preserve nonmatched records for audit; never force a match.
(OUT/"matches.json").write_text(json.dumps({"schema_version":"1.0","matched":matches,"ambiguous":ambiguous,"counts":{"jobvision":len(job),"matched":len(matches),"ambiguous":len(ambiguous)}},ensure_ascii=False,indent=2),encoding="utf-8")
print("JobVision",len(job),"matched",len(matches),"ambiguous",len(ambiguous))
