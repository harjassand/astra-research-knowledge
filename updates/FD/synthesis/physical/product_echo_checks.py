#!/usr/bin/env python3
"""Independent module-norm diagnostics and exact same-record echo certificate.

All fixtures and retained source records are simulated. Universal scope is in
PRODUCT_NORM_ECHO_THEOREM.md. Exact rational statements never use beta quantiles.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import hashlib,json,math
import numpy as np
from scipy.linalg import expm
from scipy.stats import beta as beta_law

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'sources'/'cray_active_acquisition'

def norm(a):
    return float(np.linalg.norm(a,2))

def partial_trace_s(a,d,b):
    return np.einsum('aiaj->ij',a.reshape(d,b,d,b))

def module_norm(a,d,b):
    out=partial_trace_s(a.conj().T@a,d,b)/d
    return math.sqrt(max(0,float(np.linalg.eigvalsh((out+out.conj().T)/2)[-1])))

def herm(rng,d):
    a=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
    return (a+a.conj().T)/(2*math.sqrt(d))

def g_exact_numeric(Lam,Jc,t):
    if Jc==0:
        return Lam*t*t/2
    # Stable power series rather than subtracting two nearly equal quantities.
    x=Jc*t
    return Lam*t*t*sum(x**k/factorial(k+2) for k in range(50))

def random_diagnostics():
    rng=np.random.default_rng(202610140191)
    worst_rem=0.;minimum_ratio=math.inf;worst_right=0.;models=0
    for d in [2,3,4,5]:
        for b in [2,3,4]:
            for replicate in range(15):
                ks=herm(rng,d)
                ko=(1+replicate*50)*herm(rng,b)
                terms=[(herm(rng,d),herm(rng,b)) for _ in range(3)]
                jc=sum(norm(a)*norm(z) for a,z in terms)
                jpi=norm(ks)+jc
                rr=herm(rng,d)
                delta=float(rng.uniform(.02,.8))
                rr*=delta/norm(rr)
                cap=delta+float(rng.uniform(.02,.4))
                Lam=2*jpi+cap
                t=float(rng.uniform(.15,.65))/Lam
                g=g_exact_numeric(Lam,jc,t)
                assert 0<g<t
                K=np.kron(ks,np.eye(b))+np.kron(np.eye(d),ko)
                K+=sum(np.kron(a,z) for a,z in terms)
                R=np.kron(rr,np.eye(b))
                E=expm(1j*K*t)@expm(-1j*(K+R)*t)
                rem=E-np.eye(d*b)+1j*t*R
                r2=np.linalg.norm(rr,'fro')/math.sqrt(d)
                ratio=module_norm(rem,d,b)/(g*r2)
                assert ratio<=1+1e-8
                worst_rem=max(worst_rem,ratio)
                P=partial_trace_s((E-np.eye(d*b)).conj().T@(E-np.eye(d*b)),d,b)/(4*d)
                min_p=float(np.linalg.eigvalsh((P+P.conj().T)/2)[0])
                lb=(t-g)**2*r2*r2/4
                assert min_p+1e-12>=lb
                minimum_ratio=min(minimum_ratio,min_p/lb)
                # Test right entangling evolution on a general input operator.
                Q=rng.normal(size=(d*b,d*b))+1j*rng.normal(size=(d*b,d*b))
                rb=module_norm(Q@expm(-1j*(K+R)*t),d,b)
                rb/=math.exp(jc*t)*module_norm(Q,d,b)
                assert rb<=1+1e-9
                worst_right=max(worst_right,rb)
                models+=1
    return {'models':models,'outside_states_covered_per_model':'all via finite minimum eigenvalue',
            'largest_module_remainder_ratio':worst_rem,
            'smallest_actual_minimum_probability_to_bound_ratio':minimum_ratio,
            'largest_right_growth_to_bound_ratio':worst_right,
            'status':'floating diagnostic only, no physical evidence'}

def source_record_exact_certificate():
    path=SOURCE/'retained_memory_results.json'
    data=json.loads(path.read_text())
    assert data['N']==100_000_000 and data['failures']==7
    n=data['N'];s=data['failures'];alpha=F(1,100)
    q=F(161,10**9);x=n*q
    # Binomial lower tail <= exp(-nq) sum_{j<=s}[nq/(1-q)]^j/j!.
    # A positive Taylor sum is an exact lower bound for exp(nq).
    exp_lower=sum(x**j/F(factorial(j)) for j in range(101))
    poly=sum((x/(1-q))**j/F(factorial(j)) for j in range(s+1))
    tail_upper=poly/exp_lower
    assert tail_upper<alpha
    Jlocal=sum(map(F,['.70','.43','.31','.83','.61','.97','.79','.57','.88']))
    Jcross=F(11,10)+F(6,10)
    assert Jlocal==F(609,100) and Jcross==F(17,10)
    Jpi=Jlocal+Jcross;cap=F(2);Lam=2*Jpi+cap
    assert Jpi==F(779,100) and Lam==F(879,50)
    d=8;t=F(1,50);w=F(1,5)
    gbar=Lam*t*t/(2*(1-Jcross*t))
    assert Jcross*t<1 and gbar<t
    coefficient=(t-gbar)**2/(4*d)
    rows=[]
    for gamma,rad in [(F(0),F(139,1000)),(F(1,10**8),F(143,1000)),
                      (F(1,10**7),F(177,1000))]:
        radius_square=(q+gamma)/coefficient
        assert radius_square<rad**2
        rows.append({'gamma':str(gamma),'radius_square':str(radius_square),
                     'radius_upper':str(rad),'DeltaF_interval':[str(w-rad),str(w+rad)],
                     'sign_certified':rad<w})
    float_q=float(beta_law.ppf(.99,s+1,n-s))
    gnum=g_exact_numeric(float(Lam),float(Jcross),float(t))
    cnum=(float(t)-gnum)**2/(4*d)
    return {'source_path':str(path.relative_to(HERE.parent.parent)),
            'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'provenance':'Existing simulated unreset quantum-memory trajectory; no new data',
            'n':n,'failures':s,'alpha':str(alpha),'q_upper_exact':str(q),
            'exact_rational_tail_upper':str(tail_upper),'tail_upper_diagnostic':float(tail_upper),
            'Jlocal':str(Jlocal),'Jcross':str(Jcross),'Jpi':str(Jpi),'Lambda_pi':str(Lam),
            'dimension':d,'time':str(t),'gbar':str(gbar),
            'coefficient_exact':str(coefficient),'coefficient_diagnostic':float(coefficient),
            'exact_certificate_rows':rows,
            'floating_tighter_diagnostic':{'q_upper':float_q,'g':gnum,'coefficient':cnum,
                'gamma1e8_radius':math.sqrt((float_q+1e-8)/cnum)},
            'validity':'Conditional on product-boundary/support, reset, branch-control, uniform calibration and model contract; all beta>0 and ground energy',
            'novelty':'UNKNOWN','external_validation':'UNKNOWN','laboratory_validation':False}

def sharp_dimension_and_incompatible_extension():
    # An arbitrary entangling right unitary is not a module isometry.
    d=3;swap=np.zeros((d*d,d*d))
    for a in range(d):
        for b in range(d):
            swap[b*d+a,a*d+b]=1
    P=np.zeros((d,d));P[0,0]=1
    Q=np.kron(P,np.eye(d))
    ratio=module_norm(Q@swap,d,d)/module_norm(Q,d,d)
    assert math.isclose(ratio,math.sqrt(d),rel_tol=1e-12)
    # K=0, local rank-one residual: exact echo loss=(1-cos(delta*t))/(2d).
    # Thus a dimension-independent null coefficient is impossible under mixed reset.
    delta=.3;t=.2
    p=(1-math.cos(delta*t))/(2*d)
    assert math.isclose(p,math.sin(delta*t/2)**2/d,rel_tol=1e-12)
    return {'right_swap_module_ratio':ratio,'sqrt_d':math.sqrt(d),
            'rank_one_probability':p,
            'dimension_linear_factor_is_necessary_for_this_mixed_reset_null_protocol':True,
            'scope':'exact elementary formulas; float values are diagnostics'}

if __name__=='__main__':
    result={'random':random_diagnostics(),'same_record_exact':source_record_exact_certificate(),
            'obstructions':sharp_dimension_and_incompatible_extension()}
    (HERE/'PRODUCT_ECHO_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'random':result['random'],
        'exact_rows':result['same_record_exact']['exact_certificate_rows'],
        'coefficient':result['same_record_exact']['coefficient_diagnostic'],
        'tail':result['same_record_exact']['tail_upper_diagnostic'],
        'obstructions':result['obstructions']},indent=2))
