# Three-load coherent scalar target-power acquisition

Research continuation, 28 October 2026. Mathematical construction and synthetic checks; no laboratory execution or historical novelty claim. This deliberately changes the acquisition interface. It does not contradict the original bounded-error lower bound for total returned intensity without an external reference.

## Source dependencies

Read directly: original `theory/first_harmonic_control.md`, `theory/finite_phase_harmonic.md`, `theory/harmonic_norm_calibration.md`, `alternatives/scope_stress.md`, `alternatives/multi_target_acquisition.md`, and `acquisition/rank_one_control_theory.md`. The new extraction proof below is self-contained. The conventional sequential control proof used below is the two-dimensional variational argument in the last source. This is not an independent whole-proof audit of the archive.

## 1. New physical interface

Keep the reciprocal passive source

\[
S=\begin{pmatrix}S_0&t\\t^T&s\end{pmatrix},\quad S^*S\preceq I,
\qquad T_z=S_0+\frac{z}{1-sz}tt^T.
\]

A calibrated reciprocal launcher sends `u`, `||u||<=1`, and its same source port receives

\[
h_z(u)=u^T T_z u=h_0(u)+\frac{z}{1-sz}a(u),
\quad a(u)=(t^T u)^2,
\quad p(u)=|a(u)|.
\]

The transpose is essential. A generic receiver projection does not have this identity. A reciprocal matched multiport launcher with unused source ports terminated provides an ideal realization. Mismatch, residual reflection, insertion loss and unequal transmit/receive transfer must be calibrated or enclosed. A reference is added downstream and isolated from the specimen; reference leakage changes the model unless bounded.

Only the target states `0,+r,-r`, `0<r<1`, are needed. In an ideal real reference impedance these are resistances `Z0`, `Z0(1+r)/(1-r)`, `Z0(1-r)/(1+r)`, hence `Z0,3Z0,Z0/3` for `r=1/2`. Switch and line parasitics must be calibrated at the target reference plane; state labels are not calibration.

## 2. Four real readings acquire each complex return

A passive 50:50 combiner with reference amplitude `R>0` gives one detector power

\[
I_\theta(z,u)=\tfrac12|h_z(u)+R e^{i\theta}|^2,
\quad\theta\in\{0,\pi/2,\pi,3\pi/2\}.
\]

The complex return is acquired by

\[
\widehat h_z=\frac{(\widehat I_0-\widehat I_\pi)
+i(\widehat I_{\pi/2}-\widehat I_{3\pi/2})}{2R}.
\]

Simultaneous error `eta` in each physical detector power implies `|hhat-h|<=sqrt(2) eta/R`. A fixed detector offset cancels; a changing offset does not. Four readings per load give **twelve raw readings per target-power query**. A balanced two-detector implementation uses two reference phases but still four scalar readings per load.

The maximum physical detector power is `(1+R)^2/2`, and the reference consumes energy `R^2` per unit probe energy per exposure. Reference power, shot noise, phase stabilization, dynamic range and combining loss are charged. An arbitrarily strong unpriced local oscillator is not an allowed precision oracle.

## 3. Uniform stable elimination of the nuisance pole

Define

\[
c=\frac{h_r-h_{-r}}{2r}=\frac{a}{1-r^2s^2},
\qquad d=\frac{h_r+h_{-r}-2h_0}{2r}=rs c.
\]

Every physical pair lies in `F_r={(c,d): |d|<=r|c|}`. On it set

\[
\Psi(c,d)=c-d^2/c\quad(c\ne0),\qquad\Psi(0,0)=0.
\]

Then `Psi(c,d)=a`. For two feasible nonzero pairs let `k=d/c`, `k'=d'/c'`. Direct subtraction gives

\[
\Delta\Psi=(1+kk')\Delta c-(k+k')\Delta d.
\]

Therefore

\[
|\Delta\Psi|\le(1+r^2)|\Delta c|+2r|\Delta d|
\le\sqrt{1+6r^2+r^4}\|\Delta(c,d)\|_2.
\]

The zero case follows by continuity, or by assigning its otherwise undefined `k` zero. The useful residue is uniformly Lipschitz even at zero target strength, zero background, and an unresolvable pole. Accurate separate estimation of `s` is unnecessary.

