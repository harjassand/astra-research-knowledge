import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(61028)
I=np.eye(2);basis=[I/np.sqrt(2),np.array([[0,1],[1,0]])/np.sqrt(2),np.array([[0,-1j],[1j,0]])/np.sqrt(2),np.diag([1,-1])/np.sqrt(2)]
def feat(x):return np.r_[x*x,[2*x[i]*x[j] for i in range(4) for j in range(i+1,4)]]
anchors=list(np.eye(4))+[(np.eye(4)[i]+np.eye(4)[j])/np.sqrt(2) for i in range(4) for j in range(i+1,4)]
worst=0.;biasrat=0.;cases=0
for trial in range(25):
 eta=2.0**(-rng.integers(1,8));pi=rng.uniform(.1,1,10);pi/=sum(pi);n=10000;zeta=eta/(1e6*40*n)
 Fs=[];Ks=[];bs=[];ms=[]
 for x,p in zip(anchors,pi):
  g=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));rho=g@g.conj().T;rho/=np.trace(rho);U=2*rho+eta*I
  K=np.array([[np.trace(a@(U@b+b@U)/2).real for b in basis] for a in basis]);Fs.append(np.kron(feat(x)[:,None],np.eye(4)));Ks.append(K)
  v=rng.normal(size=4);bs.append(v/np.linalg.norm(v)*zeta);ms.append(np.ceil(n*p)+np.ceil(2+2/eta))
 V=sum(p*F@np.linalg.solve(K,F.T) for p,F,K in zip(pi,Fs,Ks));Vi=np.linalg.inv(V)
 cov=Vi@sum(100*p*p/m*F@np.linalg.solve(K,F.T) for p,m,F,K in zip(pi,ms,Fs,Ks))@Vi
 diff=100*Vi/n-cov;worst=max(worst,float(-np.linalg.eigvalsh((diff+diff.T)/2)[0]))
 bias=Vi@sum(p*F@np.linalg.solve(K,b) for p,F,K,b in zip(pi,Fs,Ks,bs));ratio=float(bias@V@bias/(zeta*zeta/eta));biasrat=max(biasrat,ratio)
 assert np.linalg.eigvalsh((diff+diff.T)/2)[0]>-1e-8 and ratio<=1+1e-8
 cases+=1
for _ in range(1000):
 eta=10**rng.uniform(-9,0);t=rng.random();c=1/16;u=3*t+32*eta;e=c*np.sqrt(eta*u)
 assert 2*t-2*e+2*eta>=t+1.25*eta-1e-12
 assert 2*t+2*e+2*eta<=3*t+2.75*eta+1e-12
out={'status':'PASS','independent_GLS_cases':cases,'Loewner_extreme_sign_cases':1000,'worst_covariance_bound_violation':worst,'max_bias_bound_ratio':biasrat,'source_calls':0,'scope':'matrix algebra diagnostics, not a matrix-query experiment'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
