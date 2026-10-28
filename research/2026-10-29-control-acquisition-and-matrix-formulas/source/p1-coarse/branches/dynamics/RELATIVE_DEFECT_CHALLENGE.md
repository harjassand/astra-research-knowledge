# Relative primitive defects do not control all-word output error

Independent check of the root construction, 28 October 2026. The algebra
is correct. The counterexample survives identity centering, finite reachable
dimension, matched preparation and scalar receiver, exact Galerkin
compression, completely positive reciprocal quantum channels, and removal
of both exact extra conservation and zero primitive eigenvalues.

The root is preserving and executing the main rational three-dimensional
fixture. This note supplies an independent derivation, a quantum-channel
embedding, and the scope of possible repairs. The independent executable
check here tests that embedding rather than duplicating the root compiler.

## 1. Exact residual identities

Write e=epsilon>0, d=e^2, a=1+e^2, t=1-e^2, and s=a+d^2. Let

\[
u_+=(d,1,e)^T,\quad u_-=(-d,1,-e)^T,\qquad
A_\pm=I-u_\pm u_\pm^T/s.
\]

These are positive orthogonal projections. Let b=e_1,
h=(0,1,e)^T, V=[b,h], and W=V^TV=diag(1,a).
The subspace is an actual two-word subspace, since

\[
A_+b=(a/s)b-(d/s)h,\qquad
h=(a/d)b-(s/d)A_+b.
\]

The displayed basis is an invertible rational change of coordinates from
[b,A_+b]. No physical superposition preparation is required. The large
coordinate coefficients do matter for finite-precision acquisition, but
cannot rescue a false exact coordinate-invariant theorem.

Let T_i=W^{-1}V^TA_iV and D_i=A_iV-VT_i. Since u_+ lies in the span of V,
D_+=0. For the minus operator, set

\[
r=(-d,t),\quad q=W^{-1}r^T,\quad
g=(0,e,-1)^T,\quad z=(2e/a)g.
\]

Then u_-=Vq+z, z is orthogonal to the dictionary, and ||z||^2=4e^2/a.
Consequently

\[
T_-=I-qr/s,\qquad D_-=-zr/s,\qquad
E_-=D_-^TD_-=\frac{4e^2}{a s^2}r^Tr.
\]

Also

\[
(I-T_-)^TW(I-T_-)
=\frac{a d^2+t^2}{a s^2}r^Tr.
\]

Thus the exact identity is

\[
\boxed{E_-=\kappa^2(I-T_-)^TW(I-T_-),\quad
\kappa^2=\frac{4e^2}{a d^2+t^2}\longrightarrow0.}
\]

For the plus operator the corresponding inequality holds because E_+=0.
Both reduced maps are positive self-adjoint contractions in the W metric.
Both Galerkin weak defects F_i=V^TA_iV-WT_i are exactly zero, so the
first-order dual correction is zero too. The counterexample therefore
applies to the exact corrected scalar predictor, not only an uncorrected
projection predictor.

## 2. The true source preserves a large part of the port

The common fixed direction is k=(e,0,-d)^T. The squared projection of b onto
that direction is e^2/(e^2+d^2). Every word fixes this component, and every
product contracts its orthogonal complement. Therefore every word obeys

\[
\boxed{\langle b,A_wb\rangle\ge
\frac{e^2-d^2}{e^2+d^2}=\frac{1-e^2}{1+e^2}.}
\]

This bound does not rely on positivity of arbitrary nonsymmetric products.
It uses the invariant orthogonal decomposition and Cauchy-Schwarz on the
remaining component.

## 3. The reduced cycle eventually erases the port

The plus compression has rank one. Its fixed line in coordinates is
w=(a,-d)^T, with ||Vw||^2=a s. Hence C=T_-T_+ has rank one and nonzero
eigenvalue

\[
\boxed{\lambda=\operatorname{tr}C
=1-\frac{4d^2}{a s^2}.}
\]

One way to see this is that r w=-2d, so projecting u_- onto the plus fixed
line has squared norm 4d^2/(a s). For e>0 the eigenvalue lies in (0,1).
For integer H>=1, C^H=lambda^(H-1)C. Since C is W-contractive and b has
unit norm,