## 4. Explicit finite-error estimator and rational implementation

Keep noisy `chat` and clip noisy `dhat` radially into the disk `|dc|<=r|chat|`. Return `ahat=Psi(chat,dc)` (zero if `chat=0`), then `phat=|ahat|`. If `|chat-c|<=ec`, `|dhat-d|<=ed`, the clipping displacement is at most `ed+r ec`, so

\[
|d_c-d|\le2e_d+r e_c,
\quad |\widehat a-a|\le(1+3r^2)e_c+4r e_d.
\]

When all three acquired fields have error at most `epsilon_h`, `ec<=epsilon_h/r` and `ed<=2epsilon_h/r`. Thus

\[
\boxed{|\widehat p-p|\le K_r\epsilon_h,
\quad K_r=1/r+3r+8.}
\]

At `r=1/2`, `K_r=23/2`. With detector error only, the physical half-power combiner yields `delta=23 eta/(sqrt(2) R)`, approximately `16.264 eta/R`. Conservative constants are not the substantive contribution.

For exact rational computation, if clipping is needed, enclose `sqrt(r^2|chat|^2/|dhat|^2)` by dyadic fractions and multiply `dhat` by the lower endpoint. This is an inward feasible clip. Its error from exact clipping is bounded by the dyadic interval width times an upper bound on `|dhat|`. If that error is `eclip`, add `2r eclip` to the residue error. An outward rational square-root interval for `|ahat|` produces the final power interval. All exact rational source values remain outside the inference routine.

A nearest-point projection is also possible by retaining both phases and projecting magnitudes onto `D<=r C`; its distance from truth is at most twice the data error. `F_r` is not convex as a subset of four real coordinates: do not claim projection nonexpansiveness.

## 5. Conventional complete control and verification

The acquired positive oracle now is **p itself**, rather than the squared-Gram observable `tau p`. The original sequential two-mode optimizer gives

\[
\tau-p(\widehat u)\le D=2(1+2\sqrt2)(n-1)\delta+\nu_{ctrl}.
\]

It makes `4(n-1)` queries: `48(n-1)` raw detector readings, plus twelve final verification readings. An additional `n` trace queries give total `60n-48` plus twelve verification readings. A final acquired interval `[pL,pH]` and regret `D` imply `tau<=pH+D` and optimum fraction at least `pL/(pH+D)` when the denominator is positive. A zero certificate remains valid.

The control proof compares true and estimated variational maxima of each two-dimensional restriction. Four scalar errors `delta` perturb its Hermitian matrix in operator norm by at most `(1+2sqrt(2))delta`; twice that is lost per merge. Rank one makes its exact top eigenvalue the sum of the two subspace energies. Re-querying each actual reference prevents accumulated idealization. Numerical eigensolver and command preparation losses belong in `nu_ctrl`.

That displayed uniform constant uses ideal normalized quadrature mixtures. The exact finite-command execution below instead uses the rational subunit probes `(r+e_j)/2` and `(r+i e_j)/2` and checks every proposed coefficient vector's norm. Its polarization multiplies those mixed powers by two; at uniform oracle error `delta`, a safe per-step operator bound is `(1+3sqrt(2))delta`. The implementation uses the sharper actual interval widths per query and exact rational optimizer-gap checks, rather than pretending the unit-mixture bound holds unchanged.

The root continuation separately supplies an `O(n)` pivot reconstruction theorem for the whole target Gram. Linear objective regret alone would not prove linear operator error for a rank-one estimate; the new reconstruction theorem must be checked separately.

## 6. Calibration errors and complete costs

A common relative reference-amplitude error `|Rtrue/Rnom-1|<=g` adds at most `g` field error when `|h|<=1`. Phase-dependent errors require actual quadrature coefficient enclosures. A reference phasor error bounded by `xi` changes one half-combined power by at most `(1+R)xi+xi^2/2`. Load error `|z-z'|<=ez`, with both bounded by `rmax<1`, changes the scalar field by at most `ez/(1-rmax^2)`, using the original passivity bound; include the matched state too.

