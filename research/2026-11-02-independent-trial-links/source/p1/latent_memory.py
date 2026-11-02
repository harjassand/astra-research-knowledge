#!/usr/bin/env python3
"""Acquisition of two persistent hidden kinetic contexts from short observable prefixes.

A synthetic controlled hidden Markov / weighted-automaton toy. This is a
classical Prony-Hankel construction, not a novel prior-art claim. Interval bounds
are rigorous *conditional on* the two-context promise, independent Bernoulli
experiments, and the simultaneous Clopper-Pearson coverage event.
"""
import json
import numpy as np
from scipy.stats import beta

SEED=202611021
DELTA=0.01
L=75
K=10
w_true=0.5
rates={
    'baseline':(0.7,0.05),
    'A_fast_specific':(0.8,0.065),
    'B_mean_friendly':(0.72,0.22),
}


def moment_p(k, arr=rates['baseline']):
    return w_true*arr[0]**k+(1-w_true)*arr[1]**k

def exact_schedule(action):
    return w_true*rates['baseline'][0]**(L-K)*rates[action][0]**K + (1-w_true)*rates['baseline'][1]**(L-K)*rates[action][1]**K


def prony(m1,m2,m3):
    den=m2-m1*m1
    s=(m3-m1*m2)/den
    p=s*m1-m2
    disc=s*s-4*p
    if disc<0: raise ValueError('No two-real-mode point fit')
    hi=(s+np.sqrt(disc))/2
    lo=(s-np.sqrt(disc))/2
    w=(m1-lo)/(hi-lo)
    return {'fast':hi,'slow':lo,'fast_fraction':w,'det_hankel':den}


def outer_interval(bs):
    """Conservative rectangular interval operations; no optimization or sign inference."""
    (l1,u1),(l2,u2),(l3,u3)=bs
    v_lo=l2-u1*u1
    v_hi=u2-l1*l1
    c_lo=l3-u1*u2
    c_hi=u3-l1*l2
    if min(v_lo,c_lo)<=0: return {'valid':False,'reason':'Hankel inverse not separated by confidence intervals'}
    s_lo=c_lo/v_hi;s_hi=c_hi/v_lo
    p_lo=s_lo*l1-u2;p_hi=s_hi*u1-l2
    discr_lo=s_lo*s_lo-4*p_hi
    discr_hi=s_hi*s_hi-4*p_lo
    if discr_lo<0: return {'valid':False,'reason':'Cannot certify distinct real modes from the three independent intervals'}
    f_lo=(s_lo+np.sqrt(discr_lo))/2
    f_hi=(s_hi+np.sqrt(discr_hi))/2
    q_lo=max(0,(s_lo-np.sqrt(discr_hi))/2)
    q_hi=min(1,(s_hi-np.sqrt(discr_lo))/2)
    den_lo=f_lo-q_hi
    den_hi=f_hi-q_lo
    if den_lo<=0 or f_lo<0 or f_hi>1:
        return {'valid':False,'reason':'Unresolved root sign/bounds'}
    w_lo=max(0,(l1-q_hi)/den_hi)
    w_hi=min(1,(u1-q_lo)/den_lo)
    if not (0<w_lo<w_hi<1):
        return {'valid':False,'reason':'Unresolved mixture weight'}
    return {'valid':True,'fast':(f_lo,f_hi),'slow':(q_lo,q_hi),'fast_fraction':(w_lo,w_hi)}


def action_bounds(baseline, za0,za1):
    f_lo,f_hi=baseline['fast']
    q_lo,q_hi=baseline['slow']
    w_lo,w_hi=baseline['fast_fraction']
    (z0_lo,z0_hi),(z1_lo,z1_hi)=za0,za1
    D_lo=f_lo-q_hi
    D_hi=f_hi-q_lo
    af_lo=max(0,(z1_lo-q_hi*z0_hi)/(w_hi*D_hi))
    af_hi=min(1,(z1_hi-q_lo*z0_lo)/(w_lo*D_lo))
    aq_lo=max(0,(f_lo*z0_lo-z1_hi)/((1-w_lo)*D_hi))
    aq_hi=min(1,(f_hi*z0_hi-z1_lo)/((1-w_hi)*D_lo))
    return {'fast':(af_lo,af_hi),'slow':(aq_lo,aq_hi)}


def final_bounds(base, a):
    wlo,whi=base['fast_fraction']
    fl,fh=base['fast']
    ql,qh=base['slow']
    afl,afh=a['fast']; aql,aqh=a['slow']
    low=wlo*fl**(L-K)*afl**K + (1-whi)*ql**(L-K)*aql**K
    high=whi*fh**(L-K)*afh**K + (1-wlo)*qh**(L-K)*aqh**K
    return (low, high)


