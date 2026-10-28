#!/usr/bin/env python3
"""Independent exact mixed-role statistics. No RNG, no source acquisition."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
from math import comb
import json
root=Path(__file__).resolve().parent
# Exact finite adaptive record tree: known physical one-parameter Choi decoders.
# C(theta)=I4/4+theta Zout⊗Zin, |theta|<=1/4; depolarizing source lambda.
# Six-state mismatch is q(theta)=1/2-2lambda theta/3. This is a diagnostic
# controller, NOT a simulated instance of the full mirror-descent learner.
trees=[];conditional=0
for qpayload in [1,2,3]:
    for N in [3,5,7]:
        if qpayload>N:continue
        for r in [F(1,4),F(1,2)]:
            p=1-r;states={(0,0):F(1)};active=0;delivered=0;L=0;comp=0;gradtotal=0
            for t in range(1,N+1):
                nxt={}
                for (used,parity),mass in states.items():
                    if used==qpayload:
                        nxt[(used,parity)]=nxt.get((used,parity),0)+mass
                        continue
                    active+=mass
                    lam=F(1+(t+used+parity)%3,4);theta=F(parity,16);aa=F(1,32)
                    loss=lambda th:F(1,2)-F(2,3)*lam*th
                    base=loss(theta);slope=-F(2,3)*lam
                    L+=mass*base;comp+=mass*r*F(3,2)*loss(F(1,8))
                    mean=0;second=0
                    # On USE no gradient/output measurement. Role count alone advances.
                    nxt[(used+1,parity)]=nxt.get((used+1,parity),0)+mass*r
                    delivered+=mass*r
                    for z in [-1,1]:
                        pp=loss(theta+z*aa);assert 0<=pp<=1
                        for y,pr in [(0,1-pp),(1,pp)]:
                            prob=p*pr/2;g=F(y*z,1)/(aa*p)
                            mean+=prob*g;second+=prob*g*g
                            key=(used,parity^y);nxt[key]=nxt.get(key,0)+mass*prob
                    assert mean==slope
                    assert second==base/(p*aa*aa)
                    gradtotal+=mass*mean;conditional+=1
                states=nxt;assert sum(states.values())==1
            short=sum(v for (u,par),v in states.items() if u<qpayload)
            binom=sum(F(comb(N,j))*r**j*(1-r)**(N-j) for j in range(qpayload))
            assert short==binom
            assert delivered==r*active==sum(u*v for (u,par),v in states.items())
            assert delivered<=qpayload and active<=N
            trees.append({'q':qpayload,'cap':N,'role_probability':str(r),'shortfall':str(short),'expected_active_calls':str(active),'expected_completed_USES':str(delivered),'delivered_marginal_loss':str(F(3,2)*r*L),'fixed_comparator_cumulative_marginal':str(comp)})
# Standard lower-tail bound checked via its exact mgf inequalities.
# log(2)<=3/4 implies (1-log2)/2>=1/8. The proof uses this symbolic inequality;
# the fixtures below certify the exponential bound with a rational upper series.
tails=[]
for q in range(1,7):
    for multiplier in [4,8,12]:
        N=multiplier*q;r=F(1,2);mu=N*r
        exact=sum(F(comb(N,j))*r**j*(1-r)**(N-j) for j in range(q))
        x=mu/8; term=F(1); partial=F(1)
        for j in range(1,65):
            term*=x/j;partial+=term
        nextterm=term*x/65
        exp_upper=partial+nextterm/(1-x/66)
        assert exact*exp_upper<=1
        tails.append({'q':q,'N':N,'mean':str(mu),'exact_shortfall':str(exact),'Chernoff_exponential_bound_exactly_certified':True})
# New finite horizon and ALL new parameters, not blind base epsilon substitution.
def ceil_log2(v):
    n=0
    while 2**n<v:n+=1
    return n
budgets=[]
for q in [1,2,7,31]:
    for w in [1,2,4]:
        for eps in [F(1),F(1,4),F(1,100)]:
            for gamma in [F(1),F(1,8)]:
                d=2**w;k=2*d;D=3*d*d;Ls=ceil_log2(16/eps);m=2*q+8*Ls;L0=ceil_log2(16*m/eps)
                bound=1024*m*D*D*k*L0/(gamma*eps)
                assert bound>=2*m
                N=2**ceil_log2(bound);r=F(m,N);p=1-r;assert p>=F(1,2)
                eta=gamma/(128*D*D);zeta=eps/(16*m);delta=eta*eps/(64*m)
                coeff=8*eta*D*D/p;assert coeff<=gamma/8
                assert r*zeta*N==eps/16
                barrier=r*k*L0/eta;assert barrier<=N*eps/8
                assert r*N*delta/eta==eps/64
                add=F(3,2)*(eps/16+eps/8+eps/64)/(1-gamma/8)
                assert add<=F(39,112)*eps
                total=add+eps/16+eps/2;assert total<=F(51,56)*eps<eps
                assert N<36864*m*d**5*L0/(gamma*eps)
                # Gaussian-free local-gradient safety, squared exactly.
                assert 8*eta*eta*D*D/(p*p)<=F(1,16)**2
                # e>=2 implies exp(-m/8)<=2^(-L_short)<=eps/16.
                assert m>=2*q and m>=8*Ls and F(1,2**Ls)<=eps/16
                nu=eps/32;R=ceil_log2(4*N/nu);ibits=ceil_log2(D)
                assert F(2*N,2**R)<=nu/2
                bits=N*(N.bit_length()-1+2+R*(ibits+2))
                budgets.append({'q':q,'w':w,'epsilon':str(eps),'gamma':str(gamma),'N':N,'m_role':m,'r':str(r),'p':str(p),'fair_bit_cap_without_optional_frame':bits,'optional_frame_bits':2*q})
assert F(39,112)+F(1,16)+F(1,2)==F(51,56)
# Comparator distinction: a common correlated X error across all q outputs.
correlated=[{'q':q,'correlated_error_probability':'1/10','global_oracle_loss':'1/10','cumulative_marginal_loss':str(F(q,10))} for q in [1,2,5,10]]
source='ordinary_prequential_mixed_payload_memory_service_20261028.md';hh=sha256((root/source).read_bytes()).hexdigest();assert hh=='99d38717805c3af7df24d0fb634d0f4617104e6d767c09796c721809c788f74d'
out={'status':'PASS_EXACT_ACTIVE_ROLE_IMPORTANCE_AND_FINITE_BUDGET_CHECKS','source_sha256':hh,'source_calls':0,'random_draws':0,'source_acquisition_simulations':0,'adaptive_conditional_importance_identities':conditional,'exact_adaptive_role_trees':trees,'exact_binomial_tail_diagnostics':tails,'finite_full_parameter_cases':len(budgets),'finite_budgets':budgets,'correlated_error_comparator_distinction':correlated,'scope':'Deterministic exact probability enumeration and parameter arithmetic. Toy physical scalar decoder policy is not the full mirror learner; full quantum/reference transfer is separately reviewed. No empirical confidence or hardware claim.'}
(root/'prequential_mixed_service_statistics_check_20261028.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['exact_adaptive_role_trees','exact_binomial_tail_diagnostics','finite_budgets']},indent=2));print('trees',len(trees),'tail_cases',len(tails))
