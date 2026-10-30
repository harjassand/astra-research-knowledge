# A randomized native entangler under arbitrary locally bounded bath motion

**The stated approximate randomized task has a positive solution.** A
ten-segment weak loop, with two fresh private signs per repetition,
implements the required entangler with uniform diamond error tending to
zero. Its sufficient duration is `O(epsilon^-2)` and its native segment
count is `O(epsilon^-3)`. The constants obtained here are large. This is a
mathematical construction for the granted known-axis interface, not a claim
of practical hardware or of the complete original P2 model.

The central estimate is a bound on the **averaged quantum channel**, retaining
arbitrary data-memory-reference correlations. It does not average
Hamiltonians or identify an average unitary with a channel.

## The actual construction

For each cycle draw independent fair signs `s_A,s_B`, put `s_C=s_A s_B`, and
apply the following chronological pulses, each for duration `d`:

```
-s_B B, -s_C C, +s_B B, +s_C C, -s_A A,
-s_C C, -s_B B, +s_C C, +s_B B, +s_A A.
```

Only one native handle is active at unit magnitude. Draw fresh signs for
each cycle. All pulse durations and all switching times are independent of
the signs. There is no memory preparation, measurement, reversal, extra
ancilla, logical pulse or positive-force interface.

For `N` repetitions choose

\[
d=\left(\frac{\pi}{16N}\right)^{1/3}.
\]

Writing `E=exp(-i pi Z_1X_2/4)`, the construction obeys

\[
\left\|\overline{\mathcal C}_{DM\to D}
-\operatorname{Ad}_{E}\circ\operatorname{tr}_M\right\|_\diamond
\le \frac{3125\pi}{4}\,d
\quad\text{when }10d\le1.
\]

This is uniform over every bath admitted in the task, with arbitrary
piecewise-continuous time dependence and arbitrary finite spectator
dimension. In particular it uses neither `||H_M||`, a bandwidth bound, nor
higher bath derivatives. The diamond norm includes an arbitrary reference.

For a concrete sufficient choice, put `e=min(epsilon,1)`, `h=e/5000`, and

\[
N=\left\lceil\frac{\pi}{16h^3}\right\rceil.
\]

The exact-duration schedule then has error below `0.491e`. Its total native
time is exactly `T=10Nd=(5pi/8)d^-2`; it has `10N` segments, `10N-1` interior
switches and `2N` private fair coin bits. This gives the advertised duration
and count scalings.

A rational common duration with relative error at most `e/100` keeps the
bound below `0.559e`. Its required absolute precision is `O(epsilon^2)`.
If implementation also perturbs every switching event, including final
turnoff, by absolute time at most `e/(160N)`, the overall bound
remains below `0.809e`. This event-time tolerance is `O(epsilon^4)`.
All required scalar descriptions have `O(log(1/epsilon))` bit length.
The explicit estimates and clock argument are in [DERIVATION.md](DERIVATION.md).

## Why a moving dirty medium does not spoil this channel

Move to the interaction frame of the uncontrolled bath alone. The three
memory operators remain a simultaneous Pauli triple and are 1-Lipschitz,
directly from the local commutator promise. A common midpoint freezing is
used only inside the proof.

The loop's frozen expansion is `I-4id^3 Z_1X_2+O(d^4)`. Its cubic term
survives because `s_A s_B s_C=1`. Its first and second frozen coefficients
vanish separately for every coin value.

Motion makes the loop's first-order residual nonzero, but its norm is only
`O(d^2)`. Averaging the fresh signs removes its linear channel contribution;
its variance contributes `O(d^4)`. The averaged second-order coherent term
is a **bath-only** anti-Hermitian operator: two occurrences of the same
native handle square its data Pauli to the identity. That term need not be
small across the whole computation and need not vanish. It is retained as
an allowed final bath unitary.

The complete one-cycle estimate, with `L=10d`, is

\[
\left\|\Phi_{\rm cycle}
-\operatorname{Ad}_{\exp(-4id^3 Z_1X_2)\otimes\exp(G)}\right\|_\diamond
\le\frac54L^4,
\qquad G^\dagger=-G,\quad G\text{ bath only}.
\]

Fresh signs make the averaged **joint** channel a composition of these
cycle channels, without resetting or tracing out the medium between cycles.
A diamond-norm telescoping argument costs at most `N(5/4)(10d)^4=O(d)`.
All comparison data factors commute with all comparison bath factors. Their
product is the target entangler tensor one bath unitary, which disappears
under the final partial trace, even for correlated inputs.

