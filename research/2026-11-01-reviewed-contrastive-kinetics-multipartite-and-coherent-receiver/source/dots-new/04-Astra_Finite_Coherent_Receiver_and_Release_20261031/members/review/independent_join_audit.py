"""Independent finite-cascade, geometry and retained-correlation release checks.
All finite-cavity calculations below are diagnostics, never cutoff certificates.
"""
from pathlib import Path
import json,itertools
import numpy as np
from scipy.linalg import expm
from scipy.sparse import csc_matrix,eye,kron as skron
from scipy.sparse.linalg import expm_multiply
from scipy.integrate import solve_ivp
from fractions import Fraction as F
from exact_source_overlap import certify_overlap
from certify_scalar_budget import receive
root=Path(__file__).resolve().parent
rng=np.random.default_rng(4872);checks=[]
def check(name,ok,**data):
 if not bool(ok):raise AssertionError((name,data))
 checks.append(dict(name=name,**data))
def close(name,x,y,tol=2e-10):
 er=float(np.linalg.norm(x-y));check(name,er<tol,error=er,tolerance=tol)
def k(*xs):
 r=np.array([[1.]])
 for x in xs:r=np.kron(r,x)
 return r
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);sm=np.array([[0,1],[0,0]],complex)
SW=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],complex)
def ptr(rho,dims,keep):
 ds=list(dims);r=rho.reshape(*(ds+ds))
 for idx in reversed(range(len(ds))):
  if idx not in keep:r=np.trace(r,axis1=idx,axis2=idx+len(ds));ds.pop(idx)
 return r.reshape(int(np.prod(ds)),int(np.prod(ds)))
def unit(n):
 a=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));return np.linalg.qr(a)[0]
# The geometric lemma must work for contractions, including non-normal ones.
for n in [2,5,9]:
 for sample in range(30):
  u=unit(n);v=unit(n);O=u@np.diag(rng.random(n))@v.conj().T
  basis=unit(n);p0=basis[:,0];chi=basis[:,1];a=[0,1,.2,.9,.999999][sample%5];delta=1-a*a;p=a*p0+np.sqrt(delta)*chi
  f=np.vdot(p,O@p);f0=np.vdot(p0,O@p0);r=abs(f0);R=abs(1-f0)
  e1=delta*(1+r)+2*np.sqrt(delta*(1-delta))*np.sqrt(max(0,1-r*r))
  check('root_contraction_complex_bound',abs(f-f0)<=e1+3e-14)
  check('root_uncorrected_bound',abs(1-f)<=R+2*delta+2*np.sqrt(2*delta*R)+3e-14)
  if r>1e-15:check('root_paid_phase_bound',abs(1-np.conj(f0/r)*f)<=(np.sqrt(1-r)+np.sqrt(delta*(1+r)))**2+3e-14)

# Source/output coherent overlap via a separate time-bin vacuum collision model.
# This retains source amplitudes, projects each output bin onto the coherent bra,
# and never substitutes a reduced-source overlap for the full output overlap.
collision=[]
for lam,b,T in [(4,.2,1),(64,.2,.3)]:
 nc=4;aa=np.diag(np.sqrt(np.arange(1,nc)),1);L=np.sqrt(lam)*sm;H=np.sqrt(lam)*b*X;beta=-2j*b
 B=np.array([[-2*b*b,np.sqrt(lam)*b],[np.sqrt(lam)*b,-lam/2-2*b*b]])
 exact=expm(T*B)[0,0];errors=[]
 for N in [200,400,800]:
  dt=T/N;V=expm(np.sqrt(dt)*(k(L,aa.T)-k(L.conj().T,aa))-1j*dt*k(H,np.eye(nc)))
  al=beta*np.sqrt(dt);coh=np.array([np.exp(-abs(al)**2/2)*al**j/np.sqrt(float(__import__('math').factorial(j))) for j in range(nc)])
  M=np.empty((2,2),complex)
  for si,so in itertools.product(range(2),repeat=2):M[so,si]=np.vdot(coh,V[so*nc:(so+1)*nc,si*nc])
  amp=np.linalg.matrix_power(M,N)[0,0];errors.append(abs(amp-exact))
 check('collision_overlap_converges_to_complete_field_projection',errors[2]<errors[1]<errors[0],errors=errors)
 collision.append(dict(lam=lam,b=b,T=T,errors=errors))

# Independently build a coherent-output-source (L1=beta Z) cascaded with cavity.
def coherent_lab(b,ke,ki,eta,T,nc):
 a=np.diag(np.sqrt(np.arange(1,nc)),1);num=a.T@a;Lc=np.sqrt(ke)*a;chi=(ke+ki)/2;beta=-2j*b
 Lp=np.sqrt(eta)*beta*np.eye(nc)+Lc;Lm=-np.sqrt(eta)*beta*np.eye(nc)+Lc
 hc=(Lc.conj().T*(np.sqrt(eta)*beta)-np.conj(np.sqrt(eta)*beta)*Lc)/(2j)
 Hp=chi*num+hc;Hm=-chi*num-hc;Id=np.eye(nc)
 G=-1j*(k(Id,Hp)-k(Hm.T,Id))
 pairs=[(Lp,Lm),(np.sqrt(1-eta)*beta*Id,-np.sqrt(1-eta)*beta*Id),(np.sqrt(ki)*a,np.sqrt(ki)*a)]
 for lp,lm in pairs:G+=k(lm.conj(),lp)-.5*k(Id,lp.conj().T@lp)-.5*k((lm.conj().T@lm).T,Id)
 v=np.zeros(nc*nc);v[0]=1;rho=(expm(T*G)@v).reshape(nc,nc,order='F')
 return np.trace(rho),rho[0,0]
