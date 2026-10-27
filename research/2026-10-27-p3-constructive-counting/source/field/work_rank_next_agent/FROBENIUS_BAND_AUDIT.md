# Independent audit of the Frobenius-band quadratic lift

27 October 2026. This audit concerns the extension from the three-term
Frobenius band to width 2s+1. It does not independently repeat the
previous field-centroid acquisition theorem.

## Verdict

The band-code, rank radius, negative-exponent folding and ordinary-degree
claims are correct when s≥1 and 2s<d. There is one necessary distinction:
the displayed diagonal trace polynomial has the correct polar form, but
an additional binary linear correction is generally required to match
the canonical Boolean quadratic exactly. The existing s=1 fitter already
restores such unary terms; the general-band fitter must retain this step.

The stated general counting exponent is
r+O(b(log n+s)). The sufficient subexponential condition is
r+b(log n+s)=o(n). For fixed b this reduces to r=o(n), s=o(n).
Without fixed b, the latter two conditions alone are insufficient.

## 1. The manufactured rank-metric code

Let F=F_(2^d), σ(x)=x², and use the nondegenerate pairing
⟨x,y⟩=Tr_(F/F₂)(xy). A binary bilinear block is represented uniquely
by a binary-linear map L:F→F through

\[
B(x,y)=\operatorname{Tr}(xL(y)).
\]

Suppose the compatible base has

\[
L(X)=\sum_{j=-s}^{s}c_j X^{2^j},
\]

where Frobenius exponents are read modulo d. Precomposing with σ^s
gives

\[
L(X^{2^s})=\sum_{j=-s}^{s}c_j X^{2^{j+s}}.
\]

This is precisely a linearized-polynomial code of dimension
k=2s+1 over F, evaluated on a full binary basis of F.
Because 2s<d, a nonzero code polynomial has ordinary degree at most
2^(2s) and hence at most 2^(2s) roots. Its root space has binary
dimension at most 2s, so its rank is at least d−2s.
This is the standard full-length Gabidulin minimum distance.

Conversion through the trace Gram matrix and precomposition with
Frobenius are invertible binary maps, so they preserve error rank.
Every block of a global binary polar-error matrix of rank r has
rank at most r. Therefore unique block recovery is justified when

\[
2r<d-2s,
\qquad\text{equivalently}\qquad
2r\le d-2s-1.
\]

The decoder radius is floor((d−2s−1)/2). Here r means the rank of
the polar matrix itself. If an error is described instead as a sum
of t products of linear forms, its polar rank is at most 2t;
that is a different parameterization and must not lose this factor.

After decoding, apply σ^(−s) to the argument to recover L.
The decoded coefficient in position s+j is c_j; no coefficient
Frobenius twist is introduced by this right precomposition.

## 2. Off-diagonal blocks have low ordinary field degree

For two distinct field variables X_i,X_j, take one representative
per unordered block pair:

\[
Q_{ij}=\operatorname{Tr}(X_iL_{ij}(X_j)).
\]

Its mixed polar block is exactly L_ij, and the reverse block is
its trace adjoint. There is no extra factor two.

For a negative index j=−a, trace invariance gives

\[
\operatorname{Tr}(c_{-a}X_iX_j^{2^{-a}})
=\operatorname{Tr}(c_{-a}^{2^a}X_i^{2^a}X_j).
\]

Thus every negative exponent can be placed as a positive exponent
on the other variable. The complete field polynomial for this
block pair is

\[
c_0X_iX_j+
\sum_{a=1}^{s}
\left(c_aX_iX_j^{2^a}
+c_{-a}^{2^a}X_i^{2^a}X_j\right).
\]

Its ordinary total degree is at most 2^s+1. The coefficients in the
folded negative terms are c_(−a) raised to 2^a, not to 2^(−a).

## 3. Exact treatment of diagonal blocks

The trace adjoint of cσ^j is c^(2^(−j))σ^(−j). Since the residues
−s,...,s are distinct, a band map is self-adjoint exactly when

\[
c_{-j}=c_j^{2^{-j}},\qquad j=1,\ldots,s.
\]

The paired contributions to Tr(xL(x)) cancel. Its remaining
diagonal value is Tr(c_0 x²). Nondegeneracy of the trace pairing
and invertibility of squaring show that this vanishes for every x
exactly when c_0=0. Thus the alternating self-adjoint band maps are
precisely the maps

\[
L(X)=\sum_{j=1}^{s}
\left(c_jX^{2^j}+c_j^{2^{-j}}X^{2^{-j}}\right).
\]

Their quadratic refinement is

\[
Q(X)=\operatorname{Tr}
\left(\sum_{j=1}^{s}c_j X^{1+2^j}\right).
\]

Expanding Q(x+y)+Q(x)+Q(y), and transferring Frobenius from one
factor to the other under the trace, gives exactly Tr(xL(y)).
The positive coefficients c_j are correct; no factor two or
division by two is present.

### The unary correction remains necessary

