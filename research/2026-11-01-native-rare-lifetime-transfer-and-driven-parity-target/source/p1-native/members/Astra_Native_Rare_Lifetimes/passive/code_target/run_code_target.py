"""Reproduce this reference-only construction and its recorded receiver run."""
from pathlib import Path
import json
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent

subprocess.run([sys.executable,str(HERE/"build_code_target.py")],check=True)
subprocess.run(["g++","-O3","-std=c++17",str(HERE/"code_receiver.cpp"),
                "-o",str(HERE/"code_receiver")],check=True)
start=time.perf_counter()
run=subprocess.run([str(HERE/"code_receiver"),str(HERE/"receiver_input.txt")],
                   capture_output=True,text=True,check=True)
elapsed=time.perf_counter()-start
data=json.loads(run.stdout)
data["host_wall_seconds_this_run"]=elapsed
(HERE/"code_receiver_counts.json").write_text(json.dumps(data,indent=2)+"\n")
subprocess.run([sys.executable,str(HERE/"analyze_code_receiver.py")],check=True)
