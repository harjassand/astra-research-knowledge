#!/usr/bin/env python3
"""Replay scoped evidence in a temporary copy; preserve supplied receipts.

Standard library only. Default: small exact comparisons, interval primitive,
uncapped sampler's recorded bit path, and state/posterior diagnostics.
--large additionally repeats the 32- and 64-component interval computations.
Hashes establish package integrity, not scientific correctness.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time

BASE = Path(__file__).resolve().parent


def integrity():
    manifest = BASE/'MANIFEST.json'
    if not manifest.exists():
        return {'status':'manifest_not_yet_created'}
    data = json.loads(manifest.read_text())
    for row in data['files']:
        path = BASE/row['path']
        assert path.is_file(), f"missing {row['path']}"
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256'], row['path']
    return {'status':'hashes_match', 'files':len(data['files']),
            'scope':'byte integrity only, not scientific validation'}


def verify_result(name, result):
    if name == 'hitting_identity':
        assert result['status']=='PASS' and result['exact_rational_cases']==57
    elif name == 'signed_sampler':
        assert all(x['exact_enumerated_identity']=='PASS' for x in result['cases'])
        assert all(x['identity']=='PASS' for x in result['prefix_sampler'])
    elif name == 'reset_exact_comparator':
        assert result['status']=='all_exact_comparisons_pass'
        assert len(result['checks'])==4 and all(x['contained'] for x in result['checks'])
    elif name == 'uncapped_sampler_path':
        assert result['replayed'] is True
    elif name == 'boundary_interval_12':
        prior=json.loads((BASE/'research/certified_boundary/receipt.json').read_text())
        for key in ('lower','upper'):
            assert result['hitting_laplace_transform'][key]==prior['hitting_laplace_transform'][key]
    elif name == 'controlled_state':
        assert result['fine'][-1]['terms']==159
        assert abs(result['fine'][-1]['state_l1_error']-0.01007326753)<1e-10
        assert result['fine'][-1]['state_l1_error']<result['coarse'][-1]['state_l1_error']
    elif name == 'adaptive_detector':
        assert result['boundary_transform_max_error']<1e-13
        fine=result['fine']
        assert fine['first_choice']['selected']=='A'
        for name2,selected in [('no_click','A'),('click','B')]:
            branch=fine['adaptive_continuations'][name2]
            assert branch['second_choice']['selected']==selected
            assert abs(branch['second_choice']['regret'])<1e-12
            assert branch['branch_l1_error']<0.004
    elif name == 'reset_interval_64':
        prior=json.loads((BASE/'research/reset_sampler/regenerative_large_receipt.json').read_text())
        for key in ('lower','upper'):
            assert result[key]==prior[key]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--large',action='store_true')
    parser.add_argument('--integrity-only',action='store_true')
    parser.add_argument('--output',type=Path,default=BASE/'REPLAY_LATEST.json')
    args=parser.parse_args()
    hashes=integrity()
    if args.integrity_only:
        print(json.dumps(hashes,indent=2))
        return
    jobs=[
        ('hitting_identity','root_hitting/verify.py',[]),
        ('signed_sampler','signed_product/sampler.py',[]),
        ('reset_exact_comparator','reset_sampler/verify_regenerative.py',[]),
        ('uncapped_sampler_path','reset_sampler/sample_regenerative.py',
            ['--replay','regenerative_sample_receipt.json','--output','replayed_sample.json']),
        ('boundary_interval_12','certified_boundary/solver.py',[]),
        ('controlled_state','controlled_product/demo.py',[]),
        ('adaptive_detector','posterior_operation/demo.py',[]),
    ]
    if args.large:
        jobs += [('boundary_interval_32','certified_boundary/replay_large.py',[]),
                 ('reset_interval_64','reset_sampler/regenerative_solver.py',['--n','64','--bits','72'])]
    records=[]
    with tempfile.TemporaryDirectory(prefix='astra-capability-replay-') as scratch:
        root=Path(scratch)/'research'
        shutil.copytree(BASE/'research',root,ignore=shutil.ignore_patterns('__pycache__'))
        for name,script,extra in jobs:
            file=root/script
            start=time.monotonic()
            proc=subprocess.run([sys.executable,str(file),*extra],cwd=file.parent,
                                capture_output=True,text=True)
            entry={'name':name,'elapsed_seconds':time.monotonic()-start,
                   'exit_code':proc.returncode,'scope':'finite replay, not general proof validation'}
            try:
                if proc.returncode:
                    raise AssertionError(proc.stderr[-4000:])
                value=json.loads(proc.stdout)
                verify_result(name,value)
                entry['status']='PASS'
                entry['result']=value
            except Exception as exc:
                entry['status']='FAIL'
                entry['error']=str(exc)
                entry['stdout_tail']=proc.stdout[-2000:]
            records.append(entry)
            print(json.dumps({k:entry[k] for k in ('name','status','elapsed_seconds')}),flush=True)
            if entry['status']=='FAIL':
                break
    result={'status':'PASS' if all(r['status']=='PASS' for r in records) else 'FAIL',
            'python':sys.version,'integrity_before_run':hashes,'large_runs_included':args.large,
            'records':records,'scope':'Scoped exact identities, analytic interval implementations and finite numerical diagnostics; no external proof or originality certification'}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    if result['status']!='PASS':
        raise SystemExit(1)


if __name__=='__main__':
    main()
