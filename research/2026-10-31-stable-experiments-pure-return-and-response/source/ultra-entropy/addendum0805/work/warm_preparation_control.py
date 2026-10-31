#!/usr/bin/env python3
"""Nonstationary boundary identities and fresh fixed-state CTMC controls."""
from fractions import Fraction as Q
from pathlib import Path
from itertools import product
import hashlib
import json
import sys
import time

ROOT=Path(__file__).resolve().parents[1];HERE=ROOT/'outputs/entropy_witnesses'
sys.path.insert(0,str(HERE))
from warm_preparation import evaluate
from checkpoint_band import evaluate as stationary_band,endpoint
from entropy_cone import log_bounds
from ctmc_reflection_control import CountedBits,ExactPoisson,exp_negative_bounds,dyadic_enclose


def decode(x):return Q(int(x['numerator']),int(x['denominator']))


def finite_boundary_controls():
    cases=[]
    P=[[Q(1,5) if i==j else Q(3,5) if j==(i+1)%3 else Q(1,5) for j in range(3)] for i in range(3)]
    cases.append((P,[Q(1,3)]*3,[Q(1,2),Q(1,3),Q(1,6)]))
    pi=[Q(1,2),Q(1,3),Q(1,6)];flow=[[Q(1,60)]*3 for _ in range(3)]
    for i in range(3):flow[i][i]=pi[i]-Q(1,30)
    cases.append(([[flow[i][j]/pi[i] for j in range(3)] for i in range(3)],pi,[Q(1,3)]*3))
    results=[]
    for P,pi,rho in cases:
        assert all(sum(P[i])==1 for i in range(3))
        assert all(sum(pi[i]*P[i][j] for i in range(3))==pi[j] for j in range(3))
        C=max(rho[i]/pi[i] for i in range(3));laws=[rho];count=negative=0
        for t in range(6):laws.append([sum(laws[-1][i]*P[i][j] for i in range(3)) for j in range(3)])
        assert all(max(law[i]/pi[i] for i in range(3))<=C for law in laws)
        for N in range(1,7):
            for path in product(range(3),repeat=N+1):
                forward=reverse=Q(1)
                for x,y in zip(path,path[1:]):forward*=P[x][y];reverse*=P[y][x]
                ref=pi[path[0]]*forward/(pi[path[-1]]*reverse)
                actual=rho[path[0]]*forward/(laws[N][path[-1]]*reverse)
                boundary=(rho[path[0]]/pi[path[0]])/(laws[N][path[-1]]/pi[path[-1]])
                assert actual==ref*boundary
                assert rho[path[0]]*forward<=C*pi[path[0]]*forward
                if actual<1:negative+=1
                count+=1
        # At time1, exp(-actual total entropy) is not conditionally a
        # supermartingale starting at1 for this nonstationary ensemble.
        conditional=[sum(laws[1][j]*P[j][i] for j in range(3))/rho[i] for i in range(3)]
        assert max(conditional)>1
        results.append({'density_ratio_bound':str(C),'hidden_paths_checked':count,
                        'negative_actual_entropy_paths':negative,
                        'max_conditional_actual_exponential_factor':str(max(conditional)),
                        'actual_entropy_exponential_not_assumed_martingale':True})
    record=[0,0,1,1,0,1,1,0,0,1]
    direct=stationary_band(record,Q(1,40));wrapped=evaluate(iter(record),1,Q(1,40))
    assert endpoint(direct)==endpoint(wrapped)
    return results


def sample_fixed_state(N,seed,p,q):
    bits=CountedBits(seed);poisson=ExactPoisson(Q(44,9));prob=p/(p+q)
    x=0;net=0;record=[0];nets=[0];minima=[];jumps=0
    for _ in range(N):
        number=poisson.draw(bits);jumps+=number;minimum=net
        for _ in range(number):
            direction=1 if bits.below(prob.denominator)<prob.numerator else -1
            x=(x+direction)%16;net+=direction;minimum=min(minimum,net)
        record.append(int(x>=8));nets.append(net);minima.append(minimum)
    return record,nets,minima,{'stationary_preparations':0,'fixed_state_preparations':1,
        'density_ratio_bound':16,'transitions':N,'observations':N+1,
        'model_duration':str(Q(4*N,9)),'hidden_jumps_simulated':jumps,
        'random_bits_generated':bits.bits,'exact_Poisson_draws':poisson.draws,
        'Poisson_interval_refinements':poisson.refinements}


def one_step(p,q):
    mu=Q(44,9);dist=[Q(i==0) for i in range(16)];term=Q(1);mass=Q(0);total=[Q(0)]*16
    for k in range(101):
        for x in range(16):total[x]+=term*dist[x]
        mass+=term
        nxt=[Q(0)]*16
        for x,v in enumerate(dist):nxt[(x+1)%16]+=p/(p+q)*v;nxt[(x-1)%16]+=q/(p+q)*v
        dist=nxt;term*=mu/(k+1)
    elo,ehi=exp_negative_bounds(mu);tail=1-elo*mass
    return [dyadic_enclose(elo*v,ehi*v+tail) for v in total]


