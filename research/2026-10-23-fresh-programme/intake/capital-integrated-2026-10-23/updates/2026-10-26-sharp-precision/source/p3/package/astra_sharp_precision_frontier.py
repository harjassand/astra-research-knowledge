"""Astra Pro3: sharp spectral precision frontier for symmetric response tasks.

Independently reproducible symbolic software controls, 2026-10-26.
Native instrument in the theorem: full-vector q -> S q, ||q||_2<=1,
per-call arbitrary Euclidean error <= eta; S=S0+H with H symmetric,
||H||_op<=R. No physical experiments, calibrated prior, or novelty proof.

Requires sympy and numpy. Writes exact symbolic certificate JSON. No imports
of missing legacy Astra modules.
"""
from __future__ import annotations
from pathlib import Path
import json
from fractions import Fraction
from random import Random
import sympy as sp
import numpy as np

ROOT=Path(__file__).resolve().parent


def simp(A):
    if isinstance(A,sp.MatrixBase):
        return A.applyfunc(sp.simplify)
    return sp.simplify(A)


def sym(q,y):
    return (q*y.T+y*q.T)/2


def jencode(obj):
    if isinstance(obj,sp.MatrixBase):
        return [[str(sp.simplify(obj[i,j])) for j in range(obj.cols)] for i in range(obj.rows)]
    if isinstance(obj,sp.Basic):
        return str(sp.simplify(obj))
    if isinstance(obj,dict):
        return {str(k):jencode(v) for k,v in obj.items()}
    if isinstance(obj,(tuple,list)):
        return [jencode(v) for v in obj]
    if isinstance(obj,np.generic):
        return obj.item()
    return obj


def make_orthogonal(n):
    seeds=[list(range(1,n+1)),[(-1)**i*(i%3+1) for i in range(n)]]
    U=sp.eye(n)
    for s in seeds:
        v=sp.Matrix(s)
        W=sp.eye(n)-2*v*v.T/(v.T*v)[0]
        assert simp(W.T*W-sp.eye(n))==sp.zeros(n)
        U=simp(U*W)
    assert U.T*U==sp.eye(n)
    return U


