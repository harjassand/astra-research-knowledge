"""Independent desired-gate, optimal-recovery, all-port and warm-scope audit."""
from pathlib import Path
import numpy as np,json
from scipy.linalg import expm
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import sympy as sy
root=Path(__file__).resolve().parent;rng=np.random.default_rng(6492);checks=[]
def ck(name,ok,**data):
 if not bool(ok):raise AssertionError((name,data))
 checks.append(dict(name=name,**data))
def close(name,a,b,tol=2e-10):
 er=float(np.linalg.norm(a-b));ck(name,er<tol,error=er,tolerance=tol)
def pt(rho,ds,keep):
 ds=list(ds);r=rho.reshape(*(ds+ds))
 for j in reversed(range(len(ds))):
  if j not in keep:r=np.trace(r,axis1=j,axis2=j+len(ds));ds.pop(j)
 return r.reshape(int(np.prod(ds)),int(np.prod(ds)))
def partial_transpose_R(rho,dA):return rho.reshape(dA,2,dA,2).transpose(0,3,2,1).reshape(2*dA,2*dA)
def randunit(n):
 a=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));return np.linalg.qr(a)[0]
B=np.array([2,0,0,-2]);Phi=np.pi/8;Ug=np.diag(np.exp(1j*Phi*B*B));Z=np.diag([1,-1]);ZZ=np.kron(Z,Z)
close('bus_itself_produces_entangler_up_to_global_phase',Ug,np.exp(1j*np.pi/4)*expm(1j*np.pi/4*ZZ))

def diamond(L):
 a=np.exp(-2*L);w=1-a;q=1-a**4
 return q if q>=2*w else 4*w*w/(4*w-q)
a_star=brentq(lambda a:a+a*a+a*a*a-1,.5,.6);L_star=-np.log(a_star)/2
for L in [0,1e-8,.001,.1,L_star-1e-6,L_star,L_star+1e-6,1,10]:
 a=np.exp(-2*L);w=1-a;q=1-a**4;x=.5 if q>=2*w else w/(4*w-q)
 ps=np.array([x,1-2*x,x]);K=np.exp(-L*(np.array([-2,0,2])[:,None]-np.array([-2,0,2])[None,:])**2/2)-1
 exact_input=K*np.sqrt(ps[:,None]*ps[None,:]);close('diamond_formula_attaining_input',np.linalg.norm(exact_input,ord='nuc'),diamond(L))
 C=np.exp(-L*(B[:,None]-B[None,:])**2/2)
 for j in range(10):
  v=rng.normal(size=16)+1j*rng.normal(size=16);v/=np.linalg.norm(v);rho=np.outer(v,v.conj())
  out=(rho.reshape(4,4,4,4)*(C-1)[:,None,:,None]).reshape(16,16)
  ck('diamond_bound_arbitrary_data_reference',np.linalg.norm(out,ord='nuc')<=diamond(L)+2e-12)

# Exact SDP dual witness for Bell-fidelity recovery of the embedded dephasing qubit.
# Objective C: Tr(C J_R); trace-preserving Choi constraint Tr_output J_R=I.
t=sy.symbols('t',nonnegative=True)
C=sy.Matrix([[1,0,0,t],[0,0,0,0],[0,0,0,0],[t,0,0,1]])/4
Y=(1+t)*sy.eye(2)/4;dual=sy.kronecker_product(sy.eye(2),Y)-C
vals=dual.eigenvals();ck('exact_recovery_dual_eigenvalues',len(vals)==3 and all(any(sy.simplify(v-w)==0 for w in [sy.Integer(0),t/2,(t+1)/4]) for v in vals))
phi=sy.Matrix([1,0,0,1]);Jid=phi*phi.T
ck('exact_recovery_dual_identity_saturation',sy.simplify(sy.trace(C*Jid)-sy.trace(Y))==0)
# Captured field can be nonorthogonal; data branch labels make accessible vectors orthogonal.
recovery=[]
for L in [.001,.1,1]:
 t=np.exp(-8*L);alpha=.4;vp=np.array([1,alpha,alpha*alpha/np.sqrt(2)],complex);vp/=np.linalg.norm(vp);vm=vp*np.array([1,-1,1])
 xp=np.kron([1,0],vp);xm=np.kron([0,1],vm);x=np.kron(xp,[1,0]);y=np.kron(xm,[0,1])
 rho=(np.outer(x,x.conj())+np.outer(y,y.conj())+t*np.outer(x,y.conj())+t*np.outer(y,x.conj()))/2
 norm=float(np.linalg.norm(partial_transpose_R(rho,6),ord='nuc'));close('captured_field_Bell_negativity',norm,1+t)
 for j in range(12):
  U=randunit(6);Ufull=np.kron(U,np.eye(2));after=Ufull@rho@Ufull.conj().T;out=pt(after,[2,3,2],[0,2])
  bell=np.array([1,0,0,1])/np.sqrt(2);F=float(np.vdot(bell,out@bell).real)
  ck('arbitrary_CPTP_recovery_Bell_bound',F<=(1+t)/2+1e-12)
  ck('arbitrary_CPTP_recovery_negativity_contraction',np.linalg.norm(partial_transpose_R(out,2),ord='nuc')<=1+t+1e-12)
 recovery.append(dict(L=L,lost_overlap=t,partial_transpose_norm=norm,optimal_Bell_fidelity=(1+t)/2,complete_error_lower=1-t))

