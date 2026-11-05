import argparse,json,os,signal,subprocess,sys,time,resource
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PYTHON=ROOT.parent/'matched_decoder_runtime_recovery_20261018/venv/bin/python'
def run(d):
    begin=time.perf_counter();stages=[]
    commands=[('acquisition',[str(PYTHON),str(ROOT/'canonical_qec_circuit_gate_20261105/acquire_graph.py'),'--distance',str(d),'--rounds',str(d)]),('floating_build',[str(PYTHON),str(ROOT/'qec_overlap_gate_20261105/fault_tuple_screen.py'),'--distance',str(d),'--cut-distance','64']),('integer_certificate',[str(PYTHON),str(ROOT/'qec_fault_tuple_20261105/build.py'),'--distance',str(d)]),('sequential_decision',[str(PYTHON),str(ROOT/'sequential_decision.py'),'--distance',str(d)])]
    import psutil
    for name,cmd in commands:
        t=time.perf_counter();maxrss=0;reason=None
        with (ROOT/f'd{d}_{name}.log').open('w') as out:
            p=subprocess.Popen(cmd,stdout=out,stderr=subprocess.STDOUT,start_new_session=True,env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'})
            while p.poll() is None:
                try:
                    proc=psutil.Process(p.pid);rss=proc.memory_info().rss+sum(x.memory_info().rss for x in proc.children(recursive=True));maxrss=max(maxrss,rss)
                except psutil.Error:pass
                if time.perf_counter()-begin>1800:reason='1800 second complete-pipeline cap'
                elif maxrss>2*1024**3:reason='2 GiB sampled process-tree RSS cap'
                if reason:os.killpg(p.pid,signal.SIGTERM);p.wait();break
                time.sleep(.1)
        item={'stage':name,'command':cmd,'seconds':time.perf_counter()-t,'sampled_process_tree_peak_rss_bytes':maxrss,'returncode':p.returncode,'kill_reason':reason};stages.append(item)
        (ROOT/f'd{d}_pipeline_resources.json').write_text(json.dumps({'distance':d,'full_pipeline_seconds':time.perf_counter()-begin,'stages':stages},indent=2)+'\n');print(json.dumps(item),flush=True)
        if p.returncode:break
    print(json.dumps({'distance':d,'full_pipeline_seconds':time.perf_counter()-begin,'success':all(x['returncode']==0 for x in stages) and len(stages)==4}),flush=True)
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--distance',type=int,required=True);v=a.parse_args();run(v.distance)
