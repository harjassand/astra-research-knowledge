"""Non-Gaussian replicate-closure KL bound, with bounded-IID confidence rule.

Exact abstract complex-vector fixture plus an explicitly labeled PRNG
illustration. This neither supplies a real Fourier/filter record contract nor
certifies IID sampling of a physical instrument or a PRNG.
"""
from fractions import Fraction as F
from itertools import product
from math import factorial,isqrt
from pathlib import Path
import json
import numpy as np

HERE=Path(__file__).resolve().parent
V=[(1,1,1),(1,1j,-1),(1,-1j,-1)]
P=[F(3,5),F(3,10),F(1,10)]
# A common uniform random global phase may be attached to every vector.
# The statistic below cancels it within each replicate.
H=(2+1j,-1+2j,3-2j)
gain=1
for h in H:gain*=int((h*complex(h).conjugate()).real)

def statistic(vs):
    a,b,c=vs
    z=(a[0]*complex(a[1]).conjugate())*(b[1]*complex(b[2]).conjugate())*(c[2]*complex(c[0]).conjugate())
    assert z.imag==int(z.imag)
    return int(z.imag)

A=M2=F(0);A_gain=M2_gain=F(0)
for idx in product(range(3),repeat=3):
    vs=[V[j] for j in idx]
    p=P[idx[0]]*P[idx[1]]*P[idx[2]]
    g=statistic(vs)
    scaled=[tuple(H[k]*v[k] for k in range(3)) for v in vs]
    gg=statistic(scaled)
    assert gg==gain*g
    A+=p*g;M2+=p*g*g
    A_gain+=p*gg;M2_gain+=p*gg*gg
exact=F(2,3)*A*A/M2
assert A==F(-6,125) and M2==F(12,25) and exact==F(2,625)
assert F(2,3)*A_gain*A_gain/M2_gain==exact

def upper_sqrt_fraction(numerator,denominator,scale=10**9):
    # Exact rational outward rounding; no floating log or sqrt in certificate.
    r=isqrt(numerator*scale*scale//denominator)
    if r*r*denominator<numerator*scale*scale:r+=1
    return F(r,scale)

assert sum(F(6)**j/factorial(j) for j in range(31))>400

def bounded_iid_certificate(sum_z,sum_z2,m):
    """Requires INDEPENDENT triples, |z|<=1, and correct reverse involution.

    Total failure<=.01: .005 for two-sided mean, .005 for one-sided2nd moment.
    This is an implemented conditional confidence rule, not a sampling-law test.
    """
    assert m>0 and 0<=sum_z2<=m and abs(sum_z)<=m
    radius_A=upper_sqrt_fraction(12,m)
    radius_M=upper_sqrt_fraction(3,m)
    mean=F(sum_z,m);second=F(sum_z2,m)
    abs_A_low=max(F(0),abs(mean)-radius_A)
    M_up=min(F(1),second+radius_M)
    lower=F(0) if M_up==0 else F(2,3)*abs_A_low**2/M_up
    return dict(failure_probability_upper='.01',triples=m,individual_vectors=3*m,
        abs_mean_lower_exact=str(abs_A_low),second_moment_upper_exact=str(M_up),
        single_vector_reverse_KL_lower_exact=str(lower),
        single_vector_reverse_KL_lower_float=float(lower))

# Actual synthetic type draws, not multinomial-fast-forwarded physical records.
N=200000;rng=np.random.default_rng(20261027)
draws=rng.choice(3,size=(N,3),p=[float(p) for p in P])
left=np.array([1,-1j,1j])[draws[:,0]]
middle=np.array([1,-1j,1j])[draws[:,1]]
right=np.array([1,-1,-1])[draws[:,2]]
sample=(left*middle*right).imag.astype(np.int64)
assert np.all(np.isin(sample,[-1,0,1]))
certificate=bounded_iid_certificate(int(sample.sum()),int(sample@sample),N)
result=dict(scope='Exact mathematical fixture and actual synthetic IID-type draw illustration; no physical record, sampling validation, historical priority or EPR-rate claim.',
    exact_mean=str(A),exact_second_moment=str(M2),
    per_original_vector_KL_lower_exact=str(exact),
    true_per_vector_KL='(1/5)*log(3)',
    complex_gain_product=gain,gain_invariance_checked_exact=True,
    exact_triple_combinations_checked=27,
    synthetic_seed=20261027,synthetic_sum=int(sample.sum()),
    synthetic_sum_squares=int(sample@sample),
    conditional_iid_confidence_certificate=certificate,
    actual_physical_reverse_and_filter_contract='NOT_ACQUIRED')
(HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
