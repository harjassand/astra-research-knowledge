# Deterministic host fixture receipt

The prior fixture and helper remain unchanged. The theorem `actual_hierarchical_host_filling_v2.md` remains unchanged (SHA256 `3ac1009ce21d0c9d7c4eba1266d46821858c8e10f5a0e036b2f8cb062e50af14`).

The old RX constructor iterated sets of cellular edges, boundary vertices and boundary edges while assigning matrix indices. Different Python hash seeds therefore changed labels and the otherwise deterministic descendant matching/incident-pair choices. This changes quotient degree statistics, not the proved bounded-load or connectivity invariants.

New entry point: `python actual_host_quotient_deterministic_test.py`.
New helper: `helpers/actual_generic_rx_deterministic.py`, with canonical `repr` sorting of those cell sets. The fixture also sorts graph traversals. This only changes enumerations, not incidences, geometry, or assertions.

All assertions pass. Runs with `PYTHONHASHSEED=0,1,42,random` have byte-identical stdout. A standalone clean copy in `/tmp`, launched from outside its directory with seed 98765, also has identical stdout. Only the fixture and its three local standard-library helper modules were copied.

Canonical results: 2895 host vertices; maximum host degree 85; ancestry children 2–66; matching fibre 2; 1428 real check vertices; 1336 real qubit vertices; maximum check degree 58; maximum completed qubit degree 273; check and qubit projection fibres both 5. Every nonexpansion/fixed-vertex/support-connectivity/completion assertion passes. No second-level physical-nearness geometry is asserted.

SHA256:
- fixture: `e1c50488e2ec3fe1a6c9a185252e2b48488c555ba31b0d690e653acc9623bb3f`
- deterministic RX helper: `1bad8fa3832c0992a165db58aad9c2de1cb27e254e166e097400e93d1f42ad27`
- result JSON: `77e2b9d664106648d56867dfe492074c07cf36c2bbdaa666ab08b27b054c158e`
- stdout (JSON plus terminal newline): `c125084a60484790fb5b8064c3ffc8268adaa808d616056fe88fe23fa2793b25`
