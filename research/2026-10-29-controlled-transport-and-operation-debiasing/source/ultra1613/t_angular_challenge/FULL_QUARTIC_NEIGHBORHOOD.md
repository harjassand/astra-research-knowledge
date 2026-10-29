# Further construction: a full 35-dimensional QC/non-PC neighborhood

Status: independently DERIVED by the reviewer from the original exact certificate;
the original target has whole acceptance below, while this new extension is offered
to root/producer for their own challenge. No new optimizer/source/gradient fixture
was used. ROBUSTNESS.json is its exact scalar consumer on the SAME old Jensen atoms.

Let E(A)=sum_(|gamma|=4) e_gamma A^gamma be ANY real homogeneous quartic in the
four row-major matrix entries. There are35 ordinary monomials. Assume EVERY
coefficient satisfies

    |e_gamma|<=1/100000000.                           (R1)

No objectivity, isotropy, alignment, evenness in individual coordinates, or retained
Hopf representation is required. Define F_E=F+E, with F the original source.

**New corollary.** Every F_E in this full coefficient box is positive away from0,
strictly rank-one convex, not polyconvex, and obeys on every bounded Lipschitz domain
and for every A0 and phi in W0^(1,4)

    integral[F_E(A0+Dphi)-F_E(A0)]
       >=(1/1200000) integral|Dphi|^4.                (R2)

This is a constructive robust receiver reusing the SAME nu and angular primitive,
not an existence argument for a freshly reoptimized form at each perturbation.
It does not classify all quartics or settle Morrey's general implication.

## 1. Whole perturbation dissipation

Let epsilon=sum |e_gamma|<=35/10^8=7/20000000. For one degree4 monomial, its second
directional derivative is the sum of12 ordered choices of differentiated factors.
The absolute value of each resulting product is at most|A|²|B|². Hence

    |E''(A)[B,B]|<=12 epsilon |A|²|B|²,
    ||E''(A)||op<=12 epsilon |A|².

Consequently, with precisely the compatible jets and skew operator already paid,

    |D_nu E|<=24 epsilon(1+|nu|)T|h|².

Take kappa=1/400000. The original certificate implies

    D_nu(F_E-kappa |A|⁴)+dalpha(B1,B2)
      >=[1/12000-24(1+|nu|)(epsilon+kappa)] T|h|².

Using the ACTUAL rational nu, its bracket is exactly

    111947330408503/7500000000000000000 >0.

The already whole-checked Stokes/skew-flow/heat-limit argument therefore proves QC
of F_E-kappa |A|⁴, and the same quartic Bregman inequality gives(R2). The non-PC
conclusion below is essential: this family cannot be explained away by a hidden
ordinary convex-minor certificate for the original target.

## 2. Same finite witness remains non-PC

Use exactly the original sol9 three atoms and weights at A=diag(36,35), already
replayed independently. For every degree4 monomial let

    C_gamma=sum_i lambda_i B_i^gamma-A^gamma.

The exact35-coefficient moment vector in ROBUSTNESS.json has

    sum |C_gamma|=435968379091245264663/237512755936250000.

Thus the perturbed minors-Jensen deficit is at most

    -13534664264487807/296890944920312500
       +(1/10^8) sum |C_gamma|
    =-1082337172779933314735337/23751275593625000000000000 <0.

The same positive weights still match the mean matrix and determinant, independently
of the integrand's coefficients. Jensen contradicts ANY convex minor lift for every
member of(R1). There is no finite-gradient law or restricted SOS inference here.

## 3. Positivity and strict ROC persist

Completing the original q-square gives

    F>=T²-[(99/25)^2/(4(252/25))]x²
      >=(1711/2800)T².

Since|E|<=epsilon T², every member is bounded below by

    (85549951/140000000)T² >0   for A!=0.

The accepted old source has the weighted half-Hessian ROC margin7/35200. The new
perturbation's half-Hessian norm is bounded by6epsilon, leaving

    (1/2)D²F_E(A)[R,R]
      >=(5411/27500000)|A|²|R|²,

for every rank-one R. This consumes the already accepted old quantitative ROC theorem;
it is not a new independent derivation of all its acoustic algebra. It proves the
claimed strictness with the same quartic-origin convention as the source.

The coefficient box is sufficient, conservative and unoptimized. Historical priority
or maximal parameter range is not asserted. Its scientific point is full polynomial
coefficient freedom beyond the source's six-dimensional Hopf sector and the passing
nearby PC control, with a reusable explicit exact-form receiver and no new search.
