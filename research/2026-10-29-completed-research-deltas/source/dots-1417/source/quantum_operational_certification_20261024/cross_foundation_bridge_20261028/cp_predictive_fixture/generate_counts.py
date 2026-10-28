"""Synthetic episode-count generator; plant is confined to this file.
One multinomial draw aggregates N independent whole-reset episodes per setting.
No laboratory acquisition or wall-clock execution of all represented calls occurs.
"""
import json
from pathlib import Path
import numpy as np
N=100_000_000
rng=np.random.default_rng(20261028)
# Columns are normalized preparation states in unnormalized Pauli coordinates.
P=np.array([[.5]*4,[0,.25,0,0],[0,0,.25,0],[0,0,0,.25]])
T=np.array([[2,0,0,0],[1,.5,0,0],[1,0,.5,0],[1,0,0,.5]])
W={};R=np.diag([1.,.8,.8,.8]);R[1:3,1:3]=.8*np.array([[.6,-.8],[.8,.6]])
W['rotate']=[R]
for j in range(1,4):
    w=np.zeros((4,4));w[:,0]=2*P[:,j];W[f'reset{j}']=[w]
for j in range(1,4):
    ws=[]
    for b in [1,-1]:
        w=np.zeros((4,4));w[0,0]=.5;w[0,j]=b*.25;ws.append(w)
    W[f'test{j}']=ws
H=T@P
base=[];shift=[]
for i in range(1,4):
    for j in range(4):
        c=int(rng.binomial(N,H[i,j]));base.append({'test':i,'prep':j,'counts':[c,N-c]})
for a,ws in W.items():
    for i in range(1,4):
        for j in range(4):
            probs=[]
            for w in ws:
                y=w@P[:,j];p=float(T[i]@y);t=float(2*y[0]);probs.extend([p,t-p])
            assert min(probs)>=0 and abs(sum(probs)-1)<1e-12
            shift.append({'action':a,'test':i,'prep':j,'counts':rng.multinomial(N,probs).tolist()})
output={'kind':'synthetic aggregate whole-reset episode counts','seed':20261028,'shots_per_setting':N,
        'observable_rank_upper_bound':4,'basis':'I,X,Y,Z','candidate_bloch_radii':['1/4','1/2','3/4'],
        'radius':'3/10000','confidence_estimands':156,'actions':{a:len(ws) for a,ws in W.items()},
        'settings':96,'represented_resets':96*N,'represented_native_calls':252*N,
        'resource_note':'Aggregate draws have the count law of the represented reset episodes; these were not actual laboratory interventions.',
        'base':base,'shift':shift}
# Base settings: 3+18=21 calls/shot. Shift:42+189=231. Total252.
assert len(base)+len(shift)==96
Path(__file__).with_name('counts.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({k:v for k,v in output.items() if k not in ['base','shift']},indent=2))
