# Weighted rays, complete quotient fitting, and the adaptive residual bound

This audit covers `weighted_homogeneous_sum` in
`work_stationary_prior_agent/homogeneous_chain_counter.py` and the root
`quotient_homogeneous_compiler.py` and `acquired_quotient_counter.py`. The
weighted formula and raw-fitting completeness hold. The fitting argument
works for **every height `0<=h<=e`**, not merely heights inside the polynomial
counting range. This justifies monotone search for the minimum height.

## 1. Why the quotient weight factors out of the transverse sum

Use the notation of `SINGULAR_RAY_AUDIT.md`. At a fixed unit radial value,
translate transverse coordinates to the exact lifted critical point. The
phase is

\[
\lambda_e\bigl(r^3(c+A u^2+\mu uv+Bv^2+C_3(u,v))\bigr),
\qquad u,v\in tA_e.
\]

The binary perturbation is `Q(r(v_*+(u,v)))`, with the chart-coordinate
embedding understood. Suppose it depends only on the quotient modulo
`t^h`, with `h<=floor(e/2)`.

The orthogonality operations forcing `u_k=v_k=0` for `1<=k<h` use the
opposite digits at level `e-1-k`. Those digits have level at least `h`, so
the quotient weight is invariant under their changes. Pure-square changes
vanish because their valuation is at least `e`. The cubic derivative has
valuation at least `e-1+k>=e`. The surviving derivative is the nondegenerate
polar coefficient `mu_0`, and hence the forcing is exact.

After these cancellations the surviving transverse variables satisfy
`u=v=0 mod t^h`. The perturbation is now exactly `Q(r v_*)`. The same
forcing operations also hold in the unweighted sum, so the entire weighted
transverse sum equals the unweighted transverse factor multiplied by
`(-1)^Q(r v_*)`:

\[
q^e\kappa^{e\bmod2}
 (-1)^{\lambda_e(c r^3)+Q(r v_*)}.
\]

This local extraction needs only quotient support of the weight. Binary
quadratic degree becomes essential in the next step, where it makes the
remaining radial sum efficiently computable.

The unit radial phase

\[
r\longmapsto\lambda_e(c r^3)+Q(r v_*)
\]

is a binary quadratic on `ed` bits. Squaring in the ring is binary-linear,
ring multiplication is bilinear, and multiplication by the fixed vector
`v_*` is binary-linear. Thus summing over all ring elements and subtracting
the sum over `tA_e` gives the exact unit sum as **two Gaussian sums**. The
implementation performs exactly these operations, including their constant
terms. It does not apply the unweighted socle cancellation rule to a
weighted ray; doing so would be incorrect.

Transverse noncritical residue classes still cancel because the highest
digits are invisible to the weight. A transverse critical point with
nonzero critical residue value also still cancels: its highest radial
derivative is nonzero, while the quotient weight is unchanged. It is
therefore correct to retain precisely the same at-most-three projective
singular rays as in the unweighted construction.

## 2. Height propagation and the global polynomial range

At the origin, substitute `X=tY`. The homogeneous cubic acquires `t^3`,
while `Q(tY)` has height at most `max(h-1,0)`. The six eliminated field
digits remain unused whenever the local height condition holds at a depth
at least four. For the global condition

\[
3h\le e+1,
\]

the same inequality holds after replacing `(e,h)` by
`(e-3,max(h-1,0))`. It implies the required local `2h<=e` at every depth
at least two. At depths two and three, the origin weight is its constant
value. At a depth-one terminal the residual quotient weight is constant.
Thus the complete weighted recurrence is polynomial apart from the
explicitly stated field-terminal implementation boundary, which the
existing fixed-degree point-counting theorem removes theoretically.

The local half-depth bound is substantive. At `e=3`, a height-two weight
can cancel the entire remaining transverse Gaussian. Our explicit example
over `F_4` gives transverse sum `256` where incorrectly extracting the
weight would give `64`.

