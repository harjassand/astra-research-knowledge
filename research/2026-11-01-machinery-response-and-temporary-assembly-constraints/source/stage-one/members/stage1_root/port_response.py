"""Physical two-port wave model for a coordinate-free mechanical response test.

Lossless scalar Helmholtz waves scatter from movable delta interfaces. The
simulation knows positions and mobility. The learner receives boundary S records,
temperature, frame times, and commanded input coherence only. Normalized units
are used for this physics/model test; no apparatus performance is inferred.
"""
from pathlib import Path
import json
import os
import numpy as np
from numpy.linalg import norm,eigh
from scipy.linalg import logm
from scipy.optimize import minimize

HERE=Path(__file__).resolve().parent
OUT=HERE/'results';OUT.mkdir(exist_ok=True)
os.environ.setdefault('MPLCONFIGDIR',str(OUT/'mpl-cache'))
PAULI=np.array([np.eye(2),[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],dtype=complex)/np.sqrt(2)

def vec(a):
    return np.real(np.einsum('aij,ji->a',PAULI,a))

def mat(v):
    return np.einsum('a,aij->ij',v,PAULI)

def scatter(q,strength,k=2.1,length=4.):
    def prop(d):return np.diag([np.exp(1j*k*d),np.exp(-1j*k*d)])
    T=np.eye(2,dtype=complex);old=0.
    for x,p in zip(q,strength):
        T=prop(x-old)@T
        D=np.array([[1-1j*p,-1j*p],[1j*p,1+1j*p]])
        T=D@T;old=x
    T=prop(length-old)@T
    return np.array([[-T[1,0],1],[1,T[0,1]]])/T[1,1]

def force_operators(q,strength):
    S=scatter(q,strength);h=1e-6;Q=[]
    for j in range(len(q)):
        e=np.zeros(len(q));e[j]=h
        dS=(scatter(q+e,strength)-scatter(q-e,strength))/(2*h)
        a=-1j*S.conj().T@dS
        Q.append((a+a.conj().T)/2)
    return S,np.array(Q)

def momentum_force(q,strength,u,k=2.1,length=4.):
    S=scatter(q,strength);out=S@u
    waves=np.array([u[0],out[0]],dtype=complex)
    old=0.;forces=[]
    for x,p in zip(q,strength):
        waves=np.diag([np.exp(1j*k*(x-old)),np.exp(-1j*k*(x-old))])@waves
        before=waves.copy()
        waves=np.array([[1-1j*p,-1j*p],[1j*p,1+1j*p]])@waves
        forces.append(k*(np.vdot(before,before).real-np.vdot(waves,waves).real))
        old=x
    return np.array(forces)

def observed_increment(S0,S1):
    # Intrinsic tangent increment; no internal coordinate used by observer.
    H=-1j*logm(S0.conj().T@S1)
    return vec((H+H.conj().T)/2)

def response_validation():
    rng=np.random.default_rng(4187)
    q=np.array([.7,1.9,3.1]);strength=np.array([.9,1.4,.6])
    S,Q=force_operators(q,strength)
    B=np.array([vec(x) for x in Q]).T
    M=np.array([[1.,.12,.02],[.12,.65,.08],[.02,.08,1.2]])
    K=B@M@B.T
    force_errors=[];drift_errors=[]
    for _ in range(30):
        u=rng.normal(size=2)+1j*rng.normal(size=2);u/=norm(u)
        C=np.outer(u,u.conj());c=vec(C)
        f=np.real(np.einsum('aij,ji->a',Q,C))
        force_errors.append(norm(f-momentum_force(q,strength,u)))
        dt=1e-6;v=M@f
        y=observed_increment(S,scatter(q+dt*v,strength))/dt
        drift_errors.append(norm(y-K@c)/max(1.,norm(K@c)))
    assert max(force_errors)<1e-7
    assert max(drift_errors)<1e-4

    # Independent, local one-step thermal experiments at one prepared state.
    # This validates the local kernel; it does NOT supply free repeated resets
    # or certify estimation from one long drifting trajectory.
    theta=.02;dt=2e-5;N=8000;L=np.linalg.cholesky(M)
    increments=[]
    for _ in range(N):
        dq=np.sqrt(2*theta*dt)*(L@rng.normal(size=3))
        increments.append(observed_increment(S,scatter(q+dq,strength)))
    inc=np.asarray(increments)
    Khat=np.cov(inc,rowvar=False)/(2*theta*dt)
    err=norm(Khat-K)/norm(K)
    assert err<.06

    # Infer a physically admissible constant wave force cancelling a hidden
    # mechanical load. The load is manufactured from a feasible coherence only
    # in the simulator; the optimizer receives Khat and observed drift y0.
    Cstar=np.array([[.34,.08+.06j],[.08-.06j,.21]])
    cstar=vec(Cstar);f0=-B.T@cstar;y0=B@M@f0
    Pmax=1.
    def obj(c):return .5*c@Khat@c+c@y0
    def jac(c):return Khat@c+y0
    constraints=[{'type':'ineq','fun':lambda c:c[0]-norm(c[1:])},
                 {'type':'ineq','fun':lambda c:Pmax/np.sqrt(2)-c[0]}]
    fit=minimize(obj,np.array([.3,0,0,0]),jac=jac,constraints=constraints,
                 method='SLSQP',options={'ftol':1e-13,'maxiter':200})
    assert fit.success
    resid=f0+B.T@fit.x
    initial_power=float(f0@M@f0);final_power=float(resid@M@resid)

    # Equally informed ordinary competitor: experimentally identify the linear
    # response with a spanning family of PSD input coherences. It receives the
    # same boundary output Y, not internal positions, forces or mobility.
    probes=[np.array([1,0],complex),np.array([0,1],complex),
            np.array([1,1],complex)/np.sqrt(2),np.array([1,1j],complex)/np.sqrt(2)]
    X=np.array([vec(np.outer(u,u.conj())) for u in probes]).T
    Y=np.column_stack([K@X[:,j] for j in range(4)])
    Kactive=Y@np.linalg.inv(X)
    assert norm(Kactive-K)<1e-10

    # A single observed configuration does not suffice for a global promise:
    # quantify expiry of the learned local action under a real displacement.
    expiry=[]
    for d in [.001,.01,.05,.1]:
        _,Qnew=force_operators(q+np.array([d,-d/2,d/3]),strength)
        Bnew=np.array([vec(x) for x in Qnew]).T
        Knew=Bnew@M@Bnew.T
        expiry.append(dict(displacement=d,relative_response_change=float(norm(Knew-K)/norm(K))))
    return dict(scope='Local lossless two-port Helmholtz model; normalized omega=1 and power-coherence normalization. Thermal covariance samples use independent local resets solely to validate kernel. Actual repeated resets and finite detector acquisition are not supplied.',
        positions_simulator_only=q.tolist(),interface_strengths=strength.tolist(),
        scattering_unitarity_error=float(norm(S.conj().T@S-np.eye(2))),
        force_identity_max_abs_error=max(force_errors),
        induced_boundary_velocity_max_relative_error=max(drift_errors),
        thermal_covariance_samples=N,thermal_kBT=theta,thermal_interval=dt,
        thermal_response_relative_error=float(err),
        response_eigenvalues=eigh(K)[0].tolist(),
        hidden_coordinate_jacobian_rank=int(np.linalg.matrix_rank(B,tol=1e-7)),
        recovered_control_power=float(np.trace(mat(fit.x)).real),
        initial_mechanical_dissipation=initial_power,
        final_mechanical_dissipation=final_power,
        residual_dissipation_fraction=final_power/initial_power,
        conventional_active_spanning_probes=len(probes),
        conventional_active_response_error=float(norm(Kactive-K)),
        local_response_expiry=expiry)

if __name__=='__main__':
    result=response_validation()
    (OUT/'port_response_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