def circular_convolve(a,b):
    result=[]
    for z in range(16):
        lo=sum(a[x][0]*b[(z-x)%16][0] for x in range(16))
        hi=sum(a[x][1]*b[(z-x)%16][1] for x in range(16))
        low,high=dyadic_enclose(lo,hi)
        result.append((max(Q(0),low),min(Q(1),high)))
    return result


def final_state_probability(N,net,p,q):
    power=one_step(p,q);law=[(Q(i==0),Q(i==0)) for i in range(16)];count=N
    while count:
        if count%2:law=circular_convolve(law,power)
        count//=2
        if count:power=circular_convolve(power,power)
    return law[net%16]


def check_path_lower_bound(band,nets,minima,ratio):
    # For delta_0 preparation at uniform pi, actual entropy is reference
    # entropy -log Pr_0(X_t), hence >=reference entropy at EVERY time.
    loglo,loghi=log_bounds(ratio)
    def ref_lower(net):return min(net*loglo,net*loghi)
    shift=decode(band['preparation_boundary_allowance'])
    lower=decode(band['stationary_reference_band']['baseline_lower_endpoint'])+shift
    history={p['transitions']:decode(p['actual_total_lower_endpoint']) for p in band['history']}
    unresolved=[]
    for N in range(1,len(nets)):
        if ref_lower(minima[N-1])<lower:unresolved.append((N,'between-grid'))
        if N in history:lower=history[N]
        if ref_lower(nets[N])<lower:unresolved.append((N,'checkpoint'))
    return unresolved


def main():
    start=time.perf_counter();finite=finite_boundary_controls();N=16384;each=Q(1,80)
    frozen={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in
            ('warm_preparation.py','WARM_PREPARATION.txt','checkpoint_band.py','quadratic_trace.py')}
    results=[]
    for name,p,q,seed in [('warm_driven_ring',Q(10),Q(1),2026110108),
                          ('warm_reversible_dynamics',Q(11,2),Q(11,2),2026110109)]:
        record,nets,minima,cost=sample_fixed_state(N,seed,p,q)
        (HERE/(name+'_record.json')).write_text(json.dumps(record)+'\n')
        band=evaluate(iter(record),16,each,keep_history=True,threshold=1000)
        unresolved=check_path_lower_bound(band,nets,minima,p/q)
        plo,phi=final_state_probability(N,nets[-1],p,q)
        assert 0<plo<=phi<=1
        rlo,rhi=log_bounds(p/q)
        reference_lo,reference_hi=min(nets[-1]*rlo,nets[-1]*rhi),max(nets[-1]*rlo,nets[-1]*rhi)
        final_lo=reference_lo-log_bounds(phi)[1];final_hi=reference_hi-log_bounds(plo)[0]
        final_lo,final_hi=dyadic_enclose(final_lo,final_hi,96)
        results.append({'name':name,'synthetic':True,'seed_frozen_before_draw':seed,
                        'initial_hidden_state':0,'cost':cost,'band':band,
                        'actual_final_total_entropy_interval':[str(final_lo),str(final_hi)],
                        'actual_final_total_entropy_preview':float((final_lo+final_hi)/2),
                        'full_path_coverage_certified_by_reference_lower_bound':not unresolved,
                        'unresolved_reference_lower_checks':unresolved,
                        'coverage_scope':'every grid point and all microscopic-jump minima; actual entropy is >=reference at all intervening times for delta preparation',
                        'zero_actual_entropy_assumed_for_reversible_dynamics':False})
    output={'scope':__doc__,'joint_time_uniform_risk':'1/40',
        'frozen_before_new_records':frozen,'exact_boundary_controls':finite,'fresh_controls':results,
        'total_additional_cost':{'stationary_preparations':0,'fixed_state_preparations':2,
             'transitions':2*N,'observed_bits':2*(N+1),'model_time':str(Q(8*N,9)),
             'hidden_jumps_simulated':sum(r['cost']['hidden_jumps_simulated'] for r in results),
             'random_bits_generated':sum(r['cost']['random_bits_generated'] for r in results)},
        'status':'PREPARATION_ROBUST_BOUNDARY_AND_FRESH_CONTROLS_CHECKED',
        'seconds':time.perf_counter()-start,
        'scope_limits':'density bound supplied by the synthetic model; no physical calibration, generic power or historical novelty claim'}
    (HERE/'warm_preparation_receipt.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':output['status'],'finite_controls':finite,
            'fresh':[{'name':r['name'],'lower':r['band']['lower_preview'],
                    'first_crossing':r['band']['first_threshold_crossing'],
                    'actual_final_total_entropy':r['actual_final_total_entropy_preview'],
                    'all_path_lower_checks':r['full_path_coverage_certified_by_reference_lower_bound']}
                    for r in results],'cost':output['total_additional_cost'],'seconds':output['seconds']},indent=2))


if __name__=='__main__':main()
