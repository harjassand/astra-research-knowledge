# Finite binary replenishment with an actual failure record

**Author:** `producer-workspace/architecture_challenge`, 29 October 2026. This is a new integration result, separate from the frozen pump author package and from the parent's energy-balanced-erasure proof. Independent review is a separate artifact.

## 1. Consequence and exact interface

A finite normalized pump need not enter the completed measured gadget with its worst purified amplitude error. With the supplied finite carrier Hamiltonian, a selective failure measurement and ordinary calibrated polar feedback, the **complete actual-record channel** has exactly

\[
\boxed{\tfrac12\|\Phi-\Psi\|_\diamond=\|F\|
\le \|S^2\|\sin^2\delta\le\sin^2\delta.} \tag{1}
\]

Here F is the actual failure effect, all failures are included, and Psi is the corrected identity gadget with a uniform eraser bit and no failure. No success postselection or renormalization is used. If the complete measurement purification remains a coherent returned output, the matched coherent-channel distance is instead sqrt(||F||); the two output contracts are different.

The input is a finite logical space already physically encoded by V_N, possibly entangled with an arbitrary reference. One exact captured binary collision has commuting Hermitian amplitudes

\[
C=\cos\Theta(Q),\quad S=\sin\Theta(Q),\quad C^2+S^2=I.
\]

For example Theta(Q) = theta sqrt(N-Q) is an acquired two-level output collision. This is not an assertion that a finite bosonic Markov interval emits at most one photon. The original captured output E must remain coherent until the eraser; an inaccessible copied count violates the interface.

Apply the exact two-sector selector and finite resonant pump of `../pump/FINITE_NORMALIZED_PUMP.md`, Sections 2 and 4, including its known phase corrections. On the one-loss number window define

\[
D(Q)=\sin\vartheta_{N-Q-1},\quad
T(Q)=\cos\vartheta_{N-Q-1},\quad D^2+T^2=I,
\quad D\succeq\cos\delta I. \tag{2}
\]

On a vacuum sector with S = 0, D and T may be defined arbitrarily with this identity; no negative Fock state is used. The actual premeasurement state has the form

\[
V_N C|\psi\rangle|e,0\rangle_{AE}
+V_N DS|\psi\rangle|g,1\rangle_{AE}
+J TS|\psi\rangle|r,1\rangle_{AE}. \tag{3}
\]

J maps the supported failed component into the lower-number physical sector. A known common failure phase is absorbed in J. The failed data-plus-battery output is off the intended code and is kept or retired through an explicit failure channel. The first two terms share the restored encoding. All C,S,D,T commute because they are functions of Q.

The selector is exact in this nominal model; detuning, carrier-pulse, phase and readout imperfections receive additional implementation allowances. In particular, an imperfect selector can leave one-loss population in carrier e, which the r-only flag would not catch. Equation (1) does not silently cover that error.

## 2. Physical instrument and actual record law

First measure **r versus span(e,g)** with the complete Luders instrument

\[
P_f=|r\rangle\langle r|,\qquad
P_s=|e\rangle\langle e|+|g\rangle\langle g|. \tag{4}
\]

No apparatus, including unobserved apparatus, may resolve e from g on the successful branch. The failure flag becomes an actual irreversible classical record: its purification is retired and does not return to interact. A mere public coarse label is insufficient if an inaccessible apparatus has also copied e/g.

The completed state must be block diagonal in this flag jointly with every returning port and arbitrary reference. Classicality of the public record marginal alone is insufficient.

Given success, the AE vectors |e,0> and |g,1> have equal actual energy under the pump's equal-gap assignment. Measure their Y basis. With consistent fixed outcome phases, the two source Kraus operators before feedback are

\[
M_\pm=(C\pm iDS)/\sqrt2.
\]

Let

\[
F=S^2T^2=S^2(I-D^2),\quad R=\sqrt{I-F},\quad
U_\pm=(C\pm iDS)R^{-1}. \tag{5}
\]

