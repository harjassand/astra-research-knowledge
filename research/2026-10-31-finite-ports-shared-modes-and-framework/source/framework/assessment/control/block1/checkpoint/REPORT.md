# A positive resolution of the frozen moving-medium subproblem

The requested averaged-channel gate is reachable under the stated local
motion promise. A ten-segment native word, repeated with fresh private
signs, gives a finite construction with duration `O(epsilon^-2)`, native
segment count `O(epsilon^-3)`, and logarithmic timing precision. The
guarantee is uniform in the drift norm, its time dependence, spectator
dimension, and initial data-memory-reference correlations.

This is a root-derived proof for the precise frozen model. It has not had
independent review, and no priority claim is made. Its conservative resource
constants are far too large to establish practical advantage.

The full proof is [PROOF.md](PROOF.md). The runnable construction is
[schedule.py](schedule.py); [check_construction.py](check_construction.py)
contains an exact rational Pauli certificate and numerical channel
diagnostics. Their saved output is [checks.txt](checks.txt).

## The construction and the difficult step

In every cycle choose independent uniform private signs `s_A,s_B`, set
`s_C=s_A*s_B`, and execute this chronological list, each for duration
`delta`:

```
B(-s_B), C(-s_C), B(+s_B), C(+s_C), A(-s_A),
C(-s_C), B(-s_B), C(+s_C), B(+s_B), A(+s_A).
```

Every handle has zero signed total duration. Frozen at a common bath time,
the word is a nested group commutator with expansion

\[
U_s=I-4i\delta^3 Z_1X_2\otimes I_M+O(\delta^4).
\]

The challenge is that a moving medium creates random errors of order
`delta^2` in individual cycles, larger than the useful third-order gate.
They cannot be bounded by summing individual cycle errors.

Move to the frame of the uncontrolled bath alone. The three memory Pauli
operators there remain Hermitian involutions and are norm-one Lipschitz
functions with Lipschitz constant one. This conclusion needs no bound on
`||H_M||`. The private-sign projection eliminates every averaged first-order
Dyson term and every second-order term containing different handles.

The surviving second-order same-handle term acts only on memory, because
the repeated data Pauli squares to the identity. Its anti-Hermitian part
is retained as a bath generator `K`, of norm at most `(500/3) delta^3`.
Its Hermitian part is order `delta^4`, since each balanced integrated
moving Pauli has norm `O(delta^2)`. At third order only one occurrence of
each handle survives, producing the required data-only generator with a
uniform order-`delta^4` motion error.

That accounts for the mean unitary. To obtain a channel result, the proof
also bounds the second moment of the order-`delta^2` fluctuations. The
result, in full diamond norm, is

\[
\boxed{
\left\|\mathbb E_s\operatorname{Ad}_{U_s}
 -\operatorname{Ad}_{e^{-4i\delta^3Z_1X_2}\otimes e^K}
 \right\|_\diamond\leq10000\delta^4,
 \qquad 0<\delta\leq0.1.}
\]

The bath generator is deterministic for the fixed bath trajectory and
cycle time; it is independent of the realized signs. Fresh cycle signs
therefore permit ordinary channel composition. After `N` cycles the
averaged joint channel is within `10000 N delta^4` of

\[
\operatorname{Ad}_{e^{-4iN\delta^3Z_1X_2}\otimes B_H}
\]

for a bath-only unitary `B_H`. The bath factors from different cycles can
fail to commute; factorization from the data gate still holds. Discarding
memory yields exactly the input/output interface in the task. All norms
apply with arbitrary reference systems, so initial correlations are
included rather than tested only on product bath states.

## Finite resources and precision

Here is an explicit family, including slack for independent duration
errors. Put `e=min(epsilon,1)`, choose the dyadic integer

\[
q=2^{\lceil\log_2(4000/e)\rceil},\qquad\delta=1/q,
\]

and approximate pi to absolute error at most `q^-3`. Let `N` be the nearest
integer to `pi_hat*q^3/16`. The ideal specified schedule then has full
diamond error at most

\[
10000N/q^4+9/(2q^3)<2000/q\leq e/2.
\]

The total resources are

\[
m=10N\leq(5\pi/8)q^3+45/8,
\qquad T=m/q\leq(5\pi/8)q^2+45/(8q).
\]

