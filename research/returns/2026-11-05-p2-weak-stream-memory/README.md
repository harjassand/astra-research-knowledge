# Causal memory for the homogeneous weak partial-SWAP stream

The supplied work derives a general finite-error prefix memory converse for this fixed physical source and exact limits for several proposed compressions. **It does not construct the requested high-fidelity sublinear-memory receiver or establish a matching general impossibility theorem.** Its large-prefix spectral estimate and optimal joint memory/processing law remain unresolved.

Read the complete [PDF](package/weak_stream_memory.pdf), [TeX proof/report](package/weak_stream_memory.tex) and [package guide](package/README.txt). The original [ZIP](original/weak_stream_memory_research_package.zip), [captured return](P2_WEAK_STREAM_MEMORY_20261105_RETURN.txt) and [source metadata/hashes](SOURCES.json) retain the supplied proof, programs, numerical receipts and unsuccessful policies.

| Result or construction | Direct route |
|---|---|
| General causal instruments, spectral profile, variable memory and qubit-time | [Prefix converse and the missing estimate](prefix-spectral-bound.md) |
| Measured-spin, consecutive-pair, purified-block and one-qubit limits | [Exact restricted receiver boundaries](restricted-receivers.md) |
| Folded two-qubit expression, physical causality and classical failure flags | [Virtual statistic and physical completion limits](virtual-statistics.md) |
| Growing-spin instruments, exact final decoder and full physical bill | [Executed candidates and costs](physical-instruments-and-costs.md) |

## Fixed source and accepted acquisition benchmark

One arbitrary input qubit, potentially entangled with an arbitrary reference, meets fresh independent tracial carriers through the same known unitary `U=cos(theta) I+i sin(theta) SWAP`. Each carrier encounters the source once; no preparation key, carrier purifier, return link or altered emitter program is available. The source is eventually discarded. All errors use **half diamond norm**. Every coherent register crossing a physical cut counts, including initialized workspace, waiting carriers and coherent flags; classical records may be unlimited.

Writing `r=1-sin(theta)^4`, the accepted all-output inverse-dummy/Petz decoder has error `3r^N/4` and retains N emitted qubits. Its sufficient collision count is

```text
N_all(theta,epsilon)=ceil(log(3/(4epsilon)) / [-log(1-sin(theta)^4)]).
```

The preserved arbitrary-decoder converse is `epsilon_opt >= 3[1-sqrt(1-r^N)]/4`. At `theta=.1`, ideal error `.01`, the source reports 43,462 sufficient and 36,552 necessary collisions, with ideal decoder error `.0099996156811` at the sufficient point. Source-state forgetting on the faster `cos(theta)^(2N)` scale is distinct from acquisition by the accessible emitted outputs.

The existing operation already uses O(N) logical inverse interactions **before routing**. Its quadratic gate count in the specified fixed-junction nearest-neighbour layout is not a general processing lower bound. The missing capability is causal high-fidelity acquisition with substantially less coherent storage and a jointly controlled angle/error/time/control bill.

## What is earned and what remains

The [general prefix theorem](prefix-spectral-bound.md) covers arbitrary permitted causal instruments with classical feedback and initialized workspace, rather than just one update ansatz. It converts successful recovery into a low-energy, dimension-capped Choi witness for the actual scattering channel. Without the required spectral profile it does not yield a linear-memory theorem, a one-percent memory conclusion at `.1`, or an efficient compression criterion.

The [restricted exclusions](restricted-receivers.md) identify actual information loss in attractive Schur and block proposals. They leave coherent multiplicities, retained outcomes and more general instruments at their stated scopes. A compact tensor formula is separately shown [insufficient as a physical causal state](virtual-statistics.md). The [growing-spin candidates and exact final readout](physical-instruments-and-costs.md) are specified operations, but their tested policies fail to acquire the desired payload fidelity. Individual trajectory diagnostics are not ensemble performance guarantees.

Efficient Schur/CG circuits, coherent gathering for suitable pure state families, permutation-symmetric mixed-i.i.d. compression, integrable transfer matrices and prior homogenization/correctability work are credited in the report. Their assumptions do not automatically supply a sufficient statistic for this ordered correlated mixed stream. Transfer eigenvalues/Jordan structure are not the singular-value profile needed here. No foundational novelty or useful physical endpoint is inferred from the representation change.

The earlier [causal payload-memory theorem and three companions](../2026-11-05-p2-causal-payload-memory/README.md) and [tracial acquisition package](../2026-11-05-p2-tracial-acquisition/README.md) remain unchanged, including both complete nested ZIPs in `package/warm/`. The programmed short-record emitter remains distinct from this homogeneous weak source. No scientific code, solver, PDF compiler, new audit or large corpus build was run for publication. Generated current retrieval is unchanged; the complete package and these scoped entries are directly public on GitHub.
