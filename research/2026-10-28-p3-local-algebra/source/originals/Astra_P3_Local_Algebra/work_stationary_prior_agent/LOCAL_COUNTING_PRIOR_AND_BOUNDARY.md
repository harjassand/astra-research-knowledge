# Prior algorithms and the equal-characteristic local-ring boundary

This is a focused comparison, not a claim that no other algorithm exists.
The specific goal is an exact sum of the primitive top-coefficient character
over F_(2^d)[t]/t^e, with both d and e growing, after acquisition from raw
Boolean coefficients.

## Established stationary phase

The highest-digit cancellation, local expansion around critical points,
and nondegenerate quadratic sums belong to the classical local stationary
phase tradition. Zuniga-Galindo's *Igusa's local zeta functions of
semiquasihomogeneous polynomials*, Theorem3.5, gives effective rationality
for semiquasihomogeneous forms with an absolutely isolated singularity over
a non-Archimedean local field, using stationary phase. It does not state
the binary raw-input acquisition or the polynomial-in-(d,e) weighted
critical-ray compiler in this work. The smooth homogeneous recurrence
should not be presented as a new principle of local analysis.

Primary source: https://arxiv.org/pdf/math/9909184,
Theorem3.5 and Section2. Published version: Transactions of the American
Mathematical Society353(2001),3193--3207,
https://doi.org/10.1090/S0002-9947-01-02323-6.

## A strong recent competitor: compact root trees for prime-power integers

Chakrabarti and Saxena's author-hosted manuscript *A compact tree structure
for the roots of multivariates mod p^k and the related Igusa's local zeta
function* gives deterministic polynomial(p+k) complexity for fixed degree
and number of variables, including singular roots. Its branching/pruning
mechanism jumps through repeated maximal-multiplicity lifting stages.
This is a substantive predecessor for manufacturing compact local
representations and must be compared rather than bypassed.

The displayed theorem is over Z/p^k Z. It does not directly cover
F_(2^d)[t]/t^e, and a naive residue-field replacement p->q still leaves
dependence polynomial in q, exponential in d. Further, congruence-zero
counts do not by themselves evaluate a chosen primitive additive
character. The exact adaptation and arithmetic costs would need proof.

Primary current version:
https://www.cse.iitk.ac.in/users/nitin/papers/IZF-n-var.pdf.
An earlier full version with the same title family and explicit exponent
(2D(b-1))^(b-1) in Theorem4 and the trivariate analysis in Section7 is
https://www.cs.columbia.edu/~sayak/files/IZF_23.pdf.
The fixed-number-of-variables restriction is essential to that bound.

## Univariate prime-power algorithms are not generic ternary algorithms

Dwivedi, Mittal and Saxena count basic-irreducible factors of univariate
polynomials modulo p^k in deterministic polynomial(degree,k log p) time,
using split ideals and a compact tree. Roots are a special case. This is
stronger in its dependence on p than the preceding multivariate bound,
but its variable restriction prevents importing it as a general ternary
local-character counter.

Primary source: *Counting Basic-Irreducible Factors Mod p^k in Deterministic
Poly-Time and p-Adic Applications*, CCC2019,
https://doi.org/10.4230/LIPIcs.CCC.2019.15.

## Positive characteristic is a real qualification

Hong and Yin's *On Igusa local zeta functions of Hauser hybrid polynomials*
explicitly distinguishes the general characteristic-zero rationality
theorem from the positive-characteristic problem, and proves rationality
for its own three-variable hybrid family. Its introduction explains why
one cannot simply invoke the characteristic-zero resolution or cell
decomposition arguments in equal characteristic. This is not evidence of
a lower bound for our restricted unit-XYZ cubic family.

Primary source: https://arxiv.org/pdf/2202.01138, introduction and main
theorems. A checked recent release, Nguyen--Yasuda (8 October2026), concerns
weighted homogeneous forms and Q-embedded resolutions over p-adic fields;
its abstract does not supply the required equal-characteristic binary
algorithm: https://arxiv.org/abs/2610.12222.

## The finite-field terminal is already polynomial

Lauder--Wan provide deterministic finite-field point counting at fixed
characteristic, degree, and number of variables, with no nonsingularity
assumption. For a ternary cubic character sum, count the four-variable
Artin--Schreier hypersurface w^2+w+H(X,Y,Z)=0. Its point count is q^3+Z.
Proposition36 and the affine torus decomposition yield soft-O(d^19) time
and soft-O(d^12) space for this fixed-degree3, characteristic2 problem.
This is a valid existing backend for all depths congruent to1 modulo3.

Primary source: https://arxiv.org/pdf/math/0612147,
Proposition36 and Section6.4.

## What the constructed extension actually removes

The new coefficient-level construction in `CRITICAL_RAY_COUNTER.md`
removes the smooth-residue requirement for homogeneous ternary cubics
with unit XYZ coefficient. It also retains arbitrary binary quadratic
weights on the low quotient. In characteristic two, each chart's
transverse gradient is an affine binary linear map with constant
invertible Jacobian. Its small kernel manufactures all candidate rays.
The radial cubic becomes a binary quadratic, so arbitrary compatible
quadratic weights remain Gaussian. Only the origin recurses. These are
proved and executed interfaces; no claim of first priority is made.

The separate raw-input acquisition theorem is what prevents the easy
coordinates and useful description from being assumed for free. Any
statement of a raw Boolean algorithm must include that acquisition,
its exact coefficient fit, and the original variable/description costs.

For the wider generic-circuit question, this remains a restricted acquired
family. The presently examined primary literature neither supplies nor
rules out a polynomial algorithm for arbitrary ternary cubic primitive
character sums over growing equal-characteristic chain rings. General
nonhomogeneous perturbations, incompatible binary quadratic weights, and
unrestricted algebra centroids require new arguments.
