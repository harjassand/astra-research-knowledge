"""Restricted phase-loop construction, synthetic action calibration and gate word.

The synthesis routine receives only nine Pauli-setting counts and native-Z
access. Matrices are used only by the synthetic source and independent model
evaluation. Floating records are not physical measurements or interval proofs.
"""
import json,time
from pathlib import Path
import numpy as np
from scipy.linalg import expm,eigh
from scipy.integrate import solve_ivp

HERE=Path(__file__).resolve().parent
OUT=HERE/'outputs';OUT.mkdir(exist_ok=True)
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1,-1]).astype(complex)
PAULI=[X,Y,Z];P=(I+Z)/2
PHI0=np.pi/2

def invsqrt(A):
    w,v=eigh(A);return (v/np.sqrt(w))@v.conj().T
def bloch_rotation(U):
    return np.array([[np.trace(a@U@b@U.conj().T).real/2 for b in PAULI] for a in PAULI])
def rz(a):return expm(-.5j*a*Z)
def pdist(A,B):
    overlap=np.trace(B.conj().T@A)
    phase=overlap/abs(overlap)
    return float(np.linalg.norm(A-phase*B,2))
def encode_complex(A):
    return [[[float(z.real),float(z.imag)] for z in row] for row in A]

def synthesize_from_counts(records,beta=np.pi/2):
    Rraw=np.array([[(r['plus']-r['minus'])/r['shots'] for r in records if r['input_pauli']==j] for j in range(3)]).T
    U,sv,Vh=np.linalg.svd(Rraw)
    J=np.diag([1,1,np.linalg.det(U@Vh)])
    R=U@J@Vh
    angle=np.arccos(np.clip((np.trace(R)-1)/2,-1,1))
    neg_axis=np.array([R[2,1]-R[1,2],R[0,2]-R[2,0],R[1,0]-R[0,1]])/(2*np.sin(angle))
    n=-neg_axis/np.linalg.norm(neg_axis)
    p=float(np.clip(angle/PHI0,.8,1.))
    delta=np.arccos(np.clip(n[2],-1,1))
    az=np.arctan2(n[1],n[0])
    N=int(np.ceil(beta/(2*delta)))
    pieces=[2*delta]*(N-1)+[beta-2*delta*(N-1)]
    word=[]
    for b in pieces:
        theta=2*np.arcsin(np.clip(np.sin(b/2)/np.sin(delta),-1,1))
        zarg=np.angle(np.cos(theta/2)-1j*np.cos(delta)*np.sin(theta/2))
        word.extend([{'native_z':float(zarg+np.pi/2-az)},
                     {'source_phase':float(-theta/p)},
                     {'native_z':float(zarg-np.pi/2+az)}])
    return {'M':p*(I+sum(n[k]*PAULI[k] for k in range(3)))/2,
            'R':R,'axis':n,'p':p,'delta':delta,'N':N,'word':word}

def eval_word(word,M):
    A=I.copy()
    for op in word:
        B=rz(op['native_z']) if 'native_z' in op else expm(1j*op['source_phase']*M)
        A=A@B
    return A

