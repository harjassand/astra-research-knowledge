# Next implementation gate: robust native equilibrium, not exact-model refinement

2026-11-01. Delivery82 is preserved. The new task is not solved.

## Operational target
Retain size-improving quantum storage in a nonzero open region of native two-body Hamiltonians, with generic small fixed local calibration errors and a defensible physical thermal environment. Fixed qudit dimension, density, coupling bounds and temperature remain independent of volume. Ideal endpoints remain an explicit separate gap, not silently charged to this theorem.

## Available consumer already earned
The earlier exact-H thermal logical-twirl theorem does NOT require a commuting reference or exact logical independence of the perturbed Hamiltonian. It needs a reference H_ref commuting with the chosen full-space decoder Pauli algebra, a perturbation V whose local data footprints are correctable on P_good, and an actual interacting Gibbs estimate p=Tr(P_bad rho_beta). Then relative entropy gives logical twirl error <=2sqrt(beta*v*n*p), equilibrium overwrite remains uniformly dominated up to that error, and exact unitary evolution under the SAME total Hamiltonian yields a reference-safe storage bound proportional to n*T*(2p+twirl_error).

The new clock reference satisfies [H_ref,Q]=0 exactly. After its finite-depth U, generic bounded-local native perturbations remain bounded-local data+clock operators, so the local commutator premise transfers after a fixed good-set enlargement. Thus the decisive unearned step is STATIC actual-Gibbs rare-witness stability under generic noncommuting V (and finite onsite bath spins with weak contacts), not a new exact physical-time consumer.

## Obstacles that cannot be hidden
- A global Gibbs or Hamiltonian norm estimate exp(beta*n*v) can overwhelm a stretched-exponential witness penalty; it does not establish local cancellation.
- A ground-band gadget error times T is useless on the desired storage horizon.
- Exact Davies dynamics can be discontinuous when a tiny logical-dependent transition splitting resolves two previously degenerate branches. This is a model-limit issue, not automatically a finite-coupling physical failure. An explicit two-qubit test is being developed independently.
- The previous generic uniform analytic operator-log premise was falsified by a local-chain complex-pole example. Do not reintroduce it implicitly.
- The exact rod gas for the unperturbed model has commuting data stabilizer fluxes. With V insertions, data syndromes become time-dependent and data-Pauli histories must close appropriately. Signed rods alone do not automatically prove the needed perturbed measure.

## Root constructive hypothesis to test
Expand generic V in local Pauli components after U, retaining ancillary operators. Its insertions form syndrome-changing worldlines. Intervals between insertions can couple to background winding rods throughout the interval, not merely at overlapping hop events. Treat the entire time cylinder beta as a finite local cost for each V-connected support. A perturbative activity may be as small as beta*v*exp(C*beta*Delta), which is still a fixed-volume-independent requirement. However one must explicitly cancel remote background free energy and prove component closure and witness-relative bounds; no such estimate is claimed yet.

The earlier commuting-code quantum polymer proof used bounded imaginary-time conjugation stars and polynomial stabilizer filling. Those stars do not directly transfer to the noncommuting ancillary reference. A successful replacement could use a joint time-contour expansion, a genuinely local Gibbs-response principle, or another physical mechanism. Spatial quasi-locality alone with exp(-radius) tails is weaker than exp(-support size) and may fail the old cardinality norm; do not identify the two.

## Decision criterion
Close this static gate, find a decisive obstruction, or identify a materially stronger physical principle. Preserve the exact native thermal construction as an obstacle-removing result. Do not spend the next stage optimizing its already-conservative constants while generic imperfections remain untreated.
