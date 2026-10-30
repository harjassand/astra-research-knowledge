# Exact heralded recovery has a quadratic native-query barrier

30 October 2026. Root construction. Independent whole challenge is pending
until its actual receipt is present. This strengthens the coverage lemma in
EXACT_HERALDING_COVERAGE.md. It is an exact-success theorem; approximate
decoding, including the positive adaptive cell, remains outside its conclusion.

## 1. Statement, access and consequence

Use the flat source N_U(X)=U(X tensor I_r/r)U*, logical k>=2, r>=2,
U:C^k tensor C^r -> C^D isometric, D>=kr. All calls are ordinary forward
physical source calls; inputs can be adaptive and entangled with the payload
and retained memory. No source environment, inverse, coherently chosen junk
input, unknown controlled dilation, or U-dependent free advice is supplied.
Every source call used to acquire advice is counted, including offline ones.

An exact success on one already encoded arbitrary payload means the complete
unnormalized logical success subchannel is p_U id, with p_U independent of
the payload/reference. Failure can retain arbitrary quantum history.

For any capped Q-call controller, uniformly in U,

    p_U <= b_r(Q) := Pr[Binomial(Q,1/r)>=r].                (S1)

In particular p_U=0 if Q<r, and

    p_U <= binomial(Q,r)/r^r <= (e Q/r^2)^r.               (S2)

Thus p_U>=alpha>0 requires Q>=r^2 alpha^(1/r)/e. This is an
Omega(r^2) necessary bill for fixed nonzero EXACT success. An exact
repeat-until-success inverse halting almost surely satisfies

    E Q_stop >= r^2.                                      (S3)

These bounds need not be tight: no protocol attaining them is constructed.
For example the exterior-hole decoder's2r-1 queries and small success
probability are consistent with(S1); this theorem does not establish its
minimum-query optimality. Nor is(S2) a lower bound for fixed-error approximate
recovery, and it is NOT a new quadratic theorem for all approximate physical
queries. It does exclude exact success-or-draw as a subquadratic-r route,
even if failures preserve an arbitrarily rich paid history.

## 2. The algebraic input, including arbitrary physical dimension

Write U_j x=U(x tensor |j>). Fix a native-query flag tuple q and an ordinary
known-control environment branch h. The success Kraus operator on the physical
payload is a holomorphic polynomial R_qh(U), separately multilinear in each
queried block, of total degree Q. Exactness and positivity imply

    R_qh(U) U_j = a_qhj(U) I_k               for EVERY j,U. (S4)

As proved in the coverage lemma, if q omits label l, right rotation of U_l
forces a_qhl=0. Polynomial density then makes R_qh itself identically zero.
The full-square proof extends to D>=kr: apply the polynomial to the first
kr columns of a D-by-D unitary. It vanishes on U(D), hence identically on
all complex D-by-D matrices by the same polar/entire-function argument.
Every D-by-kr matrix occurs as its first columns. Thus the unused block can
again be varied arbitrarily while holding the queried blocks fixed.

Consequently, for EVERY U, R_qh(U)=0 whenever q omits ANY junk basis vector.
This is a conclusion about physical-query Kraus amplitudes, not normalized
iid Choi programmes. Intervening known controls can depend on prior outcomes;
their unnormalized branches still have exactly this polynomial form.

## 3. Kraus gauge strengthens coverage to a whole representation support

Let E=(C^r)^tensor Q be the joint, INACCESSIBLE query-environment label space.
For fixed U,h regard R_qh(U) as the coefficients of a linear map T_Uh from
E to the space of payload-to-output operators:

    T_Uh |q> = R_qh(U).

For every W in U(r), replace U by U'=U(I_k tensor W). This leaves N_U
EXACTLY unchanged and rotates the displayed blocks as

    U'_j = sum_l U_l W_lj,
    T_U'h = T_Uh W^tensor Q.                              (S5)

The second identity is just multilinearity in the Q forward slots. It does
not involve rotating the physical controller, and its h environment remains
the same. Equation(S4)'s zero applies to U' as well. Therefore T_Uh annihilates

    L = span_(W in U(r)) (W C^(r-1))^tensor Q.             (S6)

It is enough to use tuples omitting a single fixed coordinate before W;
all of(C^(r-1))^tensor Q lies in their span.

Schur--Weyl decomposition gives

    E = directsum_(lambda partitions Q, length(lambda)<=r)
                         V_lambda^(r) tensor S_lambda.

Inside the fixed hyperplane C^(r-1), precisely the summands with
length(lambda)<=r-1 occur, with their FULL Specht multiplicity spaces
S_lambda. Their U(r)-orbit spans each irreducible V_lambda^(r), and no
r-row component can occur in that hyperplane. Thus L is EXACTLY the
sum of all components of height<r, and its orthogonal complement is

    range Pi_r = directsum_(length(lambda)=r)
                         V_lambda^(r) tensor S_lambda.    (S7)

Hence T_Uh=T_Uh Pi_r. In the actual Stinespring amplitude the query labels
are ket coefficients rather than arguments of T, so support is Pi_r^T.
The central symmetric-group isotypic projector Pi_r is real symmetric
(characters are real and inverse-paired), so Pi_r^T=Pi_r. Including payload
label j and using R_qh(U)U_j therefore places the entire success branch in
Pi_r on its QUERY environments. The payload's separate environment is not
counted among these Q labels. No physical measurement of these environments
is claimed or needed.

## 4. The inaccessible environments have an exactly known marginal

For the displayed Stinespring isometry

    V_U x = r^-1/2 sum_j |j>_E U_j x,

