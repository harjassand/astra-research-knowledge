# Independent desired-operation bus / quantum-eraser audit

**Decision: ACCEPT the qualified declared-model desired-gate proof and five-point exact budget. Reject the original arbitrary-variance record-noise identification; accept the controlling correction.** The bus really supplies the entangling gate in this model. Acceptance is not inherited from either preceding receiver audit and does not establish physical acquisition, novelty, fault tolerance or architectural superiority.

Audit directory: `desired_bus_independent_audit_20261031_2219UTC`.
Original six-file manifest SHA-256: `786acaf6a3c99e758a85a4a913658853648166be3394e1ca609114f3a070aee7`.
Main proof SHA-256: `e0077c981eb118e464c8f85388b8c42e71fd074178d85d70a96912329b049db3`.
Controlling correction SHA-256: `b7f80989467ef8179b9884f6891c2f3bc632b762404b14ef9fff6425bbd27410`.
Qualified binding SHA-256: `3ea9c10a2626b8f0d99edf89f662a3378d50ca8729a03b23003fb98a47f72a86`.

All six original entries and the original manifest were authenticated before copying and rechecked unchanged at completion. `QUALIFIED_BINDING_ROOT.json` and `RECORD_NOISE_SCOPE_CORRECTION.md` were independently inspected and hash-verified. All execution and receipt changes occurred in this unique audit directory.

## 1. A real issue found and resolved

The original Section 4 statement that independent record noise of variance sigma^2 adds `k^2 sigma^2` to `L_eff` is false without a Gaussian assumption. For independent centered noise xi=+/-1/4 with correction gain k=1, the B=+2/-2 coherence is `cos(1)=0.5403023059`, whereas the proposed Gaussian substitution gives `exp(-1/2)=0.6065306597`. Consequently the actual extreme-pair complete-error lower bound is **0.4596976941**, exceeding the wrongly substituted Gaussian diamond prediction **0.3934693403**. This is not merely a different representation of the same channel.

The controlling addendum correctly restricts the exact addition to independent zero-mean Gaussian noise. General independent additive noise contributes its characteristic function `E exp(i k(b-c)xi)`; a nonzero mean adds a deterministic local-B phase. For centered independent finite-variance noise, Taylor's integral remainder for unitary conjugation gives

`||E Ad_exp(i k xi B)-Id||_diamond <= (k^2 Var(xi)/2) diam(B)^2`, capped at 2.

I independently verified this bound: subtract the midpoint scalar from B so `||ad_B||_diamond<=diam(B)`; the linear term averages to zero; each conjugation in the second-order remainder has norm one. This is an extra diamond-error allowance, not an exact Gaussian parameter. The counterexample above obeys its valid upper bound 0.5. Correlated controller noise is outside both rules. The five-point certificate never invokes the faulty extra-noise formula, so no grid number changes.

## 2. Global phase/factorization and warm correlated apparatus

The exact Hamiltonian is a **fixed-B linear spin-dependent force** plus data-independent passive oscillator/port evolution. In the passive interaction picture the drive is linear in canonical quadratures, and its commutator at two times is a scalar times B^2. Thus the Magnus series stops at the second term. Restoring the passive evolution gives the claimed global factorization with terminal oscillator displacement alpha(T), output displacement components sqrt(kappa_j)alpha(t), and phase

`Phi=-Re integral epsilon alpha* = Im integral alpha* alpha' + Delta I`.

The signs agree with the actual oscillator ODE. For closed alpha the original oscillator component vanishes and the output vector has squared norm kappa I, summed over **all** ports. Passive processing only transforms this displacement vector; its phase/sign must be matched by the measured mode and correction. A real implementation containing an additional data-dependent cross-Kerr term B a†a or another nonlinear term is not this exact force model and requires new receiving; no such term is hidden in the proof.

For B=Z1+Z2 and Phi=pi/8, the phase is `exp(i pi/4) exp(i pi Z1 Z2/4)`: the bus itself supplies a maximally entangling ZZ gate, rather than assuming a separate desired ZZ service.

The conditional displacement has one generator quadrature. Its projective measurement followed by the opposite local-B rotation gives an outcome operator factorized into the desired data gate and an apparatus quadrature instrument. This is an operator identity, so full-access erasure works for arbitrary warm apparatus and arbitrary initial data/apparatus/reference correlations. Individual warm-input outcomes may reveal pre-existing correlations and condition the data; the **averaged** corrected data/reference marginal is the desired one. No claim of an outcome-independent warm distribution is needed.

