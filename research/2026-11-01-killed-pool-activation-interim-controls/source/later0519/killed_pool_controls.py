"""Exact finite-state killed-generator solves for the new activation bridge.

Numerical controls, not asymptotic proof or physical chemistry. All timing is
the original mass-action clock. No stationary mixing/averaging is used.
"""
import math,json,hashlib
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix,csc_matrix
from scipy.sparse.linalg import splu
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/mechanism_selection_20261101'
def falling(x,k):
    if x<k:return 0
    return math.prod(range(x-k+1,x+1))
def solve_case(model,N):
    m=3;B=4;activity=falling(B,4);D=1 if model=='bistable' else 4;eta=1/(m*D+1)
    if model=='bistable':
        states=[(a,N-a) for a in range(N+1)]
        complexes=[(0,3),(1,2),(2,1),(3,0)]
        reactions=[]
        for i,(b,d) in enumerate(zip((1.,.01,11.11),(11.11,.01,1.))):
            reactions.extend(((complexes[i],complexes[i+1],b),(complexes[i+1],complexes[i],d)))
    elif model=='cascade':
        assert N%3==0
        states=[(a,N-a-d,d) for a in range(0,N+1,3) for d in range(0,N-a+1,3)]
        complexes=[(0,3,0),(0,0,3),(3,0,0)]
        reactions=[(complexes[i],complexes[(i+1)%3],1.) for i in range(3)]
    else:
        states=[(a,N-a-d,d) for a in range(N+1) for d in range(N-a+1)]
        complexes=[(0,3,0),(0,2,1),(0,1,2),(0,0,3),(1,0,2),(2,0,1),(3,0,0)]
        rates=(1.,2.,3.,5.,7.,11.,13.)
        reactions=[(complexes[i],complexes[(i+1)%len(complexes)],rates[i]) for i in range(len(complexes))]
    lookup={s:i for i,s in enumerate(states)};dim=len(states);rows=[];cols=[];vals=[];diag=np.zeros(dim)
    scale=activity*N**m
    kill=np.array([activity*falling(s[0],m) for s in states]);act=np.array([B*s[0] for s in states],float);imm=np.ones(dim)
    reward=np.array([math.prod(1/(1+b*(s[0]-m+b)) for b in range(1,m+1)) if s[0]>=m else 0. for s in states])
    for i,s in enumerate(states):
      for y,z,k in reactions:
        r=activity*k*math.prod(falling(v,j) for v,j in zip(s,y))
        if not r:continue
        t=tuple(v+j-h for v,h,j in zip(s,y,z));j=lookup[t]
        rows.append(i);cols.append(j);vals.append(-r/scale);diag[i]+=r/scale
    diag+=(kill+act+imm)/scale
    rows.extend(range(dim));cols.extend(range(dim));vals.extend(diag)
    H=csc_matrix(coo_matrix((vals,(rows,cols)),shape=(dim,dim)))
    rhs=np.column_stack((np.ones(dim)/scale,kill/scale,act/scale,imm/scale,kill*reward/scale,
                         kill*np.array([s[0]/N for s in states])/scale))
    lu=splu(H);v=lu.solve(rhs)
    residual=float(np.max(abs(H@v-rhs)));probs=float(np.max(abs(v[:,1:4].sum(axis=1)-1)))
    assert residual<2e-10 and probs<2e-9 and v.min()>-1e-11
    a0=lookup[(0,N)] if model=='bistable' else lookup[(0,N,0)]
    ratio=v[:,4]/v[:,2];worst=int(np.argmax(ratio));maxt=int(np.argmax(v[:,0]))
    forcing_bound=activity*math.factorial(m)*v[:,0]
    assert np.max(v[:,4]-forcing_bound)<2e-11
    return {'model':model,'population':N,'states':dim,'activation_order_D':D,'candidate_power_gain':eta,
        'max_mean_first_terminal_time':float(v[maxt,0]),'max_time_scaled_by_new_power':float(v[maxt,0]*N**(m-1+eta)),
        'max_mean_time_state':states[maxt],'max_weighted_clear_to_activation_ratio':float(ratio[worst]),
        'max_ratio_state':states[worst],'all_input_killed_equation_residual':residual,
        'all_input_terminal_probability_sum_error':probs,
        'pure_C_entrance':dict(zip(('mean_time','P_clear','P_activation','P_immigration','weighted_terminal_up_reward','unconditional_terminal_A_fraction'),map(float,v[a0])))}
def main():
    rows=[]
    for model,pops in (('bistable',(24,48,96,192,384)),('cascade',(24,48,96,192,384)),('mixed_cycle',(24,48,96,192))):
      for n in pops:
        r=solve_case(model,n);rows.append(r)
        print(json.dumps({k:r[k] for k in ('model','population','states','max_time_scaled_by_new_power','max_weighted_clear_to_activation_ratio')}),flush=True)
    result={'status':'PASS finite killed-generator and weighted actual-terminal controls',
       'new_candidate':'uniform first-killing time O(N^(-(m-1+1/(mD+1)))) from finite activation order D, with actual terminal inverse-population reward',
       'rows':rows,'scope':'floating linear solves on exact finite CME state spaces; no proof of global recurrence or asymptotic constants',
       'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'killed_pool_controls.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
