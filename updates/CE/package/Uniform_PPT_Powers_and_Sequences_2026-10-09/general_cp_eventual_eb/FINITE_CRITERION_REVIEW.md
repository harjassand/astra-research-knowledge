# Targeted review of the finite eventual-EB criterion

9 October 2026. Continuation of the same focused mathematical review that
checked the mapping-cone uniformization proof. This report concerns the
new, broader theorem in `FINITE_CRITERION.md`, not a further numerical or
literature survey.

## Verdict and scope

**The finite criterion passes this targeted check under the stated CP
assumption.** No gap was found in the fixed-period flag construction,
nonorthogonal-to-orthogonal quotient passage, primitive-or-zero diagonal
blocks, flagwise cross killing, positive gluing, negative witness, or
finite-dimensional decision quantifiers.

The reviewed theorem states, with `L=lcm(1,...,d)`, `Psi=Phi^L`, and
`m=d^2`, that eventual EB and eventual PPT are equivalent to nilpotence
of the cross transfer at every proper invariant projection of `Psi`,
equivalently its mth power vanishing. The proof does not need a mapping
cone or a uniform bound on the EB index.

This is internal mathematical checking, not formal verification or an
independent priority determination. The prior-comparison claims in
Section 5 of the candidate were not broadly audited. The supplied
nonfaithful family and exact rational test results were read for scope;
no new numerical tests were run or used as proof substitutes.

Reviewed candidate SHA-256 at the start of this check:
`78bc442a624dd25afed2617f188a8efa4f01e71e382c97fea8c0983cc70187d4`.

## 1. Invariant corners, necessity, and the all-powers negative certificate

For a CP map, the condition `Q Psi(P) Q=0` is precisely common Kraus
invariance. Indeed

    Q Psi(P) Q=sum_i (Q K_i P)(Q K_i P)*,

so every `Q K_i P` is zero. Kraus operators are upper triangular in
orthogonal coordinates adapted to `P`.

For an input in `P M Q`, an upper-triangular Kraus tuple can produce only
a `P M P` part and a `P M Q` part. The former never feeds the latter under
iteration, by invariance. Thus the cross transfer of `Psi^n` is exactly
`T^n`, even though the full image of a cross input need not be a cross
input. This distinction is correctly retained in the candidate.

The PPT obstruction is also correct. In adapted basis indices, with
partial transpose on the Choi input factor,

    J(Psi)^Gamma_(q p;q p)=sum_i |K_i[q,p]|^2=0

for `q in Q`, `p in P`. A positive semidefinite matrix with a zero
diagonal entry has its corresponding row and column zero. The entries
against indices `a in P`, `j in Q` give

    sum_i C_i[q,j] conj(A_i[a,p])=0.

These are the conjugates of all coefficients of the cross transfer.
Hence every invariant-corner cross transfer of a PPT map is zero.

If `Phi^k` is PPT, `Phi^(Lk)=Psi^k` is PPT: complete copositivity is
preserved by CP composition on either side. Therefore every invariant
cross transfer of `Psi` satisfies `T^k=0`. Its complex dimension is
`rank(P)rank(Q)<=d^2`, so nilpotence is equivalent to `T^m=0` by
Cayley–Hamilton. These arguments verify all claimed necessary conditions.

Conversely, `T^m!=0` implies that `T` is not nilpotent and has a nonzero
eigenvalue. Every `T^n` is then nonzero, making every `Psi^n` NPT. A PPT
power of `Phi` would give a PPT power of `Psi`, a contradiction. Thus a
single such projection is a valid finite certificate that **every**
positive power of the original map is NPT. No map-changing postfilter is
used to produce this certificate, and no cone assumption is hidden here.

## 2. The fixed-L composition-series refinement

### Original quotient tuples

A finite-dimensional tuple of Kraus matrices has a composition series
of common invariant subspaces. In orthogonal quotient coordinates the
diagonal blocks define CP maps. A proper invariant subspace of a diagonal
quotient tuple would lift to a refinement of the original series, so each
such tuple is irreducible.

The zero tuple is irreducible only in dimension one. Every nonzero
irreducible CP map has positive spectral radius and faithful positive
left and right Perron eigenmatrices. One can see the support issue
directly: the support of a positive Perron eigenmatrix is invariant; the
adjoint is also irreducible, since an invariant subspace for the adjoint
Kraus tuple would give an invariant orthogonal complement for the
original tuple. If the radius were zero, a faithful Perron matrix would
force the entire CP map to vanish. Thus the normalization used in the
candidate is legitimate for every nonzero quotient.

