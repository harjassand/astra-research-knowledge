import subprocess,sys,time,json,resource,datetime,os
from pathlib import Path
root=Path(__file__).resolve().parents[1]
command=[str(root/'venv/bin/python'),str(root/'src/run_guide_experiment.py'),'--input',str(root/'common/Astra_PostB3_Empirical_Probe_20261021/data/WesselsSatija2023.h5ad'),'--output',str(root/'results')]
start=time.perf_counter();stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='2',VECLIB_MAXIMUM_THREADS='2',OMP_NUM_THREADS='2')
with (root/'results/ANALYSIS_STDOUT.txt').open('w') as log,(root/'results/ANALYSIS_STDERR.txt').open('w') as err:
    process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=err,text=True,env=env)
    for line in process.stdout:
        log.write(line);log.flush();print(line,end='',flush=True)
    status=process.wait()
receipt={'start_utc':stamp,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'entire_command_wall_s':time.perf_counter()-start,'returncode':status,'child_cpu_s':resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime+resource.getrusage(resource.RUSAGE_CHILDREN).ru_stime,'child_peak_rss_bytes':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'command':command,'scope':'entire analysis command including input hashing, loading, bootstrap, seven control omissions, and serialization; reasoning/dependency setup/source retrieval separate'}
(root/'results/OUTER_RESOURCE_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
sys.exit(status)