# Separate exact finite-dimensional quadrature identity with arbitrary data,
# reference, and apparatus correlations and nontrivial passive preprocessing.
# It tests the correction algebra, not a finite-Fock approximation to CCR.
for trial in range(8):
 d=6;basis=randunit(d);eigen=np.linspace(-3,3,d);P=basis@np.diag(eigen)@basis.conj().T;U0=randunit(d)
 v=rng.normal(size=4*2*d)+1j*rng.normal(size=4*2*d);v/=np.linalg.norm(v);rho=np.outer(v,v.conj())
 BB=np.kron(np.diag(B),np.eye(2));coupling=expm(-1j*.9*np.kron(BB,P));gate=np.kron(Ug,np.eye(2*d));prep=np.kron(np.eye(8),U0)
 state=gate@coupling@prep@rho@prep.conj().T@coupling.conj().T@gate.conj().T
 final=np.zeros((8,8),complex)
 for j in range(d):
  bra=np.kron(np.eye(8),basis[:,j].conj().reshape(1,d));block=bra@state@bra.conj().T;corr=expm(1j*.9*eigen[j]*BB);final+=corr@block@corr.conj().T
 old=pt(rho,[4,2,d],[0,1]);target=np.kron(Ug,np.eye(2))@old@np.kron(Ug.conj().T,np.eye(2))
 close('warm_correlated_full_access_with_reference_and_passive_U0',final,target,3e-12)

# Independent original bus ODE and geometric phase, including nonzero detunings.
T=2*np.pi;kap=.2;C0=1/np.sqrt(6);physical=[]
for Delta in [-2,0,1.7]:
 om=1-Delta
 def force(t):
  f=C0*np.sin(t/2)**2;fp=C0*np.sin(t)/2
  al=np.exp(1j*om*t)*f;dal=np.exp(1j*om*t)*(fp+1j*om*f)
  return 1j*dal+(1j*kap/2-Delta)*al
 def rhs(t,v):
  al=v[0]+1j*v[1];e=force(t);da=-(kap/2+1j*Delta)*al-1j*e
  return [da.real,da.imag,abs(al)**2,-np.real(e*np.conj(al))]
 sol=solve_ivp(rhs,[0,T],[0,0,0,0],rtol=3e-12,atol=1e-13,max_step=.015)
 close('actual_bus_closes',sol.y[:2,-1],np.zeros(2),1e-10);close('actual_bus_occupation',sol.y[2,-1],np.pi/8,2e-10);close('actual_bus_entangling_phase',sol.y[3,-1],np.pi/8,3e-10)
 physical.append(dict(detuning=Delta,phase=sol.y[3,-1],occupation=sol.y[2,-1],residual_displacement=float(np.linalg.norm(sol.y[:2,-1]))))

# Two-port filter energy balance includes stored cavity at the finite endpoint.
filters=[]
for beta in [1,2,4,8,16]:
 W=1/beta
 def rhs(t,y):
  f=C0*np.sin(t/2)**2 if t<=T else 0;z=y[0]
  return [beta*(f-z),z*z,(f-z)**2,f*f]
 sol=solve_ivp(rhs,[0,T+W],[0,0,0,0],rtol=3e-12,atol=1e-13,max_step=.005)
 z,trans,refl,input_=sol.y[:,-1];stored=z*z/beta
 close('finite_filter_all_ports_storage_conservation',trans+refl+stored,input_,5e-11)
 loss=kap*np.pi/8-.999*kap*trans;accounted=kap*(refl+stored+.001*trans)
 close('finite_receiver_loss_partition',loss,accounted,5e-11)
 ck('finite_filter_storage_not_silently_collected',stored>0)
 filters.append(dict(beta=beta,transmission_energy=kap*trans,reflection_energy=kap*refl,stored_energy=kap*stored,detector_loss=.001*kap*trans,total_inaccessible=loss))

# Poincare equality shape is not the finite-slew envelope: endpoints retain force.
x,Delta=sy.symbols('x Delta',real=True);aa=sy.sin(x/2)*sy.exp(sy.I*(1-Delta)*x)
eps=sy.I*sy.diff(aa,x)+(sy.I*sy.Rational(1,10)-Delta)*aa
ck('sine_energy_saturator_has_nonzero_endpoint_force',sy.simplify(eps.subs(x,0))==sy.I/2)
# Exact same-variance counterexample to the draft's unsupported general noise formula.
sigma=.25;gain=1;pair_difference=4
actual=np.cos(gain*sigma*pair_difference);gaussian=np.exp(-gain*gain*sigma*sigma*pair_difference**2/2)
ck('non_Gaussian_record_noise_counterexample',1-actual>1-gaussian+0.05)
noise={'law':'independent centered Rademacher noise ±1/4, correction gain 1','variance':1/16,'extreme_pair_actual_coherence':actual,'claimed_Gaussian_coherence':gaussian,'actual_extreme_pair_error_lower':1-actual,'incorrect_Gaussian_diamond_prediction':1-gaussian,'valid_general_variance_bound':8*gain*gain*sigma*sigma,'required_fix':'Exact L_eff addition requires Gaussian noise. Otherwise use characteristic function; centered independent noise has diamond upper (diam(B)^2/2)*gain^2*variance.'}
result={'checks':len(checks),'details':checks,'diamond_branch_boundary_L':L_star,'recovery_witnesses':recovery,'bus_phases':physical,'finite_filter_energy_partition':filters,'record_noise_counterexample':noise,'scope':'Independent proof checks and diagnostics; no hardware acquisition or vacuum-to-warm extrapolation.'}
(root/'independent_bus_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='details'},indent=2))
