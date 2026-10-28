"""SOURCE-DISABLED replay: consumes only public integer records/diagnostics.
Does not import simulator, use private_source_audit, U, memory, or probabilities.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from learner import Learner
from ordinary_comparator import OrdinaryComparator

def replay(directory):
    # Algorithm inferred from the public directory label, not private metadata.
    algorithm=directory.name.split('_')[0]
    learner=Learner() if algorithm=='bandit' else OrdinaryComparator()
    error=0.;calls=0;start=time.perf_counter()
    for line in (directory/'public_records.jsonl').read_text().splitlines():
        r=json.loads(line);calls+=1
        if algorithm=='bandit':
            learner.act(r['i'],r['z']);learner.observe(r['y'])
            error=max(error,float(np.linalg.norm(learner.theta-np.array(r['update']['theta_after']))))
        else:
            learner.decoder();learner.observe(r['j'],r['s'],r['m'],r['b'])
    return {'run':directory.name,'records_replayed':calls,'max_theta_replay_error':error,
            'replay_seconds':time.perf_counter()-start,'private_source_files_read':False}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('runs',type=Path);a=p.parse_args()
    print(json.dumps([replay(d) for d in sorted(a.runs.iterdir()) if d.is_dir()],indent=2))
