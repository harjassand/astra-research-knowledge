# Independent audit: a PC/QC quartic with no polynomial global support map

**Accepted at the complete stated mathematical scope.** I independently
reconstructed the finite exact data and reviewed the arguments extending
them to every real base point, every increment, every polynomial selector
degree, and every energy in the stated full35 coefficient box. I found no
remaining mathematical gap in this theorem. This is an internal substantive
audit, not a claim of external peer review, world priority, or a solution of
the general rank-one-convex/quasiconvex problem.

## 1. Claim and source binding

For row-major `A=(a,b,c,d)`, set

\[
u=a^2+c^2,\quad v=b^2+d^2,\quad w=ab+cd,\quad q=ad-bc.
\]
The audited energy is

\[
F=\frac{55220381}{10^{10}}(u^2+v^2)
 +\frac{114430029}{625000000}uv
 -\frac{801761987}{5000000000}w^2
 +\frac{118849817}{4000000000}q(u-v).
\]

It has a finite, real-valued convex lift in its five nonconstant minors,
and the uniform compatible-gradient lower bound in Section 4. It has no
polynomial touching minor-affine support map of any degree, even with an
unrestricted globally nonnegative remainder. These conclusions hold after
changing each of the 35 ordinary degree-four monomial coefficients in the
four entries by at most `1/4928000000`.

The original unsymmetrized combined-search target is also inside this box.
Both targets are therefore positively resolved as PC/QC. Neither is a
quasiconvexity-counterexample candidate after this result.

Exact certificate bindings:

- Positive: `rational_selector/EXACT_RATIONAL_SUPPORT.json`, SHA256
  `ecbd2bd7d333abe79810625c7be6e1d218d4411095cc28c049fa731958059191`.
- Negative: `quartic_boundary_alternative/EXACT_POLYNOMIAL_SELECTOR_OBSTRUCTION.json`,
  SHA256 `e51d9be90ba977c34f5daab4a75901eb6acc377dc53c0004d479425fed945d22`.
- Exact symmetric target: `common_cone_review/EXACT_SYMMETRIC_TARGET.json`,
  SHA256 `88769c8c3ff995312e7a34967c43959e4e46715b59d3ad781cbba545194ab4f3`.

The accompanying `AUDIT_RECEIPT.json` binds the reviewed proof editions.
The historical atomic proof and earlier operation note correctly describe
their acquisition-time unknowns; the new positive proof supersedes those
unknown statuses for this target.

## 2. Independent finite reconstruction

`independent_audit.py` uses only Python's standard library. It imports no
producer, peer verifier, symbolic engine, numerical solver, saved polynomial
map, or interface array. The matrix-feature serialization convention was
read from the two feature-order declarations in the producer and is now
explicit in the final proof. All mathematical constructions are separate.

I rebuilt the literal eight-variable polynomial

\[
T^2\{F(A+X)-F(A)-DF(A):X\}-p_6(A)\det X,\qquad T=|A|^2,
\]

from the nine invariant terms, direct monomial differentiation and
substitution. I rebuilt all six stated Hopf-cubic numerator terms. The
complete 998 nonzero coefficients agree exactly with the supplied rational
Gram, not merely with a sampled residual.

I generated the 180 features independently: 80 products `A^alpha X_i`
with `|alpha|=3`, followed by 100 products `A^alpha X^beta` with both degrees
two. I checked every Gram coefficient and every symmetric entry. The
feature products span all 3,185 possible monomials of bidegrees `(6,2)`,
`(5,3)`, `(4,4)`, with respective counts 840, 1120, 1225.

I also recomputed the full dyadic-factor residual with exact integers.
All entries of the 180-by-180 factor are consumed. No triangularity,
floating eigenvalue or accuracy of its acquisition is needed: every real
matrix `L` gives `LL^T` PSD. With shift `s=1/200000`, the exact symmetric
residual in `R=LL^T+sI+E` has maximum absolute row sum

\[
\eta=
\frac{4305014904500628945243}
{3022314549036572936765440000000000}
<\frac1{400000}.
\]

For symmetric `E`, its spectral norm is at most that row sum. Consequently
`R >= (s-eta)I > I/400000`. This proves the claimed margin without a
floating positivity premise. The exact replay receipt records the stronger
actual rational lower bound as well.

The latest complete finite replay took approximately 0.27 seconds on this
host. This is a replay timing; it does not measure acquisition complexity
or establish an algorithmic advantage.

## 3. The zero base point and global minor support

