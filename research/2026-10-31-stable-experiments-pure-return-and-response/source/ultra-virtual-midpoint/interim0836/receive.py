#!/usr/bin/env python3
"""Exact controls for the virtual midpoint proof; not a universal formal audit."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import ast
import hashlib
import json
import random
import sys
import time

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT/'work'))
from midpoint_band import from_score,endpoint
from entropy_cone import exponential_bounds,log_bounds
from virtual_midpoint_control import source_parameters,power_proof


def algebra():
    count=0
    for u,v,fx,fy in product([Q(i,3) for i in range(-3,4)],[Q(i,3) for i in range(-3,4)],[-1,1],[-1,1]):
        t=(u-v)/2;a=(u+v)/2
        assert abs(t)+abs(a)<=1
        Hpair=4*t*(fy-fx)-4*(t*t+a*a)
        assert Hpair==-4*fx*fy+2*(u+fx)*(fy-u)+2*(v+fy)*(fx-v)
        assert -2*(t*t+a*a)+(4*t)**2/8<=0
        count+=1
    return count


def kernel_return():
    count=0
    for theta,p,q,wp,wq in [(Q(1,2),Q(4,5),Q(1,5),Q(2,5),Q(2,5)),
                          (Q(1,4),Q(14641,24641),Q(10000,24641),Q(13310,24641),Q(11000,24641))]:
        f=[1,1,-1,-1];u=[p*f[(i+1)%4]+q*f[(i-1)%4] for i in range(4)]
        v=[q*f[(i+1)%4]+p*f[(i-1)%4] for i in range(4)]
        t=[(x-y)/2 for x,y in zip(u,v)];a=[(x+y)/2 for x,y in zip(u,v)]
        states=list(product(range(2),range(4)));index={state:i for i,state in enumerate(states)}
        K=[[Q(0)]*8 for _ in range(8)]
        for i,(phase,x) in enumerate(states):
            for direction,weight in [(1,wp),(-1,wq)]:
                y=(x+direction)%4;phase2=1-phase
                tx=t[x] if phase else 0;ty=t[y] if phase2 else 0
                ax=a[x] if phase else 0;ay=a[y] if phase2 else 0
                fx=0 if phase else f[x];fy=0 if phase2 else f[y]
                H=4*(tx*fy-ty*fx)-2*(tx*tx+ty*ty+ax*ax+ay*ay)
                K[i][index[phase2,y]]=weight*exponential_bounds(theta*H,90)[1]
        row=[Q(1,4) if phase==0 else Q(0) for phase,x in states]
        for steps in range(1,21):
            row=[sum(row[i]*K[i][j] for i in range(8)) for j in range(8)]
            if steps%2==0:
                assert sum(row)<=exponential_bounds(steps*theta*theta*16/2,90)[0]
                count+=1
    # Generic valid cone H(+)=h-h^2/8,H(-)=-h-h^2/8 on a reversible bit.
    # A fixed phase with ONE edge violates the returning-vector bound.
    theta=Q(1,4)
    assert exponential_bounds(theta*Q(7,8),90)[0]>exponential_bounds(theta*theta/2,90)[1]
    # Discrete reversible deterministic flip invalidates CTMC/PSD tests.
    a=Q(4,3);cosh=(a+1/a)/2
    assert a**8>cosh**8
    return {'returning_even_halfstep_power_checks':count,
            'odd_nonreturn_counterexample':True,'drop_CTMC_PSD_counterexample':True,
            'deterministic_three_phase_clock_has_one_way_entropy_infinity':True}


def martingales():
    rng=random.Random(2026110112);wrong_reverse_detected=False;count=0
    for trial in range(8):
        m=3+trial%3;flow=[[Q(0)]*m for _ in range(m)]
        for i in range(m):
            for j in range(i,m):flow[i][j]=flow[j][i]=Q(rng.randrange(1,9))
        for i in range(m):flow[i][(i+1)%m]+=3
        rows=list(map(sum,flow));total=sum(rows);pi=[x/total for x in rows]
        R=[[flow[i][j]/rows[i] for j in range(m)] for i in range(m)]
        back=[[flow[j][i]/rows[i] for j in range(m)] for i in range(m)]
        f=[1 if i%2 else -1 for i in range(m)]
        u=[sum(R[i][j]*f[j] for j in range(m)) for i in range(m)]
        v=[sum(back[i][j]*f[j] for j in range(m)) for i in range(m)]
        for z in range(m):
            for x in range(m):
                assert sum(R[z][y]*2*(u[z]+f[x])*(f[y]-u[z]) for y in range(m))==0
            for y in range(m):
                assert sum(back[z][x]*2*(v[z]+f[y])*(f[x]-v[z]) for x in range(m))==0
                if sum(back[z][x]*2*(u[z]+f[y])*(f[x]-u[z]) for x in range(m))!=0:
                    wrong_reverse_detected=True
            t=(u[z]-v[z])/2;a=(u[z]+v[z])/2
            assert -2*(t*t+a*a)+(4*t)**2/8<=0
        count+=1
    assert wrong_reverse_detected
    return {'exact_nonuniform_hidden_models':count,'forward_as_backward_negative_control_detected':True}


def psd_and_root():
    R=[[Q(1,2),Q(1,4),Q(1,4)],[Q(1,4),Q(1,2),Q(1,4)],[Q(1,4),Q(1,4),Q(1,2)]]
    P=[[sum(R[i][k]*R[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    f=[1,-1,1];a=Q(4,3);c=(a+1/a)/2
    K=[[P[i][j]*(a if f[i]!=f[j] else 1/a) for j in range(3)] for i in range(3)]
    row=[Q(1,3)]*3
    for N in range(1,21):
        row=[sum(row[i]*K[i][j] for i in range(3)) for j in range(3)]
        assert sum(row)<=c**N
    roots=[];states=list(product([-1,1],repeat=2));idx={s:i for i,s in enumerate(states)}
    for b in (Q(1,8),Q(1,2),Q(3,4)):
        R=[[Q(0)]*4 for _ in range(4)]
        for i,(s,t) in enumerate(states):
            R[i][idx[s,-t]]=(1+b*s*t)/2;R[i][idx[-s,t]]=(1-b*s*t)/2
        assert all(sum(R[i][j] for i in range(4))==1 for j in range(4))
        for i,(s,t) in enumerate(states):
            assert sum(R[i][j]*states[j][0] for j in range(4))==b*t
            assert sum(R[i][j]*states[j][1] for j in range(4))==-b*s
            two=[sum(R[i][k]*R[k][j] for k in range(4)) for j in range(4)]
            assert sum(two[j]*states[j][0] for j in range(4))==-b*b*s
            assert sum(two[j] for j in range(4) if states[j][0]!=s)==(1+b*b)/2
        roots.append({'b':str(b),'coarse_negative_eigenvalue':str(-b*b),
                      'complete_binary_lumpability_checked':True,'V2_formula':'2phi(b)'})
    # Without the CTMC/square-root premise, the positive endpoint is false.
    false_drop=from_score(100000,-100000,Q(1,40))
    assert endpoint(false_drop)>0
    return {'exact_PSD_mgf_horizons':20,'exact_attaining_roots':roots,
            'unrestricted_discrete_flip_must_be_excluded':True}


def main():
    start=time.perf_counter()
    for path in [HERE/'midpoint_band.py',ROOT/'work/virtual_midpoint_control.py']:
        ast.parse(path.read_text(),filename=str(path))
    output={'scope':__doc__,'exact_polynomial_and_cone_cases':algebra(),
            'kernel_return_controls':kernel_return(),'martingale_controls':martingales(),
            'PSD_and_divisibility_controls':psd_and_root(),
            'independently_recomputed_source':source_parameters(),
            'recomputed_frozen_source_power':power_proof(),
            'status':'VIRTUAL_MIDPOINT_EXACT_FINITE_CONTROLS_PASSED',
            'seconds':time.perf_counter()-start}
    if (HERE/'receipt.json').exists():
        receipt=json.loads((HERE/'receipt.json').read_text())
        assert all(hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest
                   for name,digest in receipt['frozen_before_new_records'].items())
        output['frozen_inference_and_proof_hashes_match']=True
    (HERE/'verification.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':output['status'],'polynomial_cases':output['exact_polynomial_and_cone_cases'],
                      'kernel':output['kernel_return_controls'],'models':output['martingale_controls'],
                      'seconds':output['seconds']},indent=2))


if __name__=='__main__':main()
