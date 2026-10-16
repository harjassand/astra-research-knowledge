import subprocess,time,json,resource
from pathlib import Path
p=Path(__file__).resolve().parent;t=time.perf_counter()
with (p/'dense_stdout.txt').open('w') as out, (p/'dense_stderr.txt').open('w') as err:
    child=subprocess.Popen(['python',str(p/'dense_comparator.py')],stdout=out,stderr=err)
    try: status=child.wait(timeout=240);termination='completed'
    except subprocess.TimeoutExpired:
        child.terminate();status=child.wait();termination='240 second comparison budget reached'
r=dict(exit_status=status,termination=termination,wall_seconds=time.perf_counter()-t,child_peak_RSS_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
(p/'dense_process_receipt.json').write_text(json.dumps(r,indent=2));print(r)
