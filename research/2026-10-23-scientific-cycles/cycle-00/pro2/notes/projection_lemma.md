# Shifted spectral projections: proof, sharpness and weighted-CDF obstruction

Prepared independently for the PRO2 restoration construction, 21 October 2026.
This note proves the mathematical lemma directly. It does not claim historical
novelty. Its elementary perturbation ingredients are consistent with the usual
ordered-spectrum Sylvester and projection-angle methods; the separate literature
task determines attribution.

## 1. Main statement

Let A and B be self-adjoint matrices on the same finite-dimensional complex
Hilbert space, and let ||A-B||_op <= e. For a unit vector v define

F_A,v(t) = <v, 1_{(-infinity,t]}(A) v>.

For every real t and every eta > 0, put delta = min(1,e/eta). Then

F_B,v(t-eta) - delta <= F_A,v(t) <= F_B,v(t+eta) + delta.

Each side may of course be clipped to [0,1]. The coefficient 1 in e/eta is
optimal uniformly over all dimensions, matrices, unit vectors and thresholds.
The inclusions at t and t +/- eta are exactly as displayed. No spectral-gap
assumption on A or B is required.

The stronger, probability-dependent statement is

L_delta(F_B,v(t-eta)) <= F_A,v(t) <= U_delta(F_B,v(t+eta)),

where, for 0 <= q <= 1,

U_delta(q) = 1, if q >= 1-delta^2;
U_delta(q) = (sqrt((1-delta^2)q) + delta sqrt(1-q))^2, otherwise;

L_delta(q) = 0, if q <= delta^2;
L_delta(q) = (sqrt((1-delta^2)q) - delta sqrt(1-q))^2, otherwise.

Equivalently these maps add/subtract asin(delta) to the angle asin(sqrt(q)),
clipping the resulting angle to [0,pi/2] before taking sin^2. Both maps are
monotone. In particular an upper quadrature bracket q_U and a lower bracket q_L
for the shifted B probabilities can be substituted directly:

L_delta(q_L) <= F_A,v(t) <= U_delta(q_U).

Near a zero upper bracket, U_delta(0)=delta^2, an appreciable improvement over
the universal additive delta. This sharper statement follows from the same
operator information; it does not assume a favorable unknown eigenvector.

## 2. Ordered-spectrum leakage lemma

Set P=1_{(-infinity,t]}(A), Q=1_{(-infinity,t+eta]}(B), and R=I-Q.
The zero-rank cases are immediate. Otherwise let A_P and B_R denote the
restrictions to ran(P) and ran(R). Define X=PR as a map ran(R) -> ran(P).
Since P commutes with A and R commutes with B,

A_P X - X B_R = P(A-B)R.

Let C=t I-A_P >= 0 and D=B_R-t I > eta I. Then

C X + X D = -P(A-B)R.

The unique solution is the norm-convergent integral

X = - integral_0^infinity exp(-s C) P(A-B)R exp(-s D) ds.

Indeed differentiating exp(-s C)Y exp(-s D) and integrating proves the
Sylvester identity and uniqueness. Its norm is bounded by

||X|| <= integral_0^infinity e exp(-eta s) ds = e/eta.

In finite dimension, the actual minimum eigenvalue of D is strictly larger
than eta because R selects B eigenvalues strictly above t+eta. This yields
the stronger denominator if that eigenvalue is known. The stated e/eta bound
is valid without knowing it. The general separated bound is

||PR|| <= ||A-B|| / (min spec(B_R)-max spec(A_P)).

No ordering of the full operators A and B was assumed or inferred.

## 3. From leakage to an additive Loewner bound

For arbitrary orthogonal projections P,Q and 0 < delta <= 1, the condition
||P(I-Q)|| <= delta implies P <= Q+delta I.

Proof: set H=Q+delta I > 0. The inequality P <= H is equivalent to
P H^{-1} P <= P on ran(P): both are equivalent to
||H^{-1/2}P||^2 <= 1. Directly,

P H^{-1}P
 = P/(1+delta) + P(I-Q)P/[delta(1+delta)]
 <= P/(1+delta) + delta P/(1+delta)
 = P.

At delta=0, the leakage condition gives ran(P) subset ran(Q), so P<=Q.
At delta>=1 the bound P<=Q+I is trivial. Thus the leakage estimate of section 2
proves the upper additive bound. Interchanging A and B and shifting the
threshold from t to t-eta proves the lower bound.

The implication also identifies the optimal nonnegative additive slack for a
fixed pair of projections: it is exactly ||P(I-Q)||. This remains true when
their ranks differ. When P-Q is negative semidefinite that quantity is zero;
one must not replace it by an unconstrained possibly negative largest eigenvalue.

## 4. Sharp probability-dependent bound

Assume ||P(I-Q)|| <= delta and let q=||Qv||^2. If Pv=0 the upper bound is
immediate. Otherwise x=Pv/||Pv|| is a unit vector in ran(P), so
r=||Qx||^2 >= 1-delta^2. Cauchy-Schwarz in the mutually orthogonal Q and I-Q
subspaces gives

sqrt(<v,Pv>) = |<x,v>| <= sqrt(rq)+sqrt((1-r)(1-q)).

The maximum over r in [1-delta^2,1] is 1 if q lies in that interval; otherwise
it is attained at r=1-delta^2. Squaring proves U_delta(q).
Applying the same result to the reversed shifted pair gives

