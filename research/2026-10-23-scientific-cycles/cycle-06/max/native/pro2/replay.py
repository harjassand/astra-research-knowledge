#!/usr/bin/env python3
"""Verify frozen payloads and run only the two new independent checkers."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys,time


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    out=args.output.resolve()
    if out==root or root in out.parents:
        raise ValueError('receiving output must be outside the frozen source')
    if out.exists() and any(out.iterdir()):
        raise ValueError('use a new or empty receiving directory')
    out.mkdir(parents=True,exist_ok=True)
    begin=time.perf_counter()
    manifest=json.loads((root/'MANIFEST.json').read_text())
    for item in manifest['files']:
        p=root/item['path']; raw=p.read_bytes()
        assert len(raw)==item['bytes'],item['path']
        assert hashlib.sha256(raw).hexdigest()==item['sha256'],item['path']
    # This small standalone checker writes beside itself. Relocate it and its
    # immutable input, rather than modifying its independently authored code.
    staged=out/'transition_check/research'
    (staged/'structure').mkdir(parents=True)
    (staged/'cut_balance_review').mkdir()
    shutil.copyfile(root/'research/structure/RESULT.json',staged/'structure/RESULT.json')
    transition=staged/'cut_balance_review/check_strip_transition_certificate.py'
    shutil.copyfile(root/'research/cut_balance_review/check_strip_transition_certificate.py',transition)
    commands=[
      [sys.executable,str(root/'verification/check_cut_balance_independent.py'),
       '--fixture',str(root/'results/cut_balance_operations.json'),
       '--output',str(out/'cut_balance_independent_result.json')],
      [sys.executable,str(transition)]
    ]
    runs=[]
    for index,cmd in enumerate(commands):
        start=time.perf_counter()
        result=subprocess.run(cmd,cwd=out,text=True,capture_output=True)
        (out/f'check_{index+1}_stdout.txt').write_text(result.stdout)
        (out/f'check_{index+1}_stderr.txt').write_text(result.stderr)
        runs.append({'checker':Path(cmd[1]).name,'returncode':result.returncode,
                     'whole_process_wall_seconds':time.perf_counter()-start})
        if result.returncode:
            raise RuntimeError(f'Independent checker failed; inspect {out}')
    record={'status':'PASS','payloads_verified':len(manifest['files']),
            'runs':runs,'whole_replay_wall_seconds':time.perf_counter()-begin,
            'scope':'new source integrity and exact receiving checks; no older campaign or novelty claim'}
    (out/'REPLAY_RECEIPT.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))


if __name__=='__main__': main()
