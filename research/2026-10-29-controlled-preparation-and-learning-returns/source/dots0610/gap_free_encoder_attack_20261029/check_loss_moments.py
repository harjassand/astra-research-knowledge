import numpy as np,itertools,json
from scipy.linalg import qr
rng=np.random.default_rng(106291)
I=np.eye(2,dtype=complex);P=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1,-1]).astype(complex)]
vec=[]
for p in P:
 e,v=np.linalg.eigh(p);vec.append({-1:v[:,0],1:v[:,1]})
rows=[]
for case in range(24):
 q=rng.normal(size=4);q/=np.linalg.norm(q);v=q[0]*I-1j*sum(q[j+1]*P[j] for j in range(3));C=np.array([[np.trace(P[a]@v@P[b]@v.conj().T).real/2 for b in range(3)]for a in range(3)])
 Q,_=np.linalg.qr(rng.normal(size=(16,4))+1j*rng.normal(size=(16,4)));ks=[Q[4*j:4*j+4] for j in range(4)]
 S=.5*(np.eye(4)+sum(C[a,b]*np.kron(P[a],P[b]) for a in range(3)for b in range(3)))
 delta=1-sum(np.trace(S@k.conj().T@S@k).real for k in ks)/4
 m1=m2=0.
 for c,d in itertools.product(range(3),repeat=2):
  for u,w in itertools.product([-1,1],repeat=2):
   inp=np.kron(vec[c][u],vec[d][w]);rho=sum(np.outer(k@inp,(k@inp).conj()) for k in ks)
   for a,b in itertools.product(range(3),repeat=2):
    corr=np.trace(np.kron(P[a],P[b])@rho).real
    # yz is a Bernoulli sign with mean corr; only this product enters estimator.
    for yz in [-1,1]:
     prob=(1+yz*corr)/2/324
     x=.75-2.25*yz*C[a,b]-20.25*yz*u*w*C[a,b]*C[c,d]
     m1+=prob*x;m2+=prob*x*x
 assert abs(m1-delta)<1e-12 and abs(m2-(747/16+1.5*delta))<1e-11
 rows.append(dict(case=case,delta=delta,mean=m1,second=m2,predicted_second=747/16+1.5*delta,nonunital_norm=float(np.linalg.norm(sum(k@k.conj().T for k in ks)-np.eye(4)))))
print(json.dumps(dict(cases=24,rows=rows,max_mean_error=max(abs(x['delta']-x['mean']) for x in rows),max_second_error=max(abs(x['second']-x['predicted_second']) for x in rows)),indent=2))
