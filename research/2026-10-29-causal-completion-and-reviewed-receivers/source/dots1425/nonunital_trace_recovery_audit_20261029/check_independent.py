import numpy as np,sympy as sp,json,hashlib
from scipy.integrate import quad
from pathlib import Path
pdir=Path(__file__).parent;src=pdir.parent/'nonunital_trace_recovery_comparator_20261029'
for manifest in ['SHA256SUMS.txt','BIASED_SHA256SUMS.txt','ACTUAL_PRIOR_SHA256SUMS.txt']:
 for line in (src/manifest).read_text().splitlines():
  if line.strip():
   h,f=line.split(maxsplit=1);assert hashlib.sha256((src/f.lstrip('*')).read_bytes()).hexdigest()==h
# Exact symbolic map action: parameter eta rather than gamma.
e,p=sp.symbols('eta p',positive=True);q=1-p;r=e*q
K=[sp.Matrix([[0,sp.sqrt(e)],[1,0]]),sp.diag(0,sp.sqrt(1-e))]
D=sp.diag(sp.sqrt(p),sp.sqrt(q));Ninv=sp.diag(1/sp.sqrt(r),1/sp.sqrt(1-r))
R=[D*k.T*Ninv for k in K]
E01=sp.Matrix([[0,1],[0,0]])
F=lambda x:sum((k*x*k.T for k in K),sp.zeros(2))
RF=lambda x:sp.simplify(sum((k*F(x)*k.T for k in R),sp.zeros(2)))
coef=sp.simplify(RF(E01)[0,1]);a2=e*p/(1-e+e*p)
assert sp.simplify(coef**2-a2)==0
assert RF(E01)[1,0]==0
assert sp.simplify(sum((k.T*k for k in R),sp.zeros(2)))==sp.eye(2)
# Choi support has unique product ray, for every eta>0.
x,y=sp.symbols('x y');assert sp.det(sp.Matrix([[0,x],[sp.sqrt(e)*x,y]]))==-sp.sqrt(e)*x*x
rng=np.random.default_rng(130911);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);mins={'fidelity_margin':1.,'projection_margin':1.,'trace_bound_margin':1.};maxres=0;cases=0

def ent(A):
 v=np.linalg.eigvalsh((A+A.conj().T)/2);assert min(v)>-1e-10;v=v[v>1e-13];return -float(v@np.log(v))
def root(A):
 v,u=np.linalg.eigh((A+A.conj().T)/2);return (u*np.sqrt(np.maximum(0,v)))@u.conj().T
def td(A,B):return float(abs(np.linalg.eigvalsh((A-B+A.conj().T-B.conj().T)/2)).sum()/2)
for gamma in [.5,.7,.99]:
 eta=1-gamma;ks=[X@np.diag([1,np.sqrt(eta)]),np.diag([0,np.sqrt(gamma)])]
 for pv in [.0001,.1,eta/(1+eta),.9,.9999]:
  sv=np.array([pv,1-pv]);nv=np.array([eta*(1-pv),1-eta*(1-pv)])
  rs=[np.diag(np.sqrt(sv))@k.conj().T@np.diag(1/np.sqrt(nv)) for k in ks]
  a=np.sqrt(eta*pv/(gamma+eta*pv));theta=np.log(a)
  # Independent quadrature for beta-average, alongside its elementary Fourier expression.
  kap=quad(lambda t:np.pi/(2*(np.cosh(np.pi*t)+1))*np.cos(t*theta),-25,25,epsabs=1e-12)[0]
  maxres=max(maxres,abs(kap-theta/np.sinh(theta)));z=a*kap
  for d in [1,2,4]:
   lifts=[np.kron(k,np.eye(d)) for k in ks];recs=[np.kron(k,np.eye(d)) for k in rs];zz=np.kron(Z,np.eye(d))
   for rank in [1,2*d]:
    A=rng.normal(size=(2*d,rank))+1j*rng.normal(size=(2*d,rank));rho=A@A.conj().T;rho/=np.trace(rho)
    out=sum(k@rho@k.conj().T for k in lifts);unrot=sum(k@out@k.conj().T for k in recs)
    rec=unrot.copy();rec[:d,d:]*=kap;rec[d:,:d]*=kap
    # Off-diagonal multiplier and trace preservation are checked before using the inequality.
    assert np.linalg.norm(rec[:d,d:]-z*rho[:d,d:])<1e-12
    assert abs(np.trace(rec)-1)<1e-12 and np.linalg.eigvalsh(rec)[0]>-1e-12
    L=ent(out)-ent(rho)+np.trace(out@np.kron(np.diag(np.log(nv)),np.eye(d))).real-np.trace(rho@np.kron(np.diag(np.log(sv)),np.eye(d))).real
    sr=root(rho);fid=float(np.trace(root(sr@rec@sr)).real);fid=min(1.,fid)
    fm=L+2*np.log(fid);mins['fidelity_margin']=min(mins['fidelity_margin'],fm);assert fm>-2e-6
    deph=(rho+zz@rho@zz)/2;dist=td(rho,deph);recoverdist=td(rho,rec)
    pm=recoverdist-(1-z)*dist;mins['projection_margin']=min(mins['projection_margin'],pm);assert pm>-1e-10
    bm=np.sqrt(max(0,L))/(1-a)-dist;mins['trace_bound_margin']=min(mins['trace_bound_margin'],bm);assert bm>-1e-10
    cases+=1
out={'manifests_verified':True,'exact_symbolic_Petz_coefficient_squared':str(a2),'exact_symbolic_TP_and_unique_product_ray':'pass','actual_averaged_recovery_cases':cases,'reference_dimensions':[1,2,4],'minimum_margins':mins,'beta_characteristic_quadrature_residual':maxres,'scope':'Exact symbolic Petz arithmetic plus independent floating actual-average recovery/fidelity tests; not proof of imported recovery theorem or hardware.'}
(pdir/'INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
