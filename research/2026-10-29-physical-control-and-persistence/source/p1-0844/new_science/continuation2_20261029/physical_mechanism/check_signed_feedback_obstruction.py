"""Independent exact finite fixtures for source-B signed-path obstruction.
The continuum/continuous-time theorem is proved analytically, not by these checks.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, math, random

ZERO=(F(0),); ONE=(F(1),)
P=((F(1,10),F(1,20)),(F(3,10),F(3,20)),
   (F(1,4),F(1,10)),(F(7,20),F(1,10)))
HSTAR=F(-4)

def trim(a):
    a=list(a)
    while len(a)>1 and a[-1]==0:a.pop()
    return tuple(a)
def add(a,b):
    return trim(tuple((a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0)
                      for i in range(max(len(a),len(b)))))
def scale(a,c):return trim(tuple(c*x for x in a))
def mul(a,b):
    z=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):z[i+j]+=x*y
    return trim(z)
def ev(a,x):
    ans=F(0)
    for coeff in reversed(a):ans=ans*x+coeff
    return ans
def one_minus(a):return add(ONE,scale(a,-1))

def full_trees(depth):
    trees=[ZERO]
    counts=[1]
    for _ in range(depth):
        prior=trees
        trees=[ZERO]
        for p in P:
            stay=one_minus(p)
            for a,b in product(prior,repeat=2):
                trees.append(add(mul(stay,a),mul(p,one_minus(b))))
        counts.append(len(trees))
    return trees,counts

full,counts=full_trees(3)
assert counts==[1,5,101,40805]
min_at_star=F(0)
for f in full:
    if f==ZERO:continue
    degree=len(f)-1
    assert degree>=1
    assert ((-1)**(degree-1))*f[-1]>0
    assert ev(f,HSTAR)<0
    assert ev(one_minus(f),HSTAR)>0
    for h in (F(-1),F(0),F(1)):
        assert 0<ev(f,h)<1
    min_at_star=min(min_at_star,ev(f,HSTAR))

# Arbitrary rejected leaves: bounded positive completion with a heralded bit.
# Pair (F,E) counts accepted opposite/same terminal parity relative to local input.
heralded=[(ZERO,ONE),(ZERO,ZERO)]
heralded_counts=[2]
for _ in range(2):
    prior=heralded
    heralded=[(ZERO,ONE),(ZERO,ZERO)]
    for p in P:
        stay=one_minus(p)
        for (fa,ea),(fb,eb) in product(prior,repeat=2):
            heralded.append((add(mul(stay,fa),mul(p,eb)),
                             add(mul(stay,ea),mul(p,fb))))
    heralded_counts.append(len(heralded))
assert heralded_counts==[2,18,1298]
positive_completion=0
for f,e in heralded:
    fv,evv=ev(f,HSTAR),ev(e,HSTAR)
    assert fv<=0<=evv
    assert (f==ZERO)==(fv==0)
    assert (e==ZERO)==(evv==0)
    if f!=ZERO:
        degree=len(f)-1
        assert degree>=1 and (-1)**(degree-1)*f[-1]>0
    if e!=ZERO:
        degree=len(e)-1
        assert (-1)**degree*e[-1]>0
    if f!=ZERO or e!=ZERO:
        positive_completion+=1
        for c in (F(3,20),F(3,10),F(1,2)):
            residual=add(scale(f,1-c),scale(e,-c))
            assert residual!=ZERO and ev(residual,HSTAR)<0

# Randomized policies with positive weights preserve the sign certificate.
rng=random.Random(20261029)
for _ in range(32):
    selected=[rng.randrange(1,len(full)) for _ in range(16)]
    weights=[rng.randrange(1,33) for _ in range(16)]
    mix=ZERO
    for index,w in zip(selected,weights):mix=add(mix,scale(full[index],F(w,sum(weights))))
    assert ev(mix,HSTAR)<0 and len(mix)>1

# The opposite-slope source A lies outside the negative-entry premise and cancels.
sourceA0=P[0];sourceA1=(F(3,10),F(-3,20))
assert add(scale(sourceA0,F(3,4)),scale(sourceA1,F(1,4)))==(F(3,20),)
assert ev(sourceA1,HSTAR)>0

# Continuous-time numerical sanity checks, not finite acquisition claims.
def q(j,h):return -math.log(1-2*float(ev(P[j],F(h))))/2
ct=[]
for h in (-4,-1,0,1):
    a,b=q(0,h),q(3,h)
    flip=a*(-math.expm1(-(a+b)))/(a+b)
    hit=-math.expm1(-b)
    if h==-4:assert a<0 and b<0 and flip<0 and hit<0
    else:assert a>0 and b>0 and 0<flip<1 and 0<hit<1
    ct.append({'h':h,'q0':a,'q3':b,
               'state_feedback_q0_at_zero_q3_at_one_T1_flip':flip,
               'mode3_first_jump_by_T1_signed_mass':hit})

out={
 'scope':'Independent exact rational finite adaptive-tree checks; continuous-time rows are numerical sanity checks only',
 'source_B_flip_affine_coefficients':[[str(x) for x in row] for row in P],
 'negative_witness_h':str(HSTAR),
 'negative_witness_flip_values':[str(ev(p,HSTAR)) for p in P],
 'complete_tree_counts_depth_zero_through_three':counts,
 'nonidentity_complete_trees_checked':len(full)-1,
 'all_positive_flip_polynomials_nonconstant':True,
 'all_odd_endpoint_signed_evaluations_negative':True,
 'most_negative_complete_tree_at_witness':str(min_at_star),
 'heralded_tree_counts_depth_zero_through_two':heralded_counts,
 'heralded_trees_with_positive_completion':positive_completion,
 'all_nondegenerate_heralded_target_residuals_negative_at_witness':True,
 'positive_mixture_fixtures':32,
 'source_A_exact_flip_3_over_20_passes_outside_scope':True,
 'continuous_time_sanity':ct}
Path(__file__).with_name('SIGNED_FEEDBACK_OBSTRUCTION_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
