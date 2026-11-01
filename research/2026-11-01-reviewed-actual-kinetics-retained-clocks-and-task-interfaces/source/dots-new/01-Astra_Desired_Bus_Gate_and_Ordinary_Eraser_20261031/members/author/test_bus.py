"""Independent-style author diagnostics; no finite Fock cutoff is an infinite-mode proof."""
from pathlib import Path
import json,math
import numpy as np
import sympy as sy
import mpmath as mp
from scipy.integrate import solve_ivp,quad
from scipy.optimize import minimize
from scipy.linalg import expm
from numpy.polynomial.hermite import hermgauss
from fractions import Fraction as Q
from certify_bus import IV,pi_interval,exp_neg,sqrt,certify
ROOT=Path(__file__).resolve().parent
checks=[]
def ck(name,condition,**extra):
 assert bool(condition),(name,extra);checks.append(dict(name=name,**extra))
def close(name,a,b,tol=1e-9):
 er=float(np.linalg.norm(np.asarray(a)-np.asarray(b)));ck(name,er<tol,error=er,tolerance=tol)
# Exact analytic filter ODE, endpoint, pulse area and phase integrals.
t,beta,k=sy.symbols('t beta k',positive=True,real=True)
f=(1-sy.cos(t))/sy.sqrt(24);D=beta**2+1
z=(1-(beta**2*sy.cos(t)+beta*sy.sin(t))/D-sy.exp(-beta*t)/D)/sy.sqrt(24)
ck('symbolic_filter_equation',sy.simplify(sy.diff(z,t)+beta*z-beta*f)==0)
ck('symbolic_initial_filter',sy.simplify(z.subs(t,0))==0)
ck('symbolic_final_filter',sy.simplify(z.subs(t,2*sy.pi)-(1-sy.exp(-2*sy.pi*beta))/(sy.sqrt(24)*D))==0)
ck('exact_bus_integrated_occupation',sy.integrate(f*f,(t,0,2*sy.pi))==sy.pi/8)
ck('exact_extra_envelope_energy',sy.integrate(sy.diff(f,t)**2,(t,0,2*sy.pi))==sy.pi/24)
ck('zero_force_endpoints',all(sy.simplify(v.subs(t,x))==0 for v in [f,sy.diff(f,t)] for x in [0,2*sy.pi]))
# Complete finite-cavity off-diagonal blocks independently propagated.
T=2*np.pi;kappa=.2;Phi=np.pi/8;I=Phi;A=kappa*I
C=1/np.sqrt(6)
def force(t):
 f=C*np.sin(t/2)**2;fp=C*np.sin(t)/2
 return np.exp(1j*t)*(-f+1j*(fp+kappa*f/2))
finite=[]
for ncut in [10,14]:
 a=np.diag(np.sqrt(np.arange(1,ncut)),1).astype(complex);ad=a.T;n=ad@a;rho0=np.zeros((ncut,ncut),complex);rho0[0,0]=1
 for m,nn in [(2,-2),(2,0),(0,-2)]:
  def rhs(t,v):
   r=v.reshape(ncut,ncut);e=force(t);h=e*ad+e.conjugate()*a
   return (-1j*(m*h@r-nn*r@h)+kappa*(a@r@ad-(n@r+r@n)/2)).reshape(-1)
  sol=solve_ivp(rhs,[0,T],rho0.reshape(-1),rtol=2e-11,atol=2e-12,max_step=.035)
  value=np.trace(sol.y[:,-1].reshape(ncut,ncut));expected=np.exp(1j*Phi*(m*m-nn*nn)-A*(m-nn)**2/2)
  close('actual_finite_bus_coherence',value,expected,tol=2e-8 if ncut==10 else 2e-9)
  finite.append(dict(cutoff=ncut,m=m,n=nn,coherence=[float(value.real),float(value.imag)],error=float(abs(value-expected))))
