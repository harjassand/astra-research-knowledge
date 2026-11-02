#!/usr/bin/env python3
"""Task-only long-cascade action ranking from four short experiments.

Exact theorem for two persistent latent contexts; no latent labels, no kinetic
parameter fitting. Claims rely on conditional independence of stages given
unchanging context and stable action response at the modified stage.
"""
import json
import numpy as np
from scipy.stats import beta

TRUE={'w_fast':0.5,'p_fast':0.7,'p_slow':0.05,
      'A_fast':0.80,'A_slow':0.065,'B_fast':0.72,'B_slow':0.22}
L=75
DELTA=.01
seed=931071
w=TRUE['w_fast'];pf=TRUE['p_fast'];ps=TRUE['p_slow']
z={}
for a in ('A','B'):
    af=TRUE[a+'_fast'];q=TRUE[a+'_slow']
    z[a+'0']=w*af+(1-w)*q
    z[a+'1']=w*pf*af+(1-w)*ps*q

d0=z['A0']-z['B0']
d1=z['A1']-z['B1']
true_yA=w*pf**(L-1)*TRUE['A_fast']+(1-w)*ps**(L-1)*TRUE['A_slow']
true_yB=w*pf**(L-1)*TRUE['B_fast']+(1-w)*ps**(L-1)*TRUE['B_slow']


def cp(x,n,tail):
    return [float(beta.ppf(tail/2,x,n-x+1)) if x else 0.0,
            float(beta.ppf(1-tail/2,x+1,n-x)) if x<n else 1.0]

out={'model':TRUE,'L':L,'moment_probabilities':z,'true_single_action_contrast_d0':d0,
     'true_prefix_action_contrast_d1':d1,'true_75_stage_yield_A':true_yA,
     'true_75_stage_yield_B':true_yB,'true_yield_improvement_ratio_A_over_B':true_yA/true_yB,
     'iid_marginal_model_prefers':'B',
     'native_experiments':[]}
for n in (1000,2000,5000,10000,20000):
    rng=np.random.default_rng(seed+n)
    cnt={name:int(rng.binomial(n,p)) for name,p in z.items()}
    ci={name:cp(cnt[name],n,DELTA/4) for name in z}
    d0_conf=[ci['A0'][0]-ci['B0'][1],ci['A0'][1]-ci['B0'][0]]
    d1_conf=[ci['A1'][0]-ci['B1'][1],ci['A1'][1]-ci['B1'][0]]
    out['native_experiments'].append({
        'trials_per_short_assay':n,
        'four_assays_total_trials':4*n,
        'maximum_native_stage_attempts':6*n,
        'experiment_counts':cnt,
        'simultaneous_99_percent_CI':ci,
        'd0_CI':d0_conf,'d1_CI':d1_conf,
        'confident_reversal_for_every_L_at_least_2':bool(d0_conf[1]<0 and d1_conf[0]>0)})

with open('producer-workspace/task_only_decision_results.json','w') as f: json.dump(out,f,indent=2)
print('True short contrasts d0, d1',d0,d1)
print('True 75-stage success A, B, ratio',true_yA,true_yB,true_yA/true_yB)
for x in out['native_experiments']:
 print('N',x['trials_per_short_assay'],'CI(d0)',x['d0_CI'],'CI(d1)',x['d1_CI'], 'certified',x['confident_reversal_for_every_L_at_least_2'])
