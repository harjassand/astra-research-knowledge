# Executed fixed-column rational pruning on certified retained-memory effects

2026-10-29 UTC. Construction/check pending independent review. This executes the previously accepted `compact_prequential_flag_recovery_20261028/RATIONAL_PRUNING_v2.md` mechanism; it is not a new pruning theorem or a hardware compiler.

## Operation and acquisition interface

The input is the rational compressed learner POVM, its observed-label dictionary, and the public Pauli alphabet size A. No source matrices or retained environment state are read by the algorithm. For K unseen labels, sample a uniform rank in[0,K), then map it to the corresponding actual unseen label by scanning the sorted observed dictionary and incrementing past excluded labels. This needs O(number_observed) integer operations; it does not enumerate the A-label alphabet. Put the whole unseen aggregate effect on that one actual label. Averaging over the private choice restores C/K on every unseen label.

Keep the resulting original positive effect columns FIXED. Each is represented by its four rational Pauli coordinates. Starting with scalar weights1, if more than4 effects remain, find an integer dependence among5 active original columns by rational row reduction. For dependence c, let t_plus=min_{c_i>0} w_i/c_i and t_minus=max_{c_i<0} w_i/c_i. Both signs exist because nonzero positive effects have positive trace. The two feasible endpoint weights are w-t_plus*c and w-t_minus*c. Pick the plus endpoint with probability -t_minus/(t_plus-t_minus). The exact conditional mean weight is w and each endpoint removes at least one effect. Fixed columns, rather than recursively changing matrices, preserve the accepted rational bit-growth argument.

The operational code uses a capped rejection sampler with128 attempts for each exact rational endpoint/default choice. Every returned branch remains a physical POVM even on cap failure. The exact mean identity belongs to the uncapped ideal coins; cap failure couples the actual whole correction channel to it with half-diamond debit at most(number_of_pruning_steps+one_default_draw)*2^-128. Null dependence, effect positivity and sum-to-identity are exact rational tests.

Since a flag measurement followed by label-dependent correction is linear in its effects (including on arbitrary external reference and retained memory), preserving each label's mean effect preserves the **whole averaged correction channel**, not only Bell fidelity or one empirical source score. Every realized receiver has at most4 effects/corrections. Quantum synthesis of those effects' Naimark dilation, gate precision, reference storage and teleportation are still separately paid/unexecuted interfaces here.

## Executed certificate-bank test

Inputs are the final certified POVMs of each3×N4096 retained-memory run (seed7301/7302/7303). Each has8 observed labels plus an unseen aggregate. `check_pruned_receiver_v1.py` enumerates all32 pruning leaves only as a small-instance independent exact-mean validator; exhaustive enumeration is NOT the operational sampler. It checks exact rational equality of every average effect to its input column. It separately verifies the uniform-default rank map on the small16-label fixture. One actual bounded-coin path per seed produces at most4 labeled effects, all exactly positive and summing exactly to identity. Detailed private-bit/debit and sample output records are retained in check_pruned_receiver_v1.json.

No new source calls were acquired. This is a receiver realization check on the certified learned state. Old N64/N4096 poor recovery scores remain unchanged; compact realization does not cure their scientific negative result. The outputs are classical descriptions of physical POVMs, not measured hardware states.
