import json, hashlib
import numpy as np
from scipy.linalg import expm
from pathlib import Path
p=Path(__file__).parent
rng=np.random.default_rng(572131)
I2=np.eye(2,dtype=complex)
h=.8; kappa=2*h
hs=np.diag([0.,h]); ls=np.array([[0,np.sqrt(2*h)],[0,0]],complex)
H=np.kron(hs,I2); L=np.kron(ls,I2); Id=np.eye(4,dtype=complex)
sqrtH=np.diag(np.sqrt(np.diag(H).real))
def herm(A): return (A+A.conj().T)/2
def randomV(scale=.23):
    x=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)); x=herm(x)
    return scale*x/np.linalg.norm(x,2)
def superop(V,lam,q):
    K=np.sqrt(lam)*V; D=L.conj().T@L
    return -1j*(np.kron(Id,K)-np.kron(K.T,Id))+lam*((1+q)*np.kron(L.conj(),L)-.5*(np.kron(Id,D)+np.kron(D.T,Id)))
def evolve(rho,V,lam,q,T):
    return (expm(T*superop(V,lam,q))@rho.reshape(-1,order='F')).reshape(4,4,order='F')
def mgf(rho,V,lam,q,T): return np.trace(evolve(rho,V,lam,q,T)).real
def adj(X,V,lam,q):
    K=np.sqrt(lam)*V; D=L.conj().T@L
    return 1j*(K@X-X@K)+lam*((1+q)*L.conj().T@X@L-.5*(D@X+X@D))
def constants(V,q):
    C=np.linalg.norm(sqrtH@V,2); a=4*q/(kappa-4*h*q); r=2*a*C*C/kappa
    return C,a,r
bell=np.array([1,0,0,1],complex)/np.sqrt(2)
rhos=[np.outer(bell,bell.conj())]
for i in range(4):
    x=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)); z=x@x.conj().T; rhos.append(z/np.trace(z))
Vs=[randomV() for i in range(4)]
rows=[]
for V in Vs:
 for rho in rhos:
  E0=np.trace(H@rho).real
  for lam in [.1,1.,20.]:
   for T in [.05,.5,2.]:
    for q in [.05,.15,.35,.49]:
     C,a,r=constants(V,q); W=Id+a*H
     actual=mgf(rho,V,lam,q,T); bound=(1+a*E0)*np.exp(r*T)
     residue=np.linalg.eigvalsh(herm(adj(W,V,lam,q)-r*W)).max()
     rows.append(dict(lam=lam,T=T,q=q,mgf=actual,bound=bound,ratio=actual/bound,residual_max_eigenvalue=residue))
# Exact un-driven source: Bell source excited probability 1/2, at most one jump.
undriven=[]
for lam in [.1,1.,20.]:
 for q in [.05,.49,2.]:
  exact=1+.5*q*(1-np.exp(-2*h*lam*.7))
  numeric=mgf(rhos[0],np.zeros((4,4)),lam,q,.7)
  undriven.append(dict(lam=lam,q=q,exact=exact,numeric=numeric,error=abs(numeric-exact)))
# Actual data instrument followed by outcome-adaptive Hamiltonian and miss probabilities.
P0=np.kron(I2,np.diag([1.,0.])); P1=Id-P0
q=.35; lam=3.; t1=.4; t2=.8; eta=.3
V0,V1,V2=Vs[:3]; Cenv=max(np.linalg.norm(sqrtH@V,2) for V in [V0,V1,V2])
a=4*q/(kappa-4*h*q); r=2*a*Cenv*Cenv/kappa
inter=evolve(rhos[0],V0,lam,q,t1)
full=sum(np.trace(evolve(P@inter@P,V,lam,q,t2)).real for P,V in [(P0,V1),(P1,V2)])
control_bound=(1+a*np.trace(H@rhos[0]).real)*np.exp(r*(t1+t2))
# Misses can have different probabilities by record; use common max eta.
inter_m=evolve(rhos[0],V0,lam,eta*q,t1)
miss=sum(np.trace(evolve(P@inter_m@P,V,lam,et*q,t2)).real for P,V,et in [(P0,V1,.05),(P1,V2,eta)])
am=4*eta*q/(kappa-4*h*eta*q); rm=2*am*Cenv*Cenv/kappa
miss_bound=(1+am*np.trace(H@rhos[0]).real)*np.exp(rm*(t1+t2))
# MGF derivative obtained from augmented moment evolution, avoiding finite differences.
V=Vs[0]; lam=2.; T=1.2; rho=rhos[0]; S=superop(V,lam,0); J=lam*np.kron(L.conj(),L)
aug=np.block([[S,np.zeros_like(S)],[J,S]])
x=expm(T*aug)@np.concatenate([rho.reshape(-1,order='F'),np.zeros(16)])
mean=np.trace(x[16:].reshape(4,4,order='F')).real
C=np.linalg.norm(sqrtH@V,2); E0=np.trace(H@rho).real
mean_bound=4*E0/kappa+8*C*C*T/kappa**2
# Warm initial common-cause correlation defeats multiplication of marginal means.
m=4; warm=.02; lamT=10
marginal=warm*(1-np.exp(-2*h*lamT))
all_selected=warm*(1-np.exp(-2*h*lamT))**m
res={
'source_sha256':hashlib.sha256((p/'SOURCE_FROZEN.md').read_bytes()).hexdigest(),
'grid_cases':len(rows),'grid_max_mgf_to_bound_ratio':max(z['ratio'] for z in rows),
'grid_max_LsW_minus_rW_eigenvalue':max(z['residual_max_eigenvalue'] for z in rows),
'grid_violations':[z for z in rows if z['ratio']>1+1e-10 or z['residual_max_eigenvalue']>1e-10],
'undriven_analytic_max_error':max(z['error'] for z in undriven),
'adaptive_instrument':{'mgf':full,'bound':control_bound,'W_contraction_residual':float(np.linalg.norm(P0@(Id+a*H)@P0+P1@(Id+a*H)@P1-(Id+a*H)))},
'conditional_thinning':{'mgf':miss,'bound':miss_bound,'eta':eta},
'derivative':{'actual_mean':mean,'bound':mean_bound},
'correlated_warm_counterexample':{'m':m,'warm_probability':warm,'marginal_event_probability':marginal,'all_selected_probability':all_selected,'product_marginals':marginal**m},
'example_rows':rows[:4],
'limitations':'Finite matrix checks corroborate signs/constants only; not a proof, dilation construction, hardware validation, or all-selected-location theorem.'}
assert not res['grid_violations']; assert full<=control_bound; assert miss<=miss_bound; assert mean<=mean_bound
(p/'check_tilted.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
