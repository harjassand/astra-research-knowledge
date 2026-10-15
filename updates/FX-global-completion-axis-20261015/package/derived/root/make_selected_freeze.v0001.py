from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
W=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-global-completion-axis-20261015')
I='updates/FX-global-completion-axis-20261015/'
sel=json.loads((W/I/'SELECTED_FREEZE.template.v0001.json').read_text())
candidate=json.loads((R/'workers/global_round_curation_draft/SELECTED_FILES.candidates.v0001.json').read_text())
items={x['research_relative_path']:x for x in candidate['files']}
orig=json.loads((R/'sources/SOURCE_MANIFEST.json').read_text())
original_hashes={x['sha256'] for x in orig['files']}
exclude_dirs={'sources','acquired','text','rendered','__pycache__','embedded_previous_moving_kernel_package','disposable_source'}
allowed={'.md','.txt','.json','.jsonl','.py','.csv','.tsv'}
selected=[]
for top in ['workers','root','independent_audits']:
 for p in sorted((R/top).rglob('*')):
  if not p.is_file() or p.is_symlink() or p.suffix not in allowed: continue
  rel=p.relative_to(R).as_posix()
  if any(part in exclude_dirs for part in p.relative_to(R).parts):
   # Acquisition/read receipts inside source folders are safe authored pointers.
   if not(p.suffix=='.json' and (p.name.startswith('ACQUISITION_RECEIPT') or p.name=='PROOF_INSPECTION_RECEIPT.json')): continue
  if p.name.startswith(('SELECTED_FREEZE.root-final','SELECTION_REVIEW')): continue
  raw=p.read_bytes(); raw.decode('utf-8'); h=hashlib.sha256(raw).hexdigest()
  if h in original_hashes: continue
  if rel in items:
   item=dict(items[rel]); assert item['sha256']==h and item['bytes']==len(raw),rel
  else:
   review=any(q in rel for q in ['independent_audit','reconstruction','projection_claim_audit','axis_evidence_adversary'])
   role='root_synthesis' if top=='root' else ('same_team_review' if review else 'worker_derivation')
   kind='code' if p.suffix=='.py' else ('receipt' if p.suffix in {'.json','.jsonl','.tsv','.csv'} else ('synthesis' if top=='root' else 'review' if review else 'proof'))
   if any(q in p.name.lower() for q in ['acquisition_receipt','source_receipt','reading_receipt','source_inventory','source_ledger']):
    role='acquired_primary_literature_receipt'; kind='receipt'
   item={'research_relative_path':rel,'path':I+'package/derived/'+rel,'sha256':h,'bytes':len(raw),'provenance_role':role,'payload_kind':kind,'contains_external_fulltext':False,'contains_external_dataset_or_clone':False,'selection_reason':'Root reviewed authored research, executable checks, scoped acquisition/provenance receipts, correction history or curation software. Source fulltexts, figures, archives, clones and caches are excluded; internal review does not establish external truth.'}
  selected.append(item)
assert all(x in {i['research_relative_path'] for i in selected} for x in items),set(items)-{i['research_relative_path'] for i in selected}
sel.update(status='root_frozen',selected_by='root',files=selected,total_files=len(selected),total_bytes=sum(x['bytes'] for x in selected))
out=R/'root/SELECTED_FREEZE.root-final.v0001.json'
with out.open('x') as f: json.dump(sel,f,indent=2);f.write('\n')
print(json.dumps({'files':sel['total_files'],'bytes':sel['total_bytes'],'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'path':str(out)}))