This is the difficult step missing from the packet's preflight foothold.
The complete proof, including channel cross terms, the time-dependent
Dyson remainder and dimension-independent constants, is in
[DERIVATION.md](DERIVATION.md).

## Exact checks and adversarial tests

`exact_word_check.py` checks all four sign choices with Gaussian-integer
arithmetic: the first two derivatives vanish and the third derivative is
exactly `-24i Z_1X_2`. It also exposes sign-dependent fourth derivatives,
which are not silently treated as a common unitary.

`exact_moving_expansion.py` goes beyond the frozen calculation. For the
admitted bath `H_M=Z_M/2`, it establishes the exact leading channel noise

\[
d^4\bigl[25(\operatorname{Ad}_{X_1Y_M}-\mathrm{Id})
 +16(\operatorname{Ad}_{X_2X_M}-\mathrm{Id})\bigr]+O(d^5)
\]

after removing the cubic data/bath comparison unitary. Its normalized Choi
trace norm is `82d^4+O(d^5)`. Thus the fourth-order channel fluctuation is
real for this loop. This is not an all-policy lower bound or an optimality
claim.

Numerical cycle checks approach that coefficient: at `d=0.005`, the
normalized Choi trace-norm error divided by `d^4` is approximately `81.993`.
They also test a rotating bath with frequency `3/d`, and a two-spin bath
with a spectator-only term of norm `10^6`; the latter's irrelevant fast
factor is canceled analytically before numerical propagation. These finite
tests are consistency checks, not the uniform proof.

Full-gate diagnostics compare the requested channel after the **final**
memory discard. At `N=32,768,000`, `d≈0.00181632`, the normalized Choi
witness error is about `0.02894` for `H_M=Z_M/2`, and `0.01136` for a public
zero-mean bath that switches between `+Z_M/2` and `-Z_M/2` within each
cycle. Both witnesses decrease proportionally to `d` along the tested
family.

The same deterministic bath trajectory can challenge an unjustified
shortcut. Reusing the same two signs throughout all cycles gives witness
error about `1.858` in the public zero-mean example at that `N`. The bath
does not know the realized signs. Conversely, coin reuse performs better
than fresh signs in the constant-bath finite examples. These results
support the stated construction and expose the scope of its proof; they
do not establish that fresh signs are necessary for every possible policy.

All numerical distances reported here are normalized Choi witnesses, hence
lower bounds on diamond error. They are not certified diamond upper bounds.
The analytic theorem supplies the upper bound. Recorded outputs and a
step-refinement check are in [CHECKS.txt](CHECKS.txt).

## Difference from the supplied predecessors and remaining frontier

The frozen packet already supplies an exact five-pulse pure-control
entangler. No drift-free controllability novelty is claimed. The native
source capture's forward-motion estimate instead requires a short gate or
small local motion; repeating calibration does not make that exposure
vanish. Here the local-motion bound stays fixed at one, and the bath may
vary arbitrarily throughout a growing total duration. The proof controls
the averaged channel by retaining harmless bath curvature and suppressing
the remaining fluctuations with private signs.

The packet also supplies deterministic exact finite-word impossibility.
There is no conflict: this construction has nonzero error for finite `N`
and asserts correctness of the averaged channel. It makes no claim for
each individual coin realization.

The latest P2 positive-force instrument is a different qualified interface.
Its meter, positive parity force, readout and adaptation are not used here.
The theorem does not derive that interface or give measurement-based
universality from the three handles.

The existence question in `CONTROL_TASK.md` is resolved by the proof above.
Resource optimality and practical usefulness remain open. The conservative
duration constant is approximately `4.91e7 epsilon^-2` in rate-one units;
for `epsilon=0.01`, the displayed sufficient choice uses about
`2.45e17` native segments and native time `4.91e11`. Those costs preclude
calling this an established practical advantage. The original uncertain
axes/gains, physical switching budgets, additional data noise, and a full
hardware model remain outside this granted-information subproblem. This
tranche has not received an independent scientific audit.

Frozen sources used: `../../packet/CONTROL_TASK.md` (operational contract,
five-pulse baseline, exact-impossibility boundary, and unproved randomized
foothold); `../../packet/control/P2_NATIVE.json` (native-control and
forward-bath predecessor); `../../packet/control/P2_FINAL_NATIVE_PREFIX.json`
and `P2_FINAL_RENDERED_OVERLAP_TAIL.txt` (the separately qualified
positive-force instrument and its remaining interface-construction gap).