def exact_action_heteromoments(action):
    af,aq=rates[action]
    f,q=rates['baseline']
    return (w_true*af+(1-w_true)*aq, w_true*f*af+(1-w_true)*q*aq)


def cp(k,n,alpha):
    l=beta.ppf(alpha/2,k,n-k+1) if k>0 else 0.
    u=beta.ppf(1-alpha/2,k+1,n-k) if k<n else 1.
    return (l,u)


def experiment(n, seed):
    rng=np.random.default_rng(seed)
    trials={}
    for k in (1,2,3):
        trials[f'm{k}']=float(moment_p(k))
    for action in ['A_fast_specific','B_mean_friendly']:
        z0,z1=exact_action_heteromoments(action)
        trials[f'{action}_z0']=z0
        trials[f'{action}_z1']=z1
    nobs=len(trials)
    observations={k:int(rng.binomial(n,p)) for k,p in trials.items()}
    intervals={k:cp(v,n,DELTA/nobs) for k,v in observations.items()}
    allcovered=all(intervals[k][0]<=p<=intervals[k][1] for k,p in trials.items())
    m=[observations[f'm{k}']/n for k in (1,2,3)]
    point=prony(*m)
    est_actions={}
    for a in ['A_fast_specific','B_mean_friendly']:
        z0=observations[f'{a}_z0']/n
        z1=observations[f'{a}_z1']/n
        xfast=(z1-point['slow']*z0)/(point['fast_fraction']*(point['fast']-point['slow']))
        xslow=(point['fast']*z0-z1)/((1-point['fast_fraction'])*(point['fast']-point['slow']))
        est_actions[a]=(xfast,xslow)
    outer=outer_interval([intervals['m1'],intervals['m2'],intervals['m3']])
    action_outer={}
    final_outer={}
    if outer['valid']:
        for a in ['A_fast_specific','B_mean_friendly']:
            action_outer[a]=action_bounds(outer,intervals[a+'_z0'],intervals[a+'_z1'])
            final_outer[a]=final_bounds(outer,action_outer[a])
    estimated_yield={a:point['fast_fraction']*point['fast']**(L-K)*est_actions[a][0]**K+(1-point['fast_fraction'])*point['slow']**(L-K)*est_actions[a][1]**K for a in est_actions}
    output={
        'n_each_observation_type':n, 'types':nobs,'total_short_experiments':n*nobs,
        'max_stage_attempts_before_early_termination':n*(1+2+3+2*3),
        'simultaneous_interval_coverage':1-DELTA,
        'coverage_realized_for_seed':bool(allcovered),
        'point_baseline_model':point,
        'point_action_response':{a:list(v) for a,v in est_actions.items()},
        'point_yield':estimated_yield,
        'baseline_outer_interval':outer,
        'action_outer_interval':action_outer,
        'yield_outer_interval':final_outer,
        'intervals_raw':{k:list(v) for k,v in intervals.items()},
        'counts':observations,
    }
    if final_outer:
        la,ha=final_outer['A_fast_specific'];lb,hb=final_outer['B_mean_friendly']
        output['certifies_A_beats_B']=bool(la>hb)
        output['A_certified_advantage_lower_ratio']=float(la/hb)
    return output

if __name__=='__main__':
    true={
        'mode_rates':rates,'mixture_weight_fast':w_true,'L':L,'intervened_stages':K,
        'baseline_true_yield':moment_p(L),
        'A_true_yield':exact_schedule('A_fast_specific'),
        'B_true_yield':exact_schedule('B_mean_friendly'),
        'true_A_over_B':exact_schedule('A_fast_specific')/exact_schedule('B_mean_friendly'),
        'naive_A_mean_survival':(w_true*rates['baseline'][0]+(1-w_true)*rates['baseline'][1])**(L-K)*(sum(rates['A_fast_specific'])/2)**K,
        'naive_B_mean_survival':(w_true*rates['baseline'][0]+(1-w_true)*rates['baseline'][1])**(L-K)*(sum(rates['B_mean_friendly'])/2)**K,
        'exact_m1m2m3':[moment_p(k) for k in (1,2,3)],
        'exact_prony':prony(*(moment_p(k) for k in (1,2,3))),
    }
    records={str(n):experiment(n,SEED+n) for n in [200_000,1_000_000,5_000_000,20_000_000]}
    with open('producer-workspace/latent_memory_results.json','w') as f:
        json.dump({'exact':true,'experiments':records},f,indent=2)
    print('EXACT',true)
    for n,v in records.items():
        print('N',n,'point',v['point_baseline_model'], 'est_yield',v['point_yield'],
              'outer',v['yield_outer_interval'],'decision',v.get('certifies_A_beats_B'))
