from pathlib import Path
import math,json,itertools
import numpy as np
max_ratio=0.;tests=0
for d in [.001,.01,.1,.3]:
    M=np.array([[1+d/3,d/2],[d/2,1-d/4]])
    assert np.linalg.norm(M-np.eye(2),2)<=d
    for a in [1e-100,1e-30,1e-6,1.,1e30,1e100]:
        A=np.diag([0.,a]);C=(1+.7*d)*A;B=np.linalg.solve(M,C);lam=float(np.trace(B))
        for s in [0.,1e-8,.01,.1,1.,10.,1e4]:
            EA=np.diag([1.,math.exp(-s)])
            EB=np.eye(2)-((-math.expm1(-s*lam/a))/lam)*B
            error=float(np.linalg.norm(EA-EB,2));bound=8*d/(1-d)
            assert error<=bound+1e-12
            max_ratio=max(max_ratio,error/bound);tests+=1
N=6;target=(0,1,0,1,0,1);zeta=.05;beta=1.
states=list(itertools.product([0,1],repeat=N));idx={x:i for i,x in enumerate(states)}
blocks=[(0,1,2),(3,4,5)];types=[0,1,0,1,0,1]
btable=np.array([[.7,1.2,.9,1.8],[1.4,.8,1.7,1.1]])
bmin=float(np.min(btable));bmax=float(np.max(btable))
neighbors={i:tuple(j for j in V if j!=i) for V in blocks for i in V}
def E(x):
    s=[2*sum(x[i] for i in V)-3 for V in blocks]
    return -.12*(s[0]**2+s[1]**2)-.09*s[0]*s[1]
J=0.
for x in states:
    for i in range(N):
        y=list(x);y[i]=1-y[i];J=max(J,abs(E(tuple(y))-E(x)))
H=J/2+math.log(4*N*bmax/(zeta*bmin))/(2*beta)
Acor=bmin*math.exp(beta*(H-J/2));Berr=bmax*math.exp(-beta*(H-J/2))
t=math.log(4*N/zeta)/Acor
W=np.array([sum(a!=b for a,b in zip(x,target)) for x in states],float)
L=np.zeros((64,64))
for row,x in enumerate(states):
    for i in range(N):
        y=list(x);y[i]=1-y[i];y=tuple(y)
        pat=2*x[neighbors[i][0]]+x[neighbors[i][1]]
        dPin=2*H if x[i]==target[i] else -2*H
        rate=btable[types[i],pat]*math.exp(-beta*(E(y)-E(x)+dPin)/2)
        L[row,idx[y]]+=rate;L[row,row]-=rate
assert max(L@W-(N*Berr-(Acor+Berr)*W))<1e-10
R=float(max(-np.diag(L)));P=np.eye(64)+L/R
assert min(P.flat)>-1e-13
rt=R*t;v=np.zeros(64);v[idx[target]]=1
weight=math.exp(-rt);acc=weight*v;total_weight=weight
for k in range(1,math.ceil(rt+15*math.sqrt(rt)+100)+1):
    v=P@v;weight*=rt/k;acc+=weight*v;total_weight+=weight
assert abs(total_weight-1)<1e-12
worst_error=float(1-min(acc));cert=N*math.exp(-Acor*t)+N*Berr/Acor
assert worst_error<=cert+1e-10 and cert<=zeta/2+1e-12
throttle=math.exp(-beta*(H+J/2));rate_cap=R*throttle
assert rate_cap<=N*bmax+1e-10
res={'status':'PASS','rank_one_mass_metric_cases':tests,'max_error_over_certificate':max_ratio,'writer':{'N':N,'target':target,'zeta':zeta,'J':J,'H':H,'minimum_correction_rate':Acor,'maximum_wrong_rate':Berr,'t':t,'worst_source_wrongstring_probability':worst_error,'first_moment_certificate':cert,'global_throttle':throttle,'throttled_total_rate':rate_cap,'throttled_duration':t/throttle},'scope':'Finite independent analytic-structure diagnostics; no physical hardware trial, asymptotic proof or novelty claim.'}
Path(__file__).with_name('check_mass_metric_and_writer_result.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
