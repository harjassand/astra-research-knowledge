"""Root application of the reviewed create-only overlay and append-only deltas."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess

R=Path(__file__).resolve().parent.parent
W=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016')
U=W/'updates/GA-conformal-causal-genesis-20261016'
STAGE=R/'integration_overlay_v2'


def sha(raw):return hashlib.sha256(raw).hexdigest()


def git(*args):return subprocess.check_output(['git','-C',str(W),*args],text=True).strip()


def main():
    plan=json.loads((STAGE/'PLAN.json').read_text())
    if git('rev-parse','HEAD')!=plan['pins']['expected_branch_head'] or git('status','--porcelain'):
        raise RuntimeError('Branch state changed after review')
    if git('ls-remote','--heads','origin','main').split()[0]!=plan['pins']['expected_remote_main']:
        raise RuntimeError('Main moved; reconcile before apply')
    if sha((R/'root/claim_config.json').read_bytes())!=plan['config_sha256']:
        raise RuntimeError('Root-reviewed config changed')
    for rel,digest in plan['base_registry_sha256'].items():
        if sha((W/rel).read_bytes())!=digest:raise RuntimeError('Registry changed: '+rel)
    for rel,digest in plan['staged_files'].items():
        if sha((STAGE/rel).read_bytes())!=digest:raise RuntimeError('Overlay changed: '+rel)
    for name,prefix in [('SOURCE_MANIFEST.json','package/originals'),('DERIVED_MANIFEST.v0001.json','')]:
        for item in json.loads((U/name).read_text())['files']:
            file=U/prefix/item['path']
            if sha(file.read_bytes())!=item['sha256']:raise RuntimeError('Frozen evidence changed: '+str(file))
    outputs={}
    for p in (STAGE/'overlay').rglob('*'):
        if p.is_file():
            rel=p.relative_to(STAGE/'overlay');dst=W/rel
            if dst.exists():raise RuntimeError('Create-only target exists: '+str(rel))
            outputs[rel.as_posix()]=p.read_bytes()
    for p in (STAGE/'additions').rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(STAGE/'additions');dst=W/rel;old=dst.read_bytes()
        if rel.suffix=='.jsonl':new=old+p.read_bytes()
        else:
            obj=json.loads(old);delta=json.loads(p.read_bytes())
            if isinstance(obj,list):obj+=delta
            elif rel.as_posix()=='indexes/query_aliases.json':
                if set(obj)&set(delta):raise RuntimeError('Alias collision')
                obj.update(delta)
            else:
                for key,values in delta.items():obj[key]+=values
            new=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
        outputs[rel.as_posix()]=new
    for rel,b in outputs.items():
        dst=W/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
    for src,name in [(STAGE/'PLAN.json','APPLIED_OVERLAY_PLAN.v0002.json'),
                     (R/'root/claim_config.json','CURATION_INPUT.v0001.json'),
                     (R/'root/STAGING_COMPATIBILITY.v0002.json','STAGING_COMPATIBILITY.v0002.json'),
                     (R/'root/build_ga_overlay.v0002.py','build_ga_overlay.v0002.py'),
                     (Path(__file__),'apply_reviewed_overlay.v0001.py'),
                     (R/'workers/ga_nonlinear_stress_audit/FREEZE_CONFIRMATION_V1.json','FREEZE_CONFIRMATION.v0001.json')]:
        dst=U/name
        if dst.exists():raise RuntimeError('Control artifact exists')
        shutil.copyfile(src,dst)
    receipt={'schema':'astra.ga.applied-overlay.v1','expected_head':plan['pins']['expected_branch_head'],
             'remote_main':plan['pins']['expected_remote_main'],'output_paths':sorted(outputs),
             'config_sha256':plan['config_sha256'],'historical_source_bytes_changed':False,
             'scientific_status':'source_derived_unreviewed; application is not scientific proof'}
    (U/'APPLY_RECEIPT.v0001.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'applied_paths':len(outputs),'new_claims':len(plan['claim_ids'])}))


if __name__=='__main__':main()
