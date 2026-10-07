"""Owned complement-degree-two and API-boundary audit.

Independent reference uses full selected-column permutation determinants and
the complemented polynomial; production uses reciprocal Gram contractions.
"""
from paired_phase_estimator import *
from itertools import combinations
from pathlib import Path
import json, random, time

started=time.perf_counter();rng=random.Random(910221)
d,m,k=6,5,3
columns=[[G(int(a==b)) for a in range(d)] for b in range(d)]
columns += [[G(rng.randrange(-1,2),rng.randrange(-1,2)) for _ in range(d)] for _ in range(4)]
U=columns[::2];V=columns[1::2];lam=[Q(1,2),Q(2,3),Q(3,5),Q(4),Q(9,7)]
coeff={}
for omitted in combinations(range(m),2):
    selected=[a for a in range(m) if a not in omitted]
    selected_columns=[vec for a in selected for vec in (U[a],V[a])]
    coeff[omitted]=determinant([[vec[i] for vec in selected_columns] for i in range(d)])
target=Q(0);lambda_all=Q(1)
for w in lam:lambda_all*=w
for omitted,a in coeff.items():
    weight=lambda_all
    for j in omitted:weight/=lam[j]
    target+=weight*a.norm()
assert target>0

# Acquire a rational ordinary-transpose kernel, then check complementary
# Pluecker coordinates coefficient by coefficient. The first six columns
# are the identity, so the kernel is [-T;I_4] in the original column order.
N=[[-columns[d+j][i] for j in range(4)] for i in range(d)]
N += [[G(int(i==j)) for j in range(4)] for i in range(4)]
assert all(sum((columns[j][i]*N[j][a] for j in range(2*m)),G())==G()
           for i in range(d) for a in range(4))
ratios=[]
for omitted,a in coeff.items():
    omitted_rows=[i for j in omitted for i in (2*j,2*j+1)]
    dual=determinant([N[i] for i in omitted_rows])
    if not dual:assert not a
    else:ratios.append(a/dual)
assert ratios and all(a==ratios[0] for a in ratios)

def radius(variance):
    a,b=variance.numerator,variance.denominator;sa,sb=isqrt(a),isqrt(b)
    if sa*sa==a and sb*sb==b:return Q(sa,sb)
    t=isqrt(16*a*b)
    return Q(t+int(t*t<16*a*b),4*b)
radii=[radius(1/w) for w in lam]
square={}
for A,a in coeff.items():
    for B,b in coeff.items():
        alpha=tuple(int(i in A)+int(i in B) for i in range(m))
        square[alpha]=square.get(alpha,G())+a*b
second=Q(0)
for alpha,a in square.items():
    weight=Q(1)
    for j,e in enumerate(alpha):
        if e==1:weight/=lam[j]
        elif e==2:weight*=radii[j]*radii[j]/lam[j]
    second+=weight*a.norm()*lambda_all*lambda_all
assert second<=Q(24,5)*target*target

draws=[]
phases=[G(1),G(-1),G(0,1),G(0,-1)]
for h in range(m+1):
    z=[G() if j<h else radii[j]*phases[(j+h)%4] for j in range(m)]
    polynomial=sum((a*z[i]*z[j] for (i,j),a in coeff.items()),G())
    reference=lambda_all*polynomial.norm()
    actual=evaluate_complement(U,V,k,z,lam,d)
    assert actual==reference
    draws.append({'zero_labels':h,'value':str(actual)})

rejected=[]
for name,thunk in [
    ('negative_k',lambda:sample_value(U,V,-1,lam)),
    ('noninteger_k',lambda:sample_value(U,V,Q(1,2),lam)),
    ('negative_activity',lambda:sample_value(U,V,k,[-1]+lam[1:])),
    ('dimension_mismatch',lambda:sample_value(U,V[:-1],k,lam)),
    ('epsilon_zero',lambda:approximate(U,V,k,lam,epsilon=0)),
    ('delta_one',lambda:approximate(U,V,k,lam,delta=1))
]:
    try:thunk()
    except ValueError:rejected.append(name)
    else:raise AssertionError(name)
assert sample_value(U,V,m+1,lam)[0]==0

result={'status':'PASS','d':d,'positive_labels':m,'k':k,'effective_complement_degree':2,
        'target':str(target),'activated_second_moment_ratio':str(second/(target*target)),
        'kernel_complement_minor_ratio':str(ratios[0]),
        'complement_coefficients_checked':len(coeff),'zero_pattern_samples':draws,
        'rejected_invalid_inputs':rejected,
        'scope':'Independent full-minor polynomial and rational kernel audit; finite, not proof of the universal 24/5 bound.',
        'elapsed_seconds':time.perf_counter()-started}
Path('work/cycle6/c02_s01/revisions/PHASE_COMPLEMENT_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
