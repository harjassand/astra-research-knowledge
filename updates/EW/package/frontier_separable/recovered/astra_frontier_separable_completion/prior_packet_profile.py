"""Profile the *saved* prior successful certificate, without rerunning discovery.
Requires the mounted/extracted prior package. No uniform tail law is inferred.
"""

if not __debug__:
    raise RuntimeError('Do not run with Python -O: certificate checks must execute.')
from pathlib import Path
from collections import defaultdict
from fractions import Fraction as F
import sys,json,numpy as np,time
import argparse
_parser=argparse.ArgumentParser()
_parser.add_argument('--prior-package',type=Path,default=Path('/mnt/data/prior_thermo/astra_frontier_thermodynamic_certificate'))
ROOT=_parser.parse_args().prior_package
if not (ROOT/'benchmark_run/step8_exact.npz').exists():
    raise FileNotFoundError('Supply --prior-package pointing to the extracted earlier thermodynamic certificate package.')
sys.path.insert(0,str(ROOT))
from fast_algebra import build
from exact_certificate import integer_matrix,safe_dot

def degree(w):
    x,z=map(int,w);p=0;count=0
    for j in range((x|z).bit_length()-1,-1,-1):
        if x>>j&1:count+=1;p^=1
        elif ((z>>j)&1)^p:count+=2
    assert count%2==0
    return count//2

def run():
    start=time.perf_counter();cert=json.loads((ROOT/'benchmark_run/step8_certificate.json').read_text())
    dat=np.load(ROOT/'benchmark_run/step8_exact.npz',allow_pickle=False)
    fw=[tuple(map(int,w)) for w in dat['fw']];gw=[tuple(map(int,w)) for w in dat['gw']]
    fn,gn=dat['fn'],dat['gn'];den=int(dat['den'][0]);scale=2
    er,AF=build(fw,2.,8.,2.);orr,AG=build(gw,2.,8.,2.)
    af=safe_dot(integer_matrix(AF,1),fn);ag=safe_dot(integer_matrix(AG,1),gn)
    r1=defaultdict(int);r2=defaultdict(int)
    for w,c in zip(fw,fn):r1[w]+=scale*int(c)*w[0].bit_count()
    r1[(3,1)]+=scale*den//2
    for w,c in zip(orr,ag):r1[w]+=int(c)
    for w,c in zip(gw,gn):r2[w]+=scale*int(c)*w[0].bit_count()
    for w,c in zip(er,af):r2[w]+=int(c)
    hist=defaultdict(F)
    for rr in(r1,r2):
        for w,c in rr.items():
            if c:
                q=w[0].bit_count();assert q>0
                hist[degree(w)]+=F(8*c*c,q*(scale*den)**2)
    assert sum(hist.values())==F(cert['D_width_exact'])
    energy=defaultdict(F)
    for ws,cs in[(fw,fn),(gw,gn)]:
        for w,c in zip(ws,cs):energy[degree(w)]+=F(2*int(c)**2*w[0].bit_count(),den**2)
    out=dict(seconds=time.perf_counter()-start,prior_width=cert['D_width_exact'],
      dissipative_witness_energy_by_degree={str(k):float(v) for k,v in sorted(energy.items())},
      exact_gap_by_degree={str(k):str(v) for k,v in sorted(hist.items())},
      gap_by_degree={str(k):float(v) for k,v in sorted(hist.items())},
      max_f_degree=max(map(degree,fw)),max_g_degree=max(map(degree,gw)),
      scope='Profile of a supplied successful finite packet; not an exact-solution tail theorem')
    return out
if __name__=='__main__':
    out=run();Path('prior_packet_profile.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
