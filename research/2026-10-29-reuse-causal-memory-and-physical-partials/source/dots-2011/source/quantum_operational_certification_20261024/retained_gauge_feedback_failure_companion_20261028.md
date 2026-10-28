# Exact returned-gauge failure of an effect-only adaptive comparison

28 October 2026. Independent boundary companion by `producer-workspace/review_repeated_service_factorization`. This does not amend the received CP-domination source; it violates that source's explicit discarded-gauge interface and explains why the restriction is necessary.

The first source emits a logical qubit L and a gauge qubit G initially |0>. Its exact logical extraction traces G. Consider an extended receiver which delivers L perfectly but flips G by X and returns G to future source access instead of discarding it. For every initial gauge density, its reduced logical channel is identity. Hence its complete logical Bell effect is **T0=I and b=0**. With L initially half of a Bell pair, the entire first logical/reference output is unchanged.

On the next call, the same comparison source law reads the returned gauge and applies the TP Pauli-memory instrument

`E(rho_L2,G) = (I_L2 tensor P0_G) rho (I_L2 tensor P0_G)`

`             +(X_L2 tensor P1_G) rho (X_L2 tensor P1_G)`.

This is in the complete Pauli/source-memory form, with two CP memory maps and no reset assumption. The second logical decoder is exact. The true first extraction with its unchanged retained-gauge extension returns |0> to this instrument, whereas the altered extended receiver returns |1>. A second input |0> therefore emerges as |0> in the benchmark and |1> in the altered process. After tracing final source memory, the accessible states are respectively

`Bell_(reference,L1) tensor |0><0|_L2` and
`Bell_(reference,L1) tensor |1><1|_L2`.

Their half trace distance is exactly **one**, despite the first reduced logical certificate b=0 and an exact second decoder. The issue is not key leakage, current logical error or an inaccessible error label: it is the unauthorized replacement of a traced gauge contraction by an arbitrary retained state-update instrument.

The exact check verifies T0=I from rectangular receiver Kraus operators, TP of the second source instrument, preservation of the first Bell pair, and final eigenvalues +1,-1,0,...,0 for the state difference. No hardware, source observations or random draws occur. The governing source remains unchanged and its accepted discarded-gauge theorem is not contradicted.
