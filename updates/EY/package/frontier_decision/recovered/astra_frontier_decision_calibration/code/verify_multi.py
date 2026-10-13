"""Reconstruct saved multivariate certificates without numerical optimization."""
from pathlib import Path
import hashlib,json,time,resource
import numpy as np
from multi_certificate import compile_exact
ROOT=Path(__file__).resolve().parent.parent

def verify(path):
    path=Path(path); old=json.loads(path.read_text()); wp=path.with_suffix('.npz')
    assert hashlib.sha256(wp.read_bytes()).hexdigest()==old['witness_sha256']
    with np.load(wp,allow_pickle=False) as data:
        fw=[tuple(map(int,w)) for w in data['fw']];gw=[tuple(map(int,w)) for w in data['gw']]
        inds=[tuple(map(int,w)) for w in data['indices']]
        pars=dict(zip(['t','U','V','d'],map(str,data['params'])))
        new=compile_exact(fw,gw,data['FN'],data['GN'],int(data['den'][0]),inds,pars)
    for k,v in new.items():
        if k not in ('verification_seconds','peak_rss_KiB'):assert old[k]==v, (str(path),k)
    return dict(file=str(path.relative_to(ROOT)),seconds=new['verification_seconds'],sha256=old['witness_sha256'],all_exact_fields_match=True)
if __name__=='__main__':
    start=time.perf_counter();paths=[ROOT/'results/main_multi_exact.json']+sorted((ROOT/'results/anchors').glob('*_exact.json'))
    records=[verify(p) for p in paths]
    out=dict(records=records,seconds=time.perf_counter()-start,peak_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Reconstruction by a separately invoked checker from the same investigation; not external scientific review.')
    (ROOT/'results/standalone_verification.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