\[
|\langle b,V C^H e_1\rangle|\le\lambda^{H-1}.
\]

Choose H=ceil(10/(1-lambda))+1. The right side is at most exp(-10),
whereas the true response to the corresponding 2H primitive operations
is at least (1-e^2)/(1+e^2). As e tends to zero, relative residual
kappa tends to zero but this scalar output discrepancy tends to
1-exp(-10).

The mechanism is instability of a nearly common fixed space under
compression. The source has a nearly full port weight in a direction
slightly outside the dictionary. The reduced primitives each have a fixed
line, but those lines have no exact common nonzero vector. Tiny per-step
inconsistency accumulates over H=Theta(e^-4) alternating cycles.

## 4. Removing exact extra conservation does not repair it

Set eta=e^10 and alpha=1-eta, and replace every primitive by
A'_i=alpha A_i. For sufficiently small e, these operators have no
nonzero common fixed vector. Their compressions and defects are
T'_i=alpha T_i and D'_i=alpha D_i.

The same relative bound survives because

\[
\begin{aligned}
&(I-\alpha T)^TW(I-\alpha T)
-\alpha^2(I-T)^TW(I-T)\\
&\qquad=\eta^2W+2\eta\alpha W(I-T)\succeq0,
\end{aligned}
\]

using W-self-adjointness and 0<=T<=I. Thus E'_i remains bounded by
kappa^2 times the displayed new relative defect denominator.

The true response after 2H primitives is at least

\[
(1-2H\eta)\frac{1-e^2}{1+e^2}\longrightarrow1,
\]

while the reduced response remains at most exp(-10). Here
H=Theta(e^-4), so H eta=O(e^6). The failure is therefore a slow-mode
obstruction even when the complete common fixed subspace is known and
removed.

## 5. A four-level quantum implementation with one fixed scalar receiver

The 3-by-3 plane projection itself is not a qubit Bloch dephasing map.
There is nevertheless a simple completely positive realization.
Use a four-level Hilbert space with reference level |0> and three mode
levels. Define the real Hermitian reflection

\[
U_u=\operatorname{diag}(1,I_3-2uu^T/s)
\]

and the dephasing channel

\[
\Phi_u(X)=\tfrac12(X+U_u XU_u).
\]

This is a random-unitary CPTP, unital, Hilbert-Schmidt self-adjoint
orthogonal projection. On the invariant real reference-coherence
subspace, identify v in R^3 with

\[
X_v=|0\rangle\langle v|+|v\rangle\langle0|.
\]

Direct multiplication gives

\[
\Phi_u(X_v)=X_{(I-uu^T/s)v}=X_{A_uv}.
\]

Let D(X)=tr(X)I_4/4 be complete depolarization, and use

\[
\Phi'_u=(1-\eta)\Phi_u+\eta D.
\]

Then the coherence action is precisely A'_u. The identity is the only
fixed operator, since every traceless Hilbert-Schmidt direction contracts
by at least the common factor 1-eta. The complete conserved subspace and
its baseline are therefore known, rather than hidden assumptions.

Use the same fixed preparation and two-outcome effect throughout:

\[
\rho_b=I_4/4+X_b/4.
\]

Its eigenvalues are 1/2,1/4,1/4,0, so it is both a valid density operator
and a valid measurement effect. Preparation need not be pure for the
scalar-echo construction. Since tr(X_bX_v)=2 b^Tv, every word has survival
probability