The normalized quotient has Kraus matrices

    B_i=r^(-1/2) Y^(1/2) A_i Y^(-1/2).

They are related to the original tuple by one simultaneous similarity
and a common scalar. Consequently irreducibility is unchanged, and the
map is CPTP with a faithful invariant state.

### Cyclic blocks after the same fixed power

The supplied primary source was
`../filter_closed_uniformity/private_sources/carbone_jencova_v1.pdf`,
SHA-256
`89a54764741869a57a2aff7bfb8ba67566dbc2b6ab635a00c03ed78b59aaf336`.
[Carbone–Jencova, arXiv:1905.00857v1](https://arxiv.org/abs/1905.00857v1),
Proposition 6 on PDF page 11, explicitly makes the period-power cyclic
restrictions irreducible and aperiodic. Proposition 5 and Corollary 2
supply the cyclic projections.

Apply this to the unital adjoint of each normalized quotient. Its period
`h` is at most the quotient dimension, hence at most `d` and a divisor of
`L`. The cyclic projection identity for the adjoint forces every Kraus
operator to carry one cyclic subspace into the next. Therefore every
h-letter Kraus word is block diagonal.

The adjoint of each TP corner of the hth power is precisely the cited
unital corner: block-diagonal Kraus words make the compression and
adjoint operations compatible. In finite dimension, the cited
irreducible, aperiodic corner is primitive. Primitivity passes to the
adjoint as well, since

    tr(Y E^n(X))>0 for all nonzero positive X,Y

is symmetric between `E^n` and `(E*)^n`. Thus the TP cyclic restrictions
are primitive. Their powers at exponent `L/h` remain primitive.

This supplies the required fixed exponent `L`; it does not introduce
quotient-dependent powers into the statement of the finite criterion.

### Nonorthogonal pullback and orthogonal quotient coordinates

This is the delicate part of the structural claim, and the candidate's
reasoning is valid. Pulling orthogonal cyclic subspaces back by
`Y^(-1/2)` gives invariant subspaces `D_1,...,D_h` for every length-L
quotient Kraus word. Their sum is direct, though not generally orthogonal.
Their successive sums form an invariant flag.

Here is an explicit intertwiner for the final coordinate change. Let
`F=D_1+...+D_(a-1)` and `W=F+D_a`. Put `U=W intersect F^perp` and let

    S:D_a -> U,   Sx=projection_(F^perp)(x).

Because the sum is direct, `S` is invertible. For any length-L Kraus word
`B` preserving both `F` and `D_a`, the orthogonal quotient block `C_B`
obeys

    C_B S = S (B restricted to D_a).

To check this, write `Sx=x-f` with `f in F` and project `B(x-f)` onto
`F^perp`; invariance removes the `Bf` term. The same `S` works for **every
word**, not merely for their sum as a superoperator. Therefore the CP
map represented in the final orthogonal quotient is

    Ad_S E Ad_(S^(-1)),

up to the common positive scalar coming from Perron normalization.
Powers telescope through this similarity. Invertible congruences preserve
positive definiteness and nonzero positive inputs, so primitivity is
unchanged.

The direct-sum flags in the original quotients lift through their inverse
images to a nested invariant flag in the original Hilbert space. Products
of upper-triangular matrices have products of diagonal blocks on the
diagonal, so the quotient of `Phi^L` is exactly the corresponding power
of the original quotient CP map. Hence the final flag for `Psi` really
has primitive-or-zero diagonal quotient maps.

No assertion that the pulled-back Perron subspaces are orthogonal is
needed, and their possibly poor condition numbers affect neither this
existence proof nor its fixed period-clearing exponent.

## 3. Killing flag cuts and positive gluing

Every nontrivial flag projection is among the universally quantified
invariant projections in the criterion. Therefore `Omega=Psi^m` has zero
cross transfer at every flag cut. Its diagonal quotient maps are the mth
powers of the preceding primitive-or-zero maps, so retain that property.

The positive gluing induction is valid. At the first cut `P=W_1`, zero
cross transfer implies orthogonality of the Kraus-index coefficient
spaces for its two diagonal blocks. A unitary change of Kraus coordinates
gives `Omega=F+G` with `F` output-supported on `P`, `G` input-supported on
`Q`, and `GF=0`. Both are CP; neither must separately be EB or satisfy
any mapping-cone premise.

The quotient corner `Omega_Q` inherits the remaining invariant flag.
Its zero cross-transfer equations at the cut `W_j intersect Q` are
indeed a subset of those for the original cut `W_j`: restrict both the
row and column indices of the first diagonal block to `W_j intersect Q`,
and the second block to `W_j^perp`. Thus no cross condition is lost by
passing to the quotient.

The factor identities for powers of `F` and `G` in the candidate have
the correct order. If the two corners have eventual-EB exponents
`N_P,N_Q`, then `F^(N_P+1)` and `G^(N_Q+1)` are EB. In

    Omega^n=sum_(j=0)^n F^(n-j)G^j,

all other noncommutative words vanish because they contain `GF`. At
`n=N_P+N_Q+1`, each surviving summand has an EB factor; the sum is
therefore EB. This is a positive CP decomposition, not an inference
that arbitrary positive summands of an EB map must be EB.

A primitive CP diagonal block is eventually EB: Perron similarity and
positive scaling reduce to a primitive CPTP map, whose powers converge
to a faithful state-preparation map. Its Choi matrix is an interior
separable product, so sufficiently late powers are EB. Undoing the
telescoping similarity preserves this conclusion. Zero blocks are EB
immediately.

More explicitly, if the final flag has `r` blocks with some individual
eventual-EB exponents `N_1,...,N_r`, gluing gives the finite bound

    n_EB(Omega) <= sum_j N_j + r - 1.

Thus a positive power of `Phi` is EB. These `N_j` may depend on the map;
the theorem correctly asserts no dimension-only EB-index bound.

## 4. Effective semialgebraicity and exact algebraic witnesses

For each fixed `d`, both `L` and `m` are explicitly computable fixed
integers. The entries of `Psi` are polynomials in those of `Phi`.
Hermitian projection conditions, proper rank via `0<tr(P)<d`, and
`Q Psi(P) Q=0` are finite real polynomial conditions after splitting
complex entries into real and imaginary parts.

Let `D_P(X)=PXQ`. It is an idempotent linear projection on the complex
vector space `M_d`. The extended cross operator is

    B_P=D_P Psi D_P.

Its image lies in `range(D_P)` and it annihilates `ker(D_P)`. Relative
to their direct sum it is exactly `T_P direct_sum 0`. Consequently
`B_P^m=0` is precisely the intended restricted nilpotence test; it does
not introduce an extra nilpotent block or require an extra iterate.
Testing on the `d^2` matrix units gives finitely many polynomial
equalities. Failure can be expressed by the strict polynomial inequality
`sum_ab ||B_P^m(E_ab)||_F^2>0`.

Thus the universal assertion over invariant projections is one finite
first-order real formula. Quantifier elimination applies even though
there can be continuously many invariant projections: the number of
projection variables is fixed and finite. The flag construction is used
only to prove sufficiency and need not be executed or encoded in the
decision formula.

For real-algebraic input coefficients, exact real quantifier elimination
is effective. A negative answer is an existential semialgebraic system
over the real algebraic numbers. If it has a real solution, it has a
solution over their real closed field; effective sampling supplies
real-algebraic real and imaginary parts of `P`. This gives the claimed
algebraic projection certificate, whose nonnilpotence can be checked
exactly by the finite matrix-power test.

On a positive answer, enumerate positive integers `n` and decide
separability of `J(Phi^n)` by a finite product decomposition with at most
`d^4` terms. Conic Caratheodory supplies that bound without TP or trace
normalization; the zero Choi matrix is harmless. Every test has algebraic
coefficients and is decidable by real quantifier elimination. The proved
criterion guarantees termination. Sequential testing returns the least
EB index. No computable a priori index bound is required for this
terminating algorithm.

## 5. Conclusion and limits

The implications form a complete, noncircular chain:

    eventual EB => eventual PPT => all invariant cross transfers nilpotent
       => fixed-m cross killing on a primitive-or-zero quotient flag
       => positive gluing => eventual EB.

Negating the fixed polynomial condition yields a finite certificate for
all powers being NPT. The fixed-L refinement justifies using one
universally quantified algebraic test rather than a search over arbitrary
periods or flags.

No substantive repair was required by this check. For presentation, the
explicit intertwiner `S` and the observation `B_P=T_P direct_sum 0` are
worth retaining, because they close the two most plausible hidden gaps.
This result does not establish robustness to approximate data, practical
complexity, a uniform EB index, a nonstationary-composition result, or a
priority claim.
