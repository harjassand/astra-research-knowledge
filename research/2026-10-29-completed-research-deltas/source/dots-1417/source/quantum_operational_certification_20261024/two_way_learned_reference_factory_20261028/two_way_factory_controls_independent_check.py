"""Independent exact composition checks, not source samples or accepted-code replay."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib, json

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'FINITE_TWO_WAY_LEARNED_REFERENCE_FACTORY.md'
EXPECTED='af2a155f109c33987f13f87511a5758315e605643f1bdf1938686a731283e1c8'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED

def R(f): return (10*f*f-2*f+1)/(8*f*f-4*f+5)
def P(f): return (8*f*f-4*f+5)/9
def ceil_log2(x):
    k=max(0, x.numerator.bit_length()-x.denominator.bit_length())
    while F(2)**k<x:k+=1
    while k and F(2)**(k-1)>=x:k-=1
    return k

warm_cases=0
for j in range(2,11):
    g=F(1,2**j)
    delta=g/512
    actual_debit=168*delta+(2*g)/32
    assert actual_debit==25*g/64 < g/2
    lower_f=F(1,2)+2*g-actual_debit
    assert lower_f-g/4 >= F(1,2)+5*g/4
    assert (F(1,2)+5*g/4)-g/4 == F(1,2)+g
    warm_cases+=1

# The concave growth numerator 1+4t-24t^2 has minimum >=1/2
# on [0,1/4]. This exact endpoint certificate is not a grid proof.
assert min(F(1),1+4*F(1,4)-24*F(1,4)**2)==F(1,2)
f=F(3,4)
for _ in range(9):f=R(f)
assert f>F(39,40)

# Derive the successful label masses from the two-pair Bell-label instrument,
# then check first-two-success factorization for every qualifying four-attempt
# coarse history. There are no random draws and no Bell/source simulator.
selection_checks=0
for f0 in [F(1,2),F(9,16),F(5,8),F(3,4),F(39,40)]:
    q=[f0]+[(1-f0)/3]*3
    success=[F(0)]*4
    for e1,e2 in product(range(4),repeat=2):
        x1,z1=e1%2,e1//2; x2,z2=e2%2,e2//2
        if x1==x2:success[x1+2*(z1^z2)]+=q[e1]*q[e2]
    prob=sum(success)
    assert prob==P(f0) and success[0]/prob==R(f0)
    f1=R(f0); out=[f1]+[(1-f1)/3]*3
    atoms=[1-prob]+[prob*a for a in out]  # 0=fail, 1..4=kept label
    joint={}
    for row in product(range(5),repeat=4):
        mask=tuple(int(v!=0) for v in row)
        if sum(mask)<2:continue
        labels=tuple(v-1 for v in row if v)[:2]
        weight=F(1)
        for v in row:weight*=atoms[v]
        joint[(mask,labels)]=joint.get((mask,labels),F(0))+weight
    for mask in product(range(2),repeat=4):
        count=sum(mask)
        if count<2:continue
        pattern=prob**count*(1-prob)**(4-count)
        for labels in product(range(4),repeat=2):
            assert joint.get((mask,labels),F(0))==pattern*out[labels[0]]*out[labels[1]]
            selection_checks+=1

cap_cases=0
for g,Q,dc,br in product([F(1,4),F(1,16),F(1,128)],[1,3,9,257],
                         [F(1,10),F(1,100),F(1,1024)],[F(1,8),F(1,64)]):
    k1=0;t=g
    while t<F(1,4):t*=F(9,8);k1+=1
    K=k1+9
    L=0
    while F(Q,5)*F(1,4)**(2**L)>dc:L+=1
    assert L==0 or F(Q,5)*F(1,4)**(2**(L-1))>dc
    B=Q*5**L
    tc=4*ceil_log2(2*(K+1)/br)
    assert F(1,2)**(tc//4)<=br/(2*(K+1))
    n=B;attempts=0
    for _ in range(K):
        m=4*(n+tc)
        assert 4*n<=m
        n=2*m;attempts+=m
    assert n==8**K*B+8*tc*(8**K-1)//7
    assert attempts<=n
    assert 2*Q*(F(1,4)**(2**L)/10)<=dc
    cap_cases+=1

bad_history_cases=0
for Q,bad,p in product([1,2,3,9],[F(1,64),F(1,8),F(1,4)],
                        [F(1,40),F(1,160),F(1,2560)]):
    # A concrete total replacement-on-bad Pauli channel, no renormalization.
    error=2*(1-((1-bad)*(1-p)**Q+bad/F(4)**Q))
    assert error<=2*bad+2*Q*p
    bad_history_cases+=1

assert F(1,4)+6*F(1,64)+F(1,4)+F(1,4)==F(27,32)<1
assert F(5,8)==F(1,2)+2*F(1,16)
assert 5**5<2**16  # exact entropy >1 check for (5,1,1,1)/8

result=dict(status='PASS_INDEPENDENT_EXACT_FACTORY_COMPOSITION_CHECKS',
    source_sha256=EXPECTED,source_calls=0,new_random_sampling=False,
    warm_substitution_cases=warm_cases,first_two_success_joint_checks=selection_checks,
    exact_cap_cases=cap_cases,total_bad_history_channel_cases=bad_history_cases,
    R9_three_quarters_exact_greater_than='39/40',typed_budget='27 epsilon/32',
    scope='Exact scalar and finite-history composition checks. No warm acquisition, frame compiler, QEC circuit, source, or hardware execution.')
out=ROOT/'two_way_factory_controls_independent_check.json'
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
