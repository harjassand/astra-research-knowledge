#!/usr/bin/env python3
"""Replay four decisive frozen checks in isolated scratch, retaining exact code.

The only input adapter rehydrates four byte-identical supplied snapshots from
their canonical original paths. No scientific code or source bytes are edited.
No network request, simulator, optimizer or acquired physical dataset is used.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,shutil,subprocess,sys,tempfile,time
HERE=Path(__file__).resolve().parent
W=HERE.parents[2]
I=HERE.parent
PY=Path('/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-16-positive-memory-genesis-v1/.venv/bin/python')
f=I/'SELECTED_FREEZE.v0003.json';freeze=json.loads(f.read_text())
snapshots=json.loads((I/'AUDIT_INPUT_REHYDRATION.v0001.json').read_text())['mapping']
jobs=[('reciprocal','fz_reciprocal_counterexample_audit','verify_exact.py','EXACT_AUDIT_RESULT.json'),
      ('kinetic-cap','fz_kinetic_cap_certificate_audit','check_certificate.py','EXACT_AUDIT.json'),
      ('persistent-bath','fz_memory_bath_theorem_audit','check_bath_audit_exact.py','EXACT_CHECKS.json'),
      ('conformal-diagnostic','fz_positive_conformal_genesis','verify_exact.py','VERIFICATION_RECEIPT.json')]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
before={x['path']:digest(W/x['path'])for x in freeze['files']}
assert all(before[x['path']]==x['sha256']for x in freeze['files'])
def run(job):
    name,worker,script,result_name=job;out=HERE/'replays'/name;out.mkdir(parents=True,exist_ok=True)
    assert not(out/'RECEIPT.json').exists(),'Use a new versioned replay directory rather than overwrite'
    with tempfile.TemporaryDirectory(prefix='astra-fz-review-')as temp:
        root=Path(temp);folder=root/'workers'/worker
        shutil.copytree(I/'package/derived/workers'/worker,folder)
        mappings=[]
        for x in snapshots:
            prefix=str(I.relative_to(W)/'package/derived/workers'/worker)+'/'
            if not x['audit_path'].startswith(prefix):continue
            dest=folder/x['audit_path'][len(prefix):];dest.parent.mkdir(parents=True,exist_ok=True)
            src=W/x['canonical_original_path'];assert digest(src)==x['sha256'];shutil.copyfile(src,dest)
            mappings.append(x)
        started=time.monotonic()
        result=subprocess.run([str(PY),'-B',str(folder/script)],cwd=folder,text=True,capture_output=True,timeout=120)
        elapsed=time.monotonic()-started
        (out/'stdout.txt').write_text(result.stdout);(out/'stderr.txt').write_text(result.stderr)
        status='PASS' if result.returncode==0 else 'FAIL'
        parsed=None
        if(folder/result_name).is_file():
            shutil.copyfile(folder/result_name,out/result_name)
            parsed=json.loads((out/result_name).read_text())
        receipt={'schema':'astra.fz-frozen-root-replay.v1','name':name,'worker':worker,
          'status':status,'exit_code':result.returncode,'wall_seconds':elapsed,
          'code_path':str((I/'package/derived/workers'/worker/script).relative_to(W)),
          'code_sha256':digest(folder/script),'input_rehydration':mappings,
          'code_adapter':'NONE; exact bytes. Only deduplicated supplied inputs rehydrated.',
          'stdout_sha256':digest(out/'stdout.txt'),'stderr_sha256':digest(out/'stderr.txt'),
          'output_file':result_name if parsed is not None else None,
          'output_sha256':digest(out/result_name)if parsed is not None else None,
          'scope':'Exact finite/algebraic checks only, no universal theorem from finite testing, novelty, external verification, physical evidence or performance claim.'}
        (out/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
        return receipt
with ThreadPoolExecutor(max_workers=4)as executor:receipts=list(executor.map(run,jobs))
after={x['path']:digest(W/x['path'])for x in freeze['files']}
payload={'schema':'astra.fz-root-frozen-replays.v1','status':'PASS'if all(x['status']=='PASS'for x in receipts)and before==after else'FAIL',
 'selected_files_unchanged':before==after,'selected_files_checked':len(before),
 'selection_sha256':digest(f),'replays':receipts,'scope':'Repository frozen-code replay and integrity only; four simultaneous independent scratch executions, no source overwrite.'}
(HERE/'REPLAY_SUMMARY.v0001.json').write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps({'status':payload['status'],'selected_files_unchanged':before==after,'replays':[{k:x[k]for k in ['name','status','exit_code']}for x in receipts]}))
raise SystemExit(0 if payload['status']=='PASS'else 1)
