import json,time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from model import fixture,add_context_clock,Compiler,discover_partition,from_transcript
from kinetic_tomography import acquire_unknown_support,physical_clock
from audit import replay
ROOT=Path(__file__).parent

def main():
    t=time.perf_counter();checks=0;details=[]
    for name,alter in [('unknown_support_rare',False),('unknown_support_cross',True)]:
        truth=add_context_clock(fixture(B=3,m=6,rarity=3),F(1,100))
        if alter:
            nei=set(truth['clock_contexts'][0]);a=min(nei);j=next(j for j in range(1,18) if j not in nei)
            truth['clock_contexts'][0]=sorted([a,j]);truth['clock_tables'][0]=[truth['nu'][0],truth['nu'][0]/2,truth['nu'][0]/2,truth['nu'][0]]
        model,tr=acquire_unknown_support(truth)
        for i in range(18):
            union=sorted(set(truth['clock_contexts'][i])|set(model['clock_contexts'][i]))
            for z in range(1<<len(union)):
                x=sum(((z>>k)&1)<<node for k,node in enumerate(union))
                assert physical_clock(truth,i,x)==physical_clock(model,i,x);checks+=1
        details.append(replay(name));checks+=2
    details.append(replay('matched_tensor'));checks+=2
    # Compare main baseline and context models after identical unknown-support scans.
    truth=fixture(B=3,m=6,rarity=3);model,tr=acquire_unknown_support(truth)
    json.dump(tr,open(ROOT/'unknown_support_baseline_transcript.json','w'),indent=2)
    a=json.load(open(ROOT/'unknown_support_rare_transcript.json'))
    assert tr['weights']==a['weights'];checks+=1
    for i in range(18):assert tr['balanced_rates'][f'{i}:0']==a['balanced_rates'][f'{i}:0'];checks+=1
    details.append(replay('pcg_primary_r3','unknown_support_baseline'));checks+=2
    # Prove non-invariance of the degree-one spin space by an exact nonzero
    # higher-degree Walsh coefficient of L sigma_i, using only a local table.
    nonlinear=None
    for i in range(18):
        nei=sorted(j if i==a else a for a,j in truth['edges'] if i==a or i==j)
        support=[i]+nei;vals=[]
        for z in range(1<<len(support)):
            xi=z&1;ratio=truth['fields'][i]**(1-2*xi)
            for k,j in enumerate(nei):
                tedge=truth['edges'][tuple(sorted((i,j)))];ratio*=1/tedge if xi==((z>>(k+1))&1) else tedge
            q=truth['nu'][i]*ratio/(1+ratio);vals.append(2*(2*xi-1)*q)
        for mask in range(1,1<<len(support)):
            if mask.bit_count()<2:continue
            coef=sum(v*(-1 if ((z&mask).bit_count()%2) else 1) for z,v in enumerate(vals))/len(vals)
            if coef:
                nonlinear={'coordinate':i,'support':support,'Walsh_mask':mask,'degree':mask.bit_count(),'exact_coefficient':str(coef)};break
        if nonlinear:break
    assert nonlinear is not None;checks+=1
    out={'exact_assertions':checks,'replays':details,'nonclosed_single_spin_space_witness':nonlinear,'seconds':time.perf_counter()-t}
    json.dump(out,open(ROOT/'extended_audit_results.json','w'),indent=2);print(json.dumps(out,indent=2))
if __name__=='__main__':main()