On the support of R these U are unitary; extend them arbitrarily on its kernel. Apply the ordinary polar recovery U_pm-dagger, controlled by the actual eraser bit. This leaves

\[
K_\pm=R/\sqrt2. \tag{6}
\]

There is no inversion of the positive filter R. Except when F is scalar, normalized successful runs are not the identity channel. Feedback is a known phase function of Q; for two admitted charges it is one relative Z phase. A larger charge set requires an acquired nonlinear charge-controlled phase implementation and calibrated D, C and S.

Let Fcal be any specified completely positive failed-output map with

\[
\mathcal F^\dagger(I)=F. \tag{7}
\]

Keeping the raw off-code output in (3) is one choice. Retiring it and emitting an abort state is another; the reference's conditional state is still determined by that CP map, not replaced by an invented independent reference state.

After identifying the successful encoding with the logical output, the complete instrument is

\[
\Phi(\rho)=\tfrac12\sum_{k=\pm}|0,k\rangle\langle0,k|\otimes R\rho R
+|1,\bot\rangle\langle1,\bot|\otimes\mathcal F(\rho). \tag{8}
\]

The actual law is p(1,bot|rho) = Tr(F rho) and p(0,k|rho) = [1-Tr(F rho)]/2. The eraser bit is uniform conditional on success. The failure probability can depend on the input; the whole record is not claimed independent. Equation (8) is trace preserving and retains all failure probability.

The ideal comparison is

\[
\Psi(\rho)=\tfrac12\sum_{k=\pm}|0,k\rangle\langle0,k|\otimes\rho. \tag{9}
\]

Known actual postmeasurement AE/pointer states depending only on (flag,k) can be appended to both instruments without changing their distance. Thus (8)--(9) include the successful carrier, captured field and actual records, rather than treating their disposal as unproved factorization. Failed outputs may be arbitrary subject to (7).

## 3. Exact complete-record distance: a reusable positive-filter lemma

**Lemma.** For any finite effect 0 <= F <= I, put R = sqrt(I-F). For every CP map Fcal satisfying (7), the channels (8)--(9) obey

\[
\tfrac12\|\Phi-\Psi\|_\diamond=\|F\|. \tag{10}
\]

The lemma does not require F to commute with an input density operator. It holds with an arbitrary reference and arbitrary quantum failed outputs. The diagonal pump structure is used to obtain (6), not in this norm statement.

**Proof.** Set m = ||F|| and r = sqrt(1-m). It suffices to bound a pure input |psi> on source plus reference: mixed inputs follow by convexity, and a difference of channels attains its diamond distinguishability on a reference-extended state. Define

\[
p=\langle F\otimes I\rangle,\qquad
q=\langle R\otimes I\rangle,\qquad 0\le p\le m.
\]

The successful blocks together contribute the trace norm of

`|phi><phi| - |psi><psi|`, where |phi> = (R tensor I)|psi>,

and the failed block is positive with trace p. The exact rank-two trace-norm formula therefore gives

\[
\tfrac12\|(\Phi-\Psi)\otimes\mathrm{id}(|\psi\rangle\langle\psi|)\|_1
=\frac{p+\sqrt{(2-p)^2-4q^2}}2. \tag{11}
\]

The scalar square-root function lies above its chord on [0,m], hence

\[
R\succeq I-\frac{F}{1+r},\qquad q\ge1-\frac p{1+r}.
\]

The following exact factorization controls the remaining expression:

\[
\left(1-\frac p{1+r}\right)^2-r^2(1+m-p)
=\frac{(m-p)\{m(1+r)^2-p\}}{(1+r)^2}\ge0. \tag{12}
\]

Thus q^2 >= (1-m)(1+m-p). Substitution implies

\[
(2-p)^2-4q^2\le(2m-p)^2,
\]

