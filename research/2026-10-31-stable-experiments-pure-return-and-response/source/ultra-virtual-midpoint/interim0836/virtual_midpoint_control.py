#!/usr/bin/env python3
"""Frozen virtual-midpoint inference: exact source power and fresh CTMCs."""
from fractions import Fraction as Q
from pathlib import Path
from bisect import bisect_right
import hashlib
import json
import math
import sys
import time

ROOT=Path(__file__).resolve().parents[1];HERE=ROOT/'outputs/virtual_midpoint'
sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT/'work'))
from midpoint_band import evaluate,from_score,endpoint,checkpoints
from entropy_cone import log_bounds,exponential_bounds
from ctmc_reflection_control import CountedBits,exp_negative_bounds,dyadic_enclose


def pi_bounds(bits=128):
    terms=40+bits//4
    def atan(q):
        total=Q(0);power=Q(1,q)
        for k in range(terms):total+=(-1 if k%2 else 1)*power/(2*k+1);power/=q*q
        other=total+(-1 if terms%2 else 1)*power/(2*terms+1)
        return min(total,other),max(total,other)
    a,b=atan(5);c,d=atan(239)
    return dyadic_enclose(16*a-4*d,16*b-4*c,bits)


class PiPoisson:
    """Exact Poisson with mean1001*pi/999, through shrinking pi intervals."""
    def __init__(self):self.cache={};self.draws=0;self.refinements=0;self.tail_extensions=0
    def bounds(self,precision,cap):
        key=precision,cap
        if key in self.cache:return self.cache[key]
        plo,phi=pi_bounds(160+precision);mulo=Q(1001,999)*plo;muhi=Q(1001,999)*phi
        elo=exp_negative_bounds(muhi,160+precision)[0]
        ehi=exp_negative_bounds(mulo,160+precision)[1]
        elo=dyadic_enclose(elo,elo,224+precision)[0]
        ehi=dyadic_enclose(ehi,ehi,224+precision)[1]
        termlo=termhi=Q(1);sumlo=sumhi=Q(0);lower=[];upper=[]
        for k in range(cap+1):
            sumlo+=termlo;sumhi+=termhi
            a,b=dyadic_enclose(elo*sumhi,ehi*sumlo,128+precision)
            assert a<=b
            lower.append(max(Q(0),a));upper.append(min(Q(1),b))
            termlo*=mulo/(k+1);termhi*=muhi/(k+1)
        self.cache[key]=lower,upper
        return lower,upper
    def draw(self,bits):
        width=64;value=bits.get(width);precision=0;cap=64
        while True:
            ulo,uhi=Q(value,2**width),Q(value+1,2**width)
            lo,hi=self.bounds(precision,cap);k=bisect_right(hi,ulo)
            if k<=cap and uhi<=lo[k]:self.draws+=1;return k
            if k>cap:cap+=32;self.tail_extensions+=1;continue
            value=(value<<32)+bits.get(32);width+=32;precision+=32;self.refinements+=1


def source_parameters():
    plo,phi=pi_bounds();gamma_delta_lo=Q(1001,999)*plo;gamma_delta_hi=Q(1001,999)*phi
    rlo=exp_negative_bounds(gamma_delta_hi)[0];rhi=exp_negative_bounds(gamma_delta_lo)[1]
    rlo,rhi=dyadic_enclose(rlo,rhi)
    assert Q(429,10000)<rlo<=rhi<Q(43,1000)
    return {'pi_interval':[str(plo),str(phi)],'correlation_magnitude_interval':[str(rlo),str(rhi)],
            'correlation_magnitude_preview':float((rlo+rhi)/2),'clock_interval_formula':'1000*pi/999',
            'source_rates':['1','1/1000'],'matched_null_rates':['1001/2000','1001/2000'],
            'binary_source_full_law':'stationary reversible two-state Markov with flip probability(1+r)/2',
            'discrete_hidden_minimum':'0','iid_adjacent_products_is_source_fact_only':True}