def spec_plan(P,eigs,k,R,eta):
    """Exact, algebraic-eigenvector (real-field) optimal experiments."""
    n=len(eigs); eigs=[sp.Rational(x) for x in eigs]
    pos=sorted([i for i in range(n) if eigs[i]>0],key=lambda i:-eigs[i])
    neg=sorted([i for i in range(n) if eigs[i]<0],key=lambda i:eigs[i])
    actual_k=min(k,max(len(pos),len(neg)))
    Q=[];Y=[];head=[];newly_selected=[]
    for j in range(actual_k):
        hasp=j<len(pos);hasn=j<len(neg)
        if hasp and hasn:
            i=pos[j];h=neg[j];lam=eigs[i];mu=-eigs[h]
            q=(sp.sqrt(lam)*P[:,i]+sp.sqrt(mu)*P[:,h])/sp.sqrt(lam+mu)
            y=sp.sqrt(lam+mu)*(sp.sqrt(lam)*P[:,i]-sp.sqrt(mu)*P[:,h])
            head.extend([i,h]);selected=[i,h]
        elif hasp:
            i=pos[j];q=P[:,i];y=eigs[i]*P[:,i];head.append(i);selected=[i]
        elif hasn:
            h=neg[j];q=P[:,h];y=eigs[h]*P[:,h];head.append(h);selected=[h]
        else:
            raise AssertionError('invalid effective k')
        Q.append(simp(q));Y.append(simp(y));newly_selected.append(selected)
    T=simp(P*sp.diag(*eigs)*P.T)
    Z=sp.zeros(n)
    for q,y,selected in zip(Q,Y,newly_selected):
        assert simp(q.dot(q))==1
        assert simp(sp.sqrt(y.dot(y))-sum(abs(eigs[i]) for i in selected))==0
        Z+=sym(q,y)
    E=simp(T-Z)
    expected_diag=[eigs[i] if i not in head else sp.Integer(0) for i in range(n)]
    assert E==simp(P*sp.diag(*expected_diag)*P.T)
    nuclear_T=sum(abs(t) for t in eigs)
    nuclear_E=sum(abs(t) for t in expected_diag)
    head_mag=nuclear_T-nuclear_E
    norms_Y=[simp(sp.sqrt(y.dot(y))) for y in Y]
    assert simp(sum(norms_Y)-head_mag)==0
    guarantee=simp(R*nuclear_E+eta*head_mag)
    expected=simp(eta*nuclear_T+(R-eta)*nuclear_E)
    assert guarantee==expected
    witness_diag=[eta*sp.sign(eigs[i]) if i in head else R*sp.sign(eigs[i]) for i in range(n)]
    H=simp(P*sp.diag(*witness_diag)*P.T)
    assert simp(H-H.T)==sp.zeros(n)
    # Operator-norm contract is checked by the orthogonal eigenrepresentation.
    assert all(abs(x)<=R for x in witness_diag)
    for q in Q:
        assert simp(q.dot(H*H*q)-eta*eta)==0
    assert simp(sp.trace(T*H)-guarantee)==0
    S0=2*sp.eye(n)
    assert R <2
    actual=S0+H
    reports=[S0*q for q in Q]
    for q,rep in zip(Q,reports):
        actual_noise=rep-actual*q
        assert simp(actual_noise.dot(actual_noise)-eta*eta)==0
    estimated=simp(sp.trace(T*S0)+sum((y.T*(rep-S0*q))[0] for q,y,rep in zip(Q,Y,reports)))
    truth=simp(sp.trace(T*actual))
    assert simp(truth-estimated-guarantee)==0
    # A second source S0-H has identical reported centers with opposite noise;
    # their scalar targets are exactly 2*guarantee apart.
    alt_truth=simp(sp.trace(T*(S0-H)))
    assert simp(truth-alt_truth)==2*guarantee
    return dict(k=k,actual_calls=actual_k,input_width=n,returned_coordinates=n*actual_k,
         task_T=T,inputs=sp.Matrix.hstack(*Q) if Q else sp.zeros(n,0),
         decoder_Y=sp.Matrix.hstack(*Y) if Y else sp.zeros(n,0),
         residual_E=E,primal_adversary_H=H,source_center=S0,
         source_plus=actual,source_minus=S0-H,
         common_reports=sp.Matrix.hstack(*reports) if reports else sp.zeros(n,0),
         expected_nuclear_tail=nuclear_E,decoder_norm_sum=head_mag,
         certified_worst_error=guarantee,closed_formula_error=expected,
         exact_estimate=estimated,plus_truth=truth,minus_truth=alt_truth,
         exact_indistinguishable_gap=2*guarantee,
         witness_and_decoder_matching=True)


def sharp_controls():
    eigs=[16,9,4,1,-25,-16,-1,0]
    n=len(eigs);P=make_orthogonal(n)
    R=sp.Rational(1,4);eta=sp.Rational(1,100)
    plans=[spec_plan(P,eigs,k,R,eta) for k in range(5)]
    errors=[p['certified_worst_error'] for p in plans]
    assert errors==sorted(errors,reverse=True)
    assert errors[-1]==eta*sum(abs(t) for t in eigs)
    # Sharp threshold: maximum admissible k-bounded risk; returns 0,1,...,infty.
    thresholds=[sp.Rational(22),sp.Rational(8),sp.Rational(3),sp.Rational(1),sp.Rational(1,2)]
    decisions=[]
    for target_accuracy in thresholds:
        doable=[p['k'] for p in plans if p['certified_worst_error']<=target_accuracy]
        decisions.append(dict(accuracy=target_accuracy,required_calls=min(doable) if doable else 'IMPOSSIBLE_AT_THIS_NOISE_FLOOR'))
    return dict(eigenvalues=eigs,orthogonal_eigenvectors=P,n=n,prior_R=R,per_call_error_eta=eta,
                task_nuclear_norm=sum(abs(t) for t in eigs),
                optimal_calls_noiseless=4,
                optimal_risks_by_k=errors,precision_threshold_decisions=decisions,
                executed_exact_controls=plans)


