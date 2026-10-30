"""Falsification-only check of graph-path transfer, not a proof."""
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as sla, json
out=[]
for n in [12,24,48,96]:
    states=[(a,c,n-a-c) for a in range(n+1) for c in range(n-a+1)]
    ix={x:i for i,x in enumerate(states)}; rows=[];cols=[];dat=[];diag=np.zeros(len(states))
    a0=3; v=2; q=7; m=5
    for i,x in enumerate(states):
        # Residual pure-complex cycle 2A -> 2C -> 2D -> 2A.
        for j in range(3):
            if x[j]>=2:
                rate=x[j]*(x[j]-1); y=list(x);y[j]-=2;y[(j+1)%3]+=2
                rows.append(i);cols.append(ix[tuple(y)]);dat.append(-rate);diag[i]+=rate
        diag[i]+=x[0]*(x[0]-1)
    M=sp.csc_matrix((dat+list(diag),(rows+list(range(len(states))),cols+list(range(len(states))))),shape=(len(states),len(states)))
    solve=sla.factorized(M)
    aa=np.array([x[0] for x in states],float); A=aa+a0
    clock=A*(A-1)*(A-2)
    T=solve(1/clock);U=solve(A/clock)
    s=4.;g=np.where(aa>=2,(1+np.maximum(aa-2,0))**(-s),0.)
    reset=solve(aa*(aa-1)*g)
    ratio=reset/(1+A)**(-s)
    samples=[]
    for a in [0,2,int(n**.5),n//2,n]:
        x=(a,n-a,0);i=ix[x]
        samples.append({'state':x,'T_over_U':float(T[i]/U[i]),'output_profile_ratio':float(ratio[i])})
    out.append({'n':n,'states':len(states),'max_profile_ratio':float(ratio.max()),'max_time_occupation_ratio':float((T/U).max()),'samples':samples})
print(json.dumps(out,indent=2))
