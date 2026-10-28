# Completed finite-memory operating-contract construction

The general all-d frame proof passes my substantive mathematical challenge
at the whole-read snapshot scope:
[FRAME_REVIEW.md](FRAME_REVIEW.md), snapshot SHA256
10766c4a551ac37ebc9405f4a260dfecadc1070618a11dfdb91a5795ca471ca5.
This does not audit the separately replayed576-column kernel or confer
physical acquisition.

The new construction turns the missing multi-time interface into a
quantified operating decision, with a positive contract and a matching
obstruction. Derivations: [PROOF.md](PROOF.md).

## Decisive result

A homogeneous **five-state classical environment** draws fresh Pauli errors
until an unknown hazard p makes it hold and repeat one Pauli forever.
Its isolated single-use channel is exactly Phi_c at every deterministic
time, with past observations averaged. Nevertheless, after entering the
held mode every two-call echo cancels the noise.

For **any** adaptive calibration with expected T noise calls under the fresh
model, the complete-record TV distance to this alternative is at most pT.
For every p>0 a sufficiently long echo program has distance arbitrarily
near1 from fresh noise. Thus finite known dimension, homogeneity, and reset
at the start do not suffice for a finite expected-cost, uniformly sound and
complete all-depth finite-shot qualifier.

This strengthens the completed averaged-channel counterexamples to arbitrary
bounded-cost calibration protocols. It does not contradict finite exact-data
realization theory.

## Constructed positive operation

Under the **specified five-state family**, trusted environment reset, and
trusted controls/readout, an echo screen can issue a certificate for every
future adaptive program using at most H local noise calls:

    joint output TV from fresh reference <=delta,
    probability of falsely qualifying an unsafe hazard <=alpha.

It costs O((H/delta)log(1/alpha)) calls. A coupling argument gives the
necessary lower bound (1-2alpha)H/(8delta), under the stated H,delta range.
The dependence on operating duration/error is therefore substantive.

Computed plans, c=7/4:

| Future budget | TV budget | Confidence error | Calibration noise calls |
|---|---:|---:|---:|
| H=100 | .1 | .01 | 7,028 |
| H=1,000,000 | .01 | .001 | 1,000,000,040 |

Costs include K preparations and identity updates, 2K noise calls, only the
last m destructive Z readouts, and trusted environment resets before
calibration and future operation. No gate-time, energy, reset fidelity, or
spatial model was physically acquired. One-qubit testing transfers to a
wider processor only under the stated addressing/noise-family promise.

With the extra model gap p=0 or p>=p_min, the same test classifies the exact
fresh process for **all finite future depths** at cost
O(log(1/alpha)/p_min). For p_min=1/32, alpha=.001, the plan needs360 calls;
its finite hidden-state law was exactly replayed. This is a statistical
type-I/type-II guarantee, not a posterior probability after acceptance.
Finite memory and digital control descriptions do not supply p_min.

## General finite contract and ordinary comparator

For known memory Hilbert dimension D, system dimension h, stationary
intervention dynamics and fixed reset state, exact IC word probabilities
through length(hD)^2+h^2-1 imply equality at all lengths. This is the
established bilinear/quantum-machine equivalence principle.

Adding an explicit common-denominator bound Q for actual rational
transition/initial data turns that exact-data fact into a finite-shot
confidence contract via a nonzero probability gap and Hoeffding. The full
experimental cost is charged. Even the qubit memoryless Q=Q0=2 sufficient
plan requires over10^20 resets; the D=2,Q=Q0=20 plan has a130-digit reset
count. Neither the height bound nor these measurements was acquired.

Ordinary process-tensor tomography provides IC multi-time probes;
conditional Markov-order reconstruction and memory-strength error bounds
are stronger relevant incumbents. They were personally read selectively.
The short three-branch witness is an ordinary process-tensor measurement.
An equally informed persistent-fault screen has the same O(1/p_min)
hazard scaling as the echo test; no generic tomography speed advantage
is claimed.

## Executed evidence and actual limits

[contract.py](contract.py) uses only stdlib Fraction arithmetic.
[RESULTS.json](RESULTS.json) records the exact Pauli-memory process,
known-matrix reachable-span checks, IC witness probabilities, contract
plans, and sample-cost bounds. The p=0 direct-sum model has rank4; p=1/7
has rank24 with a three-letter differing word. The explicit Z-word
probabilities are3/25 versus9/100. The run took approximately0.10seconds.

Failed candidate preserved: replacing exact finite-word equality with
finite-shot tolerance under finite dimension alone does **not** provide an
all-depth guarantee. The continuously small hazard defeats it.

The next hard physical question is whether a platform supplies a defensible
reset/model/separation or finite-runtime contract at an acquisition cost that
beats an equally informed process-tensor/control workflow. This work does
not supply those facts. Physical acquisition, generic practical advantage,
and a new tractability class remain NOT_ACHIEVED. New operational
derivations await independent review.
