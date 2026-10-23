#!/usr/bin/env python3
import argparse,json,shutil,subprocess,sys,tempfile,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
def strip(x):
    if isinstance(x,dict):return {k:strip(v) for k,v in x.items() if k!='wall_seconds'}
    if isinstance(x,list):return [strip(v) for v in x]
    return x
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();t=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='astra_access_fresh_') as d:
        fresh=Path(d)/'packet';shutil.copytree(HERE,fresh)
        v=subprocess.run([sys.executable,'-I',str(fresh/'verify_package.py')],capture_output=True,text=True,check=True)
        before=json.loads((fresh/'RESULT.json').read_text())
        r=subprocess.run([sys.executable,'-I',str(fresh/'replay.py')],capture_output=True,text=True,check=True)
        after=json.loads((fresh/'RESULT.json').read_text());assert strip(before)==strip(after)
    out=dict(status='PASS',scope='New access supplement only; no principal/predecessor science rerun',
        integrity=json.loads(v.stdout),scientific_fields_match=True,
        matching_record_cases=after['matching_record_cases'],exact_joint_cells=after['exact_joint_cells'],
        exact_character_separation_cases=after['exact_character_separation_cases'],
        source_proof_sha256=after['proof_sha256'],stdout=r.stdout,stderr=r.stderr,
        wall_seconds=time.monotonic()-t,quantum_codes_executed=0,historical_priority='UNKNOWN')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('stdout','stderr','integrity')},indent=2))
if __name__=='__main__':main()
