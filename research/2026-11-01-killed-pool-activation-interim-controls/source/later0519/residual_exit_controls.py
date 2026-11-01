"""Full-CME first residual exit; overflow is absorbed and reported explicitly.

This is not a closed truncation or a recurrence test. Fast internal dynamics
are non-complex-balanced: cycle rates 1,2,3 violate 1*3=2^2 on collinear
complexes, a necessary complex-balance identity for this directed cycle.
"""
import math,json,hashlib
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix,csc_matrix
from scipy.sparse.linalg import splu
from killed_pool_controls import falling
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/mechanism_selection_20261101'
def h(b):return b-b//4
def solve_level(r,Bmax=20):
    m=3;q=4;cx=((0,3,0),(0,2,1),(0,1,2),(0,0,3),(1,0,2),(2,0,1),(3,0,0));ks=(1,2,3,5,7,11,13)
    states=[]
    for b in range(Bmax+1):
        n=r+h(b)
        states.extend((a,n-a-d,d,b) for a in range(n+1) for d in range(n-a+1))
    ix={s:i for i,s in enumerate(states)};d=len(states);rows=[];cols=[];vals=[];rhs=np.zeros((d,4))
    for i,s in enumerate(states):
        a,c,z,b=s;n=a+c+z;channels=[]
        activity=falling(b,q)
        if activity:
          for j,(y,k) in enumerate(zip(cx,ks)):
            rate=activity*k*math.prod(falling(v,t) for v,t in zip(s[:3],y))
            if rate:
                target=cx[(j+1)%len(cx)]
                ss=tuple(v+u-w for v,w,u in zip(s[:3],y,target))+(b,)
                channels.append((rate,ss))
        channels.append((1.,(a+1,c,z,b+1)))
        if a and b:channels.append((a*b,(a+2,c,z,b+3)))
        if a>=m and b>=q:channels.append((falling(a,m)*activity,(a-m,c,z,b-q)))
        total=sum(v for v,t in channels);rows.append(i);cols.append(i);vals.append(1.)
        rhs[i,3]=1/total
        for rate,t in channels:
            nr=sum(t[:3])-h(t[3]);p=rate/total
            if nr==r+1:rhs[i,0]+=p
            elif nr==r-1:rhs[i,1]+=p
            else:
                assert nr==r
                if t[3]>Bmax:rhs[i,2]+=p
                else:rows.append(i);cols.append(ix[t]);vals.append(-p)
    H=csc_matrix(coo_matrix((vals,(rows,cols)),shape=(d,d)));v=splu(H).solve(rhs)
    residual=float(np.max(abs(H@v-rhs)));sumerror=float(np.max(abs(v[:,:3].sum(axis=1)-1)))
    assert residual<2e-9 and sumerror<2e-8 and v.min()>-1e-9
    safe=np.array([i for i,s in enumerate(states) if q<=s[3]<2*q])
    low=ix[(0,r+h(m),0,m)]
    pmax=int(safe[np.argmax(v[safe,0]+v[safe,2])])
    result={'residual':r,'states':d,'B_overflow_boundary':Bmax,
       'max_safe_high_input_up_plus_overflow':float(v[pmax,0]+v[pmax,2]),
       'maximizing_input':states[pmax],
       'up_probability':float(v[pmax,0]),'explicit_overflow_probability':float(v[pmax,2]),
       'max_safe_high_input_mean_exit_time':float(v[safe,3].max()),
       'dormant_low_entrance_up_probability':float(v[low,0]),
       'all_input_equation_residual':residual,'all_input_probability_sum_error':sumerror}
    return result
def main():
    rows=[]
    for r in (8,16,24):
        v=solve_level(r);rows.append(v);print(json.dumps(v),flush=True)
    result={'status':'PASS finite full-CME open-boundary residual controls','rows':rows,
       'noncomplex_balance_witness':'directed-cycle complex flows require k0*k2=k1^2 for 3C,2C+D,C+2D; actual rates give 3!=4',
       'scope':'finite floating Dirichlet solves; up+overflow is an upper bound for first-up probability at the named safe entrances, not a global recurrence theorem',
       'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'residual_exit_controls.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
