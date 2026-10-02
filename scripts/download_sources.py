from pathlib import Path
import requests, gzip, shutil, json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/raw"
OUT.mkdir(parents=True,exist_ok=True)
SOURCES={
"jobvision.pdf":"https://fileapi.jobvision.ir/public-files/reports/jobvision-education-field-selection-guide-1405.pdf",
"sanjesh_records.ndjson.gz":"https://raw.githubusercontent.com/Hhhkarimi/sanjesh1404/main/site/data/records.ndjson.gz",
"sanjesh_summary.json":"https://raw.githubusercontent.com/Hhhkarimi/sanjesh1404/main/site/data/summary.json",
"sanjesh_capacity.csv.gz":"https://raw.githubusercontent.com/Hhhkarimi/sanjesh1404/main/site/data/sanjesh_1404_all_degrees_capacity_detailed.csv.gz",
}
for name,url in SOURCES.items():
    target=OUT/("jobvision/"+name if name=="jobvision.pdf" else "sanjesh/"+name)
    target.parent.mkdir(parents=True,exist_ok=True)
    print("GET",url)
    r=requests.get(url,timeout=120)
    r.raise_for_status()
    target.write_bytes(r.content)
    print("WROTE",target,len(r.content))
