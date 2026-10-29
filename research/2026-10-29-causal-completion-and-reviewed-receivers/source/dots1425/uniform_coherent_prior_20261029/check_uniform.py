import numpy as np,json
from lib import maps,P,I
rng=np.random.default_rng(202610291338);X=P[0];S=lambda a:-sum(x*np.log(x) for x in np.linalg.eigvalsh(a) if x>1e-14);T=lambda a,b:.5*sum(abs(np.linalg.eigvalsh(a-b)))
def randstate(n):
 g=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));r=g@g.conj().T;return r/np.trace(r)
def K(g,d):return [np.kron(X@np.diag([1,np.sqrt(1-g)]),np.eye(d)),np.kron(X@np.array([[0,np.sqrt(g)],[0,0]]),np.eye(d))]
max_un=0;max_ref=0;max_inverse=0;max_contract=0
for _ in range(300):
 gamma=rng.uniform(.5,.999);c=np.sqrt(1-gamma);aa=K(gamma,1);F=lambda r:sum(a@r@a.conj().T for a in aa);ensemble=[randstate(2) for _ in range(5)];sig=sum(ensemble)/5;delta=S(sig)-sum(map(S,ensemble))/5-S(F(sig))+sum(S(F(r)) for r in ensemble)/5;dist=sum(T(r,sig) for r in ensemble)/5;rat=dist*(1-c)/np.sqrt(delta);max_un=max(max_un,rat);assert rat<1+1e-10
 M,N,TT=maps(sig,gamma);max_inverse=max(max_inverse,np.linalg.norm(np.linalg.inv(M),2)*(1-c));max_contract=max(max_contract,np.linalg.norm(I if False else np.eye(3)-M,2)/c);assert np.linalg.norm(np.eye(3)-M,2)<=c+1e-10
 d=2;aa=K(gamma,d);F=lambda r:sum(a@r@a.conj().T for a in aa);omega=randstate(d);base=np.kron(sig,omega);ev,u=np.linalg.eigh(base);root=(u*np.sqrt(ev))@u.conj().T;h=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));h=(h+h.conj().T)/2;h-=np.trace(base@h)*np.eye(4);h*=.8/max(abs(np.linalg.eigvalsh(h)));pert=root@h@root;pair=[base+pert,base-pert];delta=S(base)-sum(map(S,pair))/2-S(F(base))+sum(S(F(r)) for r in pair)/2
 dist=0
 for r in pair:
  marginal=np.trace(r.reshape(2,d,2,d),axis1=0,axis2=2);dist+=T(r,np.kron(sig,marginal))/2
 rat=dist*(1-c)/(3*np.sqrt(delta));max_ref=max(max_ref,rat);assert rat<1+1e-10
out={'unreferenced_ensembles':300,'product_barycenter_reference_ensembles':300,'max_nonreference_ratio':float(max_un),'max_complete_ratio':float(max_ref),'max_recovered_Bloch_norm_over_c':float(max_contract),'max_inverse_norm_times_one_minus_c':float(max_inverse),'scope':'floating actual-prior diagnostics; analytic proof is governing'}
print(out);open('UNIFORM_CHECKS.json','w').write(json.dumps(out,indent=2)+'\n')