There are at most `m-1` switches and exactly `2N` private fair bits. All
active strengths are `+1` or `-1`; no pulse becomes instantaneous or
stronger. Pi needs `3 log_2 q+O(1)` bits, and the generator certifies its
approximation by an exact alternating-series calculation.

Allowing each implemented segment duration to differ independently from
`1/q` by at most `e/(4m^2)` adds at most `e/2` channel error. Thus
`7 log_2(1/e)+O(1)` absolute binary timing places suffice, conservatively.
This timing argument also works in the bath interaction frame and does
not assume a drift norm. The actual total duration increases by at most
`e/(4m)`.

The constants are deliberately loose. For `epsilon=0.1` the saved
[resource example](resources_example.txt) has `q=65536`,
`N=55,267,482,437,722`, about `5.53e14` segments, total normalized duration
`8.43e9`, and the conservative independent duration tolerance requires
104 binary places. This is an existence construction, not a usable gate
at that parameter setting. Improving these constants and resource rates
is a substantial remaining task.

## Checks and challenges to the candidate

The exact standard-library calculation checks all four sign choices,
including the orientation `-4i Z_1X_2`, zero first- and second-order frozen
coefficients, balanced native durations, and the midpoint motion weights
used in the proof.

The numerical code evaluates the complete averaged channel before tracing
memory. For constant qubit baths, powers of this channel represent exactly
independent signs in successive cycles. It reports a maximally-entangled
input lower bound and a Hilbert-Schmidt based upper bound on the reduced
channel's diamond norm. For the admitted bath `H_M=Z/2`, the reported
upper bound decreases from `0.7613` to `0.3902` to `0.1975` as `delta`
halves through approximately `0.00621, 0.00311, 0.00155`. Thus modest
cycles do have large errors; the convergence is slow, consistent with the
resource account. The no-drift diagnostic converges faster.

A separate test uses a two-dimensional spectator and fifty discontinuous,
coin-independent bath pieces per cycle. Its local commutator bound is at
most `0.8`, while a spectator Hamiltonian coefficient is either zero or
2000. Its switching frequency grows as `1/delta`, so it does not supply a
fixed bandwidth or frozen-bath assumption. At `delta=0.00625`, the reported
one-cycle reduced-channel upper bounds are approximately `1.30e-8` and
`2.59e-9`, respectively; both obey the analytic `10000 delta^4` estimate.

These floating-point outputs are diagnostics, not certified rounding
enclosures and not evidence of a physical device. The dimension-free
analytic argument establishes the uniform quantifiers. Run them with:

```
OPENBLAS_NUM_THREADS=1 python3 check_construction.py
python3 schedule.py 0.1
```

## What this adds, and what remains

The frozen task already supplies an exact five-pulse, `5*pi/4` duration
gate when drift is absent. That is the appropriate short ordinary baseline
and remains much cheaper in its scope. The new argument resolves the
separate arbitrary moving-bath approximate question by proving the
previously unproved randomized weak-cycle channel estimate and controlling
its accumulation for every retained history.

The supplied deterministic exact obstruction remains valid. Finite cycles
here have nonzero channel noise; the result is averaged over private coins,
and the total duration diverges as the requested error vanishes. No
individual-realization success claim is made.

The force-based P2 instrument in the supplied source captures has a
different physical interface: a positive operator-valued force, meter,
source band, and readout. None of those operations is used here. This
construction uses only the original signed A/B/C interactions.

The frozen subproblem is answered positively at the stated averaged
channel scope. The remaining frontier is practical efficiency, sharper
worst-case error/resource bounds and lower bounds, extension to a broader
native interface, independent checking, and physical implementation. The
proof fails without further work if same-handle second-order survivors
can act nontrivially on data, if the bath reacts to the private signs, or
if an individual-coin guarantee is requested.

Scientific sources were restricted to the frozen
`packet/CONTROL_TASK.md`, `packet/control/P2_NATIVE.json`,
`packet/control/P2_FINAL_NATIVE_PREFIX.json`,
`packet/control/P2_FINAL_RENDERED_OVERLAP_TAIL.txt`, and their supplied
`packet/SOURCES.txt` provenance. No external literature or novelty search
was performed.
