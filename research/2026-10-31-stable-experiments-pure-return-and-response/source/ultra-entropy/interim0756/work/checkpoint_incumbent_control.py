#!/usr/bin/env python3
"""Extend the same-source comparison to the previous current and LP witnesses.

Read-only reuse of the fresh records; no new sample acquisition. The free
parameter envelopes are optimistic upper comparators, not valid inference.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
import math
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'outputs/entropy_witnesses'
sys.path.insert(0,str(HERE))
sys.path.insert(0,str(ROOT/'outputs/reversible_currents'))
from checkpoint_band import checkpoints
from entropy_cone import log_bounds,exponential_bounds
from ctmc_reflection_control import exp_negative_bounds,dyadic_enclose
from dual_trace import load_certificate


def one_step_intervals():
    m=16;mu=Q(44,9);distribution=[Q(i==0) for i in range(m)]
    term=Q(1);mass=Q(0);S=[Q(0)]*m
    for k in range(101):
        for x in range(m):S[x]+=term*distribution[x]
        mass+=term
        nxt=[Q(0)]*m
        for x,p in enumerate(distribution):
            nxt[(x+1)%m]+=Q(10,11)*p
            nxt[(x-1)%m]+=Q(1,11)*p
        distribution=nxt;term*=mu/(k+1)
    elo,ehi=exp_negative_bounds(mu);tail=1-elo*mass
    return [dyadic_enclose(elo*s,ehi*s+tail) for s in S]


def multiply(a,b):
    candidates=[x*y for x in a for y in b]
    return min(candidates),max(candidates)


def alternating_current_source_tail():
    m=16;f=[1]*8+[-1]*8;P=one_step_intervals();h=[]
    for x in range(m):
        terms=[multiply(P[j],(Q(f[x]*f[(x+j)%m]),)*2) for j in range(m)]
        h.append(dyadic_enclose(sum(a for a,b in terms),sum(b for a,b in terms)))
    meanlo=sum(a for a,b in h)/m;meanhi=sum(b for a,b in h)/m
    assert max(abs(meanlo),abs(meanhi))<Q(1,50)
    g=[(a-meanhi,b-meanlo) for a,b in h]
    variance=sum(max(abs(a),abs(b))**2 for a,b in g)/m
    assert variance<Q(25,64)
    assert all(h[x]==h[x+8] for x in range(8))
    # V=(I+P)^(-1)(h-mean), via alternating Neumann terms and the
    # already-proved contraction1/4 on the mean-zero8-periodic subspace.
    V=[(Q(0),Q(0)) for _ in range(m)];power=g;order=12
    for k in range(order):
        for x in range(m):
            term=power[x] if k%2==0 else (-power[x][1],-power[x][0])
            V[x]=dyadic_enclose(V[x][0]+term[0],V[x][1]+term[1])
        nxt=[]
        for x in range(m):
            terms=[multiply(P[(y-x)%m],power[y]) for y in range(m)]
            nxt.append(dyadic_enclose(sum(a for a,b in terms),sum(b for a,b in terms)))
        power=nxt
    remainder=Q(10,3*4**order)
    V=[dyadic_enclose(a-remainder,b+remainder) for a,b in V]
    oscillation=max(b for a,b in V)-min(a for a,b in V)
    sup=max(max(abs(a),abs(b)) for a,b in V)
    assert 1+oscillation/2<Q(9,4)
    assert 2*sup+Q(1,50)<Q(5,2)
    return {'one_step_h_mean_interval':[str(meanlo),str(meanhi)],
            'h_variance_upper':str(variance),'h_variance_preview':float(variance),
            'alternating_Poisson_potential_intervals':[[str(a),str(b)] for a,b in V],
            'potential_oscillation_upper':str(oscillation),
            'potential_oscillation_preview':float(oscillation),
            'boundary_upper':'5/2','subGaussian_constant_upper':'9/4',
            'two_sided_current_tail':'2exp(-((s-5/2)_+)^2/((81/8)N))',
            'source_constants_supplied_to_inference':False}


def points_through(Ncap):
    result=[]
    for j,N in checkpoints():
        if N>Ncap:break
        result.append((j,N))
    return result


def power_bound(points,target=1000):
    elllo=log_bounds(Q(640),96)[0]
    assert elllo>6
    assert 256*log_bounds(Q(128,3),96)[1]<target
    later=[]
    for j,N in points:
        if N<=256:continue
        # phi(r)<=2r^2/(1-r^2) forces this current magnitude.
        threshold_squared=Q(target*N*N,2*N+target)
        scale=2**48
        root=math.isqrt((threshold_squared*scale*scale).numerator//
                        (threshold_squared*scale*scale).denominator)
        rootlo=Q(root,scale)
        deviation=rootlo-Q(5,2)
        assert deviation>0
        exponent=deviation*deviation/(Q(81,8)*N)
        assert exponent>17
        later.append((j,N,exponent))
    failure_current=2*len(later)*exponential_bounds(Q(-17),100)[1]
    failure_reflection=len(points)*exponential_bounds(Q(-14),100)[1]
    combined=failure_current+failure_reflection
    assert combined<Q(1,10000)
    return {'target_nats':target,'cap_transitions':points[-1][1],
            'early_current_crossings_impossible_through':256,
            'later_current_checkpoints':len(later),'later_current_tail_exponent_lower':'17',
            'free_current_crossing_probability_upper_preview':float(failure_current),
            'free_reflection_crossing_probability_upper_preview':float(failure_reflection),
            'union_crossing_probability_upper_preview':float(combined),
            'union_crossing_probability_upper_dyadic':str(dyadic_enclose(Q(0),combined,96)[1])}


def replays(points,cert):
    word=dict(zip(cert['words'],cert['H']))
    A=Q(1,128);B=-Q(3,1184);D=Q(1,8)
    for w,value in word.items():
        signs=[1 if y==0 else -1 for y in w]
        assert value==A+B*(signs[0]*signs[1]+signs[1]*signs[2])+D*signs[0]*signs[2]
    assert A+2*B>0 and cert['C']>=Q(1,4)
    out=[]
    for name in ('checkpoint_driven_ring','checkpoint_reversible_ring'):
        record=json.loads((HERE/(name+'_record.json')).read_text())
        current=0;T=Q(0);lag=0;lookup={N:j for j,N in points};best_current=None;best_dual=None
        current_cross=None;dual_cross=None
        for N in range(1,len(record)):
            current+=(1 if record[N-1]==record[N] else -1)*(-1 if (N-1)%2 else 1)
            if N>=2:
                T+=word[tuple(record[N-2:N+1])]
                lag+=1 if record[N-2]==record[N] else -1
            if N not in lookup:continue
            j=lookup[N];allocation=Q(1,320*j*(j+1));loglo,loghi=log_bounds(allocation,96)
            r=Q(abs(current),N)
            if r==1:
                # logcosh(lambda*S)-N logcosh(lambda)<=(N-1)log2.
                assert (N-1)*log_bounds(Q(2),96)[1]+loghi<0
                current_upper=Q(0)
            else:
                current_upper=N*r*log_bounds((1+r)/(1-r),96)[1]+3*loghi
            excess=max(Q(0),-T-cert['R']/2)
            dual_upper=excess*excess/((N-1)*cert['C']**2)+3*loghi
            reflection_upper=Q(max(0,-lag)**2,4*(N-1))+3*loghi
            assert dual_upper<=reflection_upper
            if best_current is None or current_upper>best_current:best_current=current_upper
            if best_dual is None or dual_upper>best_dual:best_dual=dual_upper
            if current_upper>=1000 and current_cross is None:current_cross=N
            if dual_upper>=1000 and dual_cross is None:dual_cross=N
        out.append({'name':name,'free_all_theta_lambda_current_upper_preview':float(best_current),
                    'free_current_1000_crossing':current_cross,
                    'free_all_lambda_compiled_dual_upper_preview':float(best_dual),
                    'free_dual_1000_crossing':dual_cross,
                    'compiled_dual_pointwise_dominated_by_free_reflection':True,
                    'scope':'optimistic envelopes on existing fresh records, not new valid inference or independent acquisitions'})
    return out


def main():
    start=time.perf_counter();points=points_through(16384)
    source=alternating_current_source_tail();power=power_bound(points)
    cert=load_certificate(ROOT/'outputs/reversible_currents/symmetric_dual.json')
    replay=replays(points,cert)
    output={'scope':__doc__,'alternating_current_source_tail':source,
            'source_specific_broader_comparison':power,'existing_record_replays':replay,
            'exact_compiled_reversible_columns_rechecked':cert['columns_checked'],
            'new_acquisitions':0,'status':'PREVIOUS_CURRENT_AND_LP_COMPARATORS_CHECKED',
            'scope_limit':'specified earlier families only, not all ordinary methods; power uses source constants only in validation',
            'seconds':time.perf_counter()-start}
    (HERE/'incumbent_receipt.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':output['status'],'power':power,'replays':replay,
                      'seconds':output['seconds']},indent=2))


if __name__=='__main__':main()