Having the right polar form does not make Q equal to the canonical
bit quadratic q_B=Σ_(u<v)B_uv x_u x_v. In a chosen binary basis
g_1,...,g_d, the canonical q_B vanishes on each basis vector.
Define the binary linear functional ℓ by

\[
\ell(g_t)=Q(g_t),\qquad t=1,\ldots,d.
\]

Then q_B=Q+ℓ, because both sides have the same polar form and agree
on zero and every basis vector. Solve the trace Gram system to
write ℓ(X)=Tr(aX). This correction has ordinary field degree one.

A minimal counterexample to omitting it is F_8, s=1, c_1=1:
Q(X)=Tr(X³), so Q(1)=1, whereas q_B on the corresponding bit basis
vector equals zero. The correction is nonzero in seven of the
eight alternating band maps for this field, and in fifteen of the
sixteen at d=4, as the exhaustive audit confirms.

For the full b-block quadratic, add the refinements for diagonal
blocks and a single Q_ij for each i<j. Restore all binary unary
terms by basis evaluations. Any desired constant bit is represented
by a field constant of that trace; if d is even, the field constant
1 need not have trace one.

This recovers the exact Boolean function with ordinary degree at
most 2^s+1. Adding the canonical field cubic leaves that degree
bound unchanged because s≥1.

## 4. Why the boundary 2s<d is substantive

At 2s=d, the indices +s and −s coincide. A half-period term
cX^(2^s), with c in the subfield F_(2^s), is self-adjoint and
alternating, but

\[
\operatorname{Tr}_{F/F_2}(cX^{1+2^s})=0
\]

for every X: the argument belongs to the degree-d/2 subfield,
and the relative trace from F doubles it to zero.
The naive positive-index refinement therefore has zero polar
form while L can be nonzero.

This boundary can be treated separately by choosing a with
a+a^(2^s)=c and using Tr(aX^(1+2^s)), but that is a different
coefficient rule. The present strict bound correctly excludes it.
The executable verifies the failure and the repaired coefficient
rule exhaustively at d=2,4,6.

Also, when d=2s+1 the code dimension is d and its minimum distance
is one. The theorem still applies, but its admissible error rank
is zero. A positive decoding radius cannot be claimed there.

## 5. Counting and arithmetic costs

For each Gaussian-Walsh leaf, the exact Boolean function is
Tr G(X_1,...,X_b) with ordinary degree D≤2^s+1. Added binary
parities become trace-linear terms. Introduce one Artin--Schreier
variable Z:

\[
Z^2+Z=G(X_1,\ldots,X_b).
\]

There are v=b+1 field variables. Its point count N_AS satisfies
N_AS=2N_0, and the signed Boolean sum is N_AS−2^n, where n=bd.
This relation includes no missing factor of two.

Lauder--Wan, Proposition 36 and the affine torus decomposition
immediately after it, give direct N_1 costs. With extension degree
d, characteristic two, variable count v, degree D and k=1, a safe
form of the time bound is

\[
\widetilde O\!\left(
2^{O(v)}d^{3v+7}v^{3v+5}D^{3v}2^{2v+4}
\right).
\]

The corresponding storage bound is

\[
\widetilde O\!\left(
2^{O(v)}d^{2v+4}v^{2v+3}D^{2v}2
\right).
\]

Consequently the Gaussian-Walsh family of at most 2^r leaves
has time poly(L+n)2^[r+O(b(log n+s))], with streamed leaf
accumulation. The point-counter storage is generally
poly(L+n)2^[O(b(log n+s))]; it is not automatically polynomial
when b or s grows. For fixed b and r,s=O(log n), both time and
space are polynomial. For fixed b and r,s=o(n), both are
subexponential. More generally require
r+b(log n+s)=o(n) for the time conclusion.

The degree D is charged even when the field polynomial has a short
sparse description. The full zeta function is unnecessary.
There is no general Lauder--Wan execution or practical-speed claim
in this audit.

Primary source:
https://arxiv.org/pdf/math/0612147

## 6. Executed independent checks

frobenius_band_audit.py uses its own binary-field arithmetic and
quadratic formulas. The rank-decoding tests call the root decoder
with independently generated known codewords and rank errors.

The executed run checked:

- all 512 width-three maps over F_8 and all 4,096 over F_16;
- their exact minimum nonzero ranks, self-adjointness, alternation,
  1,081,344 cross-block folding identities, and 69,632 Frobenius
  precomposition identities;
- every positive diagonal coefficient tuple for (d,s)=(5,2) and
  (6,2), comprising 5,120 refinements;
- 17,830,400 diagonal polar identities across all four strict-band
  exhaustive cases, plus the necessary unary corrections;
- the half-period failure and corrected coefficients in 29,456
  exhaustive polar checks;
- 64 bounded-rank decoding cases for bands through s=4 and field
  degree d=13, including radius-two errors and zero-radius endpoints.

Every exact assertion passed. The inputs, coefficients and aggregate
results needed to reproduce these checks are generated by the fixed
seed and retained in frobenius_band_audit.py and
frobenius_band_audit_results.json.