Finite-efficiency formulas are correctly restricted to initially vacuum apparatus. For product nonvacuum input, the lost-mode quadrature characteristic function replaces the vacuum overlap, with the stated second-order energy/variance upper bound available after paying its mean correction. Initial data/lost-mode correlations do not define a data-only channel from the lost marginal. Warm finite-ADC tails also need an admitted joint-input envelope. None of the vacuum numerical claims were promoted to arbitrary warm loss.

## 3. Complete diamond formula and serious minimax challenge

The dephasing kernel is positive. Subtracting the all-ones rank-one kernel gives at most one negative eigenvalue; after weighting by a pure data/reference input, the trace norm equals minus twice that eigenvalue. Orthogonality of the B eigenspaces makes the input/reference representation isometric to the weighted three-level kernel. Replacing the minimizing vector by its absolute values and optimizing jointly with input weights reduces the problem to the stated nonnegative probability quadratic form. Duplicate zero eigenvalues combine; they do not enlarge the optimum.

For extreme weights x,x and central weight 1-2x, the objective is exactly `8w x-4(4w-q)x^2`. Its endpoint/interior maximization proves both branches of the claimed full diamond formula. The branch transition is approximately **L=0.3046889317**. The large-loss limit is 4/3, not the extreme-pair lower bound 1. Tests covered both sides and explicit attaining inputs, not just small-loss numerics.

The unrestricted fixed-gate postprocessing minimax statement also survives challenge. On an encoded Bell input in the B=+/-2 subspace, the two data+collected-field branch vectors are orthogonal because of their data labels, irrespective of their collected-field overlap. The reference-partial-transpose norm is therefore exactly `1+t`, t=exp(-8L). Local CPTP recovery cannot increase that Hermitian trace norm. The Bell projector's partial-transpose operator norm is 1/2, giving recovered fidelity at most `(1+t)/2` and full trace/diamond error at least `1-t`.

As an independent check, I derived a recovery-channel SDP dual witness on this embedded qubit. With Choi objective matrix `C=(|00><00|+|11><11|+t|00><11|+t|11><00|)/4`, dual `Y=(1+t)I/4` has `I tensor Y-C` eigenvalues `0,t/2,(1+t)/4,(1+t)/4`, and identity recovery attains `Tr Y=(1+t)/2`. This independently certifies the Bell-fidelity optimum. Homodyne attains the full diamond lower bound in the small-loss branch, so the stated minimax conclusion follows there. It does **not** establish an unrestricted optimum in the large-loss branch, or against pre-encoding, different trajectories/interactions, squeezed inputs or access to the lost field.

## 4. Finite filter, all ports, records and release

The equal-coupling two-port filter has total energy linewidth 2 beta. Its transmitted field is proportional to z (up to the received port sign), the reflected field to f-z, and its stored displacement energy at the finite endpoint is proportional to z^2/beta. Independent integration verified the exact all-port balance

`integral f^2 = integral z^2 + integral(f-z)^2 + z(endpoint)^2/beta`.

Thus `L=kappa I-eta_d kappa F_W` counts reflection, detector inefficiency and retained filter storage, not just the transmitted tail. At beta8 the independently computed loss partition is approximately: reflection **0.000402998154**, stored filter **3.3367e-8**, detector loss **0.000078136785**, total **0.0004811683054**. The finite tail is not silently collected.

The source trajectory and force were independently propagated, including nonzero detunings with the carrier adjusted to preserve the desired phase. The oscillator closes and Phi=I=pi/8. The sin-squared force is continuous and zero outside the gate, with bounded piecewise derivative; endpoint derivative jumps do not invalidate Lipschitz continuity. Its finite slew does not imply compact spectral support.

The matched-mode, orthogonal homodyne instrument, independent vacuum loss ports, finite ADC law, saturation rule and local rotation strength are real supplied services. The ADC and saturation norm bounds are sound. The general homodyne-angle/gain formula retains its induced B^2 phase; measuring an information-bearing quadrature does not become harmless through local feedback. A terminal displacement residual adds its own orthogonal vacuum component to L, but does not excuse recomputing the actual emitted trajectory or phase after general pulse-calibration changes.

At T the force is exactly off. Remaining oscillator/filter evolution is data independent, so after the declared finite wait and local correction the data may enter noncommuting gates without a reset fiction. Residual force, uncharged electronic/processing delay, and noncommuting continuing noise would require additional bounds. The supplied gamma D[Z_j] commutes with this entire sequence and gives the stated conservative `4 gamma S` addition. The optical filter bandwidth alone certifies neither homodyne electronics nor mode/calibration accuracy.

## 5. Phase/exposure resource lower bound and comparator scope

For the closed absolutely continuous trajectory, integration by parts gives the displayed energy identity. Gauging alpha by `exp(-i Gamma t/I)` and applying the Dirichlet Poincare inequality gives `J-Gamma^2/I >= pi^2 I/T^2`. Substitution proves