where 2m-p >= 0. Equation (11) is at most m. For the matching lower bound, take a maximum-eigenvalue input of F and read only the failure flag. Its actual failure probability is m and its ideal failure probability is zero; the record total-variation distance is m. This proves (10). The m = 0 and m = 1 endpoints are included. QED.

The lower bound applies to any further correction that **preserves the actual flag** and uses the same no-failure ideal target. The polar construction therefore attains the best possible complete-record comparison under that specific target, even if failed data could otherwise be rescued. This is not a physical error floor: deleting/redefining records, allowing a different ideal record law, or redesigning the pulse is a different comparison. We make no claim of global source-only recovery optimality from (10).

Combining (2), (5) and (10) proves (1). The sharper quantity is the actual m = max_Q [S(Q)^2 cos^2(vartheta_(N-Q-1))]; sin^2(delta) is a sufficient bound and can be loose when a loss itself is unlikely.

## 4. Why the coherent-output metric is different

Purify the failure operation and keep every flag/readout purification coherent. After coherent polar feedback, the actual isometry has successful part |success-record> R and orthogonal failed part L with L-dagger L = F. The ideal has only the successful part. Their overlap is exactly R. Consequently

\[
\|V_{\rm coh}-W_{\rm coh}\|
=\sqrt{2(1-\sqrt{1-m})},\qquad
\tfrac12\|\mathcal V_{\rm coh}-\mathcal W_{\rm coh}\|_\diamond=\sqrt m. \tag{13}
\]

For the second identity, any pure reference-extended input has output overlap q >= sqrt(1-m), giving trace distance at most sqrt(m); a maximum-eigenvalue input attains it. Retiring the measurement purification converts the coherent branch relation into the actual cq instrument (8) and changes the operational output contract. It does not invalidate the original O(delta) purified pump estimate.

### A decisive coarse-record failure

Take D = I, C = |0><0| and S = |1><1|. The nominal failure effect is zero. The genuine coherent Y eraser and polar feedback perfectly correct the operation. But suppose the successful flag apparatus secretly copies e versus g into an inaccessible register, while publicly reporting only success. The cross terms between C and S are then lost. The same subsequent Y measurement and feedback yield complete Z dephasing, with a uniform visible eraser bit. Its source half-diamond error is 1/2, attained by |+>, despite the nominal F = 0. Thus observing only a coarse public flag does not certify the required complete Luders instrument.

## 5. Finite port, record and reuse ledger

The construction requires the full following interface, not only a three-outcome abstract instrument.

1. **Input and collision.** A prepared V_N encoding, an exact two-level captured output collision with calibrated phases, and coherent collection of E before any lost count copy. The source's arbitrary reference is retained. The parent multi-loss theorem and this binary finite instance have different collision contracts.
2. **Finite pump.** The exact supplied selector Hamiltonian, its carrier phase correction, and the finite resonant cavity pulse. The e/r carrier manifold must have the specified physical energy assignment for reference-free erasure. The source-charge dispersive access and absolute-offset calibration remain paid. Noncommuting data operations are paused; this is not a continuously driven bath theorem.
3. **Selective failure readout.** A pure pointer can be coupled by a controlled flip on r, preserving the entire e/g subspace. For example, with a degenerate pointer, `H_flag = J_flag P_r tensor X_pointer` for time pi/(2 J_flag) implements a flag up to a known failed-branch phase. A complete irreversible readout then retires its dephasing purification. Pointer preparation, timing, readout, retirement and later record reset are actual operations. The measurement must not leak e/g anywhere.
4. **Forward carrier and eraser.** Send A to the captured E. In the equal-energy span {|e,0>,|g,1>}, an acquired exchange of strength J_mix for time pi/(4 J_mix) implements a balanced mixer; subsequent number/internal-state readout realizes the Y instrument up to known outcome phases. Capture, travel, phase stability, spectral selectivity, detection and classical feedback latency remain paid. Success-orthogonal states have explicit extra measurement outcomes; they have zero weight only in the nominal promised model.
5. **Feedback and outputs.** Apply the phase exp[minus/plus i arg(C+iDS)] for the plus/minus outcome, as an acquired charge-controlled operation. Actual successful apparatus states and the full (flag,k) record are retained. Failed data-plus-battery output is kept off-code, or an explicit abort map retires it. No failed run is erased from the workload statistics.
6. **Holding and reuse.** The data, battery and coherent captured E must survive the actual critical path. Carrier reuse, pointer reset, record storage, forward supply and classical return all have finite service costs. A coherent cell pays selector and flag service even when no loss occurred. A vanishing collision time does not supply infinitely fast service.

