#!/usr/bin/env python3
"""Resource wrapper added after missing /usr/bin/time, before any worker run."""
from pathlib import Path
import hashlib
import json
import resource
import subprocess
import sys
import time
from datetime import datetime, timezone

base=Path(__file__).resolve().parent
if (base/"RESULT.json").exists() or (base/"FAILURE.json").exists() or (base/"PROGRESS.json").exists():
    raise SystemExit("Refusing a second scientific execution")
binding=json.loads((base/"LAUNCH_FREEZE.json").read_text())
for item in binding["files"]:
    data=(base/item["path"]).read_bytes()
    assert hashlib.sha256(data).hexdigest() == item["sha256"]
ru0=resource.getrusage(resource.RUSAGE_CHILDREN)
cpu0,wall0=time.process_time(),time.monotonic()
started=datetime.now(timezone.utc).isoformat()
timeout=False
with (base/"STDOUT.txt").open("w") as out,(base/"STDERR.txt").open("w") as err:
    try:
        p=subprocess.run([sys.executable,str(base/"markov_query.py")],cwd=base,
                         stdout=out,stderr=err,timeout=120,check=False)
        rc=p.returncode
    except subprocess.TimeoutExpired:
        timeout=True
        rc=None
ru1=resource.getrusage(resource.RUSAGE_CHILDREN)
result={"started_utc":started,"finished_utc":datetime.now(timezone.utc).isoformat(),
        "worker_return_code":rc,"wall_timeout":timeout,
        "whole_worker_user_cpu_seconds":ru1.ru_utime-ru0.ru_utime,
        "whole_worker_system_cpu_seconds":ru1.ru_stime-ru0.ru_stime,
        "whole_worker_cpu_seconds":ru1.ru_utime+ru1.ru_stime-ru0.ru_utime-ru0.ru_stime,
        "whole_worker_peak_rss_kib_linux":ru1.ru_maxrss,
        "wrapper_cpu_seconds_before_receipt":time.process_time()-cpu0,
        "whole_wall_seconds":time.monotonic()-wall0,
        "scientific_executions":1,
        "prior_missing_time_launch_executed_no_worker":True}
(base/"PROCESS_RESOURCE.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
raise SystemExit(1 if rc is None else rc)
