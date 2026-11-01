# Workspace-replacement recovery

At about 01:14 UTC on 2026-11-01 the execution workspace was replaced by an older
snapshot. The pending detour source and audit directory disappeared. Before loss,
the auditor had verified all166 old inputs, reproduced ten outputs, and matched
the main receipt and50-node DAG; its independent test suite had NOT run and no
whole PASS was issued. The old source manifest was
c6061f534160e1209c18462ddf8d303225b3b6edf3aca4a70f0dd837d29890d2.
That hash does NOT label reconstructed source bytes.

The accepted aggregate142-member package was recovered exactly by root from its
already delivered durable copy (original ZIP SHA9574065a465f3dca25f9a4c26c9207f4be974783931e94987d15100c3074b366).
It is copied byte-identically under frozen_aggregate/. New code and proof were
reconstructed from the warm transcript, and have fresh hashes. Essential formulas
and functions are all recovered; old component-test script bodies not fully in
context are replaced by explicitly new exact tests. No old timing evidence is
invented or rebound. The new main canonical receipt and executable DAG are checked
against their historical exact hashes; this is output equality, not old source
identity or independent theorem acceptance. A new full preflight and whole audit
are required. Pending checkpoint archives must be labeled PENDING.
