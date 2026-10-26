#!/usr/bin/env python3
"""Online bath-reusing TEST/USE simulation and robust operator mismatch test.

Native underlying quantum states are used only by the validation simulator.
The online observer sees TEST outcome, USE score, and the public setting/probability.
All chosen Pauli keys are fresh, independent and retired before later calls.
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm

OUT=Path(__file__).resolve().parent
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1.,-1.]).astype(complex)
P=[I,X,Y,Z]
Q0=(I+Z)/2
states=[np.array([1,0],complex),np.array([0,1],complex),
        np.array([1,1],complex)/np.sqrt(2),np.array([1,-1],complex)/np.sqrt(2),
        np.array([1,1j],complex)/np.sqrt(2),np.array([1,-1j],complex)/np.sqrt(2)]
P4=[np.kron(p,I) for p in P]
Usets=[]
for c in [0,1]:
    H=(.10+.22*c)*np.kron(Z,Q0)+(.08+.19*c)*np.kron(X,X)+(.08+.06*c)*np.kron(I,Y)
    U=expm(-1j*H)
    Bs=[.5*np.einsum('ab,biaj->ij',p,U.reshape(2,2,2,2)) for p in P]
    W=sum(B.conj().T@B for B in Bs[1:])
    Usets.append((U, Bs, W))
# A small independently calibrated coherent disturbance that occurs on TEST only,
# after the untrusted operation but before measured outputs.
phi=.07
V=np.kron(expm(-1j*phi*Z),I)
# Conservative uniform full-boundary half-diamond mismatch <= |sin(phi)|<=phi.
ETA=phi
Vb=expm(-1j*(.21*X+.26*Z))
nu=2/3
z=1.12
delta=.01
RNG=np.random.default_rng(202610260649)

# Bath update of actual TEST, with secret key and matching eigenprobe selected.
def physical_test(sigma, U, k, j, use_mismatch, rng):
    psi=states[j]; proj=np.outer(psi,psi.conj()); Rho=np.kron(proj,sigma)
    Ug=P4[k] @ U @ P4[k]
    if use_mismatch: Ug= P4[k] @ V @ P4[k] @ Ug
    end=Ug @ Rho @ Ug.conj().T
    H=np.kron(psi[:,None],I)
    good=H.conj().T@end@H
    bad=np.einsum('aiaj->ij',end.reshape(2,2,2,2))-good
    good=(good+good.conj().T)/2
    bad=(bad+bad.conj().T)/2
    pbad=max(0.,min(1.,float(np.trace(bad).real)))
    observed=int(rng.random()<pbad)
    new=bad if observed else good
    t=float(np.trace(new).real)
    if t<=1e-15: raise ValueError('Improbable branch sampled')
    new=new/t
    return observed,new


def virtual_use(sigma, Bs, rng):
    branches=[b@sigma@b.conj().T for b in Bs]
    ps=np.array([float(np.trace(a).real) for a in branches])
    ps=np.maximum(0,ps); ps/=ps.sum()
    l=int(rng.choice(4,p=ps))
    sigma2=branches[l]/float(np.trace(branches[l]).real)
    # Client's observable known-Z score: X and Y errors flip the bit.
    # The virtual label remains hidden from the controller.
    score=int(l in (1,2))
    return int(l!=0), score, sigma2


def sim_one(hardware_mismatch, horizon=680):
    # Start entangled bath with coherent superposition; not reset.
    x=RNG.normal(size=2)+1j*RNG.normal(size=2)
    x/=np.linalg.norm(x)
    sigma=np.outer(x,x.conj())
    visible=[]; last_test_fail=[]
    B=0; S_mean=0.; nuse=ntest=0
    total_ln_a=0.; total_ln_c=0.
    Vbound=0.
    Bmax=100.
    max_cross_exact=-float('inf')
    max_cross_robust=-float('inf')
    first_violation_exact=None; first_violation_robust=None
    per_round=[]
    for i in range(1,horizon+1):
        if Vbound+1 > Bmax: break
        # Public controller: source setting and test probability use ONLY received words.
        recente=visible[-16:]
        errs=sum(recente)
        setting=int(errs<=2 and len(recente)>=8)
        ptest=.5 if (sum(last_test_fail[-8:])>=2) else .3
        # Neither of these reveals current future role or its private Pauli key.
        a=1-(1-ptest)*(z-1)/(ptest*nu)
        assert 0<a<1
        U,Bs,W=Usets[setting]
        q=float(np.trace(W@sigma).real)
        role_test=RNG.random()<ptest
        if role_test:
            k=int(RNG.integers(4)); j=int(RNG.integers(6))
            fail,sigma=physical_test(sigma,U,k,j,hardware_mismatch,RNG)
            ntest+=1; last_test_fail.append(fail)
            total_ln_a+=fail*np.log(a)
            visible.append(fail)
            fault_inc=0
        else:
            fault_inc,score,sigma=virtual_use(sigma,Bs,RNG)
            nuse+=1; B+=fault_inc; S_mean+=q
            visible.append(score)
        # Exact matched-port assumption has c=1. Robust ε port bound uses c>1.
        # For operator effect F_test>=nu W-ETA I and positive use effects.
        if hardware_mismatch:
            total_ln_c+=np.log1p(ptest*(1-a)*ETA)
        U_exact=(np.log(1/delta)-total_ln_a)/np.log(z)
        U_robust=(np.log(1/delta)+total_ln_c-total_ln_a)/np.log(z)
        U_for_guard= U_robust if hardware_mismatch else U_exact
        Vbound=min(U_for_guard,Vbound+(0 if role_test else 1))
        if first_violation_exact is None and B>U_exact+1e-11:
            first_violation_exact=i
        if first_violation_robust is None and B>U_robust+1e-11:
            first_violation_robust=i
        # Classical controller cannot see B,q, or sigma.
        sigma=Vb@sigma@Vb.conj().T
        sigma=(sigma+sigma.conj().T)/2
        per_round.append((i,ntest,nuse,B,Vbound,q,int(role_test)))
    return {'rounds':len(per_round),'uses':nuse,'tests':ntest,
            'fault_count_hidden':B,'expected_faults_on_actual_use_boundaries_hidden':S_mean,
            'received_retained_fault_upper':Vbound,
            'first_violation_naive_exact_model':first_violation_exact,
            'first_violation_robust_model':first_violation_robust,
            'final_untransported_upper_exact':U_exact,
            'final_untransported_upper_robust':U_robust,
            'total_log_penalty':total_ln_c}

def summaries(results):
    keys=['rounds','uses','tests','fault_count_hidden',
          'expected_faults_on_actual_use_boundaries_hidden',
          'received_retained_fault_upper','total_log_penalty']
    summary={k:float(np.mean([r[k] for r in results])) for k in keys}
    for fail_key in ('first_violation_naive_exact_model','first_violation_robust_model'):
        summary['num_'+fail_key]=sum(r[fail_key] is not None for r in results)
    summary['halted_before_cap']=sum(r['rounds']<680 for r in results)
    return summary

matched=[sim_one(False) for _ in range(90)]
mismatched=[sim_one(True) for _ in range(90)]
res={
    'environment':'two-level coherent, noncommuting, no resets, controller updates from public records',
    'role_input':'fresh secret Pauli keys each use/test, six-state test probes; keys retired',
    'nominal_all_prefix_delta':delta,
    'per_run_horizon':680,
    'declared_retained_fault_budget':100,
    'role_mismatch_model':'extra test-only Z rotation on logical output after the bath interaction',
    'role_mismatch_uniform_half_diamond_upper':ETA,
    'matched_90_runs':summaries(matched),
    'mismatched_90_runs':summaries(mismatched),
    'first_three_matched':matched[:3],
    'first_three_mismatched':mismatched[:3]
}
(OUT/'online_causal_sealed_memory_results.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
