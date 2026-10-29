import numpy as np,json,itertools
from pathlib import Path
rng=np.random.default_rng(202610291239);I=np.eye(2);X=np.array([[0,1],[1,0]]);Z=np.diag([1,-1])
def kron(xs):
 a=np.ones((1,1),complex)
 for x in xs:a=np.kron(a,x)
 return a
def S(r):
 v=np.linalg.eigvalsh((r+r.conj().T)/2);v=v[v>1e-14];return -float(v@np.log(v))
def logarithm(r):
 v,U=np.linalg.eigh(r);return (U*np.log(np.maximum(v,1e-300)))@U.conj().T
def D(r,s):return -S(r)-float(np.trace(r@logarithm(s)).real)
def kraus(g,q):
 k0=np.diag([1,np.sqrt(1-g)]);k1=np.array([[0,np.sqrt(g)],[0,0]])
 return [np.sqrt(q)*k0,np.sqrt(q)*k1,np.sqrt(1-q)*X@k0@X,np.sqrt(1-q)*X@k1@X]
def choi(ks):return sum(np.outer(k.ravel(order='F'),k.ravel(order='F').conj()) for k in ks)
maxmarg=0.;mincp=1.;rows=[]
for g,q in itertools.product([.5,.6,.9,.999],[.01,.2,.5,.8,.99]):
 eta=1-g;V=np.zeros((8,2));V[0,0]=1;V[4,1]=V[2,1]=np.sqrt(eta);V[1,1]=np.sqrt(1-2*eta)
 assert np.linalg.norm(V.T@V-I)<1e-12
 jointks=[V.reshape(4,2,2)[:,e,:] for e in range(2)]
 for j in range(4):
  basis=np.zeros((2,2));basis.ravel()[j]=1
  out=sum(k@basis@k.T for k in jointks);red=np.trace(out.reshape(2,2,2,2),axis1=1,axis2=3);target=sum(k@basis@k.T for k in kraus(g,1))
  maxmarg=max(maxmarg,np.linalg.norm(red-target));assert np.linalg.norm(red-target)<1e-12
 ks=kraus(g,q);J=choi(ks);Jdiag=np.diag(np.diag(J));A=1-g*(1-q);B=1-g*q;alpha=1-np.sqrt(eta/(A*B));res=J-alpha*Jdiag;mineig=float(np.linalg.eigvalsh(res)[0]);mincp=min(mincp,mineig);assert mineig>-1e-12
 rows.append(dict(gamma=g,q=q,alpha=alpha,K=1/alpha,min_choi_residual_eigenvalue=mineig))
maxratio=0.;minmargin=1.
for trial in range(100):
 n=2;dR=2;d=8;params=[(.5+.49*rng.random(),rng.uniform(.02,.98)) for i in range(n)];ss=[np.diag([q,1-q]) for g,q in params]
 A=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));rho=A@A.conj().T;rho/=np.trace(rho);rR=np.trace(rho.reshape(4,2,4,2),axis1=0,axis2=2);tau=kron(ss+[rR]);out=rho.copy();de=rho.copy();alphas=[]
 for i,(g,q) in enumerate(params):
  lift=[kron([k if j==i else I for j in range(n)]+[np.eye(dR)]) for k in kraus(g,q)];out=sum(k@out@k.conj().T for k in lift)
  z=kron([Z if j==i else I for j in range(n)]+[np.eye(dR)]);de=(de+z@de@z)/2
  alphas.append(1-np.sqrt((1-g)/((1-g*(1-q))*(1-g*q))))
 loss=D(rho,tau)-D(out,tau);dloss=D(rho,tau)-D(de,tau);a=min(alphas);assert loss>=a*dloss-1e-11;minmargin=min(minmargin,loss-a*dloss);maxratio=max(maxratio,dloss/loss)
result=dict(explicit_broadcast_marginal_residual=float(maxmarg),min_choi_residual_eigenvalue=mincp,CP_rows=rows,correlated_reference_trials=100,max_observed_loss_ratio=maxratio,min_proved_margin=minmargin,scope='Floating diagnostics of exact CP and relative-entropy proof; no native physical implementation.')
Path(__file__).with_name('THERMAL_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k!='CP_rows'})
