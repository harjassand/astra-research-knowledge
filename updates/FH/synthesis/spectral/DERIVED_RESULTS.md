# Derived results: mirror-matched laminate and spectral identifiability

Audit date: 2026-10-14. These are independent mathematical/model checks of the frozen proposal, not experimental measurements or independent external review.

## 1. The exact mechanical condition for flipping one laminate

Consider N equal-thickness internal layers of width d, with layer-center coordinate

\[
z_j=d\left(j-\frac{N-1}{2}\right),\qquad j=0,\ldots,N-1.
\]

Let chi_j = 1 label h¹⁰BN and 0 label h¹¹BN, and let the fixed in-plane reduced stiffnesses be Q_L and Q_H. For a piecewise constant coefficient Q(z), the classical laminate matrices are

\[
A=\int Q(z)\,dz,\qquad B=\int zQ(z)\,dz,\qquad D=\int z^2Q(z)\,dz.
\]

For equal-width slabs, the internal-layer contributions are

\[
A=d\sum_j Q_j,\quad B=d^2\sum_j\left(j-\frac{N-1}{2}\right)Q_j,\quad
D=d^3\sum_j\left[\left(j-\frac{N-1}{2}\right)^2+\frac1{12}\right]Q_j,
\]

where Q_j = Q_H + (Q_L - Q_H) chi_j. The 1/12 term is the exact within-layer integral, rather than a point-center approximation.

Under geometric reversal chi_j maps to chi_(N-1-j), A and D are invariant and B changes sign. Since the centered sum of all layers is zero,

\[
B=d^2(Q_L-Q_H)\sum_j\left(j-\frac{N-1}{2}\right)\chi_j.
\]

Thus the necessary and sufficient ordering condition for a stack and its mirror to have the same A, B and D, for arbitrary fixed Q_L and Q_H, is

\[
\sum_j\left(j-\frac{N-1}{2}\right)\chi_j=0.
\]

The reversal itself preserves isotope inventory automatically. Requiring a 50:50 isotope fraction *inside each laminate* is an extra design constraint, not a condition for matching the flipped pair. Identical h¹⁰BN caps at both ends preserve the same conclusion: their zeroth and second moments are reflection invariant, and their first moments cancel by cap symmetry.

If each isotope has a fixed isotope-specific Q alpha and the temperature change is spatially uniform, the thermal force resultant is reversal invariant. The thermal moment changes sign and is zero for the same first-moment condition (including the symmetric caps). This does not match strain gradients, slip, imperfect adhesion, twist domains, nonlinear bending, edge damage, or arbitrary temperature fields.

## 2. A seven-layer non-palindromic construction

With zero-based indices, choose the h¹⁰BN internal layers at

\[
L=\{0,4,5\},\qquad H=\{1,2,3,6\}.
\]

The order from the target-facing side is `L H H H L L H`; its reverse is `H L L H H H L`. In doubled centered coordinates the signed h¹⁰BN first-moment weight is

\[
(2\cdot0-6)+(2\cdot4-6)+(2\cdot5-6)=-6+2+4=0.
\]

It is not palindromic and has the same three-L/four-H inventory after reversal. The second nontrivial seven-layer reversal class, L = {0,3,4,5}, also has zero first moment. The output in `analysis/independent_results.json` records both patterns and the exact layer-integrated moment fixtures.

The absence of a non-palindromic zero-first-moment pattern for N <= 6 can be shown by subset sums. In doubled centered coordinates, the positive weights for N = 1,...,6 are respectively

\[
\varnothing,\quad\{1\},\quad\{2\},\quad\{1,3\},\quad\{2,4\},\quad\{1,3,5\}.
\]

Each set has distinct subset sums. A zero-moment selection therefore has the same selected positive and negative weights term by term, forcing reflection symmetry; the center layer for odd N is free but is itself fixed by reflection. At N = 7, the positive weights ({2,4,6\}) have the collision 6 = 2 + 4, which enables L = {0,4,5}. This proves the seven-layer minimum for an equal-width binary laminate whose only requirement is a nontrivial flip pair with exact A, B and D matching. It does not assert minimality under other fabrication or composition constraints.

