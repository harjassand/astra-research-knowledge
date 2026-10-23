#!/usr/bin/env python3
"""Fresh relocation of ONLY Cycle11 new admissions, preserving recorded source."""
import argparse,json,shutil,subprocess,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def scientific(x):
    if isinstance(x,dict):
        return {k:scientific(v) for k,v in x.items() if k not in
                {'wall_seconds','cpu_seconds'}}
    if isinstance(x,list):return [scientific(v) for v in x]
    return x
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    start=time.monotonic(); records=[]
    with tempfile.TemporaryDirectory(prefix='astra_cycle11_fresh_') as td:
        fresh=Path(td)/'packet';shutil.copytree(ROOT,fresh)
        cmd=[sys.executable,'-I',str(fresh/'verify_package.py')]
        v=subprocess.run(cmd,capture_output=True,text=True,check=True)
        integrity=json.loads(v.stdout)
        for folder in ['.','studies/converse','studies/receiving','studies/search','studies/breeding']:
            here=fresh/folder; old=json.loads((here/'RESULT.json').read_text())
            run=subprocess.run([sys.executable,'-I',str(here/'replay.py')],
                               capture_output=True,text=True,check=True)
            new=json.loads((here/'RESULT.json').read_text())
            same=scientific(old)==scientific(new)
            if not same: raise AssertionError('Scientific replay mismatch: '+folder)
            records.append(dict(folder=folder,status=new['status'],scientific_fields_match=same,
                stdout=run.stdout,stderr=run.stderr))
    result=dict(status='PASS',scope='fresh relocated NEW Cycle11 admissions only; no predecessor science/code execution',
        archive_payload_integrity=integrity,new_replays=records,
        wall_seconds=time.monotonic()-start,asymptotic_quantum_codes_executed=0,
        historical_priority_certified=False,physical_implementation=False)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',replays=len(records),wall_seconds=result['wall_seconds']),indent=2))
if __name__=='__main__':main()