def restriction_control():
    T=sp.diag(1,-1);S0=2*sp.eye(2);R=sp.Rational(1,2);eta=sp.Rational(1,20)
    # With unrestricted REAL q, unit q=(e1+e2)/sqrt(2) gives 2eta.
    q=sp.Matrix([1,1])/sp.sqrt(2)
    y=sp.sqrt(2)*sp.Matrix([1,-1])
    assert simp(sym(q,y))==T
    assert simp(sp.sqrt(y.dot(y))*eta)==2*eta
    # With catalogue restricted to e0 or e1, any ONE experiment leaves
    # opposite coordinate completely uncertain. Risk is exactly R+eta.
    q0=sp.Matrix([1,0]);y0=sp.Matrix([1,0]);E=T-sym(q0,y0)
    assert E==sp.diag(0,-1)
    W=sp.diag(eta,-R)
    assert simp(W*q0)==eta*q0
    assert simp(sp.trace(T*W))==R+eta
    return dict(supplied_target_T=T,unrestricted_real_optimal_one_call_radius=2*eta,
       catalogue=['e0','e1'],catalogue_one_call_exact_minimax_radius=R+eta,
       catalogue_two_call_exact_minimax_radius=2*eta,restricted_probe_adversary=W,
       source_prior_radius_R=R,per_call_error_eta=eta,
       warning='The spectral theorem assumes freely chosen unit-norm real directions; a restricted catalogue changes the optimum.')


def arbitrary_plan_lower_tests(seed=216,num=1500):
    rng=np.random.default_rng(seed)
    worst_gap=float('inf');failures=0;examples=[]
    for trial in range(num):
        n=int(rng.integers(2,9));k=int(rng.integers(0,n+2));
        eigen=rng.choice(np.array([-13.,-8.,-5.,-3.,-1.,0.,1.,2.,4.,9.,15.]),size=n,replace=True)
        A=rng.standard_normal((n,n)); V,_=np.linalg.qr(A)
        T=V@np.diag(eigen)@V.T
        T=(T+T.T)/2
        eta=.03;R=.6
        Q=rng.standard_normal((n,k)); norms=np.linalg.norm(Q,axis=0);
        Q=Q/np.maximum(norms,1.0)
        Y=rng.standard_normal((n,k))
        Z=(Q@Y.T+Y@Q.T)/2
        E=T-Z
        candidate=R*np.sum(np.abs(np.linalg.eigvalsh(E)))+eta*np.sum(np.linalg.norm(Y,axis=0))
        positive=sorted([x for x in eigen if x>0],reverse=True)
        negative=sorted([-x for x in eigen if x<0],reverse=True)
        tail=sum(positive[k:])+sum(negative[k:])
        theoretical=eta*np.sum(np.abs(eigen))+(R-eta)*tail
        gap=float(candidate-theoretical)
        worst_gap=min(worst_gap,gap)
        if gap< -1e-8:
            failures+=1;examples.append({'trial':trial,'n':n,'k':k,'gap':gap})
    assert failures==0,examples
    return dict(random_seed=seed,cases=num,failed_lower_bounds=failures,
      smallest_observed_candidate_minus_theorem=worst_gap,
      nature_of_test='Numerical stress test of global LOWER bound on arbitrary candidate decoders; not an external SDP solution and not a mathematical proof.')


