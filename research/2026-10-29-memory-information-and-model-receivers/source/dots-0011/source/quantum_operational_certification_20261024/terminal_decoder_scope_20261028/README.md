# Actual terminal decoding versus ideal recovery

New author derivations and diagnostics, 28 October 2026. Review is pending unless a separate receipt says otherwise.

The former metric's ideal terminal map includes full syndrome recovery, not an arbitrary inverse Clifford encoder. It is an actual syndrome-decoding unitary target or measurement/correction/decoding operation and must be physically implemented to claim that output. All256 ideal bare Clifford/discard extensions of the five-qubit encoder are enumerated and evaluated on six actual terminal states. These are source-informed, ideal-endpoint diagnostics, not an acquired/noisy decoder study.

An exact general [[n,1,d]] bound shows that bare Clifford decode/discard under independent depolarizing noise has first-order infidelity coefficient at least d. Thus choosing a clever extension cannot replace syndrome correction's distance-dependent cancellation. The five-code minimum coefficient is3, attained by70 extensions. Exact exhaustive Pauli checks are saved.

A separate whole-pipeline certificate states how physical six-state tests, with explicit calibrated preparation/readout error allowances, certify the actual noisy input-to-output operation without process/environment reconstruction. It does not remove the tester assumptions; a dephasing false-pass example shows why they matter. No new sampled data were generated in this folder.

Nothing supersedes the existing correctly labelled ideal-decoder numerical calculations. The new noisy_code_boundaries_20261028 and continuous_inverse_control_20261028 implementations address the physical operation separately. AUTHOR_MANIFEST_v1.json binds governing sources and programs before review.