# Receiver capture from independent ODE + quadrature including finite tail.
for B in [1,2,4,8,16]:
 W=1/B
 def rhs(t,v):return [B*((C*np.sin(t/2)**2) if t<=T else 0)-B*v[0],v[0]**2]
 sol=solve_ivp(rhs,[0,T+W],[0.,0.],rtol=3e-12,atol=1e-13,max_step=.01)
 r=np.exp(-B*T);D=B*B+1
 F=(T*(1+B*B/(2*D))-(1-r)/(B*D*D))/24-(1-r)**2*np.exp(-2*B*W)/(48*B*D*D)
 close('finite_receiver_capture',sol.y[1,-1],F,2e-10)
# Quadrature instrument at arbitrary angle, gain, accessible/lost amplitudes.
x,weights=hermgauss(90)
for Ac,L,theta,gain in [(.2,.01,np.pi/2,1),(.17,.03,.8,.7),(.4,.2,.1,1.3)]:
 mu=np.sqrt(2*Ac)*np.cos(theta);nu=np.sqrt(2*Ac)*np.sin(theta);kk=gain*nu
 for m,nn in [(2,-2),(2,0),(0,-2)]:
  # wavefunction product divided by vacuum density exp(-x²)/sqrt(pi)
  product=np.exp(mu*(m+nn)*x-mu*mu*(m*m+nn*nn)/2+1j*(kk-nu)*(m-nn)*x+1j*Ac*np.cos(theta)*np.sin(theta)*(m*m-nn*nn))
  value=np.dot(weights,product)/np.sqrt(np.pi)*np.exp(-L*(m-nn)**2/2)
  Le=L+mu*mu/2+(kk-nu)**2/2;ph=kk*mu/2
  close('general_homodyne_instrument',value,np.exp(-Le*(m-nn)**2/2+1j*ph*(m*m-nn*nn)),2e-12)
# Exact full diamond formula versus direct input/eigenvalue optimization.
def diamond(L):
 a=np.exp(-2*L);w=1-a;q=1-a**4
 return q if q>=2*w else 4*w*w/(4*w-q)
for L in [.0001,.01,.1,.3,.7,2,10]:
 m=np.array([-2,0,2]);M=np.exp(-L*(m[:,None]-m[None,:])**2/2)-1
 def objective(p):
  p=np.maximum(p,0);v=np.sqrt(p);ev=np.linalg.eigvalsh(M*v[:,None]*v[None,:]);return -sum(abs(ev))
 ans=minimize(objective,[.33,.34,.33],method='SLSQP',bounds=[(0,1)]*3,constraints=[dict(type='eq',fun=lambda p:sum(p)-1)],options={'ftol':1e-13,'maxiter':500})
 close('diamond_formula_direct_optimization',-ans.fun,diamond(L),4e-8)
# Warm/correlated apparatus cancellation: no initial product or vacuum premise.
rng=np.random.default_rng(27189)
B=np.diag([2,0,0,-2]);d=7;aa=np.diag(np.sqrt(np.arange(1,d)),1);P=(aa-aa.T)/(1j*np.sqrt(2));p,U=np.linalg.eigh(P)
Ugate=expm(1j*Phi*B@B);coupling=expm(-1j*.7*np.kron(B,P));fullgate=np.kron(Ugate,np.eye(d))@coupling
for trial in range(6):
 v=rng.normal(size=4*d)+1j*rng.normal(size=4*d);v/=np.linalg.norm(v);rho=np.outer(v,v.conj())
 def partial(r):return np.trace(r.reshape(4,d,4,d),axis1=1,axis2=3)
 target=Ugate@partial(rho)@Ugate.conj().T;after=fullgate@rho@fullgate.conj().T;out=np.zeros((4,4),complex)
 for j in range(d):
  bra=np.kron(np.eye(4),U[:,j].conj().reshape(1,d));branch=bra@after@bra.conj().T;corr=expm(1j*.7*p[j]*B);out+=corr@branch@corr.conj().T
 close('arbitrary_correlated_warm_cancellation',out,target,3e-13)