For normalized vectors, `|u^T T_z u-v^T T_z v|<=2||u-v||`. Unequal receive and transmit modes need additional bounds. A common unknown phase across a complete three-state query leaves `|a|` unchanged; independent unknown phases across load states do not.

Each query costs twelve exposures, three target states, four reference phases, one reciprocal mask, settling and readout. `O(n)` queries can require `O(n^2)` physical channel writes with dense masks. Photon, reset, phase-stabilization and reference energies are charged. The original finite-memory matched-flush theorem can bound specimen settling at `|z|<=r`; the external reference does not accelerate it. A static frequency response cannot establish a runtime for an arbitrary resonator.

Under coherent-state illumination, physical detector counts are Poisson with the actual half-combined intensity times exposure. A simultaneous Poisson concentration bound may be used to acquire an `eta` budget. At fixed nonzero `R`, fixed dimension and bounded apparatus errors, relative target-power resolution has a sufficient bright-background exposure order `p^(-2)`; this compares with resolving an order-`p^2` intensity signal in the original intrinsic blind family. It is **not a photon/statistical lower bound**, nor a claim against conventional coherent measurement methods.

An explicit conservative sufficient exposure bound is available. If `Y_l~Poisson(N I_l)` with `I_l<=B=(1+R)^2/2`, Chernoff's inequality gives

\[
\Pr\{|Y_l/N-I_l|>\eta\}\le
2\exp\{-N\eta^2/[2(B+\eta)]\}.
\]

The upper-tail form follows from `(1+x)log(1+x)-x>=x^2/[2(1+x)]`; the lower tail is stronger. Thus for `K` charged scalar readings, choosing

\[
N\ge \frac{2(B+\eta)}{\eta^2}\log\frac{2K}{\beta}
\]

makes all detector errors at most `eta` with probability at least `1-beta`. The same conditional bound and union bound hold for adaptive settings with known conditional intensity upper bound; independence across the chosen masks is unnecessary. The launched probe-plus-reference budget is `K N(1+R^2)`, plus calibration exposures, unused source-arm loss, and reset illumination if present. This displays why an unlimited reference is not free. Systematic reference/load/receiver uncertainty is added separately and does not shrink with `N`.

## 7. Exact retained failures

**Uncalibrated target states.** For `n=1,S0=s=0`, take `t=1/4` with target states `0,+-1/2`, or `t'=1/2` with states `0,+-1/8`. The complex returns coincide at every labelled state; matched-target powers are `1/16` and `1/4`. Absolute calibration cannot be inferred from labels, even with a coherent receiver.

**Unbounded relative reference phase.** A no-target return `h_z=A` can be reported as `A(1+ikz)/(1-ikz)` by a load-dependent reference phase error. This equals a false residue `a=2ikA`, pole `s=ik`, baseline `A`, although all bare magnitudes remain `A`. Take `A=1/10,k=1/5`. The false reciprocal two-port has target power `1/25` and is passive by the absolute-row-sum bound. At `r=1/2`, phase factors are `(99+-20i)/101`. Thus reference coherence must be acquired or bounded; residual model fits cannot identify this unrestricted error.

**Nonreciprocity or receiver mismatch.** The residue becomes a product of distinct forward and reverse couplings. The original norm-gauge ambiguity persists, and `p=|a|` is invalid without further acquired structure.

The original stronger harmonic calibration's two physical roots remain valid for that interface. The new observable is a different acquired normalization; it does not erase those original ambiguities by selecting a root.

## 8. Prior-art boundary

Virtual VNA already uses three known distinct target loads and coherent accessible measurements for hidden-port scattering estimation: Philipp del Hougne, *Virtual VNA: Minimal-Ambiguity Scattering Matrix Estimation with a Fixed Set of “Virtual” Load-Tunable Ports*, arXiv:2403.08074, https://arxiv.org/abs/2403.08074. This continuation is a task-specific scalar observable and uniform bounded-error completion. It does not invent coherent detection or three-load tomography. Comparison with the complete current literature is required before any novelty claim.

## 9. Executed evidence

