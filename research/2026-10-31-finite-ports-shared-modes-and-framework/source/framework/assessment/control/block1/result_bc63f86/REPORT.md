# Unknown gains: a barrier to the direct high-degree weak-word extension

The general unknown-gain first-motion problem remains unresolved in this
tranche. I established a quantitative obstruction to its most direct
construction route: repeating a fixed higher-degree flat native word can
lose essentially all useful data information under an admissible,
coin-independent moving bath. Private global sign projection does not
remove this loss.

The obstruction applies to a family of protocols, rather than all legal
randomized programs. It is root-derived and checked locally, without
independent review or a priority claim. The proof is in
[PROOF.md](PROOF.md); [check_barrier.py](check_barrier.py) and
[checks.txt](checks.txt) give exact finite certificates and numerical
channel diagnostics.

## The established theorem

Fix a finite native loop shape, of duration `D*delta`, which uses all three
handles, has balanced signed areas, and whose frozen first and second
coefficients vanish. This includes every ordinary flat commutator word
whose first pure-control term has degree at least three. Repeat it `N`
times. The controller may choose arbitrary private global polarities in
each repetition, with arbitrary correlations between its private choices.

There are explicitly constructible word-dependent constants
`gamma>0, delta_0>0` such that, for every `delta<=delta_0`, one legal bath
and initial state give full reduced-data trace-norm error at least

\[
\boxed{1-e^{-\gamma N\delta^4}}.
\]

The bath is fixed independently of the private signs, satisfies all three
local-motion bounds, and even has Hamiltonian norm at most `1/2`. Its
spectator dimension is finite, although extremely large. The lower bound
is uniform over static gains `[1,2]^3`.

Consequently, extracting a finite gate angle from a fixed degree-`k` word
with `N=Theta(delta^-k)` fails as `delta` decreases for every `k>=5`.
The error lower bound tends to one. The degree-three known-gain result
has `N*delta^4=O(delta)` and is fully consistent with this barrier.

The loss cannot be repaired by native controls before or after that repeated
block. The constructed bath retires its spectator labels after use, so
later native operations cannot retrieve the leaked information.

## The actual bath construction

For each handle, integrate its normalized signed waveform to obtain a
primitive `F_j`. For each ordered pair of different mediator axes `j,k`,
choose a bounded drift profile `h_jk` with

\[
\int h_{jk}=0,\qquad\int h_{jk}F_l=0,\qquad
\int h_{jk}F_j=\mu_{jk}>0,
\qquad |h_{jk}|\leq1/2,
\]

where `l` is the other handle affected by a rotation about axis `k`.
Projection of `F_j` off the span of `1,F_l` constructs such a profile.
Disjoint native-handle supports ensure that the required residual is
nonzero. Thus this is an explicit finite construction for every word in
the theorem, rather than a successful drift sample.

During one cycle use mediator drift `b*h_jk(t/delta)*sigma_k`, with label
`(j,k,b)` drawn uniformly from six ordered pairs and two signs. Each
profile has zero integral, so the free bath returns exactly after the
cycle. Nevertheless the native interaction has a mixed order-`delta^2`
error, proportional to one of

\[
X_1\sigma_y,\ X_1\sigma_z,\
X_2\sigma_x,\ X_2\sigma_z,\
Y_1\sigma_x,\ Y_1\sigma_y.
\]

Fresh independent labels convert those excursions into irreversible
order-`delta^4` noise. All six noise operators together have common
commutant exactly `span{I,X_2}`. The useful observable `Z_1X_2` lies
outside this protected algebra and contracts.

There is no new stochastic bath interface in the proof. Put `N` independent
twelve-state label registers in the spectator, initially in the uniform
classical mixture. A deterministic block-diagonal Hamiltonian consults
register `i` during cycle `i` and never uses it again. Its commutator with
each mediator Pauli has norm at most one. The resulting spectator dimension
is `12^N`, allowed because every selected program is finite and no uniform
dimension bound is supplied. This bath knows the public word shape and
duration, and never reacts to current private signs.

## Why the channel lower bound is rigorous

