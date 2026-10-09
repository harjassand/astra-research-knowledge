#!/usr/bin/env python3
"""Exact independent formula/interface checks; not universal proof validation."""
from pathlib import Path
import hashlib
import json
import sympy as s

BASE = Path(__file__).resolve().parent
tests = []

def eq(a, b):
    if isinstance(a, s.MatrixBase):
        assert a.shape == b.shape
        assert all(s.simplify(x) == 0 for x in a-b)
    else:
        assert s.simplify(a-b) == 0

def psd(a):
    eq(a, a.conjugate().T)
    import itertools
    for r in range(1, a.rows+1):
        for ix in itertools.combinations(range(a.rows),r):
            x = s.simplify(a.extract(ix,ix).det())
            assert x >= 0, (ix,x)

def record(name, **details):
    tests.append(dict(name=name,status="PASS",**details))

# 1. Fully symbolic noncommuting covariance and signed inverses.
u,v = s.symbols("u v",real=True,nonzero=True)
m = s.symbols("m",positive=True)
g0,g1,g2 = s.symbols("g0 g1 g2",real=True)
F = s.diag(u,v)
G = s.Matrix([[g0,g1],[g1,g2]])
I = s.eye(2)
N = m*I
for n in range(1,5):
    N = F.inv()*(N+G)*F.inv()/2
    A = (2*F**2)**(-n)
    closed = m*A+s.zeros(2)
    D = m*A+s.zeros(2)
    slack = s.zeros(2)
    for r in range(1,n+1):
        closed += F**(-r)*G*F**(-r)/2**r
        D += (2*F**2)**(-r)
        slack += F**(-r)*(I-G)*F**(-r)/2**r
    eq(N,closed)
    eq(D-N,slack)
    H = 2*F**2-I
    eq(D,H.inv()*(I-A)+m*A)
Fex=s.diag(s.Rational(4,5),-s.Rational(9,10))
Gex=s.Matrix([[s.Rational(3,5),s.Rational(1,10)],
              [s.Rational(1,10),s.Rational(4,5)]])
assert Fex*Gex != Gex*Fex
psd(I-Gex)
Nex=2*I
for n in range(1,5):
    Nex=Fex.inv()*(Nex+Gex)*Fex.inv()/2
    Dex=2*(2*Fex**2)**(-n)+sum(
        ((2*Fex**2)**(-r) for r in range(1,n+1)),s.zeros(2))
    psd(Dex-Nex)
record("generic_signed_noncommuting_tree_covariance",
       symbolic_depths=[1,2,3,4],initial_variance="mI",
       identities=["exact recursion","same-leaf closed formula",
                   "congruence slack","finite geometric bound"],
       physical_channel_claim_for_abstract_example=False)

# 2. An actual pure six-effect POVM with fast/slow covariance cross terms.
X=s.Matrix([[0,1],[1,0]])
Y=s.Matrix([[0,-s.I],[s.I,0]])
Z=s.diag(1,-1)
pauli=[X,Y,Z]
vecs=[s.Matrix([1,0,0]),s.Matrix([s.Rational(3,5),0,s.Rational(4,5)]),
      s.Matrix([0,1,0])]

def pi(r):
    return (s.eye(2)+sum((r[a]*pauli[a] for a in range(3)),s.zeros(2)))/2

effects=[]
states=[]
scores=[]
for j,r in enumerate(vecs):
    for sign in [1,-1]:
        P=pi(sign*r)
        eq(P*P,P)
        eq(s.trace(P),1)
        effects.append(P/3)
        states.append(P)
        scores.append(sign*3 if j==0 else 0)
eq(sum(effects,s.zeros(2)),s.eye(2))
eq(sum((z*M for z,M in zip(scores,effects)),s.zeros(2)),X)
C=s.zeros(3);cross=s.zeros(3,1);K=0
for M,P,z in zip(effects,states,scores):
    p=s.trace(M)/2
    xx=s.Matrix([s.trace(P*A) for A in pauli])
    C+=p*xx*xx.T
    cross+=p*xx*z
    K+=p*z*z
J=s.Matrix([1,0,0])
eq(cross,J)
eq(K,3)
assert C[0,2] == s.Rational(4,25)
eq(C-J*J.T/K,(vecs[1]*vecs[1].T+vecs[2]*vecs[2].T)/3)
psd(C-J*J.T/K)
gram=C.row_join(J).col_join(J.T.row_join(s.Matrix([[K]])))
psd(gram)
record("full_input_Gram_with_nonzero_fast_slow_cross",
       effects=6,fast_slow_cross="4/25",estimator_variance="3",
       full_domain_schur_bound="C>=eX eX^T/3")

