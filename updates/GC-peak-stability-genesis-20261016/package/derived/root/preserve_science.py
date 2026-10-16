#!/usr/bin/env python3
"""Create-only publication of authored proofs/receipts, without acquired full texts."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];W=Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016');P=W/'updates/GC-peak-stability-genesis-20261016/package';h=lambda b:hashlib.sha256(b).hexdigest()
def main():
 fs=[]
 excluded_dirs={'__pycache__','external_excluded_from_publication','acquired_excluded_from_publication'}
 for p in sorted((R/'workers').rglob('*')):
  if p.is_file() and not any(x in excluded_dirs for x in p.relative_to(R).parts):fs.append(p)
 for p in sorted((R/'root').iterdir()):
  if p.is_file() and p.suffix in {'.py','.md','.json'} and p.name not in {'claim_config.json','PUBLIC_REPLAY_PLAN.preview.json','DERIVED_MANIFEST.v0001.json'}:fs.append(p)
 rows=[]
 for p in fs:
  rel=p.relative_to(R);dest=P/'derived'/rel;raw=p.read_bytes();assert not dest.exists(),str(dest)
  rows.append({'path':str(dest.relative_to(W)),'source_path':str(rel),'bytes':len(raw),'sha256':h(raw),'role':'root_research_or_orchestration' if rel.parts[0]=='root' else 'worker_authored_proof_check_or_receipt'})
 for p,row in zip(fs,rows):
  d=W/row['path'];d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(p.read_bytes());assert h(d.read_bytes())==row['sha256']
 m={'schema':'astra.gc-derived-preservation.v1','source_pin':'9dbe934e5475f415c2d160a6c0715534aafa546b','files':rows,'exclusions':'External acquired full texts, copied repositories and __pycache__ excluded. Supplied source bytes are preserved separately in SOURCE_PUBLICATION.json. The saved pair receiver is included. Orchestration sources are retained but public replay executes only inspected bounded readers/checkers.','boundary':'Exact byte preservation; internal analytic and finite evidence remains externally unreviewed.'}
 (P/'DERIVED_MANIFEST.v0001.json').write_text(json.dumps(m,indent=2)+'\n')
 print(json.dumps({'files':len(rows),'bytes':sum(x['bytes'] for x in rows),'excluded_external_fulltexts':True}))
if __name__=='__main__':main()