## 3. The quotient-valued ambiguity lemma, for all heights

Assume `d>=3`. Let

\[
F(X)=\lambda_e(D_3(X)+D_2(X)+D_1(X)+D_0)
\]

factor through `A_e^3/t^h A_e^3`. Here `D_3` is ordinary homogeneous cubic,
`D_2` contains only cross terms, and `D_1` is ordinary linear. The fitter
omits ordinary pure squares because their traces are binary-linear. The
mixed cubic coefficient is fixed by the raw third tensor, so differences
of fitted polynomials have no `XYZ` term and their entire binary ANF has
degree at most two.

**Claim.** Every coefficient of `D_3`, `D_2`, and `D_1` belongs to
`J^(e-h)`, where `J=(t)`. Conversely, this coefficient condition makes
`F` quotient-supported. Constants are unrestricted.

For any `V in J^h A_e^3`, invariance says `F(X+V)+F(X)=0`. Replace both
`X,V` by `rho X,rho V` for every `rho in F_q`. The cubic part contributes

\[
\operatorname{Tr}\bigl(\rho^3[t^{e-1}](D_3(X+V)+D_3(X))\bigr),
\]

while the lower terms contribute trace exponents two and one. For `d>=3`,
the binary cyclotomic orbit of three has length `d` and is disjoint from
the orbit of one. Therefore

\[
[t^{e-1}](D_3(X+V)+D_3(X))=0
\]

for all `X,V`. This is a polynomial identity in the coefficient-field
variables: its degree in every variable is at most three, strictly below
`q`. Choose the variation in a coordinate whose exponent in a cubic
monomial is odd. Its coefficient at level `j>=h`, together with residue
variables in the other factors, isolates the coefficient at level
`e-1-j` of that monomial. Hence every cubic coefficient below level
`e-h` vanishes.

A cubic with coefficients in `J^(e-h)` is itself quotient-supported, so
subtract it. Vary one input coordinate by an arbitrary element of `J^h`
and then vary another input coordinate freely. Nondegeneracy of the
Frobenius pairing forces each cross coefficient into

\[
\operatorname{Ann}(J^h)=J^{e-h}.
\]

After removing the cross terms, the same pairing argument for linear
terms gives the same valuation condition on their coefficients. The
converse follows because changing an input by `J^h` multiplies every
nonconstant difference term by `J^(e-h)J^h=0`.

Nothing in this proof requires `2h<=e`. It includes `h=0` and `h=e`.

For the exact coefficient domain used by the code, this identifies the
entire kernel: it is one unrestricted constant coefficient plus 15
coefficients in `J^(e-h)`. Its binary dimension is

\[
de+15dh,
\]

and the outside-quotient coefficient matrix has rank `15d(e-h)`.

## 4. Any linear fit yields the correct normalization when one exists

Suppose a representation exists:

\[
p(X)=\lambda_e(H_*(X+a_*))+Q_*(X\bmod J^h).
\]

Expand the translated homogeneous cubic into the fitter's monomials,
absorbing pure squares into the ordinary linear trace terms. Call this
ordinary polynomial `P_*`. Let `P` be any solution of the code's linear
fit outside the quotient. Their traced difference is quotient-supported.
The preceding lemma gives

\[
H-H_*\in J^{e-h}[X]_3.
\]

Only the mixed cubic contributes ordinary cross quadratic coefficients
under translation: repeated-variable cubics contribute pure squares and
linear terms, not cross terms. Thus the fitted cross coefficients recover
a center `a` satisfying

\[
a-a_*\in(J^{e-h})^3,
\]

because the mixed coefficient `mu` is a unit.

Replacing `H_*` by `H` changes the scalar phase by a quotient-supported
function. Replacing `a_*` by `a` does too: every nonconstant coefficient
in the translation difference contains a factor from `a-a_*`, and hence
lies in `J^(e-h)`. Terms containing its square or cube need not vanish;
they still lie in the same ideal. This is the key reason the argument
works at **all** heights.

