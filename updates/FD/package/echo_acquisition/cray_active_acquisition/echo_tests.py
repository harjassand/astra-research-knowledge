"""Equilibrium-free echo certificates: numerical and simulated-data tests.
No result in this file is a laboratory observation. Numerical checks are not
substitutes for the analytic proofs. Exact special certificates are separate.
"""
from __future__ import annotations
import itertools, json, math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.stats import beta as beta_distribution
from run_tests import I,X,Y,Z,PS,pauli,kron_all,norm,herm
OUT=Path(__file__).resolve().parent

def partial_mean(op: np.ndarray, tau: np.ndarray, d: int) -> np.ndarray:
    b=tau.shape[0]
    blocks=op.reshape(d,b,d,b)
    return np.einsum('aicj,ji->ac', blocks, tau)

def density(rng,d):
    z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
    r=z@z.conj().T
    return r/np.trace(r)

def algebra_tests():
    rng=np.random.default_rng(864500)
    checks=0;worst_remainder=0.;lowest_null_ratio=1e300;worst_phase=0.
    frame_max=0.; second_max=0.
    for k in range(120):
        ell=1 if k%2 else 2;d=2**ell;b=2 if k%3 else 3
        # General, not weak, system--memory interaction. Bath-only field may
        # be arbitrarily large and is excluded from the local commutator bound.
        h_touch=herm(rng,d*b)
        bath=10*herm(rng,b)
        K=np.kron(np.eye(d),bath)+h_touch
        r=herm(rng,d);r*=float(rng.uniform(.01,.7))/norm(r)
        R=np.kron(r,np.eye(b));delta=norm(r)
        Lambda=2*norm(h_touch)+delta
        t=1/(Lambda*math.sqrt(d))
        E=expm(1j*K*t)@expm(-1j*(K+R)*t)
        rem=norm(E-np.eye(d*b)+1j*t*R)
        cap=Lambda*t*t*delta/2
        assert rem<=cap+1e-10
        worst_remainder=max(worst_remainder,rem/cap)
        for j in range(5):
            tau=density(rng,b);rho=np.kron(np.eye(d)/d,tau)
            p=float((1-np.trace(rho@E).real)/2)
            lb=delta**2/(16*Lambda**2*d**2)
            assert p+1e-13>=lb
            lowest_null_ratio=min(lowest_null_ratio,p/lb)
            B=partial_mean(E,tau,d)
            M=-(B-B.conj().T)/(2j*t)
            error=norm(M-r)
            assert error<=Lambda*t*delta/2+1e-10
            worst_phase=max(worst_phase,error/(Lambda*t*delta/2))
            checks+=1
        # Exhaustive check of the Pauli-product inverse frame on M.
        states=[(I+s*P)/2 for P in [X,Y,Z] for s in [-1,1]]
        frame=np.zeros((d,d),complex);sec=np.zeros_like(frame)
        for local in itertools.product(states,repeat=ell):
            rho_s=kron_all(local)
            dual=kron_all([3*z-I for z in local])
            frame+=d*dual*np.trace(rho_s@M)/(6**ell)
            sec+=d*d*(dual@dual)/(6**ell)
        frame_max=max(frame_max,norm(frame-M))
        second_max=max(second_max,norm(sec-10**ell*np.eye(d)))
        assert norm(frame-M)<1e-10
        assert norm(sec-10**ell*np.eye(d))<1e-10
    return dict(random_models=120,bath_states_checked=checks,
                worst_relative_remainder_ratio=worst_remainder,
                minimum_failure_probability_to_bound_ratio=lowest_null_ratio,
                maximum_phase_bias_to_bound_ratio=worst_phase,
                frame_identity_max_error=frame_max,second_moment_max_error=second_max)