coherent=[]
for b,ke,ki,eta,T in [(.2,8,0,1,1),(.2,7.8,.2,.96,.7),(.4,2,.3,.7,2),(.2,8,0,0,1)]:
 kk=ke+ki;zeta=eta*ke/kk;pc=kk*(1+1j)/2
 f0=np.exp(-8*b*b*(1-zeta)*T+4*zeta*b*b/pc*(-3+4*np.exp(-pc*T)-np.exp(-2*pc*T)))
 f,vac=coherent_lab(b,ke,ki,eta,T,12);close('coherent_finite_cascade_loss_and_phase',f,f0,3e-9)
 coherent.append(dict(b=b,ke=ke,ki=ki,eta=eta,T=T,formula=[f0.real,f0.imag],physical=[f.real,f.imag],vacuum_projection_difference=abs(f-vac)))

# Exact algebraic reduced moment identities tested on arbitrary initial source/
# downstream correlations, not only trajectories reachable from a product state.
nc=3;dims=[2,nc,2,2,2];n=int(np.prod(dims));a=np.diag(np.sqrt(np.arange(1,nc)),1)
Ls=np.sqrt(5)*k(sm,np.eye(nc),np.eye(8));Lc=np.sqrt(3)*k(I,a,np.eye(8));eta=.7
Xs=k(X,np.eye(nc),np.eye(8));Zd=k(I,np.eye(nc),Z,I,I);cs=.4
h=rng.normal(size=(8,8))+1j*rng.normal(size=(8,8));h=(h+h.conj().T)/2;H0=k(I,np.eye(nc),h)
Hcas=(Lc.conj().T@(np.sqrt(eta)*Ls)-(np.sqrt(eta)*Ls).conj().T@Lc)/(2j)
H=H0+cs*Xs@Zd+Hcas
jumps=[np.sqrt(eta)*Ls+Lc,np.sqrt(1-eta)*Ls,.2*k(I,a,np.eye(8))]
for sample in range(5):
 v=rng.normal(size=n)+1j*rng.normal(size=n);v/=np.linalg.norm(v);rho=np.outer(v,v.conj())
 dr=-1j*(H@rho-rho@H)
 for L in jumps:Q=L.conj().T@L;dr+=L@rho@L.conj().T-(Q@rho+rho@Q)/2
 R=ptr(rho,dims,[2,3,4]);Y=ptr(Xs@rho,dims,[2,3,4]);z=k(Z,I,I)
 Rdot=ptr(dr,dims,[2,3,4]);Ydot=ptr(Xs@dr,dims,[2,3,4])
 close('source_blind_swap_R_closure_correlated_cavity',Rdot,-1j*(h@R-R@h)-1j*cs*(z@Y-Y@z))
 close('source_blind_swap_Y_closure_correlated_cavity',Ydot,-1j*(h@Y-Y@h)-1j*cs*(z@R-R@z)-2.5*Y)
 p=float(np.trace(ptr(rho,dims,[0])@np.diag([0,1])).real)
 check('correlated_source_Y_energy_bound',np.linalg.norm(Y,ord='nuc')<=2*np.sqrt(p*(1-p))+1e-12)

