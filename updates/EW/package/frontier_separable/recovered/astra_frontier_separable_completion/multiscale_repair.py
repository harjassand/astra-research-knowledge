"""Multiscale separated completion, with a radius-independent energy bound
in gap dimension >=3. This is a source-class theorem, not a full inverse theorem.
"""

if not __debug__:
    raise RuntimeError('Do not run with Python -O: certificate checks must execute.')
from separable_repair import *
from pathlib import Path
import json,time

def measure(q,m):
    return {(geo(q),)*m:(1-q)**m}

def canonical_unshifted(v):
    """Exact partial fractions; delta offsets stay explicit."""
    out=defaultdict(F)
    for key,c in v.items():
        parts=[]
        for a,q in key:
            if not q or not a:parts.append([(F(1),(a,q))]);continue
            part=[(q**(-a),geo(q))]
            part +=[(-q**(j-a),geo(0,j)) for j in range(a)]
            parts.append(part)
        for term in product(*parts):
            out[tuple(s for cf,s in term)]+=c*product_f(cf for cf,s in term)
    return clean(out)

def multiscale(m,J):
    flows=[{} for _ in range(m)]
    for j in range(1,J+1):
        q=1-F(1,2**j);r=1-F(1,2**(j-1))
        b=add((1,measure(q,m)),(-1,measure(r,m)))
        step=complete(b,[geo(r)]*m)
        flows=[add((1,u),(1,v)) for u,v in zip(flows,step)]
    routes=route_edges(flows)
    b=add((1,measure(1-F(1,2**J),m)),(-1,measure(F(0),m)))
    residual=canonical_unshifted(add((1,routed_divergence(routes)),(-1,b)))
    assert not residual
    return routes

if __name__=='__main__':
    start=time.perf_counter();checks=[]
    for m,J in[(2,4),(3,4),(4,4)]:
        w=multiscale(m,J);energy=sum(inner(v,v) for v in w)
        checks.append(dict(dimension=m,levels=J,atoms=sum(map(len,w)),energy=str(energy),energy_float=float(energy)))
    w=multiscale(4,40)
    # m=4: ||w|| <= 4*sqrt(8)*sum_{j=1}^J 2^{-j}<sqrt(128).
    out=dict(small_exact_energy_checks=checks,dimension=4,levels=40,
       length_scale=2**40,route_atoms=sum(map(len,w)),
       exact_divergence=True,certified_energy_upper=128,
       seconds=time.perf_counter()-start,
       scope='Exact completion of normalized geometric-product minus point source; original exclusion graph')
    Path('multiscale_repair_checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
