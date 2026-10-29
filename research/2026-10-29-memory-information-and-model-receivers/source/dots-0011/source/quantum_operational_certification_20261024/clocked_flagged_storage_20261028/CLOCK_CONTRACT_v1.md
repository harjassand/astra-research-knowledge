# Clocked physical-memory comparison: construction contract v1

28 October2026. Work in progress; no result or acceptance claimed. Earlier ideal-idle scientific sources remain unchanged.

The next calculation charges equal elapsed time, not merely equal native channel-call count. A reference time unit is chosen arbitrarily. Parameters d1,d2,dp,dm,df specify local gate, two-qubit gate, preparation, measurement/reset-interface and classical readout/feedback durations. Illustrative dimensionless ratios are not hardware measurements. Source/native and learned-inverse durations are specified separately.

Each round uses a synchronous schedule: four flagged windows, four fresh-syndrome windows and five correction-site windows. A disabled adaptive window physically waits; it is NOT the zero-duration bypass used only for the earlier perturbative unrolling. Every data qubit continues to experience the background-memory channel during disabled windows. This changes the noisy operation and requires its own evaluation.

Native channel per source use remains the fixed earlier stationary non-Pauli source with its acquired inverse. An additional memory/background channel is independently declared per unit time; it is not inferred from the native per-use noise. To avoid giving active gates artificial immunity, the discrete interval model applies the declared memory channel to ALL live qubits over each interval, including active gate supports. Ideal gate plus systematic overrotation occurs at a specified interval endpoint; the background channel occurs in a specified order. This is an explicit stroboscopic CPTP model, not an assertion that gate Hamiltonians commute with a continuous Lindblad process.

Ancillas become live after preparation and are discarded after measurement. Their background noise acts while live, including during data gates and feedback waits. Data always remains live. Measurement intervals must specify whether noise precedes the measurement; preparation intervals must specify how a fresh state is reset. Undefined multi-fault flag syndromes use the already declared ordinary weight-one fallback.

The unencoded comparison applies the same native source and fixed learned inverse, then remains exposed to the SAME elapsed EC window duration and same data-background channel, without receiving protective EC. A stronger baseline with equally informed optimized control or another standard code is not automatically beaten. Initial injection, terminal readout and controller reliability remain separately declared interfaces.

The intended sweep uses dimensionless integrated background strengths and duration ratios. It will report regimes where protection survives and where it fails, not pick invented hardware numbers or relabel earlier native-call comparisons as lifetime advantages.
