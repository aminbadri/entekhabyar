from pathlib import Path
import fitz, math
ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/"data/raw/jobvision/jobvision.pdf"
OUT=ROOT/"data/metadata/page_contact_sheets"
OUT.mkdir(parents=True,exist_ok=True)
doc=fitz.open(PDF)
thumbs=[]
for i,p in enumerate(doc):
    pix=p.get_pixmap(matrix=fitz.Matrix(.18,.18),alpha=False)
    thumbs.append(pix)
cols=5
for start in range(0,len(thumbs),50):
    batch=thumbs[start:start+50]
    rows=math.ceil(len(batch)/cols)
    w=max(x.width for x in batch); h=max(x.height for x in batch)
    sheet=fitz.Pixmap(fitz.csRGB,w*cols,h*rows)
    sheet.clear_with(255)
    for j,pix in enumerate(batch):
        sheet.copy(pix,(j%cols*w,(j//cols)*h))
    sheet.save(str(OUT/f"pages-{start+1:03d}-{start+len(batch):03d}.png"))
print("Created contact sheets for",len(doc),"pages.")
