#!/usr/bin/env python3
"""Integrity only. Does not run science or establish mathematical correctness."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
def main():
    m=json.loads((ROOT/'MANIFEST.json').read_text()); failures=[]; total=0
    for name,entry in m['files'].items():
        p=ROOT/name
        if not p.is_file(): failures.append([name,'missing']); continue
        b=p.read_bytes(); total+=len(b)
        if len(b)!=entry['bytes'] or hashlib.sha256(b).hexdigest()!=entry['sha256']:
            failures.append([name,'identity mismatch'])
    extras=sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()
                  and str(p.relative_to(ROOT)) not in m['files'] and p.name!='MANIFEST.json')
    if extras: failures.append(['unmanifested files',extras])
    proof=(ROOT/'PROOF.txt').read_bytes()
    if hashlib.sha256(proof).hexdigest()!=m['governing_proof_sha256']:
        failures.append(['PROOF.txt','governing binding mismatch'])
    print(json.dumps(dict(status='PASS' if not failures else 'FAIL',
        scope='payload identity only; no science or external delivery check',
        files=len(m['files']),bytes=total,failures=failures),indent=2))
    if failures: raise SystemExit(1)
if __name__=='__main__':main()
