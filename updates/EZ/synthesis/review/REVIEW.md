# Adversarial review of the integration-derived synthesis

Date: 2026-10-13. Capital base: `f437df815bef12f123ae4fe313d861ec1c862bc4`.
This is an internal analytic review and finite replay, not external validation,
formal verification, historical priority clearance or a breakthrough assessment.
Original inputs, capital, Git and other investigators' files were not edited.

## Verdict and reviewed material

No decisive mathematical error was found in the proof scopes actually reviewed
below. The hypotheses and excluded transfers are essential parts of that verdict.
The review read root `TASK_CERTIFICATES.md` and its complete check program;
spectrum `REPORT.md` and its complete synthesis program; lattice `REPORT.md` and
its complete independent program; and operational `extension_checks.py` with its
results. The operational investigator also supplied the analytic detuning and
restricted-code reduction proofs directly. The complete operational final report
and any later guard-block theorem were not available during this review and are
not certified by this verdict.

## 1. Fixed-point residuals and task losses

The noncommuting modulus follows from positivity/subunitality, operator
monotonicity and the scalar bound on `g_a(Z+dI)-g_a(Z)`; no simultaneous
diagonalization of the two inputs is used. The residual inequality
`d <= eta + d/(1+ad)` correctly gives
`R_a(eta)=(eta+sqrt(eta^2+4eta/a))/2`. The example `Phi=Id, P=0, Y=eI`
attains equality and also prevents an inference of infinite-dimensional
compactness from nonzero residual. The different inside-source perturbation
root `S_a(zeta)=(sqrt(zeta^2+4zeta/a)-zeta)/2` is correct.

Two clarifications were requested and root reports incorporating both: the
approximate source Q must itself be positive, and minimax loss perturbation
holds with acquisition output laws unchanged, rather than silently changing
the observation experiment. Uniform norm/trace-class bounds and all acquisition
and evaluation costs remain required. The quadratic residual scale is a sharp
worst-case sufficient contract, not a necessity theorem for every instance.

Trace duality yields the stated loss error. A sharper pointwise action comparison,
communicated to root, is

```
|[ell_v(Y)-ell_u(Y)]-[ell_v(X)-ell_u(X)]|
    <= ||Q_v-Q_u||_1 R_a(eta).
```

Thus a selected approximate minimizer has pointwise regret at most
`max_v ||Q_v-Q_u||_1 R_a(eta)`. This cancellation cannot automatically be used
for minimax risk: a common theta-dependent loss offset can change the worst-case
theta and the optimal policy. The scalar two-subsolution example is an exact
information-interface counterexample: the comparison data alone admit two
targets with opposite optimal actions and randomized worst-case regret 1/2.
It does not imply a runtime lower bound when T or further observations are given.

## 2. Source-spectrum constructions and obstructions

The finite joint minimum-rank/minimum-Hilbert-Schmidt-source construction is
coherent. Reciprocal-window spacing gives the needed interlacing on every
rank-strided chain; the nonnegative residues give the claimed secular
polynomial, positive isospectral correction and trace equality. The countable
extension's compact order interval, bounded-rank norm limit and Ky Fan lower
bound avoid subtracting divergent traces. Kernel enlargement is still required
in that extension. This is an existence result with no effective limiting rate.

For fixed T, the positive part of `f_a(T*T)-TT*` gives minimum source trace and
positive-inertia rank. The joint construction instead changes the polar factor.
It must retain its supplied-spectrum input, dense basis/conditioning cost and
possible loss of locality. Its source squared Hilbert-Schmidt norm is not a
physical energy budget.

The additional commutator-majorant theorem is valid: from an acquired positive
`Q >= TT*-T*T`, one gets `a(T*T)^2 <= BB*+Q`. Spectral min-max plus trace
subadditivity for p<=2, or the Schatten triangle inequality for p>=2, gives the
stated S_(2p) conclusion. The harmonic-shift endpoint p>1 checks the missing
summability hypothesis exactly. A small commutator norm is not an acquired
Schatten budget.

The rank-two fixed-point family has exactly two source words but operator
Schmidt rank 4^m. The displayed realignment singular values give the stated
Hilbert-Schmidt lower bound and rank threshold at error 1/6. This decisively
rejects a generic transfer from small source-word dimension to small tensor
rank. It is specific to that norm, tensor cut and representation; the Bell
state still has a short circuit. It proves neither hardness of all
representations nor failure of N764's specific physical approximation target.