`coherent_three_load_checks.py` runs 303 exact rational algebra/clipping checks and 16 complete scalar queries (192 physical detector readings). The queries include unchanged rational sources, intrinsic harmonic blindness, original single-radius harmonic cancellation, high feedback, zero coupling, bounded load/reference errors, a resolved weak target and an unresolved weaker target. Every acquired interval contains the exact rational target power. Exact twelve-power indistinguishability transcripts are retained for the uncalibrated-load and uncontrolled-reference-phase failures.

`coherent_complete_control.py` uses the separately checked finite `/2` mixture conventional controller in `../access/reciprocal_single_detector.py`, with the new power-oracle adapter. Every source is hidden until after control, trace and final-verification intervals are constructed. Source physics, finite commands, raw powers, synthetic errors and certificates are rational. A numerical eigensolver proposes each two-mode command, whose norm and variational loss are checked exactly. Ten executions pass all target-power containment, trace containment and control-regret checks.

| Source | Raw synthetic detector error | Readings including trace/control/verification | Certified optimum fraction, rounded down |
|---|---:|---:|---:|
| Rational eight-mode seed 120 | 1e-9 | 444 | 0.99999937 |
| Rational eight-mode seed 120 | 1e-5 | 444 | 0.99378720 |
| Rational eight-mode seed 126 | 1e-9 | 444 | 0.99998712 |
| Rational eight-mode seed 126 | 1e-5 | 444 | 0.88458014 |
| Intrinsic blind, four modes | 1e-9 | 204 | 0.99999946 |
| Zero target, four modes | 1e-9 | 204 | 0 |
| Unresolved weak target, four modes | 1e-9 | 204 | 0 |
| Seed 126 with load error 1e-8 and reference phasor error 1e-9 | 1e-9 | 444 | 0.99975024 |
| IEEE 30 GHz model, offline | 1e-7 | 144 | 0.92363076 |
| IEEE 30 GHz model, offline | 1e-10 | 144 | 0.99991943 |

The IEEE model is decoded without symmetrization, rescaling, projection or interpolation by the original `numerical_source` loader, which checks its existing exact numerical reciprocity and passive row-sum bound. The delivered-power intervals are `[8.08220986203525e-5,8.407478981381065e-5]` and `[8.242199975441271e-5,8.242525244560619e-5]`, displayed outwards. They concern the unchanged numerical model and declared synthetic error, not unknown original hardware/model-fit uncertainty. No new physical load sweep was performed.

These richer coherent-interface results are not a matched photon or hardware comparison with the original total-return experiment or OpenWFS. The original comparator and original source files are unchanged. All exact raw transcripts and interval endpoints are saved alongside the results. Float displays are directed outwards, certified fractions downwards, and exact rational values remain authoritative.

Reproduce from any working directory with the archive layout retained:

```bash
python continuation/mechanisms/coherent_three_load_checks.py
python continuation/mechanisms/coherent_complete_control.py
```

## 10. Matching bounded-error exponent for a bounded reference

The linear precision exponent is sharp under fixed bounded reference amplitude. This is another bounded-error indistinguishability statement, not a photon lower bound. Suppose every allowed reference has `R<=Rmax`. For `0<eta<=Rmax+1/2`, put `tau=eta/(Rmax+1/2)<=1` and compare the zero source with the reciprocal passive source `S0=s=0`, `t=sqrt(tau) v`, where `v` is unit. Every unit/subunit input and passive load gives `|h_z(u)|<=tau`. Consequently

\[
\left|\tfrac12|h_z+R e^{i\theta}|^2-\tfrac12R^2\right|
\le R_{max}\tau+\tfrac12\tau^2
\le(R_{max}+\tfrac12)\tau=\eta.
\]

The zero-source transcript is admissible for both sources under simultaneous raw error `eta`, regardless of the number of adaptive settings. Their target Grams differ by norm `tau`, so every estimator has worst-case error at least `eta/[2(Rmax+1/2)]` on one source. For deterministic control in dimension at least two, choose `v` bilinearly orthogonal to the output command on that transcript; regret is `tau`. Thus uniform linear error scaling cannot be surpassed at fixed bounded reference. Permitting an unbounded uncharged reference under a fixed absolute detector-error oracle would change the metrology problem again.
