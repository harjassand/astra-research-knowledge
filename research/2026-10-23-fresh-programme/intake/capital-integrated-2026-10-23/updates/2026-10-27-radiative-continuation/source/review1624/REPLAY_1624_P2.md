# P2 1624: bounded source replay and mechanism assessment

**Decision:** this is a genuine construction of a different cancellation mechanism
inside the declared model. It preserves finite-time storage transfer, exact final
radiation vacuum, real internal hopping, no storage-storage edge, positive energy,
and an in-band carrier. It changes the radiation interface and expands internal
control resources; it is not a solution under the old factorized-bath premises,
nor a refutation of that correctly scoped theorem. Historical priority and a
laboratory capability are not established by this review.

This is a warm follow-through from the previous source assessment. I read the
receipt, current governing proof, all three current Python files and saved JSONs.
Only the supplied main and uniform scripts were replayed, once each, in an
isolated reviewer copy. Parameters, tolerances, quadrature and scientific code
were unchanged; only absolute file paths were redirected. No new experiments,
package installations or original-source edits were performed. All seven
original hashes remained unchanged. See REPLAY_RECEIPT.json for exact provenance,
runtime versions, logs and saved-output differences.

## Cancellation checked independently

Let F_j(z)=∫_0^T exp(izt)q_j(t)dt. For positions (-τ,0,τ), the two radiation
directions require

 exp(-iστz)F_1+F_2+exp(iστz)F_3=0,  σ=±1.

Subtracting gives sin(τz)(F_1-F_3)=0. Analytic continuation therefore gives
F_1=F_3 and F_2=-2cos(τz)F_1. Under zero extension, translation of a source by
±τ multiplies its Fourier transform by exp(±izτ). Consequently the supplied
q_1=q_3=g, q_2=-g(t-τ)-g(t+τ) cancels **both** directions identically, not just
the quadrature nodes. The support condition g⊂[τ,T-τ] is necessary to avoid
uncompensated sources outside [0,T], and sufficient; a nonzero L² history needs
T>2τ. The two-distinct-emitter determinant is proportional to sin[z(x_1-x_2)],
so the corresponding two-direction finite-duration obstruction also checks.

In the actual realization g=iα exp(-iμt)f. Since μτ=π, the two shifted carrier
phases are both -1, giving precisely the positive middle envelope used in code.
The line-24 comment says 15π, but the current parameters give π; both are odd
multiples and the executed identity is unaffected. No constant emitter vector
satisfies both radiation equations over an open band: it would require its
middle component to equal -2cos(ωτ) times an outer component for every ω.
Transient radiation is therefore allowed and reabsorbed at the terminal time;
this is not a relabelled instantaneous collective dark state.

## Realization and positivity

I checked the control equations directly. For storage amplitudes exp(-iμt)r
and emitter amplitudes i exp(-iμt)h, Schrödinger's equation reduces to
Ch=r′, Cᵀr=-h′-Re(g_bath), Qh=-Im(g_bath), where
g_bath=exp(iμt)W*ξ. Norm conservation gives the compatibility condition
rᵀr′=hᵀ(-h′-Re(g_bath)). Substitution verifies the displayed real C and symmetric
Q formulas. The upper-left correction block is exactly zero: there is no
storage-storage hopping. The full bath coupling W remains complex through
propagation phases; “real” describes the internal controls.

The uniform positivity argument is substantive and separate from the time
scan. Its coupling and Schur bounds follow from the stated form factor; the
Plancherel bound controls radiation norm. The forward/backward integral bound
uses exact initial/final vacuum and the componentwise unimodality of h. For the
shifted middle component, the stated condition 2τ<L/(2√5) keeps the relevant
derivative comparison monotone. These bounds control C,Q even as h vanishes.
The continuous-time Schur lower bound is about 1.12503; the looser strict
enclosures give >1.105. Completing the energy quadratic form with
ω^(1/2)ξ+ω^(-1/2)Wq is legitimate because ∫|v|²/ω is finite, even without a
bounded ω^-1 operator.

Thus the analytic construction has nonnegative energy with a gapless continuum.
The margin is internal, not a global gap. μ=2π lies inside (0,12). The finite
quadrature itself has no arbitrarily soft modes and cannot establish gaplessness.

## Replay evidence and its limits

Both scripts exited successfully under existing /usr/local/bin/python3. Main
replay wall time, including startup/imports/serialization, was 1.3577 seconds;
uniform replay was 0.1210 seconds. Main diagnostics reproduced the producer to
ordinary floating differences:

| Quantity | Reviewer replay |
|---|---:|
| Full fixed-phase state-vector transfer error | 2.84917e-11 |
| Terminal radiation norm of prescribed convolution | 8.96226e-14 |
| Largest sampled transient radiation norm | 0.00284406 |
| Smallest sampled Schur eigenvalue | 5.28039553 |
| Maximum sampled equation residual | 1.99994e-15 |
| Storage-storage hopping / imaginary internal H | 0 / 0 |

This uses 40 positive quadrature nodes per direction, DOP853 and ordinary
floating arithmetic. Controls are precomputed from that discretized bath
convolution, then a separate full 85-component state is propagated. It checks
the implementation, not a continuum discretization-error bound or exact zero.
The uniform script reproduces the analytic-bound numbers without a time grid,
but uses ordinary math/SciPy evaluations and assertions, not outward-rounded
arithmetic. Exact continuum cancellation and positivity rest on the analytic
identities and inequalities above.

The perturbation code/data were inspected, not rerun. The position Duhamel bound
checks algebraically: |exp(iωδx)-1|≤ω|δx| gives
||δW||≤[2∫ω²|v|²]^(1/2)||δx||₂ and hence
||Uδ(T)-U0(T)||≤TηΩ²/√140 ||δx||₂. It assumes this same bath and fixed nominal
controls. The saved onsite-0.01 result has vector error 0.01022059 but target
probability 0.99990938: it fails a 1% fixed-phase vector-error target, not a 1%
infidelity target. The 1% coupling change is an amplitude change.

## What changed and what remains unacquired

Frequency-dependent propagation columns Wσj(ω)=v(ω)exp(iσωx_j) replace the
previous v(ω)R premise. Three delayed sources create a temporal kernel despite
the absence of a common spectral dark vector. The explicitly constructed
trajectory and real positive Hamiltonian make this more than a renamed null
condition. However, preservation is of the functional target, not every former
resource restriction: two storage and three emitter modes now have a dense
network of real storage-emitter/emitter-emitter controls, inverse-engineered from
a known bath and an initially empty field. “Two-local” means quadratic two-mode
hopping, not a sparse nearest-neighbour device or universal two-qubit hardware.

The unacquired interface is a realizable phase/form-factor spectrum and that
calibrated dense control family, including amplitude, slew, work, geometry,
unmodelled radiation channels, initial preparation, capture/release and full-cycle
cost. The prescribed advanced pulse term requires precomputed pulse knowledge,
not future measurement access. No interacting multiphoton gate or physical
advantage follows. The source's proposed reduction to a sparse graph and small
control alphabet is therefore a real remaining interface question, not something
the present replay has acquired. No further research trial is implied here.