# The drive really is finite-slew; the certificate is a conservative envelope.
grid=np.linspace(0,T,10001);eps=np.array([force(t) for t in grid]);f=C*np.sin(grid/2)**2;fp=C*np.sin(grid)/2;fpp=C*np.cos(grid)/2
alpha1=np.exp(1j*grid)*(fp+1j*f);alpha2=np.exp(1j*grid)*(fpp+2j*fp-f);ep=1j*alpha2+1j*kappa*alpha1/2
ck('drive_peak_envelope',max(abs(eps))<np.sqrt(17/75),observed=float(max(abs(eps))))
ck('drive_slew_envelope',max(abs(ep))<53/(20*np.sqrt(6)),observed=float(max(abs(ep))))
# Resource identity and sharp lower bound on random closed paths, with detuning.
for sample in range(12):
 coeff=rng.normal(size=5)+1j*rng.normal(size=5);om=rng.uniform(-3,3);Delta=rng.uniform(-2,2)
 al=np.zeros_like(grid,dtype=complex);da=al.copy()
 for j,c in enumerate(coeff,1):
  al+=c*np.sin(j*grid/2)*np.exp(1j*om*grid)
  da+=c*(j/2*np.cos(j*grid/2)+1j*om*np.sin(j*grid/2))*np.exp(1j*om*grid)
 integ=lambda v:np.trapezoid(v,grid)
 ii=integ(abs(al)**2);gam=integ(np.imag(al.conj()*da));ph=gam+Delta*ii;energy=integ(abs(da+(kappa/2+1j*Delta)*al)**2)
 lower=ph*ph/ii+(kappa*kappa/4+np.pi*np.pi/T**2)*ii
 ck('resource_lower_bound_random_path',energy>=lower-1e-8,margin=float(energy-lower))
# Independent high precision checks on every exact certificate interval.
mp.mp.dps=110
cert=json.loads((ROOT/'bus_certificates.json').read_text())
def inside(name,value,record):
 lo,hi=map(Q,record['interval']);mpq=lambda x:mp.mpf(x.numerator)/x.denominator
 ck(name,mpq(lo)<=value<=mpq(hi),width=str(mpq(hi-lo)))
inside('pi_interval',mp.pi,cert['pi'])
inside('unmonitored_exact_interval',1-mp.exp(-mp.pi/5),cert['unmonitored_exact_bus_diamond'])
g=mp.mpf('.477');tt=2*mp.pi;ph=mp.pi/8;kk=mp.mpf('.26');emin=g*g*tt
imin=2*ph*ph/(emin+mp.sqrt(emin*emin-4*kk*ph*ph))
inside('minimum_occupation_exact_interval',imin,cert['all_closed_fixed_B_minimum_I'])
inside('all_closed_unmonitored_lower_interval',1-mp.exp(-mp.mpf('1.6')*imin),cert['all_closed_fixed_B_unmonitored_diamond_lower'])
for row in cert['rows']:
 B=mp.mpf(row['parameters']['beta']);TT=2*mp.pi;DD=B*B+1;rr=mp.exp(-B*TT);WW=1/B
 FF=(TT*(1+B*B/(2*DD))-(1-rr)/(B*DD*DD))/24-(1-rr)**2*mp.exp(-2*B*WW)/(48*B*DD*DD)
 ac=mp.mpf('0.999')*mp.mpf('.2')*FF;loss=mp.pi/40-ac;err=1-mp.exp(-8*loss)
 inside('capture_fraction_exact_interval',FF/(mp.pi/8),row['captured_fraction']);inside('complete_bus_exact_interval',err,row['exact_bus_diamond'])
 total=err+mp.mpf('.0004')*(TT+WW+mp.mpf('.01'))+4*mp.sqrt(ac/2)*mp.mpf('.00001')+2*mp.exp(-25)/(5*mp.sqrt(mp.pi))+mp.mpf('.001')
 inside('complete_budget_exact_interval',total,row['complete_error_upper'])
result={'scope':'Author checks; exact symbolic/interval checks separated from floating finite-cutoff diagnostics','checks':checks,'check_count':len(checks),'finite_cavity_diagnostics':finite}
(ROOT/'test_bus_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checks':len(checks),'finite_cavity_runs':len(finite),'status':'PASS'},indent=2))
