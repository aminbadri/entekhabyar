from pathlib import Path
import subprocess,sys,json,gzip,csv
ROOT=Path(__file__).resolve().parents[1]
def run(script):
    subprocess.check_call([sys.executable,str(ROOT/"scripts"/script)])
run("download_sources.py")
run("extract_jobvision.py")
run("map_jobvision.py")
run("match_sanjesh_jobvision.py")
