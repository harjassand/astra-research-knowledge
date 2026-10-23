"""Replay only the new checkpoint, in an isolated temporary directory."""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parent
VOLATILE={"resources","python","platform","wall_seconds","cpu_seconds","peak_rss_kib"}


def scientific(x):
    if isinstance(x,dict):
        return {k:scientific(v) for k,v in x.items() if k not in VOLATILE}
    if isinstance(x,list):
        return [scientific(v) for v in x]
    return x


def main(output):
    started=time.perf_counter()
    tasks=[
        ("reviews/check_prefix_tail_exact.py",[],
         "prefix_tail_exact_results.json","reviews/prefix_tail_exact_results.json"),
        ("reviews/prefix_lower_checks.py",[],
         "prefix_lower_checks.json","reviews/prefix_lower_checks.json"),
        ("reviews/prefix_scaling_boundary.py",[],
         "prefix_scaling_boundary_results.json","reviews/prefix_scaling_boundary_results.json"),
        ("prefix_calculations.py",["--precision","80","--output","principal80.json"],
         "principal80.json","results/prefix_calculations.json"),
        ("prefix_calculations.py",["--precision","120","--output","principal120.json"],
         "principal120.json","results/prefix_calculations_120.json"),
    ]
    records=[]
    with tempfile.TemporaryDirectory(prefix="astra_pro3_cycle_") as tmp:
        work=Path(tmp)
        for i,(src,args,result,expected) in enumerate(tasks):
            task=work/str(i); task.mkdir()
            script=task/Path(src).name
            shutil.copyfile(ROOT/src,script)
            before=time.perf_counter()
            proc=subprocess.run([sys.executable,str(script),*args],cwd=task,
                                capture_output=True,text=True,timeout=60)
            assert proc.returncode==0,(src,proc.stdout,proc.stderr)
            actual=json.loads((task/result).read_text())
            reference=json.loads((ROOT/expected).read_text())
            assert scientific(actual)==scientific(reference),src
            record={"script":src,"arguments":args,"status":"PASS",
                    "scientific_output_matches_saved":True,
                    "elapsed_seconds":time.perf_counter()-before,
                    "script_sha256":hashlib.sha256(script.read_bytes()).hexdigest()}
            if "resources" in actual:record["observed_resources"]=actual["resources"]
            else:record["observed_resources"]={k:actual[k] for k in VOLATILE if k in actual}
            records.append(record)
    receipt={"status":"PASS","new_replays":len(records),"records":records,
             "total_wall_seconds":time.perf_counter()-started,
             "scope":"New calculations only. Temporary paths; saved source and original receipts unchanged.",
             "limitations":"Reproducibility and exact finite arithmetic checks do not prove universal mathematics."}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt,indent=2))


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,default=Path("/tmp/astra_pro3_cycle_replay.json"))
    main(p.parse_args().output)
