from fractions import Fraction as F
from math import comb
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
def ceilq(x):return -(-x.numerator//x.denominator)
def minbits(delta):
    b=0
    while F(1,2**b)>delta:b+=1
    return b
def direct_cdf(n,p,t):
    # Direct integer binomial coefficients, independently of the author's
    # term-to-term division recurrence.
    aa,bb=p.numerator,p.denominator
    return F(sum(comb(n,i)*aa**i*(bb-aa)**(n-i) for i in range(t+1)),bb**n)

cases=[]
for alpha in [F(3,10),F(1,7),F(1,25)]:
    for delta in [F(1,5),F(1,37)]:
        b0=minbits(delta/2)
        for j in [0,2]:
            dj=delta/2**(j+1);b=minbits(dj);assert b==b0+j
            m=ceilq(32*b/alpha);threshold=(3*alpha*m/4).__floor__()
            assert threshold==24*b
            bad=direct_cdf(m,alpha,threshold)
            good_reject=1-direct_cdf(m,alpha/4,threshold)
            assert bad<=dj and good_reject<=dj**8
            cases.append({'alpha':str(alpha),'delta':str(delta),'j':j,'minimal_b':b,'tests':m,
                          'integer_accepted_failure_threshold':threshold,'boundary_false_accept':float(bad),
                          'good_rejection':float(good_reject),'allocated_risk':str(dj)})

# Independent all-tail analytic majorant. After j*=ceil(log2 r), reach is
# <=2^[-4s^2-4s]. Stage costs add 2^(p*s)*(s+1)^w after factoring out the
# polynomial dependence on r, 1/epsilon and log(1/delta).
tails=[]
for p in [0,6,16,40]:
    for w in [1,2,5]:
        S=max(0,ceilq(F(p+w-7,8)))
        def term(s):
            exponent=-4*s*s+(p-4)*s
            return F(2**exponent if exponent>=0 else 1,1 if exponent>=0 else 2**(-exponent))*(s+1)**w
        for s in range(S,S+20):assert term(s+1)<=term(s)/2
        bound=sum((term(s) for s in range(S)),F(0))+2*term(S)
        assert sum((term(s) for s in range(S+30)),F(0))<=bound
        tails.append({'rank_exponent':p,'polynomial_stage_exponent':w,'geometric_tail_starts':S,'exact_infinite_series_upper':str(bound)})

# Exact reach probabilities for a finite idealized sequence of good stages.
reach=[]
for delta in [F(1,5),F(1,37)]:
    for jstar in [0,3,8]:
        product=F(1)
        for s in range(8):
            closed=(delta/2**(jstar+1))**(8*s)*F(1,2**(4*s*(s-1)))
            assert product==closed
            if s==7:reach.append({'delta':str(delta),'jstar':jstar,'stages_past_first_good':s,'reach_upper':float(product)})
            product*=(delta/2**(jstar+s+1))**8

# Reusing one hidden training realization does not validate a fresh service
# channel. Here M=(1-p)id+pZ has infidelity p>alpha, but a single shared-good
# realization makes every validation test pass with probability1-p.
p,alpha,delta=F(1,5),F(1,10),F(1,100)
assert p>alpha and 1-p>delta
result={'exact_binomial_cases':cases,'infinite_expected_cost_majorants':tails,'closed_form_reach_checks':reach,
        'whole_block_reset_counterexample':{'true_fresh_service_infidelity':str(p),'quality_threshold':str(alpha),'false_acceptance_if_one_training_realization_is_reused':str(1-p),'allowed_risk':str(delta)},
        'finite_integer_simplification':'With0<alpha<1 and m=ceil(32b/alpha), floor(3alpha*m/4)=24b.',
        'scope':'Exact statistical and query-cost checks; candidate physical decoder and control runtime are separate dependencies.'}
(HERE/'INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print('Passed',len(cases),'direct binomial cases and',len(tails),'infinite-tail majorants')
