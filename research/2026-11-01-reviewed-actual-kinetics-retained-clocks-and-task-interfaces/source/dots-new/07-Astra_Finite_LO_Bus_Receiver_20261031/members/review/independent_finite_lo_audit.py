"""Independent quantum beam-splitter, CP overflow, warm-boundary and control audit."""
from pathlib import Path
from fractions import Fraction as F
import json,math
import numpy as np
from scipy.linalg import expm
from scipy.sparse import diags,kron,eye
from scipy.sparse.linalg import expm_multiply
from scipy.stats import poisson
root=Path(__file__).resolve().parent;rng=np.random.default_rng(39042);checks=[]
def ck(name,ok,**extra):
 if not bool(ok):raise AssertionError((name,extra))
 checks.append(dict(name=name,**extra))
def close(name,a,b,tol=2e-10):
 e=float(np.linalg.norm(a-b));ck(name,e<tol,error=e,tolerance=tol)
j=json.loads((root/'finite_lo_certificates.json').read_text());S=float(F(j['rows'][3]['source_beta8_collected_energy']['interval'][0]));ell=float(F(j['rows'][3]['source_beta8_lost_energy']['interval'][0]));b=np.array([-2,0,2]);nlo=4;theta=np.arctan(2*np.sqrt(S/nlo))/2
# Genuine two-mode quantum BS evolution, not coherent-amplitude substitution.
n=28;a=diags(np.sqrt(np.arange(1,n)),1,shape=(n,n),format='csc');aa=kron(a,eye(n),format='csc');bb=kron(eye(n),a,format='csc');G=(aa.conj().T@bb-aa@bb.conj().T)*(np.pi/4)
lo=np.array([np.exp(-nlo/2)*(1j*np.sqrt(nlo))**k/np.sqrt(float(math.factorial(k))) for k in range(n)])
ck('LO_truncation_diagnostic_norm',abs(np.vdot(lo,lo)-1)<1e-12)
counts=np.indices((n,n));diff=(counts[0]-counts[1]).reshape(-1);all_counts=(counts[0]+counts[1]).reshape(-1)
optical={};kernels={}
for initial in [0,1]:
 source=np.zeros(n);source[initial]=1;inputs=[]
 for B in b:
  alpha=B*np.sqrt(S);dis=expm((alpha*(a.conj().T-a)).toarray());inputs.append(np.kron(dis@source,lo))
 outputs=expm_multiply(G,np.stack(inputs,axis=1));optical[initial]=outputs
 corrected=outputs*np.exp(1j*diff[:,None]*theta*b[None,:]);K=corrected.T@corrected.conj();kernels[initial]=K
 close('quantum_BS_branch_normalization',np.diag(K),np.ones(3),3e-12)
v=np.exp(-(np.sqrt(nlo+4*S)-np.sqrt(nlo))**2/2);theory=np.array([[1,v,1],[v,1,v],[1,v,1]])
close('quantum_BS_two_number_kernel_matches_exact_vacuum_formula',kernels[0],theory,2e-11)
ck('warm_one_photon_does_not_inherit_vacuum_kernel',np.linalg.norm(kernels[1]-kernels[0])>1e-3)

# Exact branch-total count distribution and finite-cap fallback on actual optical state.
outputs=optical[0];mask=all_counts<=20
corrected=outputs*np.exp(1j*diff[:,None]*theta*b[None,:]);fallback=outputs.copy();fallback[mask]=corrected[mask]
Kcap=fallback.T@fallback.conj();Kideal=corrected.T@corrected.conj();bad=np.sum(abs(outputs[~mask])**2,axis=0)
close('total_count_tail_from_quantum_BS',bad,poisson.sf(20,nlo+b*b*S),2e-12)
# Explicit arbitrary-reference channel differences, not only input populations.
for _ in range(30):
 vv=rng.normal(size=9)+1j*rng.normal(size=9);vv/=np.linalg.norm(vv);rho=np.outer(vv,vv.conj());change=(rho.reshape(3,3,3,3)*(Kcap-Kideal)[:,None,:,None]).reshape(9,9)
 ck('overflow_complete_channel_reference_bound',np.linalg.norm(change,ord='nuc')<=2*max(bad)+2e-11)

# Unequal passive efficiencies: directly evaluate unobserved coherent overlaps,
# independently sum observed number amplitudes, and check the deterministic phase sign.
def coherent(z):
 c=np.zeros(81,complex);c[0]=np.exp(-abs(z)**2/2)
 for m in range(80):c[m+1]=c[m]*z/np.sqrt(m+1)
 return c