def historian_control():
    # Central EXACT retained query reduces unknown perturbations to its
    # orthogonal complement. This remains special: arbitrary old readings
    # slice a norm ball noncentrally and need not yield a centred ball.
    eigs=[9,4,-16,-1]
    T=sp.diag(*eigs)
    S0=2*sp.eye(4);R=sp.Rational(1,2);eta=sp.Rational(1,100)
    q_good=sp.Matrix([3,0,4,0])/5
    q_bad=sp.eye(4)[:,0]
    def compress(q):
        # No need orthogonal normalize if the chosen basis vectors below are
        # explicitly known and unit in Euclidean metric.
        if q==q_good:
            K=sp.Matrix.hstack(sp.Matrix([4,0,-3,0])/5,sp.eye(4)[:,1],sp.eye(4)[:,3])
        else:
            K=sp.Matrix.hstack(*[sp.eye(4)[:,i] for i in [1,2,3]])
        assert K.T*K==sp.eye(3)
        assert q.T*K==sp.zeros(1,3)
        C=K.T*T*K
        return dict(old_probe=q,unresolved_basis=K,target_compression=C,
          compression_eigenvalues=sorted([e for e in C.eigenvals().keys()],key=lambda x:float(x),reverse=True))
    a=compress(q_good);b=compress(q_bad)
    assert a['target_compression']==sp.diag(0,4,-1)
    assert b['target_compression']==sp.diag(4,-16,-1)
    def radii(eigen,k):
        pos=sorted([v for v in eigen if v>0],reverse=True)
        neg=sorted([-v for v in eigen if v<0],reverse=True)
        return simp(eta*sum(abs(v) for v in eigen)+(R-eta)*(sum(pos[k:])+sum(neg[k:])))
    for obj in [a,b]:
        obj['one_new_query_optimal_radius']=radii(obj['compression_eigenvalues'],1)
        obj['two_new_queries_optimal_radius']=radii(obj['compression_eigenvalues'],2)
    assert a['one_new_query_optimal_radius']==5*eta
    assert b['one_new_query_optimal_radius']==20*eta+R
    assert b['two_new_queries_optimal_radius']==21*eta
    return dict(meaning='Central historical response Hq=0; exact old action is available at zero new-call cost',
       source_center=S0,prior_radius=R,per_new_action_error=eta,
       aligned_history=a,misaligned_history=b,
       warning='The spectral compression exact-risk identity is NOT claimed for noncentral previously observed outputs or non-symmetric posterior sets.')


def main():
    out={'scope':'Exact mathematical controls under symmetric operator-norm-ball prior and adversarial bounded full-vector response errors; no physical source measurements, calibration, novelty or practical advantage claimed.',
        'spectral_frontier':sharp_controls(),
        'prior_transfer':historian_control(),
        'restricted_instrument_failure':restriction_control(),
        'arbitrary_plan_numerical_lower_bound_stress':arbitrary_plan_lower_tests()}
    file=ROOT/'astra_sharp_precision_frontier_results.json'
    file.write_text(json.dumps(jencode(out),indent=2,ensure_ascii=False))
    print('spectral frontier:',[float(v) for v in out['spectral_frontier']['optimal_risks_by_k']])
    print('thresholds:',[(str(x['accuracy']),x['required_calls']) for x in out['spectral_frontier']['precision_threshold_decisions']])
    print('history 1 new, aligned vs misaligned:',
          float(out['prior_transfer']['aligned_history']['one_new_query_optimal_radius']),
          float(out['prior_transfer']['misaligned_history']['one_new_query_optimal_radius']))
    print('catalogue 1 new vs real unrestricted:',float(out['restricted_instrument_failure']['catalogue_one_call_exact_minimax_radius']),float(out['restricted_instrument_failure']['unrestricted_real_optimal_one_call_radius']))
    print('random stress cases:',out['arbitrary_plan_numerical_lower_bound_stress']['cases'])
    print('results file:',file)

if __name__=='__main__': main()
