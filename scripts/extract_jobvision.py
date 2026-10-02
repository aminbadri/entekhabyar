from pathlib import Path
import json, csv, re
import pdfplumber
ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/"data/raw/jobvision/jobvision.pdf"
OUT=ROOT/"data/processed/jobvision_pages"
OUT.mkdir(parents=True,exist_ok=True)
inventory=ROOT/"data/metadata/jobvision_page_inventory.csv"
def clean(v):
    if v is None:return ""
    return re.sub(r"\s+"," ",str(v)).strip()
review=[]
with pdfplumber.open(PDF) as pdf:
    for i,page in enumerate(pdf.pages,1):
        text=page.extract_text(x_tolerance=1,y_tolerance=3) or ""
        tables=page.extract_tables({"vertical_strategy":"lines","horizontal_strategy":"lines","intersection_tolerance":5})
        rec={"page":i,"text":text,"tables":[]}
        for ti,t in enumerate(tables):
            rows=[[clean(c) for c in row] for row in (t or [])]
            if rows: rec["tables"].append({"table":ti+1,"rows":rows})
        (OUT/f"page-{i:03d}.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding="utf-8")
        if not tables or len(text)<100:
            review.append((i,"low_extraction_signal"))
        print(i, "tables",len(tables), "chars",len(text))
with (ROOT/"data/metadata/jobvision_review_queue.csv").open("w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["page","reason"]); w.writerows(review)
print("Review queue:",len(review),"pages")
