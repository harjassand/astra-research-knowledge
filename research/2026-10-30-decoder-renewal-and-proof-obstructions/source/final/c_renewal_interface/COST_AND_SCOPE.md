# Actual costs and explicit excluded resources

The sole new execution was `python3 compile_recurrence.py`. It used
stdlib integer/Fraction arithmetic and completed the declared tensor
checks in 0.011977916990872473 seconds after imports. Its saved output is
`RECURRENCE.json`; the complete generated tensor has 752 nonzero
entries (the authoritative count and digest are in that receipt).
No source, quantum circuit, native device, trajectory, Haar sample,
randomness, parameter grid, optimizer, new model or statistical
acquisition was run. No peer or previous frozen file was changed.

The executable checks are universal coefficient identities for the
canonical qubit specialization and an all-r equality-class contraction.
They do not establish the arbitrary-isometry norm theorem by finite
testing. That theorem is derived in PROOF Sections 1-4, with the accepted
complete one-query theorem as an explicit dependency. Root independently
whole-read/accepted C's proof at its declared scope; C separately
whole-read/accepted root's all-k extension. Those analytic reviews are
distinct from this execution and its hashes.

Native controller resources, if the circuit is supplied, are:

* One independent initial source call and m further online forward calls,
  with the encoded target protected throughout. The original payload
  encoding is an additional call if counted in the full service.
* Two full D-level carriers retained between cells; a third may exist
  transiently if the new call precedes the old-carrier discard. That
  discard commutes with the fresh call, so it can occur first, at the
  same resulting channel, to avoid the transient third output.
* Arbitrary known memory and every R history retained. In the scalar
  canonical realization this is m+1 known reference qubits, plus clean
  control/synthesis workspaces. The broader obstruction grants unbounded
  known memory and an arbitrary final known CPTP map, so no efficient
  final decoder is assumed as a free resource in a positive algorithm.
* Each canonical cell uses known whole-register SWAP-sector computation
  and uncomputation, costing O(log D) controlled elementary register
  swaps, and fixed-size known Pauli/amplitude gates. Finite angle/control
  synthesis errors must be allocated over all m cells; they are not
  noisy-hardware thresholds. Arbitrary V_+/- can have much larger known
  gate cost, which the obstruction already allows.
* Source cycle duration, protected-storage time, resets, source
  memorylessness, exact flat junk, known gate errors and physical
  preparation are NOT acquired. Forward-query counts are not physical
  time or work estimates.

The m-cell theorem has fixed m. It permits coherent record-dependent
memory processing inside those cells. It does not assert a variable-
stopping-time expected-cost lower bound for every recycling schedule.
Root's separate exact Las Vegas theorem has a different, broader exact
instrument scope and does state an expected cost.

The numerical coefficient in the result is not tuned or tested on
another rank. At fixed target epsilon<3/4, the obstruction is quadratic
in r. No comparison of precision exponents, running time or hardware
advantage against the complete ordinary RDS/HME implementations is made.
