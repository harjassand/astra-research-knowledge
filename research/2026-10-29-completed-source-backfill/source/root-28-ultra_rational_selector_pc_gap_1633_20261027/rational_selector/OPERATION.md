# Changing the selector representation, with a charged acquisition

The first genuinely nonlinear interface below succeeded. It now has an
exact rational180-feature certificate, a full35 open neighborhood theorem,
and a completed substantive independent audit. Read `PROOF.md` and
`../rational_selector_independent_review/REVIEW.md`. The original and
symmetric targets are PC/QC, with no polynomial global minor-support map
of any degree. The earlier failed stages below remain recorded at their
actual historical scopes.

The 24-atom obstruction in `../common_cone_review/ATOMIC_REVIEW.md` excludes
every polynomial selector in B_F(A,X)−k(A)detX≥0, not every nonlinear
degree-two homogeneous selector. The constructive next interface is

    k(A)=p_(2m)(A)/|A|^(2m−2), A≠0; k(0)=0.

The peer's complete proof at
`../quartic_boundary_alternative/RATIONAL_SELECTOR_COMPLETENESS.md`
establishes a finite SOS-plus-sphere-ideal hierarchy for arbitrary uniform
strict global minor supports. Root has whole-read and accepted its complete
conditional proof, including: the literal 2-by-2 polarization matrix,
robust local scalar selection, finite-cover continuous even selection,
rational sphere-polynomial approximation, the Archimedean matrix theorem,
and a rational positive-definite Gram construction modulo the sphere ideal.
These are applications of established approximation and Scherer–Hol
machinery. A new general positivity theorem or efficient algorithm is not
claimed. The construction covers every rational PC quartic after adding
epsilon|A|⁴ with positive rational epsilon, and every interior rational PC
quartic. It supplies no boundary termination, degree, bit, runtime or
negative-decision bound, and does not establish actual PC of our target.

## The first attempted denominator was symmetry-forced to be polynomial

`acquire.py` built the complete 80-feature SOS interface

    |A|² B_F(A,X)−p4(A)detX = Z80^T R Z80.

It allowed all 35 numerator coefficients, used 1,100 coefficient equations,
and had an ordinary norm control with positive numerical margin. The target
acquisition had margin about −1.6713e−5, status optimal_inaccurate; that
number by itself establishes no infeasibility.

The subsequent symmetry analysis explains why this representation cannot
work on the exact target, without relying on that numerical status. Put
T=u+v=|A|² and h=(x,y,z)=(u−v,2w,2q), so T²=x²+y²+z². The target is
left-SO(2) invariant and invariant under the antiunitary map h→−h and
column swap (x,y,z)→(−x,y,−z). A support selector transforms with the
determinant character: it is odd under both of those latter symmetries.
Averaging a feasible rational selector preserves feasibility because its
denominator T is invariant and the support condition is affine in k.

Every degree-four invariant numerator is degree two in (T,h), modulo
T²=|h|². Oddness under h→−h forces T times a linear form in h; the column
swap eliminates y. Thus p4=T(alpha x+beta z), and p4/T is polynomial.
The accepted atomic obstruction consequently excludes this entire rational
degree, including every larger Gram or increment-norm multiplier with the
same numerator degree. The failed acquisition is not evidence against
genuine nonlinear selection. More generally every even m reduces to m−1:
oddness in h forces a factor T, which cancels one denominator power.

The first genuinely nonlinear case is therefore m=3. Its complete
symmetry-allowed numerator space is

    p6 in span{x³,x²z,xz²,z³,xy²,y²z}.

Two combinations reproduce polynomial selectors via T²=|h|²; four
directions are new. This is a concrete change of scientific interface,
rather than another unsuccessful level of the polynomial-selector search.

## The actual first nonlinear acquisition

`acquire_first_nonlinear.py` built

    |A|⁴ B_F(A,X)−p6(A)detX = Z180^T R Z180,

using all 80 A³X and 100 A²X² monomials, 3,185 coefficient equations and
the complete six-dimensional symmetric numerator space. All map
coefficients were generated as exact integers before numerical acquisition.
The unstructured Clarabel numerical control spent over twelve minutes
without delivering a result and was terminated. It is not a completed
negative test and produced no accepted target result.

Root replaced that control with exact algebra. For the ordinary F=|A|⁴,

    B_F−(1/4)(|A|²|X|²+|X|⁴)
      =(7/4) sum_(i<j)(A_iX_j−A_jX_i)²
         +(23/4)s²+4sr+(3/4)r²,

where s=A:X and r=|X|². The remaining 2-by-2 coefficient matrix is PD,
with determinant 5/16. Multiplying by the exact multinomial for |A|⁴
constructs a full 180-feature Gram R≥I/4. Every feature has positive
diagonal coverage. The independent literal coefficient aggregation passed
in 0.073 seconds; see `EXACT_NORM_CONTROL_REPLAY.json`. This is an
algebraic control, not a comparative solver speedup claim.

`bounded_nonlinear.py` then completes the target acquisition with a
60-second solver limit and a 12,000-iteration cap. Its numerical output,
if any, is retained separately. A positive suggestion requires exact
coefficient reconstruction and positivity before any PC claim. A negative
or timed-out suggestion is not an infeasibility proof. This finite
interface is smaller than the complete two-sphere hierarchy and is not
claimed complete even at numerator degree six.

## A complementary heat attempt retained at its actual scope

`../heat_norm_multiplier/acquire.py` tested one |A|²-multiplied identity-heat
density, with all 45 closed forms, 60 features and 735 equations. The
ordinary DM control was numerically positive; the symmetric target had
negative numerical margin. No class-level impossibility follows. The
construction uses the existing homogeneous matrix-Reznick principle; see
Zheng–Fantuzzi, arXiv:2007.11410v2, Theorem 2.3, for the strict matrix
positivity premise and lack of a universal finite degree bound.

The direct compatible heat-dissipation search also found no negative
witness in its bounded Fourier family. Twenty separately acquired peer
Fourier profiles were evaluated after converting the peer's gradient-phase
convention to the root's potential-phase convention; all remained positive.
None of those finite searches establishes heat monotonicity or QC.