`E >= Phi^2/I + (kappa^2/4+pi^2/T^2) I`.

The peak cap implies E<=g^2 T and hence the stated necessary lower root for I. This is a universal lower bound **within the fixed-B, one-pass, vacuum, closed linear-force class**, not an achieved peak-constrained optimum. The Poincare/energy saturator has a sine envelope and nonzero endpoint force; it is not a free finite-slew pulse. The actual sin-squared pulse pays the extra derivative energy. Allowing the unmonitored comparator even discontinuous bounded-force pulses only enlarges its class, making the quoted lower bound conservative and fair.

At the supplied cap g=0.477 the exact occupation lower is **0.11007418683695364**, yielding an unmonitored complete-error lower **0.1614815538202856**. The extreme-pair overlap already gives this lower bound for all larger exposure, even if a different trajectory leaves the small-loss branch. Ordinary data-only postprocessing cannot defeat that Bell-input lost-information bound; encodings, variable B, added Hamiltonians, multiple modes, squeezed/loss-correlated input and coherent field reuse change the premise.

## 6. Exact numerical receiving and executed evidence

The dyadic interval implementation has correct outward arithmetic, reciprocal and square-root enclosures. Machin's pi formula uses valid alternating-series brackets. The positive-exponential Taylor remainder is bounded by the stated geometric tail at scaled argument <=1/8; reciprocal and repeated interval squaring correctly enclose the negative exponential. Dependency overestimation is conservative. Small-loss branch membership is certified by an interval-separated margin, not assumed from decimal plots.

| beta | exact bus diamond | supplied total upper | <=0.01? |
|---:|---:|---:|:---:|
|1|0.1157228286|0.1196472114|No|
|2|0.0429469551|0.0466718739|No|
|4|0.0129133782|0.0165384966|No|
|8|0.0038419472|0.0074171237|Yes|
|16|0.0014414707|0.0049916624|Yes|

- Author **72 checks** and all six finite-Fock diagnostics passed. Exact `bus_certificates.json` replayed **byte-identically**. Three floating optimizer-error decimals in the author test log changed by less than 9e-16; the log is therefore not claimed byte-identical.
- `independent_bus_audit.py`: **211 assertions**, including the exact recovery-SDP dual witness, arbitrary-reference diamond tests, warm correlated erasure with a reference and nontrivial passive preprocessing, actual bus phase/closure, all-port filter energy receiving, and the explicit record-noise counterexample.
- `independent_interval_and_noise_audit.py`: **58 independent 130-digit interval checks** over all certificate fields and **60** arbitrary-reference checks of the corrected centered non-Gaussian noise bound. High-precision evaluations are diagnostics; the interval and geometric proofs were separately reviewed.
- Finite-Fock agreement is not an infinite-mode certificate. The exact linear-unitary/Magnus argument supplies the infinite-mode theorem under its actual model premises.

## 7. Paid services, ordinary ownership and completion

The desired operation is earned as a mathematical supplied-model construction. Spin-dependent force access, faithful oscillator linearity over admitted warm sectors, all bath states/ports, optical routing, matched local oscillator, homodyne response, ADC range/accuracy, timing, local control, shutdown and residual calibration remain physical inputs. In particular the additional **0.001** complete-error allowance is supplied, not calibrated. The same available resources must be offered to competing architectures.

Ordinary precedent remains the owner of the principle: [Leroux et al.](https://eapg.mit.edu/wp-content/uploads/2018/03/pra_85_013803-cavity-squeezing-q-eraser.pdf) explicitly preserves useful collective interactions through quantum erasure; [Louis et al.](https://arxiv.org/html/0804.3240) analyzes loss and symmetrization in qubit-bus gates; [Barrett and Milburn's accessible abstract](https://arxiv.org/abs/quant-ph/0607206) describes bus-mediated gates using homodyne and local operations. These are primary context checks, not claims that their physical models equal this one or that hardware is available. No inaccessible-source retry or historical novelty claim was used.

**Completed:** independent whole proof and minimax challenge, actual phase/filter/all-port/release scope review, exact bindings/replay, counterexample and accepted correction, cost/comparator review, receipt. **Denied actions:** none. **Pending/uncertain:** acquisition and calibration of the listed physical services and broad architecture comparison; no execution remains running. No equipment, outreach, purchases, publication, external/helper agents or frozen-input mutations occurred. One audit-only symbolic assertion initially compared algebraically equal SymPy expressions structurally; that harness check was corrected and rerun successfully. The candidate issue is the separately documented record-noise assumption, now controlled by the accepted addendum.
