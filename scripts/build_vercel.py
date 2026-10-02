from pathlib import Path
import subprocess,sys,os
ROOT=Path(__file__).resolve().parents[1]
def cmd(*args): subprocess.check_call([sys.executable,*map(str,args)])
# Vercel has network during build. Install only data-build dependencies when missing.
try:
    import pdfplumber, fitz, rapidfuzz, requests
except Exception:
    subprocess.check_call([sys.executable,"-m","pip","install","-r",str(ROOT/"requirements-data.txt")])
cmd(ROOT/"scripts/build_data.py")
# Static site is already under site/. Vercel output is _site.
out=ROOT/"_site"
if out.exists():
    import shutil; shutil.rmtree(out)
import shutil
shutil.copytree(ROOT/"site",out)
print("Vercel build complete:",out)
