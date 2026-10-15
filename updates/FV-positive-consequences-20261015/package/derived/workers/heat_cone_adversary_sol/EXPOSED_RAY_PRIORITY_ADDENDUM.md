# Close priority audit of the exposed quartic ray

15 October 2026. This is a comparison audit, not a claim of first discovery.
The author's frozen `PROOF.md` is the mathematical claim under comparison;
its coefficient vector is reproduced below. **Historical originality remains
UNKNOWN.** No further numerical search was performed and no author file was
edited. `priority_exact_comparison.py` independently verifies the algebraic
distinctions and the small acoustic/contact matrices used in this audit; it
does not reverify the author's complete heat exclusion.

For (u=a^2+c^2, v=b^2+d^2, w=ab+cd, q=ad-bc), the candidate is

\[
F=u^2+v^2+\frac{166}{3}uv-\frac{460}{9}w^2
       -\frac{52}{9}q(u-v).
\]

Its vector in `(u²,v²,uv,w²,uw,vw,qu,qv,qw)` is
`(1,1,166/3,-460/9,0,0,-52/9,52/9,0)`.

## Actual Fantuzzi comparison

The inspected source is Fantuzzi–Henrion–Kružík–Murali–Weis,
[arXiv:2604.11124v1](https://arxiv.org/abs/2604.11124v1), §§2.3–2.4,
especially Theorems 2.2–2.4, Remark 2.1 and Proposition 2.4.
It separates ordinary polyconvexity, SOS support certificates and convex
polynomial lifts. Its concrete planar homogeneous quartic is

\[
f(A)=|A|^2(|A|^2-2\det A),\qquad
p_f=(1,1,2,0,0,0,-2,-2,0).
\]

Theorem 2.4 proves that (f) is SOS polyconvex but not lifted SOS
polyconvex. Proposition 2.4 excludes **every convex polynomial lift** of
this (f), not every unrestricted convex lift. Theorem 2.3's general
separation between polyconvexity and SOS polyconvexity explicitly leaves
the planar degree-four case open in Remark 2.1. These statements therefore
neither identify this candidate nor decide its PC/QC status. The source's
nonhomogeneous double-well examples also have a different polynomial.
The acoustic rank-four certificate and fixed-linear-heat exclusion are not
consequences of any of these named theorems.

## Exact distinction from the classical rotational families

For every bi-SO(2)-invariant quartic

\[
Q=\alpha |A|^4+\beta |A|^2\det A+\gamma(\det A)^2,
\]

its rank-one restriction is
`Q(x tensor y)=alpha |x|^4 |y|^4`. After arbitrary invertible real input
and output changes, a transpose, and positive scaling, the restriction for
fixed nonzero output vector is still a real quadratic square times a
constant (or identically zero). In contrast,

\[
F\!\left(\begin{smallmatrix}s&t\\0&0\end{smallmatrix}\right)
=s^4+t^4+\frac{38}{9}s^2t^2
\]

is not a quadratic square: zero cubic cross coefficients force the middle
coefficient of a possible square to vanish; its remaining cross coefficient
would then be (2) or (-2), rather than (38/9).
Thus the candidate is **outside the entire real GL-input/GL-output and
transpose orbit of this three-parameter family**, not merely unequal to
one printed formula. Also `F(e11)=1` and `F(e11 R(pi/4))=14/9`, so it is
not itself right-SO(2)-invariant.

This covers the explicit rotational quartics in the inspected sources:

* [Aubert (1988)](https://numdam.org/item/M2AN_1988__22_1_5_0.pdf),
  §3, Lemmas 3.1–3.2 and Remark 2 (printed pp.16–18):
  (f_0=|A|^4/3-(\det A)^2/6-2|A|^2\det A/3), with vector
  `(1/3,1/3,1/2,1/6,0,0,-2/3,-2/3,0)`.
  Its ROC/non-PC assertion is on `GL+(2)`; the extended function is
  infinite on nonpositive determinant. This domain is also different.
* [Dacorogna–Koshigoe (1993)](https://numdam.org/item/AFST_1993_6_2_2_163_0.pdf),
  hypothesis (H) and Theorems 1.1/2.1, impose **both** left and right proper
  rotations. They do not classify the full left-only nine-dimensional cone.
* [Bandeira–Pedregal (2009)](https://doi.org/10.1016/j.anihpc.2008.08.002),
  Theorems 1–2 and §3, give acoustic-Hessian quotient construction methods.
  Examples 1–2 are `|A|^4-c |A|² det A` and
  `|A|^4-c (det A)²`. Their remaining printed examples use trace terms,
  nonhomogeneous terms, or 2-by-3 matrices. The general construction method
  is prior; these examples are not the candidate.
* [Bruno–Pasqualotto (2026), v1](https://arxiv.org/html/2608.06367v1),
  Theorem 2 and Appendix A, handle the bi-rotational family. Appendix A
  decomposes it into a corrected-heat component and a nonnegative
  determinant-square component. This is prior compatible-heat mathematics,
  on a three-dimensional invariant subcone.

## What is already established about the operation

The acoustic SOS mechanism is classical. In a biform with groups of
dimensions four and two, nonnegativity implies a sum of bilinear squares
by Terpstra/Calderón. It does not make every ray in a linear section an
extreme ray of the ambient biform cone. The independently checked acoustic
Gram for this candidate has rank four; its `n=(1,0)` quadratic in A also
has rank four, so the acoustic biform is not a single bilinear square.

[Blekherman–Raiţă–Shankar–Sinn (2022), §2 after Corollary 2.9](https://arxiv.org/abs/2204.10625v1)
states that when one group has dimension two, ambient strong extreme
biforms are perfect squares. Its §3, especially Theorem 3.2, already uses
zeros and Hessian kernels to determine extremality constraints. The
author's claimed extremality is instead in the **nine-dimensional image
of integrable invariant quartic Hessians**. Its substantive finite statement
is that the four exact contacts leave a one-dimensional kernel: the
20-by-9 criticality matrix has rank eight. The independent comparison
script checks that rank and checks that its kernel is the displayed F.
Neither a rank-four Gram alone nor a generic contact principle proves it.

[Guerra (2019), Theorems 1.1–1.2](https://arxiv.org/abs/1812.06689)
provides explicit extreme rank-one-convex integrands and a laminate
characterization in much larger cones. Its displayed minor truncations
are different functions. Extreme-face reduction is established convex
geometry. The author's use of exposedness to force every finite positive
heat/PC summand onto the same ray is an application of that principle.
It still leaves the candidate's polyconvexity unresolved.

## Audit verdict and receipt boundary

No inspected exact example or named theorem identifies the displayed ray.
The non-orbit distinction is proved, and the acoustic/contact ingredients
have explicit predecessors. The distinct remaining specialization is the
particular nine-coefficient exposed ray together with the author's complete
fixed-strongly-parabolic-linear corrected-heat exclusion. **This audit does
not establish historical originality, a first rank-four example, a full
left-only cone classification, or non-polyconvexity/non-quasiconvexity.**

The close historical coverage is incomplete: Parry (1995), *On the planar
rank-one convexity condition*, and Parry–Šilhavý (2000), *On Rank One
Connectedness, for Planar Objective Functions*, were reached only at
primary abstracts; the possible Gurvich predecessor credited by Aubert was
not independently retrieved. No stronger priority claim follows from a
failed access attempt or absence of a match in the inspected sources.

`PRIORITY_EXACT_COMPARISON.json` records exact algebra checks and frozen
author input hashes. `PRIORITY_SOURCE_RECEIPTS.json` records primary URLs,
local PDF hashes and inspected scope. All acquired fulltexts and rendered
pages remain in `private_primary_fulltexts/`, which is explicitly excluded
from the manifest and every dissemination package.
