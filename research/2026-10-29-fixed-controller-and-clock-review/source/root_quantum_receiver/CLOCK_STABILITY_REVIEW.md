# Root analytic review of the two-body clock stability transfer

Root whole-read b_conventional/clock_stability/PROOF.md, including the added
quasilocal initial-Hamiltonian argument in section8a, on29October2026.
ACCEPTED at its parameter-qualified mathematical scope. This is a substantive
analytic internal review; no new finite-model run or physical validation.

The sectorwise use of spectral flow is legitimate: the derivative and all
dynamics preserve the formal check signs, and every clock ground fiber has
the same positive intra-sector gap. A global band isolating all those fibers
is not required for this projection identity. LR locality follows separately
from local interaction/filter bounds. Pullback through dependent physical
checks is a norm-contracting homomorphism; whole-check support is retained.

Root checked the vacuum martingale exactly. Product vacuum expectations and
formal-sign averaging preserve Hermiticity and fiberwise vacuum annihilation.
Anchored differences receive contributions only from terms containing their
anchor. Ball differences thus have the stated tail and Q_B T Q_B property.
Allocating explicit scalar tail majorants from the onsite penalties produces
an exact positive FF interaction. The large excited-clock terms are paid by
those penalties, rather than falsely declared small in absolute norm.

Marked amplitudes live in the SAME unmerged l1 power-series algebra as the KT
contraction. Differentiation counts multiplicities before regrouping signs or
physical relations. Connected-cluster support and the convergence disk pay
the spatial tails of the syndrome-energy remainder, not just its total norm.
Positive per-check allocation then retains the source local ground projectors.
The new FF restricted Hamiltonians have exactly the bare-code/vacuum kernels
and a uniform local gap; this is not asserted for cut original clock rings.

Polynomial check soundness implies polynomial-buffer compression of EVERY
local observable. Applying it to O^dagger O gives the exact norm identity
||O P_local||=||O P_global||. Root reconstructed the telescoping localization:
global block diagonality makes the offending compressed pieces controlled by
the discarded spatial tail; nesting makes each difference annihilate the
larger local projector. The relative-form cost is a sum of polynomial overlap
counts times a rapid tail, hence finite uniformly in N. Strong spatial LTQO
and support-volume spectral-flow decay are not smuggled in.

Root directly checked the displayed primary scope: BMNS1102.0842v2
Proposition2.4 and Theorem4.8 supply projection transport/filter locality;
NSY2010.15337v3 section4 explicitly assumes FINITE-RANGE initial h_x. Root
raised that mismatch. Section8a now supplies the missing extension: pair sums
give a uniform stretched-exponential F norm; a perturbation light-cone split
gives an O(epsilon) polynomial-time Duhamel bound; short/long filter integration
retains O(epsilon) with a rapid spatial tail. Convolution against the initial
quasilocal shells pays the anchored bound. A raw exponential-in-time Duhamel
bound could not have been filter-integrated. This repair is load-bearing.

The final min-max bootstrap is sound: form bound<=1/4 and tail remainder
delta_N<gamma/16 give logical width<=2delta_N<gamma/4 and outside gap
>=3gamma/4-2delta_N>gamma/2, closing the assumed interval. Polynomial distance
growth makes N times the rapid tail vanish. Finitely many small sizes can be
absorbed in one lower perturbation threshold.

Conclusion: for SOME fixed lambda<=min(lambda_*,lambda_FF), with correspondingly
fixed Delta, the source-qualified two-body QUDIT endpoint has a stable logical
ground band under arbitrary sufficiently small bounded-range physical errors.
Thresholds may depend disastrously on those fixed parameters but not on N.
The old literal clock recipe was NOT numerically qualified against lambda_FF.
No two-body-qubit conversion, native thermal memory, useful physical threshold,
efficient full FF-table compiler, or historical-priority claim follows.