For the proposal's 80 nm internal thickness, seven equal layers are 80/7, about 11.4286 nm each, with the same 5 nm h¹⁰BN caps. The independent scalar fixture Q_L = 299, Q_H = 281 gives unit-width internal moments (A, B, D) = (2021, 0, 8288.4166667) for both orientations; rescaling to physical width d = 80/7 nm multiplies these by d, d^2 and d^3, respectively. The chosen coefficients are an algebra check only; they are not measured moduli of the proposed laminate.

## 3. Three design classes that must not be conflated

The exact enumeration distinguishes:

| Constraint class | Defining condition | First nontrivial mirror pair | Later enumerated examples |
|---|---|---|---|
| Unrestricted physical flip | Any isotope fraction; zero centered first moment | N = 7, two reversal classes | N = 8: 1; N = 12: 37; N = 16: 568 non-palindromic reversal classes |
| 50:50 flip-only | Exactly half each isotope per laminate; zero centered first moment | N = 8, one reversal class | N = 12: 19; N = 16: 228 |
| Complement/Prouhet moments | 50:50 and a stack/complement pair has equal moments of degrees 0, 1, 2 | N = 8, one class | N = 12: 1; N = 16: 7 |

The table's search counts are exhaustive binary enumeration only for the stated finite N <= 16. The Prouhet condition is sufficient for mirror matching but is stronger than necessary. The source's eight-layer Thue–Morse word belongs to all three classes; the seven-layer construction belongs only to the unrestricted physical-flip class. No priority or novelty claim follows from this elementary construction.

## 4. Optical response and what static matching does not identify

The independent optical implementation is a global amplitude transfer matrix, not an import of the producer recursion. Its reference parameters are transcribed in `analysis/independent_checks.py`; they are model inputs, not jointly measured parameters for a fabricated isotope stack on κ-ET. With 80 nm of internal material, 5 nm caps, a 20 nm witness height and the h¹⁰BN-in-vacuum source model at 1470 cm-1, the seven-layer pair with h10 positions {0,4,5} gives the signed witness contrast `difference_over_mean` -0.1260006 at the nominal damping. The source's eight-layer 50:50 pattern gives -0.1329513. At damping multipliers 3 and 6, the seven-layer contrast remains approximately -0.12606 and -0.12595. These are source-parameter vacuum scenarios, not measured performance; the seven-layer result is a modest contrast trade for one fewer internal slab and four rather than six isotope interfaces when counted with the identical caps.

A separate global transfer-matrix stress test makes the missing target loading explicit. Replacing only the terminal vacuum half-space by a synthetic, nondispersive, real isotropic substrate epsilon = 1, 2, 5, 10, 20 changes the eight-layer witness from about -13.295% to -13.261%; the seven-layer witness changes from about -12.600% to -12.566%. In the *ideal* mass-scaled model, static reflection remains equal to numerical roundoff for each such substrate because every hBN layer has the same epsilon(0). These loads are stress fixtures only. They do not model κ-ET's anisotropic, complex, temperature- and superconductivity-dependent dielectric response, and the near-constant results cannot establish real-target robustness.

The ideal exact static equality is a direct consequence of identical static permittivity in every hBN layer: at omega = 0, permuting the layers leaves the complete stratified boundary-value problem unchanged. The reference model using published isotope endpoints is not exactly matched; its independently recomputed maximum relative static-reflection residual is 1.91893e-5 over the tested q grid. The h¹¹BN high-frequency permittivity, damping and out-of-plane frequencies are shared or mass-scaled assumptions rather than a complete measured dielectric tensor. Thus exact static matching is conditional on the ideal oscillator model, while actual static agreement needs a tolerance and measurement.

For the ideal eight-layer pair at fixed q = 51 per micrometre, delta Im(r_p) over 1380–1650 cm-1 spans approximately [-6.128, 7.880], despite exact static equality. Two nonnegative weights proportional to the imaginary susceptibility of passive damped harmonic oscillators, Im[1/(omega0^2 - omega^2 - i gamma omega)], with synthetic gamma = 5 cm-1 and centers 1470 and 1572 cm-1, yield normalized weighted differences -1.650 and 2.126, respectively. This is a countermodel to inferring the sign of a target-weighted response from a static match and a local optical witness. The filters are mathematical, not κ-ET spectra. A loaded target susceptibility, spatial coupling and equilibrium response are not supplied, so no superconducting sign or magnitude follows.