# Actual source -> finite cavity -> finite chi ramp -> SWAP; source remains ON.
def full_release(lam,b,ke,ki,eta,T,ts,tau,nc):
 dims=[2,nc,2,2,2];n=int(np.prod(dims));ii=eye(n,format='csc');aa=np.diag(np.sqrt(np.arange(1,nc)),1)
 sop=csc_matrix(k(sm,np.eye(nc),np.eye(8)));cav=csc_matrix(k(I,aa,np.eye(8)));Xs=sop+sop.conj().T;Zd=csc_matrix(k(I,np.eye(nc),Z,I,I));num=cav.conj().T@cav
 Ls=np.sqrt(lam)*sop;Lc=np.sqrt(ke)*cav;Hcas=(Lc.conj().T@(np.sqrt(eta)*Ls)-(np.sqrt(eta)*Ls).conj().T@Lc)/(2j)
 Hbase=np.sqrt(lam)*b*Xs@Zd+Hcas
 def comm(h):return -1j*(skron(ii,h,format='csc')-skron(h.T,ii,format='csc'))
 G=comm(Hbase)
 for L in [np.sqrt(eta)*Ls+Lc,np.sqrt(1-eta)*Ls,np.sqrt(ki)*cav]:
  Q=L.conj().T@L;G+=skron(L.conj(),L,format='csc')-.5*skron(ii,Q,format='csc')-.5*skron(Q.T,ii,format='csc')
 Gchi=comm(Zd@num);chi=(ke+ki)/2
 # D/reference maximally entangled, M in a non-ground state, cold source/cavity.
 vec=np.zeros(n,complex);tensor=vec.reshape(dims)
 for d in [0,1]:
  tensor[0,0,d,0,d]=np.sqrt(.3)/np.sqrt(2);tensor[0,0,d,1,d]=1j*np.sqrt(.7)/np.sqrt(2)
 rho=np.outer(vec,vec.conj());v=expm_multiply(T*(G+chi*Gchi),rho.reshape(n*n,order='F'))
 solution=solve_ivp(lambda t,y:G@y+(chi*(1-t/ts))*(Gchi@y),(0,ts),v,rtol=2e-10,atol=2e-12)
 check('actual_finite_ramp_solver_completed',solution.success)
 pre=solution.y[:,-1].reshape(n,n,order='F');p=float(np.trace(ptr(pre,dims,[0])@np.diag([0,1])).real)
 check('ramp_preserves_actual_source_energy_bound',p<=4*b*b/lam+1e-9,p=p,bound=4*b*b/lam)
 W=csc_matrix(k(I,np.eye(nc),SW,I));Hswap=np.pi/(2*tau)*W
 actual=expm_multiply(tau*(G+comm(Hswap)),pre.reshape(n*n,order='F')).reshape(n,n,order='F')
 ideal=W@pre@W.conj().T
 ar=ptr(actual,dims,[3,4]);ir=ptr(ideal,dims,[3,4]);err=float(np.linalg.norm(ar-ir,ord='nuc'));bound=16*b*b/lam+8*b*b*tau
 check('finite_SWAP_receives_actual_cascade_correlations',err<=bound+2e-8,actual_error=err,bound=bound)
 # Subsequent old-apparatus unitary can be arbitrary but must exclude memory/ref.
 oldU=expm(-.71j*k(X,np.eye(nc),X,I,I));post=oldU@actual@oldU.conj().T
 close('post_release_local_apparatus_no_signalling',ptr(post,dims,[3,4]),ar)
 # Before-SWAP exact source overlap + uncorrected coherent/ramp bound.
 a=certify_overlap(F(lam),F(str(b)),F(str(T))+F(str(ts)));al=float(F(a['amplitude_interval'][0]));d=1-al*al
 kk=ke+ki;zeta=eta*ke/kk;pc=kk*(1+1j)/2;f0=np.exp(-8*b*b*(1-zeta)*T+4*zeta*b*b/pc*(-3+4*np.exp(-pc*T)-np.exp(-2*pc*T)))
 R=abs(1-f0)+24*b*b*ts;prebound=R+2*d+2*np.sqrt(2*d*R)
 phi=np.eye(2).reshape(4)/np.sqrt(2);target=np.outer(phi,phi)
 preerr=float(np.linalg.norm(ptr(pre,dims,[2,4])-target,ord='nuc'));allerr=float(np.linalg.norm(ar-target,ord='nuc'))
 check('full_reference_entangled_pre_SWAP_bound',preerr<=prebound+2e-8,actual_error=preerr,bound=prebound)
 check('full_released_reference_entangled_bound',allerr<=prebound+bound+2e-8,actual_error=allerr,bound=prebound+bound)
 return dict(lam=lam,b=b,ke=ke,ki=ki,eta=eta,T=T,ramp=ts,swap=tau,nc=nc,source_excitation=p,actual_before_error=preerr,before_upper=prebound,actual_SWAP_difference=err,swap_upper=bound,released_Choi_error=allerr,released_upper=prebound+bound,scope='Finite-cavity numerical diagnostic, including actual retained source/cavity correlations; not an infinite-mode certificate.')
release=[]
for args in [(64,.2,7.8,.2,.96,.7,.01,.02,4),(4096,.2,127.872,.128,.999,1,.0001,.001,4)]:release.append(full_release(*args))

# Bare-source lower bound independently evaluated over the entire certified grid.
rows=json.loads((root/'scalar_budget_certificates.json').read_text())['rows'];passed=0
for r in rows:
 p=r['parameters'];lam=float(F(p['lambda']));b=float(F(p['b']));T=float(F(p['T']));c=np.sqrt(lam)*b
 v=expm(T*np.array([[0,-2j*c],[-2j*c,-lam/2]]))@np.array([1,0]);err=abs(1-v[0]);lo=float(F(r['unchanged_source_complete_channel_lower']))
 check('unchanged_source_lower_bound',lo<=err+3e-10)
 passed+=r['meets_declared_model_budget']
check('grid_retains_successes_and_failures',0<passed<len(rows),passing=passed,failing=len(rows)-passed)
result={'checks':len(checks),'details':checks,'collision_source_projection':collision,'coherent_reference':coherent,'full_release':release,'grid':{'rows':len(rows),'pass':passed,'fail':len(rows)-passed},'scope':'Independent mathematical joins and floating diagnostics; source-field geometry supplies no-cutoff proof. No apparatus services acquired.'}
(root/'independent_join_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='details'},indent=2))