## 3. Lattice pumping, causal discrimination and elastic energy

Independent derivation confirmed the force-tilted rates, occupation equation,
coefficient `Cd R[sin(phi)-cos(phi)/r]`, geometric coefficient
`Cg R[sin(phi)+r cos(phi)]`, and two-channel inversion. Around v=z=0, neither
field changes occupation at first order and there is no direct v*z current
term at total bilinear order, so the proposed leading-order mixture is sound.

The force-only alternative reproduces the phase-odd signal and its one-pole
rolloff for unequal sites. This is a genuine model-level falsifier of using that
signal alone to identify structural pumping, not evidence that either mechanism
has occurred in a specimen. Separation requires independently acquired
relaxation rate, force law and phase, the stipulated memory-free chain and
controlled higher-order errors. Unknown memory, contacts and other mechanisms
are not separated by four phases.

The compliance-determinant bound follows from the two-volume inequality and
the Gram arithmetic-geometric mean bound. Equal orthogonal normalized controls
attain it within the quadratic model, and its fixed-stored-energy speed bound
is maximized at omega=lambda. It bounds the leading orientation-odd term only;
rank-one finite-rate rectification survives. Stored elastic energy excludes
actuator loss, preparation, heating, screening, contacts and retention costs.
The periodic local-detailed-balance work/entropy identity has consistent signs.

## 4. Operational extensions: reviewed scope only

The single-excitation protection against degree>=2 diagonal density monomials
is exact: every such monomial annihilates that occupation sector. This supplies
a protected sensor subspace under the stated switching/preparation interface;
it does not supply stationary many-body payoffs, noise-free preparation or
physical control availability.

The constant acquisition-only differential-detuning bound is sound. In the
phase-rotated Bloch generator, changing detuning sign reverses x alone, while
the anti-trine bad probability reads y. Its first derivative at zero therefore
vanishes. For `K=-i[Z/2,.]`, the Hermitian trace-norm induced bound is 1; CPTP
contraction and the second Duhamel derivative give `||rho''||_1<=T^2`.
Centering the POVM effect by I/3, using trace-zero derivatives, gives
`|p_bad(delta)-p_bad(0)|<=delta^2 T^2/6`. Keeping detuning active during output
operation requires a new payoff certificate.

A stronger analytic consequence was communicated to the operational
investigator: arbitrary measurable acquisition-only detuning delta(t) obeys
the same bound with `|delta|T` replaced by `integral |delta(t)|dt`. The first
Dyson term vanishes pointwise because K sends the baseline yz plane into x.
One further Duhamel expansion, Hermitian CPTP contraction and the ordered
simplex integral give `(integral |delta|)^2/6`. This extension needs the same
fixed-phase baseline and fixed anti-trine effect; no time-dependent-detuning
numerical fixture was independently executed in this review.

The exact-cover reduction is valid only for the explicit occupation-pair
family: nuisance templates `n_p sum_i A_li n_i+n_q` act as a scalar on the pair
iff `Ax=1`. The binary-only variant requires an occupied reference. This is
not hardness of arbitrary coherent/QEC codes, nor hardness of finding the
original empty-spectator single-excitation pair. The all-identifier angular
argument in the supplied operational source is consistent with half spectral
range and the hard summed unknown-link exposure cap; parallel wall time,
expected-time caps, uncharged phase references and later operation observations
cannot replace that interface.

## Replay receipt and scientific limits

After inspecting each complete program, this review copied and replayed four
investigator programs into isolated `review/replays/` subdirectories. All four
exited 0. `replays/RECEIPT.json` records source hashes and runtimes; individual
logs and result JSONs are preserved there. The spectrum replay includes 6,908
mixed exact/floating checks; the other programs retain their original count and
scope labels. Replaying these programs is reproduction, not a new independent
implementation of every numerical result or verification of a universal proof.

The main surviving publication risks are scope promotion: treating an acquired
fixed-point certificate as an acquired physical response, treating a redesigned
polar factor as the original operator, changing norms in the tensor obstruction,
calling stored energy wall energy, broadening restricted code hardness, or
silently allowing operation observations in a bounded acquisition comparison.
No current result removes those interfaces or establishes a validated
civilisation-enabling capability.
