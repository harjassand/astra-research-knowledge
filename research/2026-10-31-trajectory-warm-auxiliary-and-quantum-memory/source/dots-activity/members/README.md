# Activity scaling, precision limits and fair comparison
31 October 2026

## Strongest result in this checkpoint
The already checked retained-reservoir compiler now has a checked resource refinement. For bounded drive-to-loss ratio, its overhead is nearly linear in accumulated interaction activity and ordinary free-Hamiltonian action, apart from the displayed polynomial mode/input factors and logarithmic rate/precision factors. The fixed-window schedule sums the costs of actual controlled circuits; it does not assume a free variable-time operation or charge only a randomly realized path.

An exact one-lossy-qubit construction proves that linear activity dependence cannot generally be removed in the supplied-coupling oracle model. A separate exact construction at fixed activity proves a precision-query obstruction of order log(1/error)/log log(1/error). These are separate lower bounds, not a proof that every factor in the upper bound is optimal.

All results are mathematical. Internal independent checks are not external peer review, a full circuit implementation, a practical crossover or a novelty determination.

## Read in this order
1. NEAR_LINEAR_ACTIVITY_SCHEDULE_CANDIDATE.md and NEAR_LINEAR_SCHEDULE_INDEPENDENT_REVIEW.md: refined upper resource bound, including actual query-versus-gate costs and safe finite windows.
2. EXACT_ACTIVITY_QUERY_LOWER_BOUND_CANDIDATE.md and its independent review: exact finite-rate clock/parity construction, total acquisition costs and linear activity obstruction.
3. EXACT_PRECISION_QUERY_LOWER_BOUND_CANDIDATE.md and its independent review: Erlang renewal and a uniform-channel Fourier argument at fixed activity. The growing clock size and costly rare-event readout are explicit.
4. PRIMARY_COMPARISON_AND_CONSEQUENCE.md, CONTROLLED_MEMORY_WITNESS.md and their scoped reviews: what strong ordinary methods already do and what remains unresolved. The dense-comparator review covers Section 3 of the comparison only, not its whole literature survey.
5. GRADED_SECTOR_FIRST_EVENT_RECEIVING.md and GRADED_WHOLE_INDEPENDENT_REVIEW.md: complete physical compiler and acquired interacting/hard-core interfaces. Earlier bosonic/domain/bridge foundations are included for continuity.

## Physical and access restrictions
The main theorem retains a private initially vacuum reservoir under common loss, with a compatible number-preserving interacting Hamiltonian, bounded encoded system couplings and interventions at prescribed times. All operator acquisition, encoding, arithmetic, Hamiltonian simulation and consumer costs are paid. Opaque query access does not confer cheap elementary gates. The bounded drive-to-loss qualification is needed to turn occupation factors into logarithmic factors for the stated broad bosonic scaling; an exact finite hard-core cutoff can instead be used when available.

Unequal losses mixed by the free Hamiltonian, arbitrary thermal nonlinear reservoirs, public bath observations, adaptive intervention times and normalized rare postselection are not covered. Previous harmonic thermal results are separate capital, not a blanket thermal extension of the interacting theorem.

## What the comparison establishes
Small full-dimension problems already admit ordinary dense high-precision channel construction with logarithmic stiffness dependence. Fixed-accuracy adiabatic elimination can be cheaper; exact higher-order reductions exist for special models. Retained process-tensor and memory methods are serious alternatives. No general superiority over all such acquired representations is proved.

The controlled-memory example only excludes a common future CPTP map on the reduced system alone below a finite-rate error floor. It does not exclude history-aware or retained-memory methods. Similarly the precision lower bound does not allow cheap experimental estimation of an exponentially small signal.

The defensible capability is succinct finite-rate controlled-channel simulation with explicit costs, not a claimed practical or civilization-level breakthrough. The comparison identifies the remaining issue: when, if ever, does this representation beat strong acquired-memory alternatives on a consequential task?

## Historical corrections and evidence
Original source headings sometimes say candidate; later source-bound receipts record their accepted scope. Earlier precursor words lacking the explicit (-i)^V Hamiltonian insertion phase are superseded by the final receiving bodies. The activity lower-bound source's reference to a higher-polynomial upper bound predates the separate near-linear refinement and should be read historically. No frozen proof was rewritten to conceal that progression.

The scripts and JSON outputs are small finite-matrix and Monte Carlo diagnostics. They do not execute the full quantum compiler. The new clock diagnostic used four input bits and two damping rates; it checks probabilities and trace preservation, not the oracle lower bound itself.

## Integrity
MANIFEST.json records original and delivered source hashes. Administrative reviewer labels were normalized and administrative access history removed from the comparison delivery copy; the scientific comparison and proof text were otherwise preserved. Hashes quoted inside receipts refer to original sources. The unused duplicate schedule derivation is excluded in favor of the exact reviewed final source. ZIP CRC and every member hash were checked before saving.
