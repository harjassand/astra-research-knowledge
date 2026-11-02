"""Independent numerical regression, not a proof of the storage theorem.
Tensor order for evolved states is L,G,R. Gibbs uses shifted eigenvalues.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh, expm
I=np.eye(2); X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]]); Z=np.diag([1.,-1.]); P1=np.diag([0.,1.])
Delta,epsilon,g=2.,.15,.4
H=Delta*np.kron(I,P1)+epsilon*np.kron(I,X)+g*np.kron(Z,P1)
P=np.kron(I,P1); Q=[np.kron(q,I) for q in (X,Y,Z)]
C=[H@q-q@H for q in Q]
cs=[float(np.linalg.norm(c,2)) for c in C]
def gibbs(h,beta):
    es,vs=eigh(h); w=np.exp(-beta*(es-es.min())); w/=w.sum()
    return (vs*w)@vs.conj().T

def norm1(a): return float(np.abs(np.linalg.eigvalsh((a+a.conj().T)/2)).sum())
def gauge(rho): return np.trace(rho.reshape(2,2,2,2),axis1=0,axis2=2)
def decoded(rho): return np.trace(rho.reshape(2,2,2,2,2,2),axis1=1,axis2=4).reshape(4,4)
def overwrite(xi,tau):
    # kron has order L,R,G; transpose into L,G,R.
    return np.kron(xi,tau).reshape(2,2,2,2,2,2).transpose(0,2,1,3,5,4).reshape(8,8)
phi=np.array([1,0,0,1],complex)/np.sqrt(2)
plus=np.array([1,1],complex)/np.sqrt(2)
inputs={'Bell_LR':np.outer(phi,phi.conj()),
        'plus_L_pure_R':np.kron(np.outer(plus,plus.conj()),np.diag([1.,0.])),
        'zero_L_pure_R':np.diag([1.,0.,0.,0.])}
rows=[]; max_violation=0.; max_variance_projector_difference=0.
for beta in [.1,1.,10.,100.,1e4,1e6]:
    states={'actual_Gibbs':gibbs(H,beta)}
    for s in [1,-1]:
        # Exactly stationary, perfectly polarized logical state; not generally Gibbs(H).
        logical=np.diag([1.,0.]) if s==1 else np.diag([0.,1.])
        states[f'stationary_polarized_{s:+d}']=np.kron(logical,gibbs(Delta*P1+epsilon*X+s*g*P1,beta))
    for kind,rho in states.items():
        tau=gauge(rho); p=float(np.trace(P@rho).real)
        sigmas=[float(np.sqrt(max(0,np.trace(rho@c.conj().T@c).real))) for c in C]
        variance_rate=sum(sigmas); projector_rate=sum(cs)*np.sqrt(p)
        max_variance_projector_difference=max(max_variance_projector_difference,abs(variance_rate-projector_rate))
        stationary_residual=float(np.linalg.norm(H@rho-rho@H))
        assert stationary_residual<1e-12
        for name,xi in inputs.items():
            initial=overwrite(xi,tau)
            assert np.linalg.norm(decoded(initial)-xi)<1e-12
            for T in [0.,.1,1.,5.,20.,100.]:
                U=np.kron(expm(-1j*T*H),I); final=U@initial@U.conj().T
                full_error=norm1(final-initial); logical_error=norm1(decoded(final)-xi)
                variance_bound=min(2.,T*variance_rate)
                projector_bound=min(2.,T*projector_rate)
                max_violation=max(max_violation,full_error-variance_bound,full_error-projector_bound,logical_error-full_error)
                assert full_error<=variance_bound+1e-10
                assert full_error<=projector_bound+1e-10
                assert logical_error<=full_error+1e-10
                rows.append(dict(beta=beta,stationary_state=kind,input=name,T=T,
                    p=p,logical_Z=float(np.trace(rho@Q[2]).real),
                    stationarity_residual=stationary_residual,
                    commutator_variance_rate=variance_rate,projector_rate=projector_rate,
                    exact_full_trace_norm_error=full_error,exact_decoded_trace_norm_error=logical_error,
                    variance_bound=variance_bound,projector_bound=projector_bound))
result=dict(model=dict(Delta=Delta,epsilon=epsilon,g=g),
    conventions='Trace norm, not half trace distance; tensor order L,G,R; stable shifted Gibbs eigenvalues.',
    proof_status='Numerical regression only; theorem established separately by algebra.',
    checks=len(rows),commutator_norms=cs,
    projector_kernel_residuals=[float(np.linalg.norm(c@(np.eye(4)-P))) for c in C],
    maximum_bound_violation=max_violation,
    maximum_variance_projector_difference=max_variance_projector_difference,
    rows=rows)
path=Path(__file__).with_suffix('.json'); path.write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
print('Selected actual-Gibbs Bell input rows:')
for row in rows:
    if row['stationary_state']=='actual_Gibbs' and row['input']=='Bell_LR' and row['beta'] in [1.,100.,1e6] and row['T'] in [1.,20.,100.]:
        print(json.dumps(row))
