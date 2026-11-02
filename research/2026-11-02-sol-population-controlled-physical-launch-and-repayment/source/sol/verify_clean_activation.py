#!/usr/bin/env python3
"""Exact finite-rate core activation, retaining all noncore interruptions."""
from fractions import Fraction as F
from math import factorial,ceil
from pathlib import Path
import json
from conservative_fiber_kernel import tridiagonal,raw_network,falling

P=Path(__file__).resolve().parent

def run(n,A,D):
    # Base residuals 0,0,n,n, plus the ACTUAL normal packets at A,D.
    Y=((0,0,0),(1,1,0),(2,1,1),(3,2,2))
    x=(A,Y[A][1],Y[A][2],D,n+Y[D][1],n+Y[D][2])
    states=[];weights=[];w=F(1)
    for j in range(min(x[4],x[5])//2+1):
        v=(A,x[1]+2*j,x[2]+2*j,D,x[4]-2*j,x[5]-2*j)
        if j:
            prev=states[-1]
            up=A*D*falling(prev[4:6],(2,2))
            down=2*A*D*falling(v[1:3],(2,2))
            w*=F(up,down)
        states.append(v);weights.append(w)
    mode=max(range(len(states)),key=lambda j:weights[j])
    target=max(1,mode-max(1,ceil(F(n,100))))
    # Keep only the cold side before a fixed narrow interior band.
    kept=states[:target];raw=raw_network();lower=[];diag=[];upper=[];haz=[];upall=[]
    for j,v in enumerate(kept):
        up=F(A*D*falling(v[4:6],(2,2)))
        down=F(2*A*D*falling(v[1:3],(2,2)))
        h=[k*falling(v,s) for s,u,k in raw[:8]]
        assert sum(h)>0
        lower.append(-down if j else F(0));upper.append(-up if j+1<target else F(0))
        diag.append(up+down+sum(h));haz.append(h);upall.append(up)
    rhs=[F(1)]*target
    t=tridiagonal(lower,diag,upper,rhs)
    r=[F(0)]*target;r[-1]=upall[-1]
    success=tridiagonal(lower,diag,upper,r)
    interrupt=[]
    for channel in range(8):interrupt.append(tridiagonal(lower,diag,upper,[v[channel] for v in haz])[0])
    assert success[0]+sum(interrupt)==1
    # All genuine interrupting channels at these clean phases are Z-neutral or repaying.
    m=lambda a:(0,2,4)[a] if a<3 else 7
    Z=lambda v:15+sum(v)-m(v[0])-m(v[3])
    for v,h in zip(kept,haz):
        for c,rate in enumerate(h):
            if rate:
                s,u,_=raw[c];out=tuple(a-b+d for a,b,d in zip(v,s,u))
                assert Z(out)<=Z(v)
    return {'n':n,'anchors':[A,D],'cold_start':x,'core_band_target':states[target],
            'transient_core_states':target,'actual_time_exact':str(t[0]),
            'actual_success_probability_exact':str(success[0]),
            'all_eight_interrupt_probabilities_exact':list(map(str,interrupt)),
            'time_times_n_cubed':float(t[0]*n**3),
            'interruption_times_n':float((1-success[0])*n)}

def main():
    rows=[run(n,A,D) for n in (10,30,100) for A,D in ((1,1),(2,1),(1,2))]
    (P/'results/clean_activation_checks.json').write_text(json.dumps({'exact_cases':rows,
        'scope':'Exact finite-rate killed core law with every noncore interruption. Uniform asymptotics are proved in the source notes.'},indent=2)+'\n')
    print(json.dumps([{'n':v['n'],'anchors':v['anchors'],'states':v['transient_core_states'],
         'N3_time':v['time_times_n_cubed'],'N_interruption':v['interruption_times_n']} for v in rows],indent=2))

if __name__=='__main__':main()
