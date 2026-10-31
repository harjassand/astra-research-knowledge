#!/usr/bin/env python3
"""Rational CTMC power certificate plus exact Poisson-source controls.

No matrix exponential or floating decision is used. Simulation is synthetic,
using a seeded PRNG. It is not experimental evidence or a physical sampler.
"""
from bisect import bisect_right
from fractions import Fraction as Q
from pathlib import Path
import json
import math
import random
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'outputs/reversible_currents'
sys.path.insert(0,str(HERE))
from currents import log_bounds
from reflection_trace import evaluate


def exp_negative_bounds(x, terms=160):
    assert x>=0 and terms+2>x
    term=Q(1); total=Q(1)
    for j in range(1,terms+1):
        term*=-x/j
        total+=term
    next_total=total+term*(-x)/(terms+1)
    return min(total,next_total),max(total,next_total)


def dyadic_enclose(lo,hi,bits=112):
    scale=2**bits
    a,b=lo*scale,hi*scale
    return Q(a.numerator//a.denominator,scale),Q(-((-b.numerator)//b.denominator),scale)


def correlation_enclosure(states=16,dt=Q(4,9),order=100):
    # exp(2dt Q)=e^-mu sum mu^j/j! R^j, R jumps +1 with 10/11.
    mu=22*dt
    distribution=[Q(i==0) for i in range(states)]
    f=[1 if i<states//2 else -1 for i in range(states)]
    term=Q(1); mass=Q(0); total=Q(0)
    for k in range(order+1):
        corr=sum((distribution[j]*Q(sum(f[i]*f[(i+j)%states] for i in range(states)),states)
                  for j in range(states)),Q(0))
        assert -1<=corr<=1
        total+=term*corr; mass+=term
        nxt=[Q(0)]*states
        for i,p in enumerate(distribution):
            nxt[(i+1)%states]+=p*Q(10,11)
            nxt[(i-1)%states]+=p*Q(1,11)
        distribution=nxt
        term*=mu/(k+1)
    elo,ehi=exp_negative_bounds(mu)
    assert 0<elo<=ehi
    remainder=1-elo*mass
    assert 0<=remainder<1
    lo,hi=min(elo*total,ehi*total)-remainder,max(elo*total,ehi*total)+remainder
    return dyadic_enclose(lo,hi),dyadic_enclose(Q(0),remainder)


class CountedBits:
    def __init__(self,seed):
        self.rng=random.Random(seed)
        self.bits=0
    def get(self,n):
        self.bits+=n
        return self.rng.getrandbits(n)
    def below(self,n):
        width=(n-1).bit_length()
        while True:
            value=self.get(width)
            if value<n:return value


class ExactPoisson:
    """Inverse CDF with directed rational enclosures and refining bit cells."""
    def __init__(self,mean):
        self.mean=mean
        self.cache={}
        self.draws=0
        self.refinements=0
    def bounds(self,precision,cap):
        key=precision,cap
        if key in self.cache:return self.cache[key]
        elo,ehi=exp_negative_bounds(self.mean,160+precision)
        lo=[];hi=[];term=Q(1);total=Q(0)
        for j in range(cap+1):
            total+=term
            low,high=dyadic_enclose(elo*total,ehi*total,128+precision)
            lo.append(max(Q(0),low));hi.append(min(Q(1),high))
            term*=self.mean/(j+1)
        self.cache[key]=lo,hi
        return lo,hi
    def draw(self,bits):
        width=64; value=bits.get(width); precision=0; cap=64
        while True:
            lowU=Q(value,2**width);highU=Q(value+1,2**width)
            lower,upper=self.bounds(precision,cap)
            k=bisect_right(upper,lowU)
            if k<=cap and highU<=lower[k]:
                self.draws+=1
                return k
            if k>cap:
                cap+=32
                continue
            value=(value<<32)+bits.get(32);width+=32;precision+=32
            self.refinements+=1


def sample(states,dt,steps,seed,forward=Q(10),backward=Q(1)):
    bits=CountedBits(seed)
    poisson=ExactPoisson((forward+backward)*dt)
    assert forward+backward==11
    probability=forward/(forward+backward)
    x=bits.below(states);record=[int(x>=states//2)];jumps=0;net_jumps=0
    for _ in range(steps):
        count=poisson.draw(bits);jumps+=count
        for _ in range(count):
            direction=1 if bits.below(probability.denominator)<probability.numerator else -1
            net_jumps+=direction
            x=(x+direction)%states
        record.append(int(x>=states//2))
    return record,{'stationary_initializations':1,'time_grid_transitions':steps,
        'microscopic_jumps_simulated':jumps,'net_oriented_jumps':net_jumps,
        'random_bits_generated':bits.bits,
        'exact_poisson_draws':poisson.draws,'poisson_interval_refinements':poisson.refinements,
        'source_sampler':'exact Poisson inverse CDF from directed rational intervals; synthetic seeded PRNG'}


def main():
    start=time.perf_counter()
    corr,remainder=correlation_enclosure()
    assert corr[1]<-Q(19,50)
    # cos(pi/8)<37/40: sqrt(2)<17/12, and (37/40)^2>41/48.
    assert Q(17,12)**2>2 and Q(37,40)**2>Q(41,48)
    rho_upper=exp_negative_bounds(Q(11,30))[1]
    assert rho_upper<Q(7,10)
    delta=Q(19,50);V=Q(29,3);alpha=beta=Q(1,40)
    n=10800;steps=n+1;dt=Q(4,9)
    assert n*delta*delta/32>log_bounds(1/alpha)[1]
    type_II_bound=4*V/(n*delta*delta)
    assert type_II_bound<=beta
    # theta(i)=7-i mod16 preserves the binary label and reverses Q exactly.
    states=16
    gen=[[Q(0)]*states for _ in range(states)]
    for i in range(states):
        gen[i][i]=-11;gen[i][(i+1)%states]=10;gen[i][(i-1)%states]=1
    theta=[(7-i)%states for i in range(states)]
    labels=[int(i>=8) for i in range(states)]
    assert all(labels[theta[i]]==labels[i] for i in range(states))
    assert all(gen[theta[i]][theta[j]]==gen[j][i] for i in range(states) for j in range(states))
    acquisitions=[]
    for name,p,q,seed in [('driven_ring',Q(10),Q(1),202610311),
                          ('matched_reversible_ring',Q(11,2),Q(11,2),202610312)]:
        record,cost=sample(states,dt,steps,seed,p,q)
        path=HERE/(name+'_record.json')
        path.write_text(json.dumps(record)+'\n')
        result=evaluate(record,alpha)
        lower=result['rate_lower_per_step']
        lower_time=Q(int(lower['numerator']),int(lower['denominator']))/dt
        acquisitions.append({'name':name,'forward_rate':str(p),'backward_rate':str(q),
            'cost':cost,'result':result,'rate_lower_per_time':str(lower_time),
            'rate_lower_per_time_preview':float(lower_time)})
    log10=log_bounds(Q(10))
    output={'scope':__doc__,'model':{'hidden_states':16,'forward_rate':'10',
        'backward_rate':'1','stationary_law':'uniform','observation':'binary half-ring',
        'sampling_interval':'4/9','true_entropy_rate':'9 log(10) nats/time',
        'true_entropy_rate_enclosure':list(map(str,dyadic_enclose(9*log10[0],9*log10[1]))),
        'all_observed_word_laws_reversal_invariant':True,
        'mechanism':'theta(i)=7-i mod16 preserves labels and theta Q theta=Q^T'},
        'rational_power_certificate':{'C2_enclosure':list(map(str,corr)),
            'C2_preview':[float(x) for x in corr],
            'uniformization_tail_upper':str(remainder[1]),
            'C2_upper_less_than':'-19/50','normal_spectral_radius_upper':'7/10',
            'variance_per_window_upper':'29/3','overlapping_windows':n,
            'sampled_transitions':steps,'observations':steps+1,
            'type_I_risk_at_most':str(alpha),'type_II_bound':str(type_II_bound),
            'type_II_risk_at_most':str(beta),
            'decision_event_for_power_proof':'lag-two score <= -n*(19/50)/2'},
        'cost':{'stationary_preparations_per_record':1,'duration_per_record':str(steps*dt),
            'expected_hidden_jumps_per_record':str(11*steps*dt),
            'mean_full_path_entropy_driven_record':f'{9*steps*dt} log(10) nats',
            'resets_or_mixing_gaps':0,
            'unacquired_physical_costs':'stationary preparation, state network, drive, timing and detector'},
        'acquisitions':acquisitions,'seconds':time.perf_counter()-start,
        'status':'EXACT_MATHEMATICAL_CTMC_CONTROL_PASSED',
        'comparison':'the evaluator IS the ordinary reflection baseline; no algorithmic advantage claimed'}
    (HERE/'ctmc_receipt.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':output['status'],'seconds':output['seconds'],
        'C2_enclosure_preview':output['rational_power_certificate']['C2_preview'],
        'type_II_upper':float(type_II_bound),'duration':str(steps*dt),
        'synthetic_controls':[{'name':x['name'],
            'reject':x['result']['reject_reversible'],
            'lag_two_score':x['result']['lag_two_product_sum'],
            'rate_lower_per_time':x['rate_lower_per_time_preview'],
            'cost':x['cost']} for x in acquisitions]},indent=2))


if __name__=='__main__':
    main()