start=time.perf_counter();rng=np.random.default_rng(20261028)
W0=np.array([[1,1],[0,.2],[.1,0]],complex)
Q=np.array([[2,.4,0],[.4,1.6,.2],[0,.2,2.4]],complex)
fixtures=[]
for label,phase in [('real',0.),('phase_0p7',.7),('phase_minus_1p1',-1.1)]:
    W=W0@np.diag([1,np.exp(1j*phase)])
    G=Q@W;L=W.conj().T@W
    Gamma=float(np.linalg.norm(W,'fro'));a=1/(2*Gamma)
    C=invsqrt(I+a*a*L);M=C@P@C
    p=float(np.trace(M).real)
    n=np.array([np.trace(M@s).real/p for s in PAULI])
    rho=abs(L[0,1])/(Gamma*Gamma)
    delta=float(np.arccos(n[2]));dmin=2*np.arctan(rho/(5*np.sqrt(5)))
    assert delta>=dmin-1e-12
    calU=expm(1j*PHI0*M);Rtrue=bloch_rotation(calU)
    records=[];shots=1_000_000
    for j in range(3):
        for k in range(3):
            probability=float(np.clip((1+Rtrue[k,j])/2,0,1))
            plus=int(rng.binomial(shots,probability))
            records.append({'input_pauli':j,'measurement_pauli':k,'shots':shots,
                            'plus':plus,'minus':shots-plus,'erasure':0})
    acquired=synthesize_from_counts(records)
    ideal_target=expm(-.25j*np.pi*Y)
    reconstructed=eval_word(acquired['word'],acquired['M'])
    actual_ideal_model=eval_word(acquired['word'],M)
    assert pdist(reconstructed,ideal_target)<1e-10
    fixtures.append({'label':label,'Q':encode_complex(Q),'G':encode_complex(G),
                     'Gamma_frobenius':Gamma,'eta':a,'rho':float(rho),'axis_angle':delta,
                     'analytic_axis_lower_bound':float(dmin),'true_M':encode_complex(M),
                     'synthetic_source':'ideal adiabatic logical unitary; finite-time errors are separate',
                     'sampling':'numpy PCG64 seed 20261028; floating probabilities; no finite-bit statistical certificate',
                     'records':records,'total_synthetic_shots':9*shots,
                     'acquired_p':acquired['p'],'acquired_axis':acquired['axis'].tolist(),
                     'non_native_rotations':acquired['N'],'word_math_order_rightmost_first':acquired['word'],
                     'estimated_word_target_operator_error_up_to_phase':pdist(reconstructed,ideal_target),
                     'true_ideal_model_target_operator_error_up_to_phase':pdist(actual_ideal_model,ideal_target)})

# Whole chiral propagation check on a genuine noncommuting Q,G fixture.
W=W0;G=Q@W;r=Q.shape[0];dim=2+2*r
Gamma=float(np.linalg.norm(W,'fro'));a=1/(2*Gamma)
L=W.conj().T@W;C=invsqrt(I+a*a*L);M=C@P@C
Pc=np.zeros((dim,dim),complex);Pc[:2,:2]=P
V0=np.eye(dim,dtype=complex)[:,:2]
def H(eta):
    out=np.zeros((dim,dim),complex)
    out[:2,2:2+r]=eta*G.conj().T;out[2:2+r,:2]=eta*G
    out[2:2+r,2+r:]=Q;out[2+r:,2:2+r]=Q
    return out
def propagate(reverse,T):
    def ode(t,y):
        eta=a*((1-t/T) if reverse else t/T)
        return (-1j*H(eta)@y.reshape(dim,dim)).reshape(-1)
    sol=solve_ivp(ode,[0,T],np.eye(dim,dtype=complex).reshape(-1),method='DOP853',rtol=3e-10,atol=2e-12)
    assert sol.success
    return sol.y[:,-1].reshape(dim,dim),sol.nfev
propagation=[]
for Tload,Tphase in [(40.,80.),(80.,160.),(160.,320.)]:
    Uload,nl=propagate(False,Tload);Uunload,nu=propagate(True,Tload)
    phi=np.pi/2
    # Endpoint native D correction cancels the conjugating phase frames.
    Ufull=Uunload@expm(-1j*(H(a)-phi/Tphase*Pc)*Tphase)@Uload
    final=Ufull@V0;ideal=V0@expm(1j*phi*M)
    err=float(np.linalg.norm(final-ideal,2))
    bound=2*19/(16*Tload)+2*abs(phi)*(1+abs(phi))/Tphase # Gershgorin B>=1
    assert err<bound
    propagation.append({'Tload':Tload,'Tphase':Tphase,'B_lower':1.,'operator_isometry_error':err,
                        'analytic_bound':float(bound),'ode_evaluations':nl+nu,
                        'scope':'floating ODE diagnostic; continuum bound is analytic, not inferred from these values'})

result={'status':'DERIVED_RESTRICTED_CONTROL_OPERATION; not independently reviewed; priority and advantage UNKNOWN',
        'ordinary_comparator':'same plant and controls, ordinary holonomic gate/action calibration/two-axis synthesis; no advantage shown',
        'physical_chiral_plant':'imported unqualified doubled-bath interface, not acquired',
        'fixtures':fixtures,'finite_time_propagation':propagation,
        'elapsed_seconds':time.perf_counter()-start}
(OUT/'PHASE_GATE_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'fixture_summary':[
    {k:f[k] for k in ['label','axis_angle','non_native_rotations','total_synthetic_shots','true_ideal_model_target_operator_error_up_to_phase']} for f in fixtures],
    'finite_time_propagation':propagation,'elapsed_seconds':result['elapsed_seconds']},indent=2))
