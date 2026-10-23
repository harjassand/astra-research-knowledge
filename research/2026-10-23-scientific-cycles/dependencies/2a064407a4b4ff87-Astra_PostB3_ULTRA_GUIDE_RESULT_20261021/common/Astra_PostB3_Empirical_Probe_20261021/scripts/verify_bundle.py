"""Portable integrity check, not scientific validation of the assay or result."""
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parent.parent
PINNED_DATA='5da0485aed81b23bda57b4a7b4510a394682d54911416db89b4846ff6dd34732'
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
    return h.hexdigest()
def main():
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    checked=0
    for row in manifest['files']:
        rel=Path(row['path'])
        if rel.is_absolute() or '..' in rel.parts:raise ValueError('Unsafe relative path')
        p=ROOT/rel
        if p.stat().st_size!=row['bytes'] or digest(p)!=row['sha256']:
            raise ValueError('Integrity mismatch: '+str(rel))
        checked+=1
    if digest(ROOT/'data/WesselsSatija2023.h5ad')!=PINNED_DATA:
        raise ValueError('Independent input pin failed')
    print(json.dumps({'status':'PASS','files_checked':checked,
                      'scope':'File integrity and pinned input only; not scientific acceptance'}))
if __name__=='__main__':main()
