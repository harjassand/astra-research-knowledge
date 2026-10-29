# Root whole review: bounded-effect noisy asynchronous FIFO

29 October2026. ACCEPTED at the specified finite-bit/atomic-channel model.
PROOF.md SHA2564f6b081b4c9c2e91336fbdf2c0c4dfc42af9b27f113fd2096adcb1b3d12c59f5.
COVERAGE_ERODER.md SHA256155ffde677aa61a39088f716b916673dfb61886e124b78c5f1218d215ae2ad69.
I whole-read/reconstructed both, PRIOR_AND_DECISION, RESULT, fifo.py and
compile_deadline.py. No producer bytes were edited and no consumer rerun.

Every tag pattern is a valid bounded FIFO occupancy. I reconstructed all
local tag-flip cases, the queue-word invariant and the<=2q packet-edit
effect of a q-bit replacement. Input append and output pop preserve the
concatenated word relation; subsequent nominal stages do not amplify an
earlier edit. The local overwrite/commit guards supply causal release
without a global mathematical majority or fixed source-holding interval.

The all-state coverage argument is pathwise. In a fault-free covered
window, either a nonidentity action already lowered workload or the
unchanged relevant state retains an enabled clock until it rings. The
Lindley majorant from deterministic Wmax therefore avoids an anticipative
starting-pattern drift assumption. I reconstructed its mgf constant,
optional-stopping exponential/mean bounds and rational deadline compiler.
The fixed-boundary union, not strong Markov at a future-selected time,
pays all acceptance times. For an undamaged accepted packet, later inputs
lie behind its FIFO prefix; the same rightmost-packet/service argument
applies. The alternative is deadline OR a charged edit, equivalently a
small event of late AND undamaged, not small probability of raw edits.

The literal transition program matches these guards and occupancies.
The exact deadline compiler pays its M-dependent noise, clock coverage,
future-start union and bit arithmetic. Producer's all1024-state and57344-
fault-case receipt is a separately scoped execution; this review did not
repeat it or turn it into an all-size proof.

Accepted: the bounded-local dynamic noisy FIFO, unlocated edit budget,
schedule-uniform drain-epoch and transfer deadline-or-edit theorem. The
Finner extension requires the stated private clocks/independent streams;
serial concatenation instead uses the single pathwise queue invariant.
Ready-consumer/atomic-channel assumptions and source values remain inputs.

Not inferred: reliable encoded acknowledgement, heralded erasures,
constant-noise growing-wire threshold, a restored feedback token ring,
transistor realization or quantum-data decoding. Scalar-port and closed-
ring obstructions are correct at their displayed scopes. Sutherland and
stabilizing-link/queueing methods are strong controlling prior; no generic
architecture novelty or practical advantage follows. This is a substantive
dynamic-interface improvement over the earlier fixed-source copy, while
the full autonomous logical-controller target remains open.