The proof uses a variance identity in Hilbert-Schmidt operator space.
Each label-conditioned conjugation is an isometry; averaging it contracts
by the variance of the order-`delta^2` excursion. The six Pauli noises give
a uniform spectral gap outside `span{I,X_2}`. A direct bounded-Hamiltonian
Dyson remainder gives an explicit positive `delta_0`.

If `mu_min=min mu_jk`, one sufficient rate is
`gamma=mu_min^2/3`. Taking initial data in the normalized positive
eigenspace of `Z_1X_2`, the target preserves its expectation one, whereas
the actual output expectation is at most `exp(-gamma*N*delta^4)`.
Duality with this norm-one data observable gives the stated trace-norm
lower bound. No convenient product-bath success criterion replaces the
original channel requirement: a single admitted product input is a valid
failure witness for that requirement.

## Exact instance and numerical challenge

The checked example is the 46-segment flat word for
`ad_A^2([A,[B,C]])`, with an overall C reversal to match the target sign.
At zero drift its expansion is

\[
I-16i\delta^5 g_A^3g_Bg_C Z_1X_2+O(\delta^6).
\]

This degree-five monomial is the same algebraic kind already supplied in
the predecessor supplement. The exact rational Pauli calculation checks
vanishing degrees one through four for all eight global native sign
variants. Exact rational half-cell profiles verify every zero moment,
the `1/2` amplitude bound, and positive isolation coefficient. They give

\[
\mu_{\min}=1135/234,\qquad
\gamma=1288225/164268\approx7.84.
\]

The conservative proved small-step threshold is about `3.59e-7`. The
concrete repeated native word lasts `46*N*delta`; its adversarial bath
has at most `92*N` constant-profile pieces, `N` twelve-state label
registers, and rational profile amplitudes bounded by `1/2`. All of these
resources are finite for the selected word and repetition count.
The numerical tests use larger steps and therefore serve as diagnostics rather
than evaluations inside that conservative theorem threshold. They average
the complete data-plus-mediator channels over all twelve bath labels and
four private even-sign choices. At unit gains, the contraction gap divided
by `delta^4` approaches about `63` as `delta` decreases.

For `delta=0.1,0.05,0.025,0.0125,0.00625`, take the integer number of
repetitions that would produce a pi/4 gate from the ideal fifth-degree
coefficient. The reported final `Z_1X_2` expectations are all essentially
zero; the trace-norm lower witness is approximately one. The numerical
propagation uses exact constant-Hamiltonian pulse pieces via floating-point
eigendecomposition. It removes roundoff leakage into the two exact
invariant Pauli modes before very large matrix powers. These results are
not interval-certified bounds; the analytic variance proof carries the
quantified claim.

Run the saved check with:

```
OPENBLAS_NUM_THREADS=1 python3 check_barrier.py
```

It reuses the retained first tranche's Gaussian-rational Pauli arithmetic.

## Predecessor difference and remaining frontier

The supplement corrects a genuine initial-source omission. Prior Astra
already supplies native sign-group projection, order raising, extraction
of odd chirality powers and coarse unknown-gain polynomial compensation.
In particular, `uniform_gate_THEORY.md` Sections 4–9 give the algebra and
flat-word compiler; `LOCAL_REGULARITY.md` Section 1 explicitly requires
the finite-order orbit bounds reached by that compiler. None of that
general machinery is claimed as newly invented here.

The new result is a failure mechanism at the weaker operational boundary:
arbitrary time dependence with only first local motion permits a bath that
turns fixed high-degree weak-word synthesis into irreversible data noise.
The bath becomes faster as `delta` decreases. It is therefore outside the
older static/high-regularity promises, despite its small instantaneous norm.

This blocks simply attaching the first tranche's randomized-channel
reasoning to the old higher-degree monomials. It does not prove that gain
compensation itself is impossible. Accuracy-dependent growing word shapes,
different internal randomization, and nonperturbative native constructions
are not covered. A positive general construction would need to avoid this
accumulated noise or prove a different uniformly qualified nonlinear gain
primitive. A complete negative result would need a lower bound for every
legal randomized schedule; that has not been established.

The source scope was the frozen control packet, the named p01 checkpoint,
the supplied predecessor supplement, and retained own artifacts. No network,
provider feedback, calibration, new physical operation, or nested agent was
used. The first tranche's scientific source and proof files were not edited.