unequal=[]
for eta1,eta2 in [(1,1),(.4,.9),(0,1),(.999,.997),(.274,.354)]:
 A=np.sqrt(S);L=np.sqrt(nlo);zp=(b*A+1j*L)/np.sqrt(2);zm=(b*A-1j*L)/np.sqrt(2)
 cp=np.stack([coherent(np.sqrt(eta1)*z) for z in zp]);cm=np.stack([coherent(np.sqrt(eta2)*z) for z in zm]);m=np.arange(81)
 observed=(cp*np.exp(1j*theta*b[:,None]*m))@(cp*np.exp(1j*theta*b[:,None]*m)).conj().T
 observed*= (cm*np.exp(-1j*theta*b[:,None]*m))@(cm*np.exp(-1j*theta*b[:,None]*m)).conj().T
 lost=np.ones((3,3),complex)
 for v_ in [np.sqrt(1-eta1)*zp,np.sqrt(1-eta2)*zm]:lost*=np.exp(-abs(v_)[:,None]**2/2-abs(v_)[None,:]**2/2+v_[:,None]*v_.conj()[None,:])
 chi=A*L*(eta1-eta2)/2;actual=observed*lost*np.exp(-1j*chi*(b[:,None]-b[None,:]));avg=(eta1+eta2)/2;lam=nlo+b*b*S
 expected=np.exp(-avg*(np.sqrt(lam)[:,None]-np.sqrt(lam)[None,:])**2/2-(1-avg)*S*(b[:,None]-b[None,:])**2/2)
 close('unequal_efficiency_full_overlap_and_phase',actual,expected,3e-11)
 unequal.append(dict(eta_plus=eta1,eta_minus=eta2,local_phase=chi,kernel_error=float(np.linalg.norm(actual-expected))))

# Schur-channel diamond formula, including exact attaining input and arbitrary reference.
for row in j['rows']:
 t=float(F(row['LO_adjacent_factor']['interval'][0]))*np.exp(-2*ell);d=np.exp(-8*ell);w=1-t;q=1-d;x=.5 if q>=2*w else w/(4*w-q)
 K=np.array([[1,t,d],[t,1,t],[d,t,1]]);p=np.array([x,1-2*x,x]);value=np.linalg.norm((K-1)*np.sqrt(p[:,None]*p[None,:]),ord='nuc');expected=float(F(row['exact_bus_receiver_diamond']['interval'][0]));close('finite_LO_diamond_attaining_state',value,expected,2e-12)
 for _ in range(5):
  vv=rng.normal(size=9)+1j*rng.normal(size=9);vv/=np.linalg.norm(vv);rho=np.outer(vv,vv.conj());change=(rho.reshape(3,3,3,3)*(K-1)[:,None,:,None]).reshape(9,9)
  ck('finite_LO_diamond_arbitrary_reference',np.linalg.norm(change,ord='nuc')<=expected+2e-12)

# Every finite command is computationally enclosed; physical tolerance must include it.
precision=[]
for row in j['rows']:
 er=max(F(t['computation_error_upper']) for t in row['finite_correction_table']);maxcmd=max(abs(F(t['local_Z_coefficient_angle'])) for t in row['finite_correction_table'])
 ck('rounded_commands_fit_declared_control_strength',float(maxcmd)+1e-6<np.pi/2)
 precision.append(dict(nlo=row['parameters']['observed_LO_mean'],max_table_error=str(er),max_table_error_display=float(er),extra_diamond_if_actuator_only=float(4*er),actuator_margin_required_for_total_1e_6=float(F(1,10**6)-er)))

# Classical number confusion is not a general coherent POVM distance guarantee.
# Rotated two-number basis misclassifies each number eigenstate with probability eps,
# while the measurement distributions differ by sqrt(eps(1-eps)) on |+>.
eps=1e-4;ang=np.arcsin(np.sqrt(eps));ket=np.array([np.cos(ang),np.sin(ang)]);plus=np.ones(2)/np.sqrt(2);P=np.outer(ket,ket);tv=abs(np.vdot(plus,P@plus)-.5)
ck('Fock_confusion_does_not_bound_arbitrary_POVM_by_2epsilon',2*tv>2*eps*50)
misassignment={'Fock_misclassification_probability':eps,'measurement_channel_distance_lower':2*tv,'incorrect_2epsilon_claim_if_only_Fock_confusion':2*eps,'qualification':'2 epsilon is valid for classical record corruption after the declared PNR instrument or a received CP bad-event coupling, not generic coherent instrument error inferred from Fock confusion alone.'}

result={'checks':len(checks),'details':checks,'vacuum_quantum_BS_kernel':[[[float(z.real),float(z.imag)] for z in row] for row in kernels[0]],'one_photon_signal_quantum_BS_kernel':[[[float(z.real),float(z.imag)] for z in row] for row in kernels[1]],'warm_kernel_difference':float(np.linalg.norm(kernels[1]-kernels[0])),'quantum_BS_total_cap_overflow':bad.tolist(),'unequal_efficiency_checks':unequal,'table_precision':precision,'misassignment_scope_counterexample':misassignment,'scope':'Independent full quantum BS and channel diagnostics; finite optical cutoffs are diagnostics only, analytic coherent-state sums and CP receiving prove the model.'}
(root/'independent_finite_lo_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['details','vacuum_quantum_BS_kernel','one_photon_signal_quantum_BS_kernel']},indent=2))