F_B,v(t-eta) <= U_delta(F_A,v(t)).

The smallest admissible argument on the right is L_delta(F_B,v(t-eta)),
which proves the lower bound, including the cases with probabilities 0 and 1.

The maps satisfy U_delta(q) <= min(1,q+delta) and
L_delta(q) >= max(0,q-delta), by section 3. They are sharp given only the
projection leakage bound and q: two-dimensional rank-one projections realize
the extremal angle, or a smaller angle in the clipped cases.

## 5. Exact two-dimensional sharpness family

Choose gamma>eta, 0<s<1, c=sqrt(1-s^2), and

A = gamma [[0,0],[0,1]],
B = gamma [[s^2,s c],[s c,c^2]].

Both matrices have eigenvalues 0,gamma. With t=0, their relevant projections are

P = [[1,0],[0,0]],
Q = [[c^2,-s c],[-s c,s^2]],
P-Q = [[s^2,s c],[s c,-s^2]].

The identities (P-Q)^2=s^2 I and A-B=-gamma(P-Q) imply

||A-B||=gamma s=e; lambda_max(P-Q)=s=e/gamma.

The unit vector

w = (sqrt((1+s)/2), sqrt((1-s)/2))

has F_A,w(0)=(1+s)/2 and F_B,w(eta)=(1-s)/2. Their difference is s.
For fixed 0<e<eta, choose any gamma>eta and set s=e/gamma; sending gamma down
to eta shows that no universally smaller additive slack than e/eta is possible.
For e=eta the same limit approaches 1. For e>eta the value 1 is already attained
in dimension one by A=0 and eta<B<=e. Thus min(1,e/eta) is the exact universal
supremum, although the strict cutoff in the high subspace can prevent attainment
at e<=eta.

The probability-dependent bounds are sharp in the same limiting sense by
choosing the probe angle to produce the desired q. The additive worst-case
probe above has q=(1-s)/2 and attains U_s(q)=(1+s)/2.

## 6. Counterexample to horizontal shifts alone

The same family is an explicit counterexample even if eta=e, the usual Weyl
eigenvalue-shift magnitude. Fix gamma=1 and choose arbitrarily small 0<e<1,
with s=e. For the fixed probe v=(1,0),

F_A,v(0)=1, whereas F_B,v(e)=1-e^2 < 1.

For the unit probe w above the failure is linear: the difference is e.
The failure is not caused by evaluating at an atom: the same projections and
inequality failure hold at every threshold 0<t<1-e in this gamma=1 example.
The unweighted spectra are identical. Therefore this example does not challenge
Weyl's eigenvalue inequality or its implication for the unweighted normalized
trace CDF. It isolates the incorrect transfer from eigenvalue counting to a
probe-weighted spectral measure. Arbitrarily small operator error can rotate
spectral projectors, and the weighted measure detects that rotation.

Likewise, a proposed universal quadratic slack (e/eta)^2 is false: the sharp
family has difference e/gamma arbitrarily close to e/eta.

## 7. Consequence for probe-dependent backward errors

For each realized probe v, suppose a computed Krylov construction is exactly
representable for a self-adjoint B_v with a verified norm bound
||A-B_v||<=e_v. B_v may depend arbitrarily on v. The deterministic inequalities
above hold for that realized pair before averaging or applying a random-probe
concentration theorem for the original fixed A. They require no independence
between B_v and v. One must apply concentration to the original A, not pretend
the random B_v is a fixed operator independent of its own probe.

If the first computed basis vector is w instead of the desired unit v, add a
separate starting-vector correction. For every projection Pi,

|<v,Pi v>-<w,Pi w>| <= sqrt(1-|<v,w>|^2).

Proof: vv*-ww* has its two possible nonzero eigenvalues equal to plus/minus
sqrt(1-|<v,w>|^2); maximizing its trace against 0<=Pi<=I gives the positive
eigenvalue. This correction is at most the phase-aligned distance ||v-exp(i phi)w||.
It is not automatically zero after a global polar orthogonalization.

## 8. Verification scope and cost

The companion checker `checks/check_projection_lemma.py` verifies exact rational
identities for three members of the sharpness family, including the projector
and perturbation norm identities and weighted-CDF differences. It also performs
bounded deterministic-seed floating tests on general complex Hermitian pairs
and unequal-rank projections. The latter tests are diagnostics, not proofs or
certified floating-point error bounds. Their observed runtime and platform
information are recorded in `results/projection_lemma_checks.json`.

Observed checker result: three rational sharpness cases passed; 512 complex
Hermitian pairs with four probes each and 256 arbitrary projection pairs passed
the declared floating diagnostic tolerance. The largest positive numerical
violation was 1.3322676295501878e-15. Checker body wall time was
0.18680997000046773 seconds and CPU time was 0.659672336 seconds on the recorded
runtime. These figures exclude agent reasoning, file preparation and tool
startup. The CPU/wall difference reflects the runtime's underlying numerical
execution; no total scientific-cost claim is inferred.

The mathematical proof is complete for finite self-adjoint matrices with an
already valid operator-norm error bound. It does not certify how that norm bound
was obtained, the exact orthogonality of floating-point Krylov vectors, random
number generation, or the full stochastic Lanczos construction. Those are
separate proof obligations retained by the main branch.