Write `B_F=F(A+X)-F(A)-DF(A):X`. The numerator `p6` is homogeneous of degree
six. Its boundedness on the unit sphere gives
`|p6(A)/|A|^4| <= C|A|^2`. Thus `k(A)=p6(A)/|A|^4`, extended by `k(0)=0`,
is continuous on all of matrix space. No division at zero is used.

For the unweighted monomial sums `S_j(A)=sum_(|alpha|=j) A^(2alpha)`, the
largest multinomial coefficients give `S3(A)>=|A|^6/6` and
`S2(A)>=|A|^4/2`. I checked the relevant integer coefficients independently.
The feature norm is exactly

\[
|Z|^2=S_3(A)|X|^2+S_2(A)S_2(X).
\]

Dividing the exact Gram identity for `A != 0` therefore gives

\[
B_F(A,X)-k(A)\det X
\ge \frac{|A|^2|X|^2}{2400000}
   +\frac{|X|^4}{1600000}. \tag{1}
\]

Taking `A -> 0` with `X` fixed is legitimate by continuity. Since
`F(0)=DF(0)=k(0)=0`, (1) holds at zero too, giving
`F(X)>=|X|^4/1600000`. The vanishing multiplier does not leave an unproved
zero-base case.

For each `A`, define

\[
\ell_A(B,s)=F(A)+(DF(A)-k(A)\operatorname{cof}A):(B-A)
                    +k(A)(s-\det A).
\]

The determinant identity reduces `F(B)-ell_A(B,det B)` exactly to the left
side of (1), at `X=B-A`. Hence every affine function lies below `F` on
the minors graph and touches at its own base point.

The supremum `g(B,s)=sup_A ell_A(B,s)` is convex and equals `F(B)` when
`s=det B`. Its global finiteness deserves a separate check. Given arbitrary
`(B,s)`, choose a real matrix `Y` with `det Y=s-det B`. Then

\[
(B,s)=\tfrac12(B+Y,\det(B+Y))
      +\tfrac12(B-Y,\det(B-Y)).
\]

Every affine support is therefore bounded above at `(B,s)` by the finite
number `[F(B+Y)+F(B-Y)]/2`, uniformly in its base point. The fixed support
`ell_0=0` supplies a finite lower bound. Thus `g` is finite on all of
`R^5`; it is not merely a possibly infinite extension with the right values
on the graph. This directly proves polyconvexity.

## 4. The QC conclusion is compatible-gradient, not atomic

In (1), keep the affine background `A` fixed and put `X=Dphi`. For a
smooth zero-boundary test, both the integral of its gradient and the
integral of its determinant vanish. The multiplier `k(A)` is a fixed
number here. There is no assumption about the integral of a spatially
varying `k(A+Dphi) det Dphi`. Consequently

\[
\int_\Omega [F(A+D\phi)-F(A)]
\ge\frac{|A|^2}{2400000}\int_\Omega|D\phi|^2
 +\frac1{1600000}\int_\Omega|D\phi|^4. \tag{2}
\]

Strong `W^{1,4}` approximation extends (2) to `W_0^{1,4}` on bounded
Lipschitz planar domains; quartic growth makes all terms continuous under
that approximation. The periodic version follows from the same gradient
and determinant null-Lagrangian identities. This verifies the stated
uniform strict QC bound, in addition to ordinary QC. Rank-one convexity
also follows; no previous acoustic certificate is needed for this positive
theorem.

## 5. All polynomial degrees and all support components are excluded

I evaluated all 24 actual rational atoms directly. Every weight is
strictly positive. Each of the ten quantities

\[
\sum_s \omega_s A_i^{(s)}A_j^{(s)}\det X^{(s)},\quad i\le j,
\]

is exactly zero. The weighted literal Bregman pairing is exactly the
certificate's negative rational, and is less than `-1/100000`. I checked
these values both by the rebuilt Bregman polynomial and by direct function
and directional-derivative evaluations. No symmetry argument, three-cut
optimization, SOS pseudo-moment or atomic-generation procedure is trusted.

Suppose a polynomial `k` satisfied `B_F-k detX>=0` globally. Fix any `A0`
and fixed increments `X+`, `X-` with determinants `+1`, `-1`. Simultaneous
scaling by `t>0` shows

\[
-B_F(A_0,X_-)\le k(tA_0)/t^2\le B_F(A_0,X_+).
\]

For a polynomial in `t`, these two finite bounds at both `t -> 0` and
`t -> infinity` force every homogeneous component except degree two to
vanish. This holds at every `A0`, so those components vanish identically.
The zero polynomial is included. The ten annihilators then make the
positive weighted sum of all support remainders strictly negative, a
contradiction. This excludes all degrees, not just the degree used by a
failed numerical hierarchy.

