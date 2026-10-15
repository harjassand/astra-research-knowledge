#!/usr/bin/env python3
"""Replay two hard-coded-path checkers with a disclosed path-only adaptation."""
from __future__ import annotations
import ast
import datetime as dt
import difflib
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

R=Path('/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-sharp-ion-genesis-v1')
W=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-sharp-ion-20261015')
OUT=Path(__file__).resolve().parent
PIN='b32943eeb62d0d79929a9e572a344219a785ebf9'
SCRATCH=OUT/'scratch.git'
PYTHON=R/'.venv/bin/python'


def sha(raw): return hashlib.sha256(raw).hexdigest()
def write(path,raw):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as stream: stream.write(raw)
def dump(path,value): write(path,(json.dumps(value,indent=2)+'\n').encode())
def git(*args): return subprocess.check_output(['git','--git-dir',str(SCRATCH),*args])


def source_list(path,var):
    for node in ast.parse(path.read_bytes()).body:
        if isinstance(node,ast.Assign) and any(isinstance(target,ast.Name) and target.id==var for target in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError('Required protected input list missing')


def main():
    specs=[
        {'name':'uniform_margin_adapted_path','script':'workers/fy_uniform_margin_genesis/check_exact.py','var':'sources',
         'outputs':['EXACT_CHECKS.json','PROVENANCE.json'],'extras':[],'count':None},
        {'name':'global40_adapted_path','script':'workers/fy_global_projection_audit/verify.py','var':'source_names',
         'outputs':['EXACT_VERIFICATION.v0002.json','EXACT_VERIFICATION.json'],'count':40,
         'extras':['workers/fy_contact_angle_genesis/REPORT.md',
                   'workers/fy_global_projection_audit/input_snapshots/generic_angle_REPORT.v0001.md',
                   'workers/fy_global_projection_audit/input_snapshots/generic_angle_REPORT.v0002.md']},
    ]
    protected=sorted(set(name for spec in specs for name in source_list(R/spec['script'],spec['var'])))
    pinfiles=[]
    for name in protected:
        pinned=git('show',PIN+':'+name)
        live=(W/name).read_bytes()
        assert pinned==live, 'Protected live scientific input differs from pin: '+name
        pinfiles.append({'path':name,'sha256':sha(pinned),'bytes':len(pinned),'live_equals_pinned':True})
    head=subprocess.check_output(['git','-C',str(W),'rev-parse','HEAD'],text=True).strip()
    changed=subprocess.check_output(['git','-C',str(W),'diff','--name-only',PIN,head],text=True).splitlines()
    assert all(name.startswith('updates/FY-sharp-ion-genesis-20261015/') for name in changed)
    checkout=OUT/'detached-pinned-checkout'
    commands=[]
    def run_git(argv,stdin=None):
        result=subprocess.run(argv,input=stdin,capture_output=True,check=True)
        commands.append({'argv':argv,'exit_code':result.returncode,'stdout':result.stdout.decode(),'stderr':result.stderr.decode()})
    run_git(['git','--git-dir',str(SCRATCH),'worktree','add','--detach','--no-checkout',str(checkout),PIN])
    run_git(['git','-C',str(checkout),'sparse-checkout','init','--no-cone'])
    patterns=('\n'.join('/'+name for name in protected)+'\n').encode()
    run_git(['git','-C',str(checkout),'sparse-checkout','set','--no-cone','--stdin'],patterns)
    run_git(['git','-C',str(checkout),'read-tree','--reset','-u','HEAD'])
    assert subprocess.check_output(['git','-C',str(checkout),'rev-parse','HEAD'],text=True).strip()==PIN
    assert subprocess.check_output(['git','-C',str(checkout),'status','--porcelain=v1'])==b''
    for item in pinfiles:
        assert sha((checkout/item['path']).read_bytes())==item['sha256']
    dump(OUT/'PINNED_SCIENTIFIC_INPUT_CHECK.v0001.json',{
        'schema':'astra.fy-pinned-input-reconstruction.v1','original_pin':PIN,'live_head_after_parent_source_commit':head,
        'paths_changed_by_parent_source_commit':changed,'protected_scientific_input_count':len(protected),
        'protected_inputs':pinfiles,'detached_sparse_checkout':str(checkout),'git_commands':commands,
        'adaptation_authorization':'Root explicitly authorized a transparent one-path substitution in disposable script copies; no algorithm or assertion changes.',
        'worktree_mutation_by_this_worker':'NONE; scratch.git and detached scratch checkout only'})
    receipts=[]
    try:
        for spec in specs:
            folder=OUT/'replays'/spec['name']
            folder.mkdir(parents=True,exist_ok=False)
            original=(R/spec['script']).read_bytes()
            assert original.count(str(W).encode())==1
            adapted=original.replace(str(W).encode(),str(checkout).encode())
            write(folder/'ORIGINAL_SCRIPT.py',original)
            write(folder/'ADAPTED_PATH_SCRIPT.py',adapted)
            patch=''.join(difflib.unified_diff(original.decode().splitlines(keepends=True),adapted.decode().splitlines(keepends=True),
                                             fromfile='original/'+spec['script'],tofile='path-adapted/'+spec['script']))
            write(folder/'PATH_ONLY_ADAPTER.patch',patch.encode())
            before={str(R/spec['script']):sha(original)}
            for name in spec['extras']:
                before[str(R/name)]=sha((R/name).read_bytes())
            for name in spec['outputs']:
                producer=(R/spec['script']).with_name(name)
                if producer.exists(): before[str(producer)]=sha(producer.read_bytes())
            with tempfile.TemporaryDirectory(prefix=spec['name']+'-',dir=OUT/'disposable') as temp:
                temp=Path(temp);script=temp/spec['script']
                script.parent.mkdir(parents=True);script.write_bytes(adapted)
                for name in spec['extras']:
                    path=temp/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes((R/name).read_bytes())
                env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1';env['XDG_CACHE_HOME']=str(temp/'.cache')
                argv=[str(PYTHON),'-B',str(script)];tick=time.monotonic()
                started=dt.datetime.now(dt.timezone.utc).isoformat()
                result=subprocess.run(argv,cwd=script.parent,capture_output=True,timeout=120,env=env)
                elapsed=time.monotonic()-tick
                write(folder/'stdout.txt',result.stdout);write(folder/'stderr.txt',result.stderr)
                outputs=[];parsed=[]
                for name in spec['outputs']:
                    path=script.with_name(name)
                    if not path.exists(): continue
                    raw=path.read_bytes();write(folder/'outputs'/name,raw)
                    parsed.append(json.loads(raw));outputs.append({'path':str(folder/'outputs'/name),'sha256':sha(raw),'bytes':len(raw)})
                count=parsed[0].get('checks_passed') if parsed else None
                scope_status=(parsed[0].get('algebra_status') or parsed[0].get('status')) if parsed else None
                unchanged=all(sha(Path(name).read_bytes())==wanted for name,wanted in before.items())
                protected_unchanged=all(sha((W/item['path']).read_bytes())==item['sha256'] for item in pinfiles)
                passed=result.returncode==0 and bool(parsed) and unchanged and protected_unchanged and (spec['count'] is None or count==spec['count'])
                receipt={'schema':'astra.fy-adapted-path-replay.v1','case':spec['name'],
                         'status':'PASS_ADAPTED_PATH_REPLAY' if passed else 'FAIL_ADAPTED_PATH_REPLAY',
                         'argv':argv,'cwd':str(script.parent),'started_at_utc':started,'measured_wall_seconds':elapsed,
                         'exit_code':result.returncode,'original_script_sha256':sha(original),'adapted_script_sha256':sha(adapted),
                         'adapter_patch_sha256':sha(patch.encode()),'adapter_script_sha256':sha(Path(__file__).read_bytes()),
                         'adapter_change':'Exactly one absolute W path changed to the actual detached b32943e sparse checkout; all algorithms and assertions retained.',
                         'exact_byte_script_execution':False,'observed_checks':count,'expected_checks':spec['count'],
                         'recorded_scope_status':scope_status,'outputs':outputs,
                         'stdout_sha256':sha(result.stdout),'stderr_sha256':sha(result.stderr),
                         'producer_files_unchanged':unchanged,'protected_scientific_inputs_unchanged':protected_unchanged,
                         'producer_file_pins':before,'supersedes_failure_for_execution_portability_only':str(OUT/'replays'/spec['name'].replace('_adapted_path','')/'RECEIPT.json'),
                         'full_all_affine_margin':parsed[0].get('full_all_affine_margin') if parsed else None,
                         'scientific_scope':'Same-team exact algebra with disclosed path substitution. Universal analytic proof, historical novelty, physical control, and unrestricted margin are not certified.'}
                dump(folder/'RECEIPT.json',receipt);receipts.append(receipt)
                print(json.dumps({'case':spec['name'],'status':receipt['status'],'checks':count,'exit_code':result.returncode}),flush=True)
    finally:
        run_git(['git','--git-dir',str(SCRATCH),'worktree','remove','--force',str(checkout)])
    dump(OUT/'ADAPTED_PATH_REPLAY_SUMMARY.v0001.json',{
        'schema':'astra.fy-adapted-path-replay-summary.v1','original_pin':PIN,
        'status':'ALL_ADAPTED_PATH_REPLAYS_PASS' if all(x['status']=='PASS_ADAPTED_PATH_REPLAY' for x in receipts) else 'FAILURE_PRESENT',
        'receipts':receipts,'protected_input_count':len(protected),'scratch_detached_checkout_removed':True,
        'original_failed_exact_byte_replays_retained':True,'source_code_or_producer_artifact_changes':'NOT_PERFORMED',
        'scope':'Transparent path-only portability repair in disposable copies; no unqualified exact-byte replay claim.'})


if __name__=='__main__': main()
