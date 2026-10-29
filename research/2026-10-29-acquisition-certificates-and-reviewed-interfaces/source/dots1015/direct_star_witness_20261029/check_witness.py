import json,numpy as np
from pathlib import Path
rng=np.random.default_rng(202610290945)
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);pa=[X,Y,Z]
e=np.eye(4);bell=[(e[1]-e[2])/2**.5,(e[0]+e[3])/2**.5,(e[0]-e[3])/2**.5,(e[1]+e[2])/2**.5];sign=[-1,1,1,1]
res=[]
for k in range(40):
 q=rng.normal(size=4);q/=np.linalg.norm(q);V=q[0]*I-1j*sum(q[j+1]*pa[j] for j in range(3));W=np.kron(I,V);states=[W@v for v in bell];S=sum(s*np.outer(v,v.conj()) for s,v in zip(sign,states))
 # Random Stinespring isometry gives generic, usually nonunital channel.
 A=rng.normal(size=(16,4))+1j*rng.normal(size=(16,4));Q,_=np.linalg.qr(A);Ks=[Q[4*j:4*j+4] for j in range(4)]
 N=lambda rho:sum(K@rho@K.conj().T for K in Ks)
 target=float((1-np.trace(S@N(S))/4).real);mean=0.;pflip=0.
 for s,v in zip(sign,states):
  rho=N(np.outer(v,v.conj()));tmean=np.trace(S@rho).real;mean+=(1-s*tmean)/4;pflip+=(1-s*tmean)/8
 residual=abs(mean-target);assert residual<1e-12 and -1e-12<=pflip<=1+1e-12
 res.append(dict(target=target,mean=mean,pflip=pflip,residual=residual,nonunital_norm=float(np.linalg.norm(N(np.eye(4))-np.eye(4)))))
out=dict(scope='Floating diagnostic of exact signed-ensemble identity, not physical observation',cases=len(res),max_residual=max(x['residual'] for x in res),results=res)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out['max_residual'])