def power_proof(Ncap=320398,target=1000,alpha=Q(1,80)):
    points=[]
    for j,N in checkpoints():
        if N>Ncap:break
        points.append((j,N))
    j,N=points[-1];assert N==Ncap
    allocation=alpha/Q(4*j*(j+1));descent=log_bounds(allocation)[0]
    def continued(s):return endpoint(from_score(N,-s,allocation))+descent
    lo,hi=0,N//2;parity=N%2
    while lo<hi:
        mid=(lo+hi)//2
        if continued(parity+2*mid)>=target:hi=mid
        else:lo=mid+1
    critical=parity+2*lo;assert continued(critical)>=target
    margin=Q(429,10000)*N-critical;assert margin>0
    exponent=margin*margin/(2*N)
    newfail=exponential_bounds(-exponent,100)[1]
    later=[];log2hi=log_bounds(Q(2),96)[1]
    for jj,NN in points:
        if 2*NN*log2hi<target:continue
        threshold=Q(target*NN*NN,NN+target);scale=2**48;z=threshold*scale*scale
        rootlo=Q(math.isqrt(z.numerator//z.denominator),scale)
        difference=rootlo-Q(43,1000)*NN;assert difference>0
        exponent_old=difference*difference/(2*NN)
        assert exponent_old>26
        later.append((jj,NN))
    oldfail=len(later)*exponential_bounds(Q(-26),100)[1]
    assert newfail+alpha<Q(1,40)
    timing=Q(1001,1000)*N*Q(1,10**9)
    return {'cap_transitions':N,'cap_observations':N+1,'checkpoint_index':j,'target_nats':target,
            'new_critical_adjacent_sum':-critical,'new_output_failure_upper':str(dyadic_enclose(0,newfail,96)[1]),
            'new_output_failure_preview':float(newfail),
            'new_stop_or_coverage_failure_preview':float(newfail+alpha),
            'ordinary_psd_free_lambda_crossing_probability_upper':str(dyadic_enclose(0,oldfail,96)[1]),
            'ordinary_psd_free_lambda_crossing_probability_preview':float(oldfail),
            'ordinary_checkpoints_remaining_after_impossible_early_times':len(later),
            'ordinary_hoeffding_exponent_lower':'26',
            'all_discrete_hidden_class_any_positive_endpoint_probability_upper':str(alpha),
            'timing_error_bound':'1/1000000000',
            'finite_timing_total_variation_upper':str(timing),'finite_timing_TV_preview':float(timing),
            'source_specific':True,'source_parameters_supplied_to_inference':False}


def sample(N,seed,forward_probability):
    bits=CountedBits(seed);poisson=PiPoisson();x=bits.below(4);record=[int(x>=2)]
    net=0;nets=[0];minima=[];jumps=0;prob=Q(forward_probability)
    for _ in range(N):
        count=poisson.draw(bits);jumps+=count;minimum=net
        for _ in range(count):
            direction=1 if bits.below(prob.denominator)<prob.numerator else -1
            x=(x+direction)%4;net+=direction;minimum=min(minimum,net)
        record.append(int(x>=2));nets.append(net);minima.append(minimum)
    plo,phi=pi_bounds();duration=dyadic_enclose(N*Q(1000,999)*plo,N*Q(1000,999)*phi,96)
    return record,nets,minima,{'stationary_preparations':1,'observations':N+1,'grid_intervals':N,
        'model_duration_interval':[str(a) for a in duration],
        'model_duration_preview':float(sum(duration)/2),'latent_jumps_simulated':jumps,
        'PRNG_bits_generated':bits.bits,'Poisson_draws':poisson.draws,
        'Poisson_refinements':poisson.refinements,'Poisson_tail_extensions':poisson.tail_extensions,
        'initial_pi_precision_bits':160,'initial_CDF_precision_bits':128,
        'unobserved_midpoint_measurements':0}


def decode(d):return Q(int(d['numerator']),int(d['denominator']))


def verify_coverage(band,nets,minima,ratio):
    llo,lhi=log_bounds(ratio)
    def actual_lower(net):return min(net*llo,net*lhi)
    history={p['transitions']:p for p in band['history']};lower=decode(band['baseline_lower_endpoint']);fail=[]
    for N in range(1,len(nets)):
        if actual_lower(minima[N-1])<lower:fail.append({'interval':N,'kind':'microscopic minimum'})
        if N in history:lower=decode(history[N]['running_lower_endpoint'])
        if actual_lower(nets[N])<lower:fail.append({'interval':N,'kind':'grid endpoint'})
    return fail


def psd_oracle(record,alpha):
    lookup={}
    for j,N in checkpoints():
        if N>=len(record):break
        lookup[N]=j
    S=0;best=log_bounds(alpha/2)[1];first=None
    for N in range(1,len(record)):
        S+=1 if record[N-1]==record[N] else -1
        if N not in lookup:continue
        r=Q(max(0,-S),N)
        if r==1:psi=log_bounds(Q(2),96)[1]
        else:psi=((1+r)*log_bounds(1+r,96)[1]+(1-r)*log_bounds(1-r,96)[1])/2
        j=lookup[N];allocation=alpha/Q(4*j*(j+1))
        best=max(best,2*N*psi+3*log_bounds(allocation,96)[1])
        if first is None and best>=1000:first=N
    return {'upper_envelope_preview':float(best),'first_1000_crossing':first,
            'valid_inference':False,'role':'optimistic upper over every fixed/mixed/charged lambda in the CTMC-PSD family'}


def main():
    start=time.perf_counter();N=320398;each=Q(1,80)
    source=source_parameters();power=power_proof(N,1000,each)
    frozen={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ('PROOF.txt','midpoint_band.py')}
    results=[]
    for name,prob,ratio,seed in [('driven_alias',Q(1000,1001),Q(1000),2026110110),
                               ('reversible_matched',Q(1,2),Q(1),2026110111)]:
        record,nets,minima,cost=sample(N,seed,prob)
        (HERE/(name+'_record.json')).write_text(json.dumps(record)+'\n')
        new=evaluate(iter(record),each,keep_history=True,threshold=1000)
        old=evaluate(iter(record),each,method='psd',keep_history=True,threshold=1000)
        newfail=verify_coverage(new,nets,minima,ratio);oldfail=verify_coverage(old,nets,minima,ratio)
        llo,lhi=log_bounds(ratio)
        results.append({'name':name,'synthetic':True,'seed_frozen_before_draw':seed,
                        'cost':cost,'midpoint_band':new,'ordinary_psd_band':old,
                        'ordinary_free_lambda_envelope':psd_oracle(record,each),
                        'actual_full_path_entropy_preview':float(nets[-1]*llo),
                        'actual_entropy_net_oriented_jumps':nets[-1],
                        'midpoint_coverage_failures':newfail,'ordinary_coverage_failures':oldfail})
    out={'scope':__doc__,'source':source,'source_power':power,'frozen_before_new_records':frozen,
         'fresh_controls':results,'each_method_time_uniform_risk':str(each),'joint_methods_risk_per_record':'1/40',
         'total_new_cost':{'stationary_preparations':2,'observed_bits':2*(N+1),'grid_intervals':2*N,
             'model_duration_formula':f'{2*N*1000}*pi/999',
             'model_duration_preview':sum(r['cost']['model_duration_preview'] for r in results),
             'latent_jumps_simulated':sum(r['cost']['latent_jumps_simulated'] for r in results),
             'PRNG_bits_generated':sum(r['cost']['PRNG_bits_generated'] for r in results),
             'midpoint_measurements':0},
         'all_observed_coverage_checks_passed':all(not r['midpoint_coverage_failures'] and not r['ordinary_coverage_failures'] for r in results),
         'status':'VIRTUAL_MIDPOINT_POWER_AND_FRESH_CONTROLS_COMPLETE','seconds':time.perf_counter()-start,
         'scope_limits':'specific finite CTMC source, mathematical timing and synthetic randomness; no physical device or generic CTMC-aware advantage'}
    (HERE/'receipt.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'power':power,
        'fresh':[{'name':r['name'],'new':r['midpoint_band']['lower_preview'],
                  'new_crossing':r['midpoint_band']['first_threshold_crossing'],
                  'old':r['ordinary_psd_band']['lower_preview'],'old_oracle':r['ordinary_free_lambda_envelope'],
                  'actual_full_entropy':r['actual_full_path_entropy_preview'],
                  'coverage_failures':len(r['midpoint_coverage_failures'])+len(r['ordinary_coverage_failures'])}
                 for r in results],'cost':out['total_new_cost'],'seconds':out['seconds']},indent=2))


if __name__=='__main__':main()
