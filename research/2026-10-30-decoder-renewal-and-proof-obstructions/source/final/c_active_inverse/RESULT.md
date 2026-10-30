# A native coherent feedback controller; the linear-r question stays open

30 October2026. The original target was near-linear-r, near-perfect recovery
from an unknown exact flat mixed encoding using physical forward queries.
That asymptotic target is NOT_ACHIEVED. The following constructive boundary
is complete.

The new controller uses two fresh forward source calls, one after the
already encoded payload arrives. It coherently controls a known Pauli
Stinespring by a physical relative-SWAP sector, retains the Pauli label,
and feeds its correlated logical qubit into the second source call. A
six-label coherent permutation kernel and a fixed rational24->2 map
finish the operation. No unknown adjoint, controlled source, exposed junk,
quantum switch, generic Schur/RDS factory or inverse-mean oracle is used.

The SAME positive controller works for every r>=1 and D>=2r, arbitrary
unknown U. Its EXACT fidelity is

  Fe(r)=1/4+157722669488099/(495042781126656r)
           +40484174315045/(247521390563328r^2).

A physically allowed Pauli intervention on each fresh logical source
input, with its INTERNAL seed discarded, converts this to a whole-channel
halfdiamond error exactly1-Fe(r). Source copies/ancillas are consumed per
payload; this is not a learnt inverse requiring no later source use.

At r=2, its exact CPTP certificate gives Fe>=.4501916312687661. Root's
separate exact dual bounds EVERY two-query parallel strategy, with
arbitrary entangled probes and ancillas, by.4329406865435885. C independently
reconstructed all six rational dual blocks and normalizations. Thus the
causal cell has a strict full-throughput all-input/reference minimax gain
greater than1/80 at this mixed-source family. This does not claim a general
adaptive exponent separation or historical priority.

Two failed independent mechanisms are retained: the exterior-hole decoder
has an exact but superexponentially small admission; the typical-sector
single-logical-spin receiver has an exact optimal all-r formula showing
quadratic rank cost for a fixed fidelity increment and a1/2 ceiling.
Fixed singlet query blocks are explicitly corrected as constant-overhead
Choi-simulable, not a physical-query advantage by themselves.

Only classical circuit algebra, exact rational/Young computations and
three small final-decoder proposals ran; no source, quantum circuit,
Haar sampler, device or calibrated hardware ran. The completed strong
ordinary RDS/flat-Petz route still supplies the best admitted near-perfect
upper here at quadratic r cost, with different offline/holding resources.
The next missing operation is a scalable coherent-history/restoring
controller, rather than another small-r fit or a classical Markov reset.

See C_COHERENT_FEEDBACK.md, C_COMPARISON.md, ALL_R_FAMILY.json,
COHERENT_FEEDBACK_DECODER.json and COST_AND_EXECUTION.md. Root's independent
literal physical composition separately accepted the normalized Choi,
all-r coefficients, exact CPTP controller and physical Pauli-twirl scope.