def adaptive_null_test():
    # Three locally reset spins; one unreset memory spin. Same retained memory
    # register across shots. A history-dependent CPTP operation by the memory
    # controller selects its state at block boundaries. The certificate permits
    # this adversarial history dependence. Counts are simulated, not measured.
    arr=np.load(OUT/'local_search_matrices.npz')
    u=np.kron(arr['u'],I);k0=arr['k0'];k1=arr['k1'];w=.2
    outside_terms=[(1.1,{2:3,3:3}),(.6,{2:1,3:1}),(.5,{3:1})]
    ext=sum(c*pauli(4,p) for c,p in outside_terms)
    K0=np.kron(k0,I)+ext
    K1=np.kron(k1,I)+ext
    U=np.kron(u,I)
    B=U.conj().T@K1@U-w*np.eye(16)
    R=B-K0;delta=norm(R)
    J=sum([.70,.43,.31,.83,.61,.97,.79,.57,.88])+1.1+.6
    # A declared conservative residual cap, not its exact value, is used.
    Rcap=2.;Lambda=2*J+Rcap;d=8
    t=1/50  # rational interrogation time for the exact certificate
    E=expm(1j*K0*t)@expm(-1j*B*t)
    probs=[]
    for s in [-1,1]:
        rho=np.kron(np.eye(d)/d,(I+s*Z)/2)
        probs.append(float((1-np.trace(rho@E).real)/2))
    rng=np.random.default_rng(486592)
    block=10000;N=100_000_000;counts=0;states=[0,0];expected=0.
    for j in range(N//block):
        state=(j%2) ^ (counts%2)
        states[state]+=block
        counts+=int(rng.binomial(block,probs[state]))
        expected+=block*probs[state]
    alpha=.01
    q=float(beta_distribution.ppf(1-alpha,counts+1,N-counts))
    c=t*t*(1/math.sqrt(d)-Lambda*t/2)**2/4
    rad=math.sqrt(q/c)
    rows=[]
    for gamma in [0.,1e-8,1e-7,1e-6]:
        rr=math.sqrt((q+gamma)/c)
        rows.append(dict(gamma=gamma,radius=rr,interval=[w-rr,w+rr],
                         sign_certified=rr<w))
    return dict(N=N,failures=counts,expected_failures=expected,
                conditional_failure_probabilities=probs,memory_state_shots=states,
                J=J,Lambda=Lambda,d=d,t=t,Rcap=Rcap,true_residual=delta,
                q_upper=q,coverage=1-alpha,calibration_rows=rows,c=c,
                qualification='Synthetic acquisition. Beta quantile not outward-rounded; exact certificate is separate.')

def phase_memory_test():
    # Phase-frame test with a drifting, history-dependent memory. Coherent
    # interrogation uses fixed time; no derivative is extrapolated to zero.
    rng=np.random.default_rng(928590)
    ell=1;d=2;t=.05
    K=.7*np.kron(X,X)+.9*np.kron(Y,Y)+.8*np.kron(Z,Z)+.4*np.kron(I,X)
    r=.14*X-.09*Y+.06*Z
    R=np.kron(r,I);delta=norm(r)
    Lambda=2*(.7+.9+.8)+.25
    a=Lambda*t/2
    E=expm(1j*K*t)@expm(-1j*(K+R)*t)
    states=[(I+s*P)/2 for P in [X,Y,Z] for s in [-1,1]]
    duals=[3*p-I for p in states]
    Ms=[];means=np.empty((2,6))
    for si,s in enumerate([-1,1]):
        b=partial_mean(E,(I+s*Z)/2,d)
        m=-(b-b.conj().T)/(2j*t);Ms.append(m)
        for j,state in enumerate(states):means[si,j]=t*np.trace(state@m).real
    N=2_000_000; block=2000; accum=np.zeros((d,d),complex)
    target=np.zeros_like(accum);memory_shots=[0,0];last_score=0
    for b in range(N//block):
        mem=(b%2) ^ (last_score>0)
        ns=rng.multinomial(block,np.ones(6)/6)
        score=0
        for j,n in enumerate(ns):
            plus=int(rng.binomial(int(n),(1+means[mem,j])/2));sy=2*plus-n
            score+=int(sy)
            accum+=(d/t)*duals[j]*sy
        target+=block*Ms[mem];memory_shots[mem]+=block;last_score=score
    estimate=accum/N;target/=N
    alpha=.01;v=10**ell/t**2;B=2*d*d/t;x=math.log(2*d/alpha)
    # Positive root of n e^2 -(2/3) B x e-2vx=0.
    stat=((2/3)*B*x+math.sqrt(((2/3)*B*x)**2+8*N*v*x))/(2*N)
    rad=(norm(estimate)+stat)/(1-a)
    assert norm(target-r)<=a*delta+1e-12
    return dict(N=N,t=t,Lambda=Lambda,relative_bias=a,
                residual_norm=delta,estimate_norm=norm(estimate),
                estimator_to_average_conditional_mean=norm(estimate-target),
                true_bias=norm(target-r),statistical_radius_99percent=stat,
                certified_norm_radius=rad,memory_shots=memory_shots,
                note='Synthetic memory-dependent data; matrix Freedman gives analytic coverage; floating numerical endpoints.')

def resources():
    rows=[]
    for ell in [1,2,3,4]:
        d=2**ell;Lambda=1.;alpha=.01
        for epsilon in [.1,.03,.01]:
            N=math.ceil(16*Lambda**2*d*d*math.log(1/alpha)/epsilon**2)
            rows.append(dict(ell=ell,d=d,epsilon_over_Lambda=epsilon,
                             minimum_no_failure_shots=N,
                             maximum_gamma_for_floor_below_epsilon=epsilon**2/(16*d*d),
                             duration_if_cycle_10_microseconds_seconds=N*1e-5))
    return dict(null_test=rows,assumed_cycle_time_seconds=1e-5,
                note='Best-case zero-failure budget. Cycle time is illustrative, not measured. Nonzero failure probability increases the limiting radius.')

if __name__=='__main__':
    result=dict(algebra=algebra_tests(),null_simulation=adaptive_null_test(),
                phase_simulation=phase_memory_test(),resources=resources())
    (OUT/'echo_results.json').write_text(json.dumps(result,indent=2))
    for key in ['algebra','null_simulation','phase_simulation']:
        print(key,json.dumps(result[key],indent=2))
