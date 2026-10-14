#!/usr/bin/env python3
"""Bounded copy-first scientific checks. Published and incoming bytes stay intact."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time

REPO=Path(__file__).resolve().parents[2]
PACKET=Path(__file__).resolve().parent
BASE='00631610750c708263d5cf6d812ebbb8edc77335'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def hashes(root):return {str(p.relative_to(root)):sha(p) for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}

def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--output-dir',type=Path,required=True);args=a.parse_args()
    out=args.output_dir.resolve()
    if out.is_relative_to(REPO) or out.exists():raise ValueError('Use a new output directory outside the publication checkout.')
    before=hashes(PACKET);out.mkdir(parents=True)
    work=out/'work';shutil.copytree(PACKET,work)
    replacements={
        '/Users/harjas/Downloads/ASTRA_Universal_Compensation':str(work/'package/universal'),
        '/Users/harjas/Downloads/astra_conditional_exchange':str(work/'package/exchange'),
        '/Users/harjas/.codex/attachments/70979206-4b3f-415e-9ff1-e22869ba8372/Pasted text.txt':str(work/'package/physical_pasted.txt'),
        '/Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-compensation-exchange':str(REPO),
    }
    adapters=[]
    for p in (work/'synthesis').rglob('*.py'):
        old=p.read_text();new=old;used=[]
        for x,y in replacements.items():
            if x in new:new=new.replace(x,y);used.append({'old':x,'new':y})
        if used:
            p.write_text(new);adapters.append({'file':str(p.relative_to(work)),'original_sha256':hashlib.sha256(old.encode()).hexdigest(),'adapted_sha256':sha(p),'replacements':used})
    # The inherited heat verifier is itself executed on a copy. Require its exact
    # pinned dependency bytes; allowing later HEADs never permits source drift.
    heat_rel=Path('updates/FE/synthesis/quartic/checks')
    heat=out/'heat_source';heat.mkdir();deps=[]
    for p in sorted((REPO/heat_rel).iterdir()):
        if not p.is_file() or p.suffix not in ('.py','.json'):continue
        rel=str(p.relative_to(REPO))
        baseline=subprocess.check_output(['git','-C',str(REPO),'show',BASE+':'+rel])
        if p.read_bytes()!=baseline:raise ValueError('Pinned heat dependency changed: '+rel)
        shutil.copyfile(p,heat/p.name);deps.append({'path':rel,'sha256':sha(p),'source_revision':BASE})
    p=work/'synthesis/external_machinery/verify_transfer.py';old=p.read_text()
    needle="source_verifier = ASTRA/'updates/FE/synthesis/quartic/checks/verify_closed_heat.py'"
    if needle not in old:raise ValueError('Unexpected external replay adapter shape')
    new=old.replace(needle,'source_verifier = Path('+repr(str(heat/'verify_closed_heat.py'))+')')
    needle2='assert actual_pin == EXPECTED_PIN'
    if needle2 not in new:raise ValueError('Unexpected pin check shape')
    new=new.replace(needle2,"subprocess.run(['git','merge-base','--is-ancestor',EXPECTED_PIN,'HEAD'], cwd=ASTRA, check=True)")
    p.write_text(new);adapters.append({'file':str(p.relative_to(work)),'original_sha256':hashlib.sha256(old.encode()).hexdigest(),'adapted_sha256':sha(p),'reason':'Run heat verifier on pinned copy; permit later descendant HEAD only with exact pinned dependency bytes.'})
    steps=[('incoming_math','package/universal/verify_universal_obstructions.py'),('incoming_cycle','package/universal/certify_free_cycle.py'),('incoming_exchange','package/exchange/verify.py'),
        ('finite_jets','synthesis/higher_order_rigidity/check_coefficients.py'),('linear_selector','synthesis/nonlocal_compensation/verify_no_linear_selector.py'),
        ('quantum','synthesis/quantum_information_operation/verify_operation.py'),('matching','synthesis/exchange_robustness/verify_extensions.py'),
        ('critical_trace','synthesis/external_machinery/verify_transfer.py'),('electromechanical','synthesis/alternative_physical_operation/calculate.py'),
        ('optical','synthesis/optical_force_audit/calculate.py'),('overlap','synthesis/overlap_capital_audit/verify_transfers.py'),('routing','synthesis/root/verify_routing_correlations.py'),
        ('clock_extension','late_capital/overlap/late_pr87/verify_clock_extension.py'),('variance_acquisition','late_capital/adversarial/verify_late_pr87_acquisition.py')]
    receipt={'status':'RUNNING','scope':'Bounded finite algebra/numerical corroboration only; analytic proofs, physical obtainability, external correctness and priority are separate.','runtime':{'python':sys.version,'executable':sys.executable},'checks':[],'runtime_adapters':adapters,'pinned_dependencies':deps,'published_input_files':len(before)}
    for name,rel in steps:
        start=time.monotonic()
        command=[sys.executable,str(work/rel)]
        if name=='clock_extension':command+=['--primitive',str(work/'late_capital/adversarial/late_pr87_sources/verify_snapshot_operation.py')]
        try:r=subprocess.run(command,cwd=(work/rel).parent,capture_output=True,text=True,timeout=180)
        except subprocess.TimeoutExpired as e:
            stdout=e.stdout or '';stderr=e.stderr or ''
            if isinstance(stdout,bytes):stdout=stdout.decode(errors='replace')
            if isinstance(stderr,bytes):stderr=stderr.decode(errors='replace')
            class TimedOut:pass
            r=TimedOut();r.stdout=stdout;r.stderr=stderr+'\nTIMEOUT: 180 seconds';r.returncode=124
        log=out/(name+'.log');log.write_text(r.stdout+'\nSTDERR:\n'+r.stderr)
        receipt['checks'].append({'name':name,'script':rel,'command':command,'exit_code':r.returncode,'wall_seconds':time.monotonic()-start,'log':log.name,'log_sha256':sha(log)})
        print(name+': '+('PASS' if r.returncode==0 else 'FAIL'),flush=True)
    receipt['published_inputs_hash_unchanged']=before==hashes(PACKET)
    receipt['status']='PASS' if all(x['exit_code']==0 for x in receipt['checks']) and receipt['published_inputs_hash_unchanged'] else 'FAIL'
    receipt['total_steps']=len(steps)
    (out/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k not in ('checks','runtime_adapters','pinned_dependencies')},indent=2))
    return 0 if receipt['status']=='PASS' else 1

if __name__=='__main__':raise SystemExit(main())
