"""Small exact stationary-flow and rational path-message diagnostic."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,math
import numpy as np

def weight(x,a,b):
    out=F(1)
    for i,z in enumerate(x):out*=a[i]**z
    for i in range(len(b)):out*=b[i]**(x[i]*x[i+1])
    return out

def messages(a,b,fix):
    n=len(a);beta=[[F(1),F(1)] for _ in range(n)]
    allowed=lambda i,z:i not in fix or fix[i]==z
    for i in range(n-2,-1,-1):
        for x in [0,1]:
            beta[i][x]=sum(a[i+1]**y*b[i]**(x*y)*beta[i+1][y]
                           for y in [0,1] if allowed(i+1,y))
    return sum(a[0]**x*beta[0][x] for x in [0,1] if allowed(0,x)),beta

def main():
    a=[F(4,5),F(5,4),F(4,5),F(5,4)]
    b=[F(4,5),F(5,4),F(4,5)]
    kappas=[F(1,3),F(2,3),F(1,2)]
    n=len(a);states=list(product([0,1],repeat=n));index={x:i for i,x in enumerate(states)}
    ws=[weight(x,a,b)for x in states];z=sum(ws);pi=[w/z for w in ws]
    q=[[F(0) for _ in states]for x in states]
    m0=F(4,5)**5
    minaccept=F(1);maxaccept=F(0)
    for si,x in enumerate(states):
        for i in range(n):
            r=a[i]
            if i:r*=b[i-1]**x[i-1]
            if i<n-1:r*=b[i]**x[i+1]
            y=list(x);y[i]=1-y[i];sj=index[tuple(y)]
            rate=(r if x[i]==0 else 1)/(1+r)
            q[si][sj]+=rate
        for i,kappa in enumerate(kappas):
            local=(x[i],x[i+1])
            cycle=[(0,0),(0,1),(1,1)]
            if local not in cycle:continue
            u,v=local
            wl=a[i]**u*a[i+1]**v*b[i]**(u*v)
            if i:wl*=b[i-1]**(x[i-1]*u)
            if i+2<n:wl*=b[i+1]**(v*x[i+2])
            accept=m0/wl
            assert 0<accept<=1
            minaccept=min(minaccept,accept);maxaccept=max(maxaccept,accept)
            y=list(x);y[i],y[i+1]=cycle[(cycle.index(local)+1)%3]
            q[si][index[tuple(y)]]+=kappa*accept
    for i in range(len(states)):q[i][i]=-sum(q[i])
    residual=[sum(pi[i]*q[i][j] for i in range(len(states)))for j in range(len(states))]
    assert all(v==0 for v in residual)
    detailed_balance_failures=sum(pi[i]*q[i][j]!=pi[j]*q[j][i]
        for i in range(len(states))for j in range(i))
    assert detailed_balance_failures>0
    qn=np.array([[float(v)for v in row]for row in q]);d=np.sqrt([float(v)for v in pi])
    weighted=-d[:,None]*qn/d[None,:]
    gap=float(np.linalg.eigvalsh((weighted+weighted.T)/2)[1])
    certificate=8*math.sqrt(5)-17
    assert gap>=certificate-1e-10
    zmsg,_=messages(a,b,{})
    zcond,_=messages(a,b,{0:1,3:1})
    assert zmsg==z
    zcond_enumerated=sum(w for x,w in zip(states,ws)if x[0]==1 and x[3]==1)
    assert zcond==zcond_enumerated
    result=dict(states=len(states),stationarity_exact=True,
        detailed_balance_failed_pairs=detailed_balance_failures,
        minimum_cycle_acceptance=str(minaccept),maximum_cycle_acceptance=str(maxaccept),
        certified_gap=certificate,numerical_actual_gap=gap,
        exact_partition=str(z),exact_conditioned_partition=str(zcond),
        exact_target_probability=str(zcond/z),
        transfer_message_matches_enumeration=True,
        scope='Exact rational flow and transfer checks; gap diagnostic is floating and the all-size proof is in LOCAL_PATH_CALIBRATION.txt.')
    Path(__file__).with_name('local_path_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
