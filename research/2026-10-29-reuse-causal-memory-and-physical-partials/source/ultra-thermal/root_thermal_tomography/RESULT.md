For a **known endpoint chain**, the finite-temperature Gibbs variance at
one port, under **n selected uniform stiffness shifts**, identifies all n
nonnegative local quartic coefficients on a supplied bounded box. The
known-K computation can select those shifts from any 3n−2 distinct positive
candidates. This adds calibrated global stiffness control and a distributed
mechanical heat bath; it does not identify unknown K from passive noise.

PROOF.txt pays finite-temperature bias and then proves a uniform Jacobian
bound. At a sufficiently small positive temperature it gives global
injectivity and a projected contraction receiver on the WHOLE box. Exact
zero-temperature derivatives, distinct coefficients and a local optimizer
are unnecessary. The forward operator is acquired by degree≤10 Gaussian
moments with a finite alternating Taylor remainder, without assuming the
quartic perturbation series converges. Wick/FDT/continuants/contraction and
finite moment bounds are established mathematical operations. Historical
novelty remains UNKNOWN. B's substantive independent whole proof/code review
is now ACCEPTED at these declared scopes; see
../bridge_cross_review/thermal_tomography/REVIEW.md and RECEIPT.json.

The actual execution qualifies the EXISTING decoded four-node star K by
exact rank, rather than asserting the chain theorem applies to that star.
FRAME.json, GLOBAL_INVERSE.json and FORWARD.json preserve the exact inputs
and bounds: selected shifts1,2,3,4, theta≈6.24546e−10, global contraction
q≈.0242643, whole-box transformed forward error≤9.97126e−11. With the
stated .04/.95 data contract, two inexact contraction steps would give a
conditional parameter radius≤.0213805. **No variance observations or
inverse iterations on data were performed.**

Only the exact mathematical map needs the q contraction bound. The
polynomial approximation has a uniformly bounded evaluation error;
finite-step comparison to the exact map suffices, without asserting that
the approximate map itself is q-contractive. The staged GLOBAL_INVERSE.json
predates FORWARD.json, which closes its candidate-forward requirement for
this actual input. A complete physical observation/receiver run is absent.

The conservative stationary point-read design costs roughly1e37 total
reads even without electronic noise. This is a sufficient budget, not an
information lower bound or optimal cost. It does not justify a practical
instrument claim, nor rule out better temperatures, shifts, full nonlinear
likelihood or a different experiment. The same-bath active FDT comparator
has the same static information. Finite exposure, initialization, physical
K/bath/shift/temperature calibration and actual model validity remain unpaid.

Measured arithmetic after imports: .00641475s initial ten-resolvent frame,
.00036913s saved-frame global composition, .00336350s four-resolvent
whole-box moment compiler; sum .01014738s. Derivation, primary retrieval,
imports, tool overhead and peer review are additional untimed costs. These
are computational construction costs, not experiment costs or a speedup.

This completes a computational conditional interface and a stronger
identifiability theorem. It does not complete the civilisation-level goal.
