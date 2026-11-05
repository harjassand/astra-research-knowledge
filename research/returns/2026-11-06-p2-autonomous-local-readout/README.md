# Autonomous quantum readout: a necessary cost of removing the tick

P2's completed return proves a resource converse for bounded-strength, time-independent local Lindblad dynamics delivering an unknown quantum input through a fixed compact port at a predetermined late physical time. At any fixed positive allowed burst intensity, fixed nontrivial reference-inclusive accuracy requires `N=Omega(T)` installed registers and `U_all=Omega(T^2)` register time.

The [complete supplied return, actual prompt and visible activity](P2_AUTONOMOUS_LOCAL_READOUT_20261106_RETURN.txt) are published byte-for-byte. The [original ZIP](original/autonomous_local_readout_package.zip) arrived locally through the existing transfer during intake. All nine members are published, including the [full report](package/autonomous_local_readout_bound.pdf), [editable proof](package/autonomous_local_readout_bound.tex), [retained failures and scope](package/retained_failures_and_scope.txt), [diagnostic code](package/check_readout_bound.py), [recorded results](package/finite_checks.json) and both predecessor files. All eight supplied member checksums match. See the [package guide](package/README.txt), [manifest](package/MANIFEST.json) and [source metadata](SOURCES.json). The capture's historical pending-transfer header is preserved; the source report is dated 5 November and this intake is dated 6 November, Brisbane.

## Precise operating contract

The finite device can depend on the horizon. Local dimension, density, interaction range/strength and incident-term multiplicity are bounded independently of `T`. Its ideal generator is a sum of at most `m_0 N` bounded-support local Lindblad generators. Coherent Hamiltonian dynamics, dissipative control and corrupted clocks are included. All mutable timing, program, syndrome, buffer and I/O records count; no input-bearing environment or noiseless output store is free.

At a deterministic public time `t_*>=T`, a fixed compact port must yield half-diamond error `delta<1/2` from identity on an unknown qubit. The decoder may be selected per horizon and is granted ideal local readout. The accepted `delta=1/4` target requires Bell fidelity at least `3/4`. Perfect initial preparation and arbitrary encoding are granted by the converse, so it does not impose the stronger arbitrary-junk startup contract. A prescribed one-qubit unitary reduces to identity via the mathematical decoder.

| Resource or contract | Accepted synchronous processor | New continuous-time converse |
|---|---|---|
| Installed registers | `T^(1/r+o(1))`, attained for `r=alpha-d>1` | `Omega(T)` at fixed positive intensity |
| All-installed-register time | `T^(1+1/r+o(1))`, attained | `Omega(T^2)` |
| Output | Fixed compact raw port at declared public time | Same local fixed-time requirement |
| Startup | Paid noisy known-controller initialization | Same permitted; stronger preparation granted in proof |
| Status | Constructive theorem with matching exponents | Converse; matching upper bound remains open |

Read the [availability and timing proof](availability-and-timing-proof.md) and [scope, comparators and open construction](interfaces-comparators-and-open-construction.md). The [accepted sparse processor](../2026-11-05-p2-sparse-autonomous-processor/README.md) and its complete [proof record](../2026-11-05-p2-sparse-autonomous-processor/package/report.txt)/[reusable predecessor](../2026-11-05-p2-sparse-autonomous-processor/package/accepted_reusable_report.tex) remain unchanged.

This converse identifies the cost of a particular output/timing contract. It does not prove clock repair impossible or construct a processor. Random completion-event delivery changes the interface and requires its own receiving and resource theorem. The separate arbitrary-junk restart law remains distinct; the separate continuous-time quantum gate-order/protected-idle construction remains open. Earlier Gibbs results are unchanged.

The producer reports 184 finite diagnostic cases plus the Bell-witness identity, all passing, with maximum generator residual about `4.39e-14`. These are algebra and normalization checks, not a processor simulation, threshold measurement or substitute for the proof. The source explicitly makes no independent-review or literature-priority claim. Capital did not add an audit or run scientific code.
