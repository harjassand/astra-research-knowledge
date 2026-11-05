# Arbitrary-junk restart and a causally requested quantum handoff

[Return guide](README.md) · [Full proofs, sections 8–10](package/report.txt) · [Accepted reusable construction](package/accepted_reusable_report.tex)

## Initialization contracts have different costs

The prepared sparse processor pays for noisy known controller words over a horizon-dependent prescribed region. The restart theorem instead demands that the same fixed prescribed seed work from **every** outside mutable state independent of the fresh input. Those are different contracts; the lower bound does not invalidate paid commissioning or prepared reuse.

For a time-homogeneous device of Hilbert-space dimension `D`, delay `T`, error `delta<1/2`, and an allowed independent seed-replacement event of probability `q` in each compatible slot, the report derives

```
log2 D >= q T [1-h2(delta)].
```

Independent fresh bits injected through allowed seed replacement must each remain decodable after `T` ticks. The device at a common checkpoint is then a quantum random-access encoding. Individual future decoders, Fano's inequality, the entropy chain rule and the dimension bound yield the result. The event flags belong only to the mathematical decoder; no reliable physical flags or simultaneous recovery are supplied. The report credits Nayak's established random-access machinery; the restart reduction is the new derivation.

Pareto marks replacing a prescribed seed of radius `s` give `N s^r>=c lambda T`. Fixed `s` therefore forces `N=Omega(T)`, while prepared sparse reuse has `N=T^(1/r+o(1))=o(T)` for `r>1`. The prescribed region, access and allowed reset-compatible slots matter. Arbitrary continuous-time dynamics need a separate compatibility argument.

For bounded-range bursts, prepared reuse uses polylogarithmic hardware and `T polylog T` register time. Arbitrary-junk restart has lower bounds `Omega(T)` hardware and `Omega(T^2)` register time; the accepted one-pass construction matches those polynomial exponents up to polylogarithms. The exact arbitrary-junk optimum for the full Pareto law remains unresolved. A typical initial distribution, growing seed, paid commissioning or persistent external input changes the contract.

## One internally requested quantum transfer

Two adjacent protected processors can select one handoff through constant-width raw ports. The receiver's protected causal computation selects a request frame. Every request, vote, phase, admission and control record remains corruptible and protected. A frame uses an odd number `M` of complete request samples; actions occur only at frame end, with mid-frame requests queued.

Disjoint physical source-time windows give independent geometric sample-failure indicators, even though corrupted values can be correlated. Without conditioning on global future bulk success, the wrong-decision event on good bulk is contained in a majority of sample failures. Across `J` frames its probability is at most `J exp(-c_q M)`, so `M=O(log(J/epsilon))` suffices.

The chosen frame end must be a stopping time for the actual Poisson-source filtration. Causal fault mechanisms and requests supply this premise. Future-aware fault values steering the request require an additional ideal-request coupling; that case is not claimed. The entire quantum interface begins after the selected stopping time, with future bulk failure charged separately.

The protected state remains stored through null frames. Only the chosen transaction performs actual descent, raw transfer and ascent: `D_A -> I_A -> I_B -> D_B`. Normalization and disabled guards isolate earlier arbitrary I/O histories. A fixed public final deadline can provide observable delivery. Latency is `O(MP)` and private counters use `O(log M)` logical bits. Only a fixed finite number of raw handoffs is covered; indefinitely repeated raw exchanges would accumulate error.

## Rejected route and recovery provenance

A naive mod-3 marching-soldiers asynchronous conversion admits a frozen cyclic phase pattern after a bounded burst. This is an obstruction to that conversion, with Gacs credited for the cyclic inconsistency; it is not an impossibility theorem for all asynchronous correction.

The [supplied recovery capture](P2_INTERRUPTED_RECOVERY_9952_20261105_RETURN.txt) records the issued assignment, human continuations, interrupted activity and available completed response. It is archived source data. Its final visible native text ends during the handoff discussion; the original report supplies the full statement. Capital used the forwarded capture and existing local ZIP, without reopening the producer chat or retrying attachment acquisition. No researcher message or replacement chat was created by this intake.