Therefore the residual after the fitted translation is quotient-supported,
and the code's final support check succeeds. The residual is exactly
binary quadratic because the complete third tensor has been preserved.
Recentering the noise is a binary translation on the same quotient.

Conversely, acceptance supplies and verifies such a representation. Thus
the fitter accepts exactly when a representation exists, rather than
depending on a lucky solution of an underdetermined system.

## 5. Minimum-height acquisition and the adaptive exponent

Existence is monotone in `h`; the all-height completeness proof makes actual
acceptance monotone as well. At `h=e`, the canonical mixed cubic plus its
raw binary quadratic remainder always supplies a representation. Therefore
binary search finds the minimum admissible height `h_*` in polynomial time
and without assuming a useful decomposition.

The property and its minimum height survive acquired ring coordinates:
ring isomorphisms preserve `J^h`, invertible ring-linear maps preserve
`J^h A_e^3`, and the Frobenius-functional unit preserves homogeneous degree
and coefficient valuations. Binary affine changes preserve quotient
quadratic degree. The semilinear argument in
`STATIONARY_COMPILER_AUDIT.md` thus applies to the entire height spectrum.

Let

\[
\Delta=\max\{0,h_*-\lfloor(e+1)/3\rfloor\}.
\]

After `j` origin steps, depth is `e-3j` and height is at most
`max(h_*-j,0)`. The first failure of the local half-depth condition occurs
no earlier than `j=max(0,e-2h_*+1)`. If `Delta>=1`, the resulting upper
bounds on residual depth, before clipping at the original depth, are

\[
\begin{array}{c|ccc}
e\bmod3&0&1&2\\\hline
\text{residual depth}&6\Delta-3&6\Delta-5&6\Delta-1.
\end{array}
\]

When `Delta=0`, only a possible depth-one field terminal remains. Therefore
the one explicitly enumerated residual has at most

\[
\boxed{R\le\min\{n,\;3d\max(1,6\Delta-1)\}}
\]

binary variables. Actual height can decrease faster, improving this bound.
The root binary search and adaptive-counter control flow agree with it.

For the literal current enumeration implementation, state the cost as
`poly(n,L) + 2^R poly(R)` or `poly(n,L) + O*(2^R)`, with polynomial space.
A bare `poly(n,L)+2^R` suppresses the cost of evaluating each residual
phase. This is a presentation qualification, not an exponent or correctness
failure.

## 6. Executed audit and preserved failures

`weighted_ray_fit_audit.py` completed all exact checks:

- **14 weighted transverse truth tables** at the local half-depth boundary,
  with arbitrary dense quotient quadratics and nontrivial radial units.
- **Two revived-ray examples**, at 45 and 60 original bits. For
  `H=XYZ+t^3 Z^3` at depth five, choose
  `Q=lambda_e(t^3 Z^3)`. The unweighted `Z` ray cancels, whereas its weighted
  radial sum is the full number of units. The complete weighted count
  agrees with the independent closed count for `XYZ`. These tests would
  fail if an unweighted cancellation shortcut were retained.
- **Seven complete fitting-kernel audits**, including `h=0`, `h=e`, and
  `2h>e`. Every basis relation had the required valuations, and every
  measured kernel dimension was exactly `de+15dh`.
- **5,148 depth/height pairs** through depth 100 satisfied the derived
  adaptive residual bound, including its worst residue class.
- The **local height-plus-one failure** changed the transverse count from
  the falsely predicted `64` to `256`.
- A **degree-two residue-field alias** violates the all-coefficient
  uniqueness statement at height zero; the raw completeness theorem's
  current `d>=3` hypothesis should therefore remain explicit.

All data are in `weighted_ray_fit_audit_results.json`. No root file was
modified, and the broad full-counter tests were not repeated.
