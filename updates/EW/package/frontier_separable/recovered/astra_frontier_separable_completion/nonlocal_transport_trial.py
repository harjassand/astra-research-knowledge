"""Small fully nonlocal certificate of the ORIGINAL interacting quantum model.
This demonstrates algebra/solve/verification closure, not competitive precision.
"""

if not __debug__:
    raise RuntimeError('Do not run with Python -O: certificate checks must execute.')
import gap_algebra as g
from gap_algebra import F,geo,atom
from pressure_basis import solve
from fractions import Fraction
from pathlib import Path
import numpy as np,json,time,resource

def linear_combo(basis,c):return g.add(*[(cc,v) for v,cc in zip(basis,c)])
def run():
    start=time.perf_counter();d=F(2);dens=(((0,1),F(1)),((0,2),F(1,4)));J=g.current()
    fb=[J]
    for q,ref in [(F(0),F(0)),(F(0),F(1,2)),(F(1,2),F(1,2))]:
        raw={atom((3,1,1,3),(geo(q),geo(0),geo(q))):F(-1,2),
             atom((3,2,2,3),(geo(q),geo(0),geo(q))):F(-1,2)}
        ff=g.balance(raw,reference=ref)
        if g.inner(ff,ff):fb.append(ff)
    Af=[g.apply(v,densities=dens) for v in fb]
    gb=[g.damping(Af[0],d,-1)]
    # Add local even response pieces and a genuinely infinite diagonal pressure.
    for a,c in Af[0].items():gb.append({a:F(1)})
    gb.append({atom((3,3,3),(geo(0),geo(F(1,2)))):F(1),
               atom((3,3,3),(geo(F(1,2)),geo(0))):F(-1)})
    # Remove algebraic duplicates through a numerical eigensolve; exact verification
    # does not trust that decision or a singular-value tolerance.
    Ag=[g.apply(v,densities=dens) for v in gb]
    A=[[g.inner(u,g.damping(v,d))+g.inner(au,g.damping(av,d,-1))
         for v,av in zip(fb,Af)] for u,au in zip(fb,Af)]
    a=[g.inner(J,u) for u in fb]
    B=[[g.inner(au,g.damping(av,d,-1))+g.inner(u,g.damping(v,d))
         for v,av in zip(gb,Ag)] for u,au in zip(gb,Ag)]
    b=[g.inner(J,g.damping(av,d,-1)) for av in Ag]
    x,_,_=solve(np.array(A,float),np.array(a,float));y,_,_=solve(np.array(B,float),np.array(b,float))
    Q=2**44;xr=[F(int(round(xx*Q)),Q) for xx in x];yr=[F(int(round(yy*Q)),Q) for yy in y]
    f=linear_combo(fb,xr);gg=linear_combo(gb,yr)
    lo,hi,meta=g.certificate(f,gg,densities=dens)
    record=dict(lower=str(lo),upper=str(hi),lower_float=float(lo),upper_float=float(hi),
       coefficients_f=list(map(str,xr)),coefficients_g=list(map(str,yr)),
       f_basis=len(fb),g_basis=len(gb),has_infinite_tail=any(q for (ty,gs) in f for a,q in gs),
       seconds=time.perf_counter()-start,peak_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
       model={'t':1,'U':4,'V':1,'d':2},scope='Broad exact D interval; pipeline demonstration, NOT a precision improvement',
       **meta)
    return record
if __name__=='__main__':
    out=run();Path('nonlocal_transport_trial.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
