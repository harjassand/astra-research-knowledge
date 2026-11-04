# Restricted no-go for a single tracial partial-SWAP receiver

This [complete companion proof](package/companions/scalar_receiver/scalar_receiver_no_go.txt) excludes one natural constant-memory receiver architecture. It does **not** settle the general causal-memory problem for the homogeneous mixed collision stream, and it is distinct from the [late-record memory theorem](README.md).

The source qubit has arbitrary input/reference; receiver M starts in `I/2`. Every round introduces independent `E_j=I/2`, applies source/fresh-ancilla partial SWAP of fixed `0<theta<pi/2`, then receiver/fresh-ancilla partial SWAP of arbitrary predetermined angle `phi_j`, and discards E. No output returns to the source; the source is discarded at the end. Input-independent random angle schedules with a retained seed and arbitrary final CPTP decoding are included. Intermediate measurements, measurement feedback, non-SWAP controls, pure auxiliary memories, block compression and larger quantum memories are excluded.

For `c=cos(theta)`, `s=sin(theta)`, the exact source-Z deviation stays in the span of `Z_S I_M`, `I_S Z_M`, and `X_S Y_M-Y_S X_M`. The supplied three-variable recurrence gives source visibility `A_j=c^(2j)`, a uniform correlation envelope and final depolarizing receiver visibility B_N. For every number of rounds and every permitted angle sequence,

```text
|B_N|<=min(1,L(theta)),
L(theta)^2=s^2/(1+c^2)+32s^4/(3-c)^2.
```

An arbitrary final decoder's Bell fidelity is at most `(1+3|B_N|)/4`, hence its **half diamond** error is at least `(3/4)max(0,1-L(theta))`. At `theta=.1`, `L=.0761514353682639` and error is at least `.6928864234738021`, even with unlimited rounds. As weak action tends to zero, this lower floor tends to `3/4`. It is not a bound for a general finite-memory instrument.

The [original check](package/companions/scalar_receiver/verify_scalar_receiver.py) compares the recurrence with direct three-qubit matrices; [recorded output](package/companions/scalar_receiver/scalar_receiver_verification.json) is finite floating-point evidence, not a new Capital execution. The late-selector audit also preserved in this directory reviews the main late-record theorem; it is not assigned as an independent audit of this restricted scalar recurrence.

If a physical whole induced channel is within half diamond delta of an allowed ideal receiver, the error floor decreases by at most delta. This stability statement does not supply a calibration/fault-tolerance protocol. The rejected reader has constant retained qubits and linear gate count but fails the target acquisition. The [earlier all-output tracial decoder](../2026-11-05-p2-tracial-acquisition/partial-swap-decoder.md) and unresolved more general low-memory receiver retain their scopes. No comprehensive novelty finding or physical experiment is claimed. [Original package and hashes](SOURCES.json).
