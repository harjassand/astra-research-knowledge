"""Replay only new calculations in isolation; original source/receipts untouched."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time


def scientific(x):
    if isinstance(x,dict):
        return {k:scientific(v) for k,v in x.items() if k!='resources'}
    if isinstance(x,list):return [scientific(v) for v in x]
    return x


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--receipt',type=Path)
    args=p.parse_args()
    root=Path(__file__).resolve().parent
    wall=time.perf_counter()
    configs=[('safe_local_calculations.py',['--precision','80','--output','out80.json'],
              'out80.json','results/safe_local_calculations_80.json'),
             ('safe_local_calculations.py',['--precision','120','--output','out120.json'],
              'out120.json','results/safe_local_calculations_120.json'),
             ('reviews/check_safeguarded_mechanism.py',[],
              'safeguarded_mechanism_checks.json','reviews/safeguarded_mechanism_checks.json'),
             ('reviews/safeguarded_cost_checks.py',[],
              'safeguarded_cost_checks.json','reviews/safeguarded_cost_checks.json')]
    receipts=[]
    with tempfile.TemporaryDirectory(prefix='astra_cycle2_replay_') as tmp:
        tmp=Path(tmp)
        for index,(script,flags,result,reference) in enumerate(configs):
            dest=tmp/str(index);dest.mkdir()
            shutil.copy2(root/script,dest/Path(script).name)
            start=time.perf_counter()
            proc=subprocess.run([sys.executable,str(dest/Path(script).name),*flags],
                cwd=dest,capture_output=True,text=True,check=True)
            new=json.loads((dest/result).read_text())
            old=json.loads((root/reference).read_text())
            assert scientific(new)==scientific(old),script
            receipts.append({'script':script,'arguments':flags,'status':'PASS',
                'wall_seconds_including_process':time.perf_counter()-start,
                'replay_resources':new.get('resources'),
                'scientific_output_matches_original':True})
    receipt={'status':'PASS','configurations':receipts,
        'total_wall_seconds':time.perf_counter()-wall,
        'original_source_and_receipts_unchanged':True,
        'old_theorem_or_trial_reruns':False,
        'meaning':'Producer portability replay, not independent scientific acceptance.'}
    if args.receipt:
        args.receipt.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