For a general polynomial touching minor-affine map, let `V(A)` be its
four entry coefficients and `k(A)` its determinant coefficient. At `B=A`
the nonnegative remainder has value zero; its derivative in `B` must also
vanish. This forces `V=DF-k cof A`, reducing its entire remainder exactly
to the scalar expression just excluded. A constant minor has zero
increment and changes nothing. This verifies the full polynomial-map
claim. An SOS remainder would be nonnegative, so the stated SOS-PC
obstruction follows immediately as well.

I checked the comparison definition in the primary source, [Fantuzzi et
al., arXiv:2604.11124v1, Definition 2.5 and Remark 2.1](https://arxiv.org/html/2604.11124v1).
It requires one polynomial minor-support map, with a jointly SOS
remainder; the allowed degree is unrestricted. The proved obstruction is
therefore stronger than failure of that stated sufficient condition. The
source flags the planar quartic gap as open in that edition. This audit
does not establish that no later or separate result has addressed it.

The atomic base points differ. They are not one compatible gradient
distribution and do not imply a non-QC Jensen law. The new positive half
and the negative half are thus consistent: the rational, nonpolynomial
selector escapes the representation class that the atoms exclude.

## 6. Every coefficient in the full35 box, and the original target

For each of the 35 ordinary quartic monomials `m(A)`, my checker rebuilds
`B_m` and verifies coefficient `l1` norms 11 for `B_m` and 176 for
`T^2 B_m`. These numbers also follow from removing the degree-zero and
degree-one increment terms from the binomial expansion: `16-1-4=11`,
then multiplying by `T^2`, whose coefficient sum is 16.

All resulting terms belong to the verified Gram-product span. Place each
term in one diagonal Gram entry, or put half in each of one symmetric
off-diagonal pair. That placement's entry `l1` norm equals its coefficient
magnitude. Summing terms and using the triangle inequality gives a real
symmetric correction `Delta R` with

\[
\|\Delta R\|_{op}\le\sum_{ij}|\Delta R_{ij}|
\le 6160\epsilon.
\]

At `epsilon=1/4928000000` this is exactly `1/800000`, so the corrected
Gram is at least `I/800000`. The same fixed numerator `p6` supplies a
valid global rational selector for every perturbed energy, and the constants
in (1) and (2) are halved. The limiting zero-base and finite-lift arguments
remain valid. For irrational coefficient perturbations this is an existence
proof with real Gram entries, not a rational serialization claim.

Separately, I evaluated the atomic functional on every ordinary quartic
monomial. If `S` is the sum of the absolute values of these 35 pairings,
then a coefficient-box perturbation changes the negative pairing by at
most `epsilon S`. Exact rational arithmetic shows it remains strictly
negative at the displayed radius, and also confirms the previously stated
larger atomic radius `1/336000000`. All ten selector annihilators are
independent of the energy and remain zero. Thus every energy in the full35
box has both properties. No target symmetry is retained as a hypothesis.

I bound the original combined-search target to its actual saved exact
coefficient list in `EXACT_COMMON_SEPARATOR.json`. It has determinant
coefficients `297124543/10000000000` and `-148562271/5000000000`.
Each is `1/20000000000` above the corresponding symmetric-target
coefficient. Thus its exact difference is

\[
\delta F=\frac{q(u+v)}{20000000000}
 =\frac{(ad-bc)(a^2+b^2+c^2+d^2)}{20000000000}.
\]

The eight terms are distinct ordinary quartic monomials; every coefficient
has magnitude `1/20000000000 < 1/4928000000`. I checked both that expansion
and the actual source coefficient list. The original point is covered by
the same PC/QC and all-polynomial-selector conclusion.

## 7. Finding, limits and reproducibility

There is no unresolved mathematical issue in the audited finite theorem
and its analytic extensions. The feature-order documentation omission
identified during review has been repaired in the final producer proof;
the exact positive JSON remains unchanged. Both the original and symmetric
points, and the full35 box, are accepted internally at this scope.

This does not classify the full nine-coefficient ROC/QC cone, prove a
universal rational-selector degree bound, audit the separate general
rational-hierarchy completeness argument, or provide an efficient evaluator
for the supremum lift. Those are not premises of the theorem proved here.
The numerical acquisition status is immaterial after exact reconstruction.
No publication, external priority or practical physical advantage is
claimed by this review.

Replay from any working directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 producer-workspace/independent_audit.py
```

The checker writes only its receipt in this independent review directory.
`INDEPENDENT_EXACT_REPLAY.json` contains the full exact pairings, margins,
35 sensitivities and bindings. No frozen producer or peer file was changed.
