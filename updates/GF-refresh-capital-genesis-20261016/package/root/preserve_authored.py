#!/usr/bin/env python3
"""Preserve frozen authored GF artifacts; never copy acquired fulltexts."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo', type=Path, required=True)
    args=ap.parse_args()
    root=Path(__file__).resolve().parents[1]
    repo=args.repo.resolve()
    branch=subprocess.check_output(['git','-C',str(repo),'branch','--show-current'],text=True).strip()
    assert branch=='codex/refresh-capital-genesis-20261016', branch
    assert not subprocess.check_output(['git','-C',str(repo),'status','--porcelain'],text=True).strip()
    prefix=Path('updates/GF-refresh-capital-genesis-20261016/package')
    excluded=[];files=[]
    top={'REPORT.md','CONTINUATION_HANDOFF.md','WORKER_DEPLOYMENT.json'}
    for p in sorted(root.rglob('*')):
        if not p.is_file(): continue
        rel=p.relative_to(root)
        if rel.parts[0]=='originals': continue
        if any(part.startswith('acquired') or part in {'renders','__pycache__','.venv'} for part in rel.parts):
            excluded.append({'path':rel.as_posix(),'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())});continue
        if rel.parts[0] not in {'workers','root'} and rel.as_posix() not in top: continue
        if rel.name in {'claim_config.json','AUTHORED_PRESERVATION.v0001.json'}: continue
        assert not p.is_symlink()
        assert p.suffix.lower() not in {'.pdf','.epub','.png','.jpg','.jpeg'}, rel
        raw=p.read_bytes()
        # Detect actual common credential shapes, not scientific words such as "token".
        assert not re.search(rb'(?:sk-[A-Za-z0-9_-]{32,}|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})',raw), rel
        if p.suffix.lower() in {'.md','.txt','.json','.py'}:
            assert not re.search(rb'https?://[^\s\"<>]*(?:X-Amz-Signature|X-Goog-Signature|[?&]sig=)',raw,re.I), rel
        target=repo/prefix/rel
        assert not target.exists(), target
        files.append((rel,raw))
    manifest={'schema':'astra.gf-authored-preservation.v1','source_pin':'f937563cbc5d2249b8e0dd96bcbd3b8f78eb85c6','files':[{'path':(prefix/rel).as_posix(),'bytes':len(raw),'sha256':digest(raw)} for rel,raw in files],'excluded_acquired_bodies_and_transient_files':excluded,'scope':'Byte integrity and bounded credential-shape scan only. Authored proofs remain externally unreviewed. Excluded primary source hashes/URLs/read depths are retained in worker ledgers; their bodies are not republished.'}
    for rel,raw in files:
        target=repo/prefix/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
        assert target.read_bytes()==raw
    path=repo/'updates/GF-refresh-capital-genesis-20261016/AUTHORED_PRESERVATION.v0001.json'
    assert not path.exists();path.write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'files':len(files),'bytes':sum(len(raw) for _,raw in files),'excluded':len(excluded),'scope':'preservation only'}))

if __name__=='__main__':main()
