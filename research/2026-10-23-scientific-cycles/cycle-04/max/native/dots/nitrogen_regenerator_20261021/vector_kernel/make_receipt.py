"""Hash the bounded kernel delivery and verify original source preservation."""
from pathlib import Path
import json, hashlib, sys
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent.parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def make():
    manifest=json.loads((ROOT/'manifest.json').read_text())
    original={name:{'expected':value,'actual':sha(BASE/name),'unchanged':sha(BASE/name)==value} for name,value in manifest['source_files'].items()}
    files={str(p.relative_to(ROOT)):sha(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='receipt.json'}
    return {'scope':'Bounded NumPy acceleration of unchanged supplied six-species seven-reaction thermal model. No BVP, new mechanism, geometry change, or parameter sweep.',
            'source_preservation':original,'source_files_unchanged':all(v['unchanged'] for v in original.values()),
            'cache_sha256_matches_manifest':sha(ROOT/'cache.npz')==manifest['cache_sha256'],
            'files_sha256':files,'construction_and_rounding':'Source NASA coefficients and molecular weights exported as float64 with no new decimal rounding. Original explicit kinetics evaluated in log domain. Transport is a source-pinned cubic-log table approximation; see manifest and validation for measured error/domain.',
            'limitations':'Sampled numerical cross-check and measured same-batch timing only, no universal certificate or end-to-end solver guarantee. NASA source splice discontinuity and initial validation failures retained.'}
if __name__=='__main__':
    r=make()
    if '--verify' in sys.argv:
        old=json.loads((ROOT/'receipt.json').read_text())
        ok=r==old and r['source_files_unchanged'] and r['cache_sha256_matches_manifest']
        print(json.dumps({'receipt_matches':ok,'source_files_unchanged':r['source_files_unchanged'],'cache_matches':r['cache_sha256_matches_manifest']},indent=2))
        raise SystemExit(0 if ok else 1)
    (ROOT/'receipt.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='files_sha256'},indent=2))
