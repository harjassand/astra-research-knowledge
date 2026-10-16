"""Preserve the root-selected authored science and exact audit artifacts."""
from pathlib import Path
import hashlib
import json
import shutil

R=Path(__file__).resolve().parent.parent
W=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016')
U=W/'updates/GA-conformal-causal-genesis-20261016'


def main():
    selected={}
    def add(worker,name,reason='Authored proof, exact check or provenance; no external fulltext/data'):
        src=R/'workers'/worker/name
        if not src.is_file():raise RuntimeError('Missing final artifact '+str(src))
        dest='workers/'+worker+'/'+name
        if any(x in src.parts for x in ['scratch','external_excluded_from_publication','__pycache__']):
            raise RuntimeError('Excluded source selected')
        selected[dest]=(src,reason)
    for worker in ['ga_analytic_audit','ga_ui_audit','ga_weighted_audit','ga_concentration_genesis',
                   'ga_concentration_audit','ga_nonlinear_stress_audit','ga_integration_preparation']:
        for p in sorted((R/'workers'/worker).iterdir()):
            if p.is_file() and p.suffix in {'.md','.py','.json'}:add(worker,p.name)
    for worker,manifest,key in [
        ('ga_polynomial_genesis','PUBLICATION_ALLOWLIST.json','allowed_relative_files'),
        ('ga_sharp_invention','PUBLICATION_ALLOWLIST.json','allowlist')]:
        obj=json.loads((R/'workers'/worker/manifest).read_text())
        for name in obj[key]:add(worker,name)
    # Preserve authored superseded versions with their explicit correction trail.
    # They are not current proof premises or source-catalog authorities.
    for name in ['EXTENSIONS_v1.md','weighted_jet_verify_v1.py','VERIFICATION_RECEIPT_v1.json']:
        src=R/'workers/ga_polynomial_genesis'/name
        selected['history/ga_polynomial_genesis/'+name]=(src,'Superseded authored history; current EXTENSIONS_v2 and its audit control interpretation')
    for worker,manifest in [('ga_physical_causal_audit','PUBLICATION_MANIFEST.json'),
                            ('ga_source_replay','DELIVERY_MANIFEST.json'),
                            ('ga_primary_math_prior','PUBLIC_AUTHORED_MANIFEST.json')]:
        obj=json.loads((R/'workers'/worker/manifest).read_text())
        for entry in obj['files']:
            name=entry['path'];p=R/'workers'/worker/name
            if hashlib.sha256(p.read_bytes()).hexdigest()!=entry['sha256']:
                raise RuntimeError('Worker manifest changed: '+str(p))
            add(worker,name)
        add(worker,manifest)
    worker='ga_parametric_stress_genesis'
    parametric_manifest=json.loads((R/'workers'/worker/'PUBLICATION_MANIFEST.json').read_text())
    for entry in parametric_manifest['files']:
        if hashlib.sha256((R/'workers'/worker/entry['path']).read_bytes()).hexdigest()!=entry['sha256']:
            raise RuntimeError('Parametric publication file changed')
    for name in parametric_manifest['allowlist']:
        add(worker,name)
    for p in sorted((R/'root').iterdir()):
        if p.is_file() and p.suffix in {'.md','.py','.json'} and p.name not in {'claim_config.json','SELECTED_FREEZE.json'}:
            selected['root/'+p.name]=(p,'Root-authored derivation, synthesis, replay or integration tooling')
    # Ensure the completed all-r receiving proof is part of the selection.
    if 'workers/ga_nonlinear_stress_audit/ALL_R_AUDIT.md' not in selected:
        raise RuntimeError('Final all-r audit not ready')
    rows=[]
    for name,(src,reason) in sorted(selected.items()):
        b=src.read_bytes();dest=U/'package/derived'/name
        if dest.exists():raise RuntimeError('Refusing to overwrite frozen artifact '+str(dest))
        rows.append({'path':'package/derived/'+name,'research_path':str(src.relative_to(R)),
                     'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'selection_reason':reason,
                     'source_origin':'root_authored' if name.startswith('root/') else 'worker_authored',
                     'external_fulltext_or_native_dataset':False})
    for row in rows:
        src=R/row['research_path'];dest=U/row['path'];dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(src,dest)
        if hashlib.sha256(dest.read_bytes()).hexdigest()!=row['sha256']:raise RuntimeError('Freeze copy mismatch')
    manifest={'schema':'astra.ga.authored-freeze.v1','base_revision':'f80a8f15137575133ad2c9af975513b32e8fa93e',
              'files':rows,'file_count':len(rows),'bytes':sum(x['bytes'] for x in rows),
              'boundary':'Selection/hash integrity only; not scientific verification. Superseded history is explicitly separated.'}
    path=U/'DERIVED_MANIFEST.v0001.json'
    if path.exists():raise RuntimeError('Immutable freeze manifest already exists')
    path.write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'files':len(rows),'bytes':manifest['bytes']}))


if __name__=='__main__':main()