orthogonality U_l*U_j=delta_lj I gives the complementary channel

    N_U^c(X)=Tr(X) I_r/r.                                 (S8)

This is a COMPLETE replacer, including on inputs entangled with any previous
history or reference. At each new query, tracing its accessible output leaves
the fresh E marginal I_r/r independent of every earlier inaccessible E.
All later known trace-preserving operations preserve that reduced marginal
by no-signalling. Induction yields

    rho_(E_1...E_Q)=I_E/r^Q.                              (S9)

The same argument allows the payload environment as an additional reference.
It does not assert that E's are independent of the retained physical outputs;
those correlations are exactly why postselection on success is possible.
Conditioning programme preparation on success must be paid as part of the
whole instrument; it does not replace(S9) by free conditional advice.

Since the success branch is supported in Pi_r and success/failure form a
positive decomposition of the whole experiment, (S7)--(S9) imply

    p_U <= Tr(Pi_r)/r^Q
         = r^-Q sum_(length(lambda)=r) f_lambda s_lambda(1^r).
                                                               (S10)

Here f_lambda=dim S_lambda and s_lambda(1^r)=dim V_lambda^(r).
This is a bound on all adaptive physical-query strategies. Its source is
the unused-block polynomial identity plus Kraus-GAUGE covariance, not a
Choi-to-query reduction. The environments remain inaccessible throughout.

## 5. Exact evaluation of the Schur weight

The ordinary word RSK bijection maps length-Q words over an r-letter ordered
alphabet to pairs consisting of a semistandard tableau (r available symbols)
and a standard recording tableau of the same shape. Thus the number of words
of shape lambda is exactly s_lambda(1^r) f_lambda. The number of rows equals
the longest STRICTLY decreasing subsequence length. These are established
representation/combinatorial facts, not new quantum primitives.

The primary Schensted paper, Canadian Journal of Mathematics13(1961),
179--191, DOI10.4153/CJM-1961-015-3, Theorem2 and PartII's repetition
construction, was read directly. Its repetition convention identifies
strict decreases with distinct-symbol decreases while preserving weak
increases. The primary PDF is
https://www.cambridge.org/core/services/aop-cambridge-core/content/view/B5098D9BC8B226C575402B971852C05E/S0008414X00013146a.pdf/div-class-title-longest-increasing-and-decreasing-subsequences-div.pdf

On an r-letter alphabet the ONLY strictly decreasing subsequence of length r
is(r,r-1,...,1). Greedily wait for r, then r-1, ..., then1. For an iid uniform
word, each wait is an independent geometric(1/r) variable, including the
successful symbol. Equivalently the number of successful advances in Q
positions is Binomial(Q,1/r), until the rth advance. Therefore

    r^-Q sum_(length(lambda)=r) f_lambda s_lambda(1^r)
      = Pr[Binomial(Q,1/r)>=r],                            (S11)

proving(S1). The union bound on choices of r positions for the one decreasing
pattern gives binomial(Q,r)/r^r, proving(S2). This avoids asymptotic spectral
estimation or a heuristic about typical Young diagrams.

## 6. Exact expected-time consequence

For any variable-length exact algorithm, the subinstrument "successful by
time Q" is still exact: each positive finite-time Choi summand lies in the
same identity Bell ray. Pad its already stopped branches with discarded
source calls to Q; all these calls are charged only for the capped comparison.
Its success probability is Pr(Q_stop<=Q), bounded by(S1). Thus Q_stop
stochastically dominates the sum of r independent geometric(1/r) waits.
If success occurs almost surely,

    E Q_stop =sum_(Q>=0) Pr(Q_stop>Q)
             >=sum_(Q>=0) [1-b_r(Q)] =r^2.

This argument needs no joint physical Schur measurement at changing stopping
times and makes no unproved compatibility assumption about Young paths.
An infinite expected query count also satisfies the bound. A repeat service
with a positive probability of never producing success is not an almost-sure
inverse, and no unconditional expectation claim is made for it.

## 7. Research decision and exact limits

The positive feedback cell establishes an actual finite mixed-source adaptive
advantage. This theorem, if received, explains why making its success EXACT
and adding a paid restoring draw cannot remove the quadratic rank barrier.
The live opportunity must instead exploit APPROXIMATE coherent history,
a different operational target, or additional acquired source structure.

This does not show that all O(r) approximate controllers fail. Approximate
Choi output has positive wrong components, so the rank-one zero and its
polynomial continuation fail. A quantitative robust extension would be new
work, not a consequence obtained by replacing zero with epsilon in(S4).
No generic quadratic physical-query lower is asserted for approximate
recovery. In particular the separate N1104 iid-Choi quadratic bound remains
at its original access scope.

The full-height projection and its r^2 scale are ordinary one-sided rank-
testing machinery: O'Donnell--Wright, Quantum Spectrum Testing,
https://arxiv.org/abs/1501.05028 and Section6 of the author primary
https://www.cs.cmu.edu/~jswright/papers/quantum-spectrum-testing.pdf.
The new internal step is forcing this support on the inaccessible query
environments of an arbitrary adaptive reversible-source inverse. It is not
a claim to have invented Schur sampling, rank testing, RSK or its waiting
distribution. Public priority of this particular operational reduction is
UNKNOWN. Pure-unitary exact inversion and quantum discrimination predecessors
retain their full actual scope.

No quantum/source/physical experiment or optimizer is involved in this proof.
An exact finite arithmetic identity control, if run, is recorded separately
and does not substitute for the all-Q argument above.
