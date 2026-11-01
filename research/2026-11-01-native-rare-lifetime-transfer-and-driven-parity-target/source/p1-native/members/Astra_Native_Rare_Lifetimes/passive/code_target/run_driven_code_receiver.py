"""Reproduce the separate driven reference receiver; no native acquisition."""
from pathlib import Path
import json
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
if not (HERE/"receiver_input.txt").exists():
    subprocess.run([sys.executable,str(HERE/"build_code_target.py")],check=True)
subprocess.run(["g++","-O3","-std=c++17",str(HERE/"driven_code_receiver.cpp"),
                "-o",str(HERE/"driven_code_receiver")],check=True)
start=time.perf_counter()
run=subprocess.run([str(HERE/"driven_code_receiver"),str(HERE/"receiver_input.txt"),
                    "2026110205"],capture_output=True,text=True,check=True)
elapsed=time.perf_counter()-start
data=json.loads(run.stdout)
data["host_wall_seconds_this_run"]=elapsed
(HERE/"driven_code_receiver_counts.json").write_text(json.dumps(data,indent=2)+"\n")
subprocess.run([sys.executable,str(HERE/"analyze_driven_code_receiver.py")],check=True)