# 3. Actual mixed effects refined spectrally, retaining the tracial barycenter.
coarse=[(pi(vecs[0])+pi(vecs[1]))/3,
        (pi(-vecs[0])+pi(-vecs[1]))/3,
        pi(vecs[2])/3,pi(-vecs[2])/3]
eq(sum(coarse,s.zeros(2)),s.eye(2))
h=s.Matrix([2/s.sqrt(5),0,1/s.sqrt(5)])
cp=(1+2/s.sqrt(5))/3
cm=(1-2/s.sqrt(5))/3
assert cp>0 and cm>0
eq(cp*pi(h)+cm*pi(-h),coarse[0])
eq(cm*pi(h)+cp*pi(-h),coarse[1])
refined=[(cp,pi(h)),(cm,pi(-h)),(cm,pi(h)),(cp,pi(-h)),
         (s.Rational(1,3),pi(vecs[2])),(s.Rational(1,3),pi(-vecs[2]))]
eq(sum((c*P for c,P in refined),s.zeros(2)),s.eye(2))
eq(sum((c*P/2 for c,P in refined),s.zeros(2)),s.eye(2)/2)
CC=s.zeros(3);CR=s.zeros(3)
for M in coarse:
    p=s.trace(M)/2
    R=M/s.trace(M)
    xx=s.Matrix([s.trace(R*A) for A in pauli])
    CC+=p*xx*xx.T
for c,P in refined:
    xx=s.Matrix([s.trace(P*A) for A in pauli])
    CR+=(c/2)*xx*xx.T
eq(CR-CC,s.Rational(2,15)*h*h.T)
psd(CR-CC)
record("exact_pure_effect_refinement",
       refined_effects=6,barycenter="I2/2",
       covariance_gain="(2/15)h h^T")

# 4. Faithful tracial M2 direct-sum C with a genuinely center-mixing Phi.
weights=s.Matrix([s.Rational(3,10),s.Rational(3,10),s.Rational(2,5)])
W=s.diag(*weights)
P=s.Matrix([[s.Rational(9,10),0,s.Rational(1,10)],
            [0,1,0],
            [s.Rational(3,40),0,s.Rational(37,40)]])
eq(P*s.ones(3,1),s.ones(3,1))
eq(weights.T*P,weights.T)
eq(W*P,P.T*W)
assert all(x>=0 for x in P)
tt=s.symbols("t")
eq(P.charpoly(tt).as_expr(),(tt-1)**2*(tt-s.Rational(33,40)))
center=s.Matrix([0,0,1])
image=P*center
assert image[0] != image[1]  # first M2 block is not scalar
eq(image,s.Matrix([s.Rational(1,10),0,s.Rational(37,40)]))
# Three minimal projection atoms: probabilities equal tau(pi), not 1/3.
prob=weights
eq(sum((prob[j]/weights[j]*s.eye(3)[:,j] for j in range(3)),s.zeros(3,1)),
   s.ones(3,1))
assert prob != s.ones(3,1)/3
# Their relative canonical map is identity on diagonal coordinates and
# dephasing on the full M2 block, thus fixes the entire algebra center.
Psi=s.eye(3)
psd(W*(Psi-P**2))
psd(W*(Psi-(2*P**2-s.eye(3))))
record("unequal_weight_tracial_center_mixing_interface",
       algebra="M2 direct_sum C",block_weights=["3/5","2/5"],
       minimal_projection_weights=["3/10","3/10","2/5"],
       Phi_center_image=["1/10","0","37/40"],
       Phi_diagonal_spectrum=["1","1","33/40"],
       compatibility="UCP copy-state joint formula with row probabilities P",
       posterior_density="M/tau(M)",
       refined_probability="c tau(pi)",
       comparator_center_preserved=True)

# 5. Exact residual supplying factor four.
q=s.symbols("q",real=True)
eq(4*(1-q)-2*(1-q*q),2*(1-q)**2)
record("factor_four_residual",identity="4(I-Phi)-2(I-Phi^2)=2(I-Phi)^2")

out=dict(
 scope="Independent exact generic identities and finite weighted-interface controls; analytic quantified proofs separate",
 sympy_version=s.__version__,
 proof_sha256=hashlib.sha256((BASE/"BLIND_BASELINE.txt").read_bytes()).hexdigest(),
 extension_sha256=hashlib.sha256((BASE/"FAITHFUL_TRACIAL_EXTENSION.txt").read_bytes()).hexdigest(),
 originator_physical_scripts_executed=False,
 tests=tests,all_pass=True,external_formal_validation="unverified")
(BASE/"generic_replay.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))

