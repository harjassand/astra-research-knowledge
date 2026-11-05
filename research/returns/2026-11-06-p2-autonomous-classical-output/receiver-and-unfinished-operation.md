# A conditional classical receiver and the unconstructed quantum-history block

[Return guide](README.md) · [Source/timing proof](joint-exposure-and-waiting.md) · [Complete native return](P2_AUTONOMOUS_CLASSICAL_OUTPUT_20261106_RETURN.txt)

## A physical local terminal primitive

Suppose an adjacent source bit `C` already holds the correctly measured result. A time-independent local rate-`gamma` channel dephases `C` in its classical basis and overwrites receiver bit `P`, preserving `C`. After the intended measurement this preserves the corresponding conditional reference state. Both registers still receive actual physical bursts.

Let `q_P` be the actual port-hitting rate, including marks also hitting the source. If failure of the protected source over settling time `Delta` is separately bounded by `eta_C`, the supplied proof gives

```
P(receiver wrong at interval end)
 <= eta_C + q_P/(gamma+q_P)
    + gamma/(gamma+q_P) exp(-(gamma+q_P)Delta).
```

The last event among copying and port hits is a sufficient witness; source failure is union-bounded rather than conditioning future port geometry on source success. The bill is one receiver register per bit, one bounded-range copy channel, constant wiring, settling time, occupied retention register-time and an `O(lambda)` raw floor at fixed rate.

This constructs neither the protected source nor the completion detector or long-lived retention medium. Those obligations cannot be hidden inside `eta_C` when claiming the whole processor. The terminal bound is not itself the uniform full-operation readout/retention theorem.

## What a service certificate would need to supply

A certified local service word of length `ell`, minimum attempt rate `gamma_min`, bounded interference rate `Gamma_sum`, and subinterval size `delta` would have success probability at least `(gamma_min delta)^ell exp(-Gamma_sum ell delta)`. Repeated valid trials give exponential service tails, with actual clean-trial exposure charged.

Two premises remain open: the word must certify the actual quantum operation history, and its time-versus-block-size scaling must pay the large-source exposure bill. A consistent repaired clock can still accompany repeated or omitted noncommuting gates. Finite-state reachability or eventual completion alone is insufficient.

The recursively usable block remains unconstructed. It must jointly provide correct once-only causal protected gates, controller/syndrome recovery without discarding unknown logical information, protected command/acknowledgement interfaces, physical completion and waiting tails, actual-source joint witnesses, and final protected measurement/completion/classical retention and receiving.

## Strong machinery keeps its own limits

The source credits Dunnweber–Styliaris–Trivedi's finite-neighborhood repair, buffering, brickwork updates and continuous-time jump outline. It identifies the unclosed quantum-history and joint source/timing implication rather than refuting that machinery with a simpler deadlock example.

The CSS/Pauli classical-process and Floquet result does not by itself give a time-independent universal processor under arbitrary CPTP bursts. If an actual logical qubit channel is Pauli, the imported sector estimates imply half-diamond error `1-p_I<=q_X+q_Z`, including reference and subsequent measurement. A corrupted Pauli-frame register is not an ideal twirling key, and no reduction from general bursts is constructed here.

Reliable autonomous classical computation and asynchronous multiparty quantum protocols also retain their real access/noise assumptions. Classical histories do not operate directly on an unknown quantum payload; static network corruption thresholds do not provide local processors, accumulating-fault repair or bounded physical delivery time for this source.

No full runtime, hardware or all-installed-register-time upper bound is earned. Unknown compact input acquisition/raw floor, known noisy startup, wiring, resets, recovery, protected computation, measurement, completion and retention remain charged obligations. No matching upper bound, demonstrated avoidance of the previous quantum timing cost or physical advantage is claimed. The native proof and reported 476 formula checks are preserved; original standalone files remain pending transfer, without a new scientific audit or replay.
