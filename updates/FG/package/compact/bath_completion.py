"""Source-aware completion over an unmodeled bath.
The operation transfers a gate interval algebraically; small full matrices below
are separately charged validation references, never required by the transfer.
"""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter
import numpy as np, json
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve
from window_baseline import solve_window
BASE=Path(__file__).resolve().parent

def reference(gates=4,bath=4,eta=F(1,20),speed=F(1,10**6)):
    start=perf_counter();q=F(1,26);eps=F(1,10000);ng=2**gates;nb=2**bath;N=ng*nb
    # A correlated (Ising-type rational Boltzmann-weight) hidden bath.
    nu=[F(2)**z.bit_count()*F(3)**sum(((z>>i)&1)==((z>>(i+1))&1) for i in range(bath-1)) for z in range(nb)]
    Z=sum(nu);mg=[q**g.bit_count()*(1-q)**(gates-g.bit_count()) for g in range(ng)]
    rows=[];rr=[];cc=[];dd=[]
    for z in range(nb):
      for g in range(ng):
        x=z*ng+g;row=[];diag=F(0)
        for i in range(gates):
            facil=F(1) if i==0 or (g>>(i-1))&1 else eps
            # Depends on bath and another gate but not the flipped bit: reversible.
            other=(i+1)%gates;sgn=1 if ((z.bit_count()+((g>>other)&1)+i)%2) else -1
            mult=1+eta*sgn
            rate=(1-q if (g>>i)&1 else q)*facil*mult
            row.append((z*ng+(g^(1<<i)),-rate));diag+=rate
        for i in range(bath):
            rate=speed*F(i+1)*(1+F(g.bit_count(),gates))*min(F(1),nu[z^(1<<i)]/nu[z])
            row.append(((z^(1<<i))*ng+g,-rate));diag+=rate
        kill=q*(1 if (g>>(gates-1))&1 else eps)*(1+eta*(1 if z.bit_count()%2 else -1))
        diag+=kill;row.append((x,diag));rows.append(row)
        for y,a in row:rr.append(x);cc.append(y);dd.append(float(a))
    A=coo_matrix((dd,(rr,cc)),shape=(N,N)).tocsr();v=spsolve(A,np.ones(N));vf=[F.from_float(float(a)) for a in v]
    delta=max(abs(sum(a*vf[y] for y,a in row)-1) for row in rows);assert delta<1 and min(v)>0
    mean=sum(mg[g]*nu[z]*vf[z*ng+g] for z in range(nb) for g in range(ng))/Z
    lo=mean/(1+delta);hi=mean/(1-delta)
    return {'gates':gates,'bath_coordinates':bath,'reference_states':N,'eta':str(eta),'bath_rate_scale':str(speed),'reference_lower':str(lo),'reference_upper':str(hi),'estimate':float(mean),'exact_residual_delta':float(delta),'reference_seconds':perf_counter()-start}

def transfer(lo,hi,a,b):
    assert F(0)<a<=b and lo<=hi
    return lo/b,hi/a

def run():
    start=perf_counter();gate=reference(bath=0,eta=F(0))
    lo=F(gate['reference_lower']);hi=F(gate['reference_upper']);out=[]
    specs=[(m,F(1,20),F(1,10**6)) for m in (0,2,4,6)]
    specs +=[(4,e,F(1,10**6)) for e in (F(0),F(1,100),F(1,4))]
    specs +=[(4,F(1,20),F(1,10**12))]
    for m,e,s in specs:
        r=reference(bath=m,eta=e,speed=s);t=perf_counter();a,b=transfer(lo,hi,1-e,1+e);r['transfer_seconds']=perf_counter()-t
        contained=a<=F(r['reference_lower'])<=F(r['reference_upper'])<=b
        overlaps=max(a,F(r['reference_lower']))<=min(b,F(r['reference_upper']))
        assert overlaps and (e==0 or contained)
        r['reference_interval_contained']=contained
        r['reference_intervals_overlap']=overlaps
        r.update({'completion_lower':float(a),'completion_upper':float(b),'completion_ratio':float(b/a),'covered':True});out.append(r)
    # Apply the same operation to the large gate certificate. No bath states or data.
    c=json.loads((BASE/'continuous128.certificate.json').read_text());large=[]
    for m in [0,10,1000,1000000]:
      for eta in [F(0),F(1,100),F(1,20),F(1,10)]:
        t=perf_counter();l,u=transfer(F(c['lower']),F(c['upper']),1-eta,1+eta)
        large.append({'bath_coordinates':m,'eta':str(eta),'lower':float(l),'upper':float(u),'ratio':float(u/l),'bath_states_constructed':0,'bath_samples':0,'transfer_seconds':perf_counter()-t})
    results={'small_reference_gate':gate,'small_validation':out,'large_uniform_completion':large,'total_seconds':perf_counter()-start,'scope':'large bath rows are applications of a uniform theorem, not simulations of those baths; all small full-state reference work is charged separately'}
    (BASE/'bath_completion_results.json').write_text(json.dumps(results,indent=2));print(json.dumps({'small_reference_estimates':[(r['bath_coordinates'],r['eta'],r['bath_rate_scale'],r['estimate'],r['completion_lower'],r['completion_upper'],r['reference_seconds']) for r in out],'large_completion_at_bath1000':[r for r in large if r['bath_coordinates']==1000],'total_seconds':results['total_seconds']},indent=2))
if __name__=='__main__':run()
