"""Small exact rational checks and a full finite budget, not an experiment.

No sampling-state-control completed proof, external participant answer, or
physical apparatus is used. The source probabilities below are auditor-only
rational fixtures; the operational controller takes only coarse bounds.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import json
from control import make_plan

ROOT=Path(__file__).resolve().parent


def serialize(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {k:serialize(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [serialize(v) for v in x]
    return x


def population(lam,e,a):
    return (lam+e*a)/(2*lam+(1+2*e)*a)


def clipped_mass(p,t,N,hot_label):
    return sum((F(comb(N,k))*p**k*(1-p)**(N-k)*
                max(F(0), t-F(k,N) if hot_label else F(k,N)-t)
                for k in range(N+1)),F(0))


def matmul(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]


def dressed_diagonal(p1,p2):
    diag=[(1-p1)*(1-p2),(1-p1)*p2,p1*(1-p2),p1*p2]
    # U=CNOT(H tensor I)=M/sqrt(2); density matrices remain rational.
    M=[[1,0,1,0],[0,1,0,1],[0,1,0,-1],[1,0,-1,0]]
    return [[sum(F(M[i][k]*M[j][k],2)*diag[k] for k in range(4))
             for j in range(4)] for i in range(4)]


def main():
    ac,ah=F(8),F(2)
    alpha,chi=F(1,10),F(4,5)
    specs=[{'alpha':alpha,'chi':chi,'q':F(1,5),'p_c_upper':F(1,6),'p_h_lower':F(1,4)},
           {'alpha':alpha,'chi':chi,'q':F(3,10),'p_c_upper':F(1,4),'p_h_lower':F(1,3)}]
    params=[(F(1),F(1,10)),(F(2),F(1,5))]
    cases=[]
    for spec,(lam,e) in zip(specs,params):
        pc,ph=population(lam,e,ac),population(lam,e,ah)
        q=spec['q']; rc,rh,t=alpha+chi*pc,alpha+chi*ph,alpha+chi*q
        assert pc<=spec['p_c_upper']<q<spec['p_h_lower']<=ph
        hotmass,coldmass=t-rc,rh-t
        w=hotmass/(hotmass+coldmass)
        assert w==(q-pc)/(ph-pc)
        assert (1-w)*pc+w*ph==q
        covariance_record=w*(1-w)*(ph-pc)
        covariance_reuse=w*(1-w)*(ph-pc)**2
        assert covariance_record>0 and covariance_reuse>0
        small=[]
        for nc,nh in [(8,8),(17,23),(31,29)]:
            a=clipped_mass(rc,t,nc,True)
            b=clipped_mass(rh,t,nh,False)
            ec,eh=a-hotmass,b-coldmass
            assert ec>=0 and eh>=0
            wclip=a/(a+b)
            qclip=(1-wclip)*pc+wclip*ph
            assert qclip-q==(coldmass*ec-hotmass*eh)/(chi*(hotmass+coldmass+ec+eh))
            assert abs(qclip-q)<=(ec+eh)/chi
            small.append({'nc':nc,'nh':nh,'hot_trial_mass':a,'cold_trial_mass':b,
                          'clipping_excess_hot':ec,'clipping_excess_cold':eh,
                          'population_bias':qclip-q})
        cases.append({'p_c':pc,'p_h':ph,'q':q,'r_c':rc,'r_h':rh,'observed_target':t,
                      'hot_weight':w,'record_covariance':covariance_record,
                      'reused_label_covariance':covariance_reuse,'clipping_checks':small})
    mix=[[F(0) for _ in range(4)] for _ in range(4)]
    for s1,s2 in product((0,1),repeat=2):
        prob=F(1)
        pops=[]
        for s,c in zip((s1,s2),cases):
            prob*=c['hot_weight'] if s else 1-c['hot_weight']
            pops.append(c['p_h'] if s else c['p_c'])
        branch=dressed_diagonal(*pops)
        mix=[[x+prob*y for x,y in zip(row,brow)] for row,brow in zip(mix,branch)]
    target=dressed_diagonal(specs[0]['q'],specs[1]['q'])
    assert mix==target
    plan=make_plan(specs,F(1,100),
        {'alpha':alpha,'chi':chi,'lambda_lower':F(1,2),'a_c':ac},ah)
    out={'scope':'Exact rational identity checks and deterministic budget compilation only; no native or Monte Carlo experiment.',
         'sources_used':'Frozen PRE-result native equations and classical factory/concentration premises only.',
         'mixture_cases':cases,'dressed_two_factor_mixture_equals_target':True,
         'dressed_target_matrix':target,'finite_plan':plan,
         'nominal_six_term_error_bound':sum(plan['certified_error_terms'].values()),
         'native_probe_calls_executed':0,'physical_experiments':0}
    (ROOT/'EXACT_AUDIT.json').write_text(json.dumps(serialize(out),indent=2)+'\n')
    print(json.dumps(serialize({'identities':'passed','clipping_cases':6,
        'dressed_mixture':'passed','native_calls_executed':0,
        'planned_native_coin_cap':plan['total_native_coin_cap'],
        'planned_signal_coin_cap':plan['signal_coin_cap'],
        'planned_entropy_coin_cap':plan['entropy_coin_cap'],
        'planned_fair_bits':plan['fair_bit_cap'],
        'planned_pairs_per_bit':plan['pairs_per_fair_bit_cap'],
        'planned_output_reset_duration':plan['parallel_output_reset_duration'],
        'six_term_error_bound':sum(plan['certified_error_terms'].values()),
        'reserved_residual_budget':plan['reserved_residual_budget']})),flush=True)


if __name__=='__main__':
    main()
