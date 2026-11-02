#!/usr/bin/env python3
"""ONE integrated synthetic CTMC: killed excursions + persistent two-mode hidden memory.

Each fresh specimen samples one unobserved stable kinetic mode; a stage is a
CTMC with direct progression, reversible trap, independent degradation; on
progression, the mode is kept and hidden trap is reset. Short experiments are
actual Gillespie simulated clocks, with stage times and trap visits charged.
Strong ordinary comparator: 300-state exact sparse killed CTMC generator.
"""
import json
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from scipy.stats import beta

SEED=2026110202
rng=np.random.default_rng(SEED)
MU=.3
N=75
M=40000
DELTA=.01
w=(.5,.5)
p0=(.7,.05)
pa=(.8,.065)
pb=(.72,.22)
trap_rate=(.8,1.1)
trap_return=(.7,.2)

c=[MU+t*MU/(MU+g) for t,g in zip(trap_rate,trap_return)]
def forward_rates(p):return tuple(cz*pz/(1-pz) for cz,pz in zip(c,p))
R={'base':forward_rates(p0),'A':forward_rates(pa),'B':forward_rates(pb)}

# Native stage: sample first the holding time, then the competing reaction.
def simulate_assay(seq):
    z=int(rng.random()>=w[0])
    elapsed=0.; events=0; traps=0; visits=0
    for act in seq:
        while True:
            progression=R[act][z]
            total=progression+trap_rate[z]+MU
            elapsed+=rng.exponential(1/total);events+=1
            r=rng.random()*total
            if r<progression:break
            if r<progression+MU:return False,elapsed,events,traps,visits
            # Enter transient trap.  The mode z does NOT change.
            traps+=1
            g=trap_return[z];total2=g+MU
            elapsed+=rng.exponential(1/total2);events+=1
            if rng.random()*total2 >= g:return False,elapsed,events,traps,visits
            visits+=1
    return True,elapsed,events,traps,visits

# Conventional explicit 2*N stage states and 2*N trap states.
def ordinary_full_generator(action):
    size=4*N
    # local index 2*(stage*2+mode), then trap index plus 1
    I=lil_matrix((size,size),dtype=float)
    b=np.zeros(size)
    for k in range(N):
        for z in range(2):
            base=4*k+2*z
            act=action if k==N-1 else 'base'
            f=R[act][z];t=trap_rate[z];g=trap_return[z]
            I[base,base]=f+t+MU
            I[base,base+1]=-t
            if k+1<N: I[base,4*(k+1)+2*z]=-f
            else:b[base]=f
            I[base+1,base+1]=g+MU
            I[base+1,base]=-g
    return float(.5*spsolve(I.tocsr(),b)[0]+.5*spsolve(I.tocsr(),b)[2])

observed={};details={}
for key,seq in [('A0',['A']),('B0',['B']),('A1',['base','A']),('B1',['base','B'])]:
    successes=0;dur=0.;events=0;traps=0;returned=0
    for j in range(M):
        ok,dt,e,t,r=simulate_assay(seq)
        successes+=int(ok);dur+=dt;events+=e;traps+=t;returned+=r
    observed[key]=successes/M
    alpha=DELTA/4
    ci=[float(beta.ppf(alpha/2,successes,M-successes+1)) if successes else 0.,
        float(beta.ppf(1-alpha/2,successes+1,M-successes)) if successes<M else 1.]
    details[key]={'n':M,'successes':successes,'p_hat':successes/M,'ci_99_simultaneous':ci,
                  'reaction_time':dur,'events':events,'entered_trap':traps,'trap_returned':returned}

assert len(details)==4
true=lambda tag: .5*p0[0]**(N-1)*(pa[0] if tag=='A' else pb[0])+ .5*p0[1]**(N-1)*(pa[1] if tag=='A' else pb[1])
fullA=ordinary_full_generator('A');fullB=ordinary_full_generator('B')
assert np.isclose(fullA,true('A'),rtol=1e-10)
assert np.isclose(fullB,true('B'),rtol=1e-10)
lo0=details['A0']['ci_99_simultaneous'][0]-details['B0']['ci_99_simultaneous'][1]
hi0=details['A0']['ci_99_simultaneous'][1]-details['B0']['ci_99_simultaneous'][0]
lo1=details['A1']['ci_99_simultaneous'][0]-details['B1']['ci_99_simultaneous'][1]
hi1=details['A1']['ci_99_simultaneous'][1]-details['B1']['ci_99_simultaneous'][0]
result={'seed':SEED,'ctmc_state_count':4*N,'stages':N,'persistent_unobserved_mode_count':2,
'independent_death_rate':MU,'per_mode_trap_entry':trap_rate,'per_mode_trap_return':trap_return,
'per_mode_progression_rate':R,'per_mode_stage_yield':{'baseline':p0,'A':pa,'B':pb},
'assays':details,'total_native_specimens':4*M,'max_stage_attempts':6*M,
'total_native_reaction_time':sum(x['reaction_time'] for x in details.values()),
'total_native_ctmc_events':sum(x['events'] for x in details.values()),
'total_native_trap_visits':sum(x['entered_trap'] for x in details.values()),
'd0_interval':[lo0,hi0],'d1_interval':[lo1,hi1],
'all_horizon_action_A_preferred_certified_at_99pct':bool(hi0<0 and lo1>0),
'full_ctmc_yield_A':fullA,'full_ctmc_yield_B':fullB,
'latent_two_mode_formula_yield_A':true('A'),'latent_two_mode_formula_yield_B':true('B'),
'status':'CTMC Gillespie short experiments; full 300-state sparse generator strong comparator; all synthetic.'}
with open('producer-workspace/composed_ctmc_results.json','w') as f:json.dump(result,f,indent=2)
print('Observed',details)
print('Total native reaction time',result['total_native_reaction_time'])
print('d0 interval',result['d0_interval'],'d1 interval',result['d1_interval'],'certified',result['all_horizon_action_A_preferred_certified_at_99pct'])
print('full generator A,B',fullA,fullB)