\[
\boxed{p(w)=\operatorname{tr}[\rho_b\Phi'_w(\rho_b)]
=\tfrac14+\tfrac18\langle b,A'_w b\rangle.}
\]

The same physical scalar receiver therefore acquires the normalized
centered signal f(w)=8p(w)-2. Its precision cost is correspondingly
eta_f=8 eta_p. Reversed primitive sequences implement adjoints because
each primitive channel is Hilbert-Schmidt self-adjoint. This realizes
the full counterexample with an order-one asymptotic probability gap
of (1-exp(-10))/8 and no extra conserved mode.

The fixed preparation and receiver are independent of e. This is a
conditional operational construction, not an equipment demonstration.
Explicitly, prepare |+>=(|0>+|1>)/sqrt(2) with probability 1/2 and
|2>,|3> with probability 1/4 each. For the receiver, measure the fixed
orthonormal basis |+>,|->,|2>,|3>, then accept with probabilities
1/2,0,1/4,1/4 respectively. Both operations use a fixed finite apparatus;
no unknown-state tomography or changing receiver is concealed here.

## 6. Zero eigenvalues and noninvertibility are not essential either

Choose another gamma=e^10 and replace the original projections by

\[
A_i^{(\gamma)}=\gamma I+(1-\gamma)A_i.
\]

These have strictly positive eigenvalues. Their Galerkin maps satisfy
T_i^(gamma)=gamma I+(1-gamma)T_i, and their residuals are
D_i^(gamma)=(1-gamma)D_i. Therefore the original relative identity or
inequality remains true with the same kappa. Scaling by 1-eta again
preserves it by Section 4.

The actual two-word dictionary still spans the same S, since
A_+^(gamma)b is an invertible affine combination of b and A_+b.
Every 2H-word reduced product differs from the original reduced product
by at most 2H gamma, by telescoping contractions. Its scalar prediction
is thus at most exp(-10)+2H gamma, tending to exp(-10).
The true operators before scaling still share k and contract its
orthogonal complement, so the true lower bound of Section 4 is unchanged.
After scaling, every eigenvalue of each hidden primitive lies strictly
between zero and one.

Quantum mechanically the corresponding channel is

\[
(1-\eta)\big[\gamma\,\mathrm{Id}
 (1-\gamma)\Phi_u\big]+\eta D.
\]

It remains a positive, self-adjoint, unital CPTP map. It can also be
viewed as commuting reflection dephasing and depolarizing semigroup
steps: exp[t(Ad_U-Id)] has coherence multiplier gamma=exp(-2t),
while exp[r(D-Id)] supplies 1-eta=exp(-r); the two superoperators commute.
No singular projection or exact conserved state is needed for
the obstruction; the small but unbounded slow time scale remains.

## 7. What a repaired claim would have to change

The primitive relative condition does not propagate through arbitrary
composition. For example, on the slow right eigenvector of the reduced
cycle C, the cycle-level relative residual ratio diverges as e^-2
rather than tending to zero. Its physical defect has squared size
Theta(e^6), while the squared reduced increment has size Theta(e^8).
A requirement acquired for complete legal macros can therefore detect
this example even though the primitive relative tests all look good.

Ordinary qualifications such as finite dimension, positive reciprocal
primitives, exact reads, a matched scalar port, Galerkin consistency,
identity centering, strict invertibility, or absence of exact extra
conservation do not repair the proposed all-word theorem. A quantitative
joint-gap or slow-scale condition, a bound on the allowed horizon, or a
different structural condition controlling composition would be substantive
new assumptions. The parent's existing uniform certificate, which includes
the proved reduced coefficient gap, is not contradicted.

The actual two-word Gram is ill-conditioned as e tends to zero:
G=[[1,a/s],[a/s,a/s]], with determinant a d^2/s^2. A theorem explicitly
requiring a fixed lower Gram bound on actual acquired word columns would
exclude this sequence. That is a possible additional assumption, but it is
a genuine restriction with acquisition consequences, not an unnoticed
algebraic error. The displayed relative inequality itself is invariant
under the invertible basis change.

## Independent executable check

check_relative_quantum_embedding.py verifies the reflection construction,
identity preservation, trace preservation on a matrix-unit basis, the
invariant-coherence action, and the exact same-receiver probability formula.
It uses rational arithmetic for e=1/2,1/3,1/5 and all primitive words of
length zero through five, both without smoothing and with gamma=e^10.
All 378 word checks, 36 coherence-basis identities and 192 matrix-unit
trace checks passed. Its output is
RELATIVE_QUANTUM_EMBEDDING_RESULTS.json. Complete positivity is established
analytically by the displayed convex mixture of unitary and depolarizing
channels, rather than inferred from numerical Choi eigenvalues.