These ports also permit strong conventional alternatives. With actual coherent field return, reversing the captured collision can be simpler. With a known Fock state and an allowed classical boundary, a directly calibrated pump is exact. Given the same eraser outcomes, ordinary polar recovery is already the strongest relevant conventional correction; the finite integration uses it rather than claiming a new recovery principle.

## 6. Implementation error and pump-time loss

Let epsilon_j be uniform complete-channel allowances for the actual encoder/input, collision model, capture, selector/pulse calibration, flag instrument, transport and hold, eraser readout, feedback and reset. With compatible causal memory boundaries, ordinary channel composition yields

\[
\tfrac12\|\widetilde\Phi-\Psi\|_\diamond
\le\min\{1,m+\sum_j\epsilon_j\}. \tag{14}
\]

These are complete interface contracts, not marginal failure probabilities or an independence assumption. This file does not establish a many-gate threshold or allow later interaction with a retired flag purification.

In the companion pump's stated Markov model, extra pump-time emissions G may be irreversibly retired and charged by `epsilon_pump_noise <= r_max tau`. The **intended collision field E stays coherent** throughout this estimate and can be included in the reference system of that bound. If G itself is required as a coherent output, use the different sqrt(r_max tau) dilation allowance. The r-only flag need not diagnose these extra processes; they are already part of the additional complete-channel budget.

Physically separating these later G ports from stored E, and preventing G from returning, requires a supplied timing/routing/retirement interface. Temporal separation and free disposal are not inferred from different algebraic labels.

A population-transfer calibration alone does not establish the real common-phase D assumed in (2). Number-dependent pump phases can make the two eraser effects unequal; a selector error can put an off-code component inside span(e,g). Both must be corrected by acquired controls or bounded in epsilon_j. The quadratic term m does not absorb arbitrary control, preparation or readout errors.

## 7. Ancestry, checks and scope

The polar feedback in (5)--(6) is standard environment-assisted correction. Gregoratti and Werner, *On quantum error-correction by classical feedback in discrete time*, arXiv:quant-ph/0403092, section IV A, Proposition 4 and its proof, explicitly construct the inverse unitary from a Kraus operator's polar decomposition: https://arxiv.org/pdf/quant-ph/0403092 . Their channel-fidelity statement is not relabeled as our complete-record diamond statement. The earlier pump package supplies its own STIRAP/normalized-addition ancestry and physical port caveats.

`finite_binary_checks.py` and its JSON output separately test exact rational instrument identities, the exact inequality factorization, arbitrary-reference output-distance fixtures, the actual finite selector/pump matrices, and the hidden-copy negative control. Floating matrix tests are diagnostics, not an interval proof. This author's derivation establishes (10) directly.

What becomes possible is a finite, completely specified measured cell whose pump mismatch enters its retained-record budget at the actual failure probability, while source filtering and off-code failed output remain included. It is a local operation bridge, not an acquired device, an advantage over unrestricted coherent reversal, or a fault-tolerant computer. No historical-priority claim is made for polar recovery, a selective flag, or the general idea of heralding.

**Contribution provenance.** The parent proposed the finite selective-flag/eraser integration and independently supplied an alternate proof of the exact norm lemma after this branch had derived and written its factorization (12). Agreement between these derivations is not represented as an independent review of either author's result. New executable checks here were written without importing predecessor author code.
