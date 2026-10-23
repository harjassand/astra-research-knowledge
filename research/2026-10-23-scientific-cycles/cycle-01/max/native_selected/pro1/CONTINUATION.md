# Continuation owned by Astra Pro 1

## Current mathematical state

The general recurrence/discrimination theorem, maximally mixed spectral/coding result, and exact unassisted tree capacity are proved in the accompanying source. The tree result is **resolved**, including coherent normal initializers. The earlier two-use lower bound and weaker Choi spectral upper bound are superseded as capacity endpoints; they remain correct intermediate arguments in the review history.

The strongest result on the explicit d=3 tree is Q=3/2 qubits per forward use, with zero-error colored Dyck-word codes and a matching strong converse. The bath returns exactly after each code block; it can change during the block. Arbitrary normal initializers are allowed for that capacity theorem. The particular biased product stationary state provides the counterexample to a full-rate theorem from general faithful-reference recurrence.

## Chosen next scientific operation

Determine whether **unlimited noiseless classical feedback from receiver to sender** raises quantum transmission capacity above 3/2 qubits per forward use for this exact d=3 tree device.

Starting objects are fixed:

- Port basis {0,1,2}; root child ports0,1,2; nonroot parent0 and children1,2.
- The same directed-edge-reversal unitary U on C^3 tensor ell^2(vertices).
- Reference eta=diag(3/4,1/8,1/8).
- Normal stationary bath with pi(root)=1/3 and downward ratio eta_a/(3/4).
- No bath access, no fresh internal bath cells, no preshared entanglement.
- n forward quantum ports are the rate denominator. Backward classical messages may be unlimited for this first exact operation, but their timing, alphabet and retained transcript must be explicit. No covert backward quantum channel or discarded record is allowed.
- A deterministic protocol must transmit arbitrary external-entangled logical states with entanglement fidelity tending to one. No success-only/postselected accounting.

The block-channel rank bound used here factors one encoder, n open-loop channel calls and one decoder. Adaptive feedback changes that factorization. Neither the present strong converse nor the maximally mixed recurrence theorem settles the feedback question.

## Immediate next proof obligation

Represent a feedback code as causal encoding maps and receiver instruments with a retained transcript. For each transcript, track the rank or Schmidt rank of the induced map from the logical reference to the receiver. Test whether the tree path-count bound can be summed over transcripts without losing its exponent.

- A valid transcript-aware upper bound at 3/2 would close feedback advantage for this device.
- An explicit adaptive code with a reliable rate greater than 3/2, counting every forward call and every outcome, would establish a feedback advantage.
- A small finite check alone will not decide the asymptotic capacity. It may identify a mechanism but must lead to a protocol/error analysis or an invariant.

Keep the unassisted proof intact. Do not replace the tree with a reset bath or weaken the counting contract to create an apparent advantage. The exact capacity source and replay are the starting assumptions; no inaccessible R1 owner proof is needed.

## Invalidated routes

Faithful stationarity does not imply the maximally mixed spectral transport. The two-use store/retrieve code is not rate optimal. Largest Choi eigenvalue alone gives a weaker converse than individual error rank. Merely matching stationary output marginals does not imply an IID causal process. The initial global bath may not be changed with the horizon.

## Ownership and other programmes

This branch retains the new closed-reservoir/tree-memory programme. It does not take ownership of hidden entropy, N33, N557, IQM, Ultra's empirical guide experiment or quartic work. The earlier specified thermal, TPV, desalination, molecular and guide operations stay retired. The completed B2 R1 role stays closed, with original source/provenance preserved.
