#!/usr/bin/env python3
"""Exact passive equivalence and enclosed finite closed-cycle work signs.

Floating vectors propose periodic states only. A Doeblin contraction plus
the enclosed full-period residual bounds the true periodic-state error.
The positive uniformization sum rounds every vector at fixed precision;
all resulting total-variation and truncation errors are charged.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs/interventional_generator'
sys.path.insert(0,str(ROOT/'work'));sys.path.insert(0,str(ROOT/'outputs/coherent_generator'))
from coherent_generator_control import identity,mm
from ctmc_reflection_control import exp_negative_bounds,dyadic_enclose
from kinetic import log_bounds


def controlled(q,f,t):
    n=len(q);z=[[F(0)]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i!=j:z[i][j]=q[i][j]*t**((f[j]-f[i])//2)
        z[i][i]=-sum(z[i])
    return z


def floor(x):return x.numerator//x.denominator
def ceil(x):return -((-x.numerator)//x.denominator)


def round_counts(weights,scale):
    assert sum(weights)==scale
    out=[floor(x) for x in weights];left=scale-sum(out)
    assert 0<=left<len(out)
    rank=sorted(range(len(out)),key=lambda j:weights[j]-out[j],reverse=True)
    for j in rank[:left]:out[j]+=1
    assert min(out)>=0 and sum(out)==scale
    return out


def kernel_step(counts,q,dt,bits=96,order=80):
    n=len(q);scale=2**bits;cap=ceil(max(-q[i][i] for i in range(n)));I=identity(n)
    P=[[I[i][j]+q[i][j]/cap for j in range(n)] for i in range(n)]
    assert all(x>=0 for row in P for x in row) and all(sum(row)==1 for row in P)
    x=cap*dt;el,eu=exp_negative_bounds(x,160);el=F(floor(el*scale),scale)
    assert el>0
    current=list(counts);weight=F(1);sums=[F(0)]*n;mass=F(0)
    for k in range(order+1):
        a=el*weight;mass+=a
        sums=[z+a*v for z,v in zip(sums,current)]
        if k<order:
            raw=[sum(counts_i*P[i][j] for i,counts_i in enumerate(current)) for j in range(n)]
            current=round_counts(raw,scale)
        weight*=x/(k+1)
    missing=1-mass;assert 0<=missing<1
    out=round_counts([z+missing*v for z,v in zip(sums,counts)],scale)
    # k rounded P steps cost <=k*n/(2*scale); the output rounding costs
    # another n/(2*scale). Sum k*a_k<=x; missing mass costs <=missing.
    error=missing+(x+1)*F(n,2*scale)
    return out,error,{'uniformization_rate':cap,'mean_virtual_events':str(x),'P_updates':order,
                      'TV_rounding_and_truncation_upper':str(error)}


def interval_product(a,b):return min(x*y for x in a for y in b),max(x*y for x in a for y in b)


def certify(q,f,ratios,dt,candidate):
    n=len(q);bits=96;scale=2**bits;raw=list(map(F,candidate));total=sum(raw)
    counts=round_counts([x*scale/total for x in raw],scale);initial=list(counts)
    qs=[controlled(q,f,t) for t in ratios];means=[];prefix_errors=[];error=F(0);cost=[]
    for z in qs:
        means.append(F(sum(v*a for v,a in zip(counts,f)),scale));prefix_errors.append(error)
        counts,e,c=kernel_step(counts,z,dt,bits);error+=e;cost.append(c)
    residual=F(sum(abs(a-b) for a,b in zip(counts,initial)),2*scale)+error
    refresh=n*min(z[i][j] for z in qs for i in range(n) for j in range(n) if i!=j)
    assert refresh>0
    cl,cu=exp_negative_bounds(refresh*dt*len(qs),160)
    _,cu=dyadic_enclose(cl,cu,96);assert 0<=cu<1
    initial_radius=residual/(1-cu)
    logs=[log_bounds(t,64) for t in ratios];wl=wu=F(0)
    for k,(mean,e) in enumerate(zip(means,prefix_errors)):
        dlo=logs[k][0]-logs[k-1][1];dhi=logs[k][1]-logs[k-1][0]
        radius=2*(initial_radius+e)
        lo,hi=interval_product((-dhi,-dlo),(max(F(-1),mean-radius),min(F(1),mean+radius)))
        wl+=lo;wu+=hi
    wl,wu=dyadic_enclose(wl,wu,80)
    # Fixed edge chemical affinity A_ij=log(q_ij/q_ji); q^h obeys
    # local detailed balance with energy U_h=-log(t)*f.
    affinity=[[None]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i!=j:affinity[i][j]=log_bounds(q[i][j]/q[j][i],64)
    fuel_low=fuel_high=F(0)
    for z in qs:
        state_l=[];state_u=[]
        for i in range(n):
            state_l.append(sum(z[i][j]*affinity[i][j][0] for j in range(n) if j!=i))
            state_u.append(sum(z[i][j]*affinity[i][j][1] for j in range(n) if j!=i))
        fuel_low+=dt*min(state_l);fuel_high+=dt*max(state_u)
    fuel_low,fuel_high=dyadic_enclose(fuel_low,fuel_high,80)
    assert fuel_low>0 and fuel_low+wl>0
    efficiency_upper=max(F(0),-wl)/fuel_low
    return {'cyclic_work_on_interval':[str(wl),str(wu)],'cyclic_work_on_preview':[float(wl),float(wu)],
            'sign':'absorbs work' if wl>0 else 'extracts work' if wu<0 else 'inconclusive',
            'period':str(dt*len(qs)),'periodic_state_TV_radius':float(initial_radius),
            'period_map_residual_TV_upper':float(residual),'Doeblin_refresh_lower':str(refresh),
            'period_map_TV_contraction_upper':float(cu),
            'chemical_fuel_input_interval':[str(fuel_low),str(fuel_high)],
            'chemical_fuel_input_preview':[float(fuel_low),float(fuel_high)],
            'total_cycle_entropy_lower':float(fuel_low+wl),
            'ideal_output_to_chemical_input_ratio_upper':float(efficiency_upper),
            'vector_precision_bits':bits,'per_segment_cost':cost,
            'controller_losses':'unacquired; useful net-device work not established'}


def main():
    start=time.perf_counter();path=OUT/'retuned_receipt.json';data=json.loads(path.read_text())
    q=[[F(x) for x in row] for row in data['Q']];other=[[F(x) for x in row] for row in data['Q_gauge']]
    S=[[F(x) for x in row] for row in data['S']];pi=list(map(F,data['stationary_pi']));f=data['labels'];n=len(q)
    assert all(sum(row)==1 for row in S)
    assert all(S[i][j]==0 for i in range(n) for j in range(n) if f[i]!=f[j])
    assert mm(q,S)==mm(S,other)
    assert [sum(pi[i]*S[i][j] for i in range(n)) for j in range(n)]==pi
    for z in (q,other):
        assert all(sum(row)==0 for row in z)
        assert all(z[i][j]>0 for i in range(n) for j in range(n) if i!=j)
        assert all(sum(pi[i]*z[i][j] for i in range(n))==0 for j in range(n))
    ratios=list(map(F,data['field_multipliers']));dt=F(data['step_duration']);out=[]
    for name,z in [('source',q),('passive_equivalent',other)]:
        result=certify(z,f,ratios,dt,data[name]['periodic_initial']);result['name']=name;out.append(result)
    assert out[0]['sign']=='absorbs work' and out[1]['sign']=='extracts work'
    result={'status':'PASSIVE_EQUIVALENCE_OPPOSITE_CYCLIC_WORK_CERTIFIED',
            'all_timed_passive_word_laws_equal':'exact intertwining, projector commutation and initial-state identities',
            'same_calibrated_protocol':True,'field_law':'q_t(i,j)=q(i,j)*t^((f_j-f_i)/2)',
            'records':out,'new_acquisitions':0,'physical_experiments':0,
            'proposal_SHA256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'receiver_correction_preserved':'initial run rejected accidental int/int float in label mean; replaced by exact Fraction before certification',
            'elapsed_wall_seconds':time.perf_counter()-start,
            'scope':'finite rational reciprocal CTMC construction; conditional thermodynamic model, no hardware advantage'}
    (OUT/'work_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}|{'records':[
        {k:v for k,v in r.items() if k!='per_segment_cost'} for r in out]},indent=2))


if __name__=='__main__':main()
