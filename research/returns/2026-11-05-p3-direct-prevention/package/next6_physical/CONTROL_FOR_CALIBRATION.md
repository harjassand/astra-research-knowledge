# Recovering an unknown quantum input without learning its Hamiltonian

## Status and selected independent question

**Completed conditional construction.** A known pure, coherently collected Markov reservoir can be retained while an unknown bounded source Hamiltonian is randomized away. A full source-plus-output estimate, followed by the already accepted noise-only reset/export instrument, recovers an arbitrary unencoded quantum input and its reference correlations. The source Hamiltonian is never estimated. Every positive reset rate is allowed.

The additional physical access is calibrated single-site coherent control on the source. This access was absent from the output-only calibration theorem. Its strength, slew, accuracy and total pulse action are paid. The construction does not replace the accepted finite field receiver with a cheap ideal buffer, and does not establish a practical device or a same-access optimality separation. Randomized dynamical decoupling is established machinery; the new operation here is the explicit covariant **retained-output** interface and its composition with export, including finite source pulses. It is an independent alternative to the acquired classical decision programme, not a claim that this is its strongest destination.

The question is different from preserving a state in the source. The source is deliberately depolarized. The required quantum information leaves through the accessible reservoir, whose coherent state must remain correct for a decoder that does not know the drift. A small error in the reduced source channel alone would not establish this.

## 1. The source, the target, and the supplied access

There are n qubits S. At the start, their joint state with any inaccessible reference R is arbitrary. No known encoding, calibration copy of that state, source reset, or source-to-memory SWAP is supplied. The input and R are independent of the fresh controller random bits and initially independent of the receiver.

The uncontrolled source generator is

\[
\mathcal L_t(\rho)=-i[H(t),\rho]
+r\sum_{i=1}^n\bigl(\mathcal D_i(\rho)-\rho\bigr),
\quad
\mathcal D_i(\rho)=\frac{I_i}{2}\otimes\operatorname{Tr}_i\rho .
\tag{1}
\]

Here r>0 is calibrated. The actual pure vacuum dilation has ports

\[
L_{i,a}=\frac{\sqrt r}{2}\sigma_{i,a},
\qquad a\in\{X,Y,Z\}.
\tag{2}
\]

Every one of these ports is available with known phase and no unbudgeted loss. Its physical photon count intensity is r/4, so the total intensity is 3nr/4. Classical records of jumps, a mixed bath without its purifier, or only one commuting dephasing output do not satisfy (2).

After an irrelevant scalar is removed, a known bound

\[
\|H(t)\|\le\Lambda
\tag{3}
\]

holds for every time used. For a local Pauli expansion with a known summed per-site coefficient bound J, one may take \(\Lambda=nJ\). Locality is useful for such a bound but is not needed in the theorem itself. The coefficients, interaction graph, or a bounded list of local terms need not be learned. A complete bound (3) and the Markov model remain structural promises. An unknown omitted Hamiltonian, loss channel, or feedback-dependent bath is not excluded by this operation.

The drift may be a fixed unknown H or a predetermined measurable H(t). It must be independent of the fresh random frame in the block in which it acts. An adversary who observes the current frame and changes H(t) to undo it is outside the statement. No temporal smoothness of H(t) is required for the ideal-channel estimate.

The source has calibrated local X, Y and Z rotations. These are genuine source operations, not virtual changes of coordinates. Their finite-pulse interface is specified in Section 5. The receiver retains the necessary output coherently, makes known output-frame corrections, applies the noise-only export instrument, and preserves its quantum memory until completion. All receiver errors and resources remain as in the accepted coherent-port constructions. The target is the identity channel from the initial S to n receiver qubits, in the **unhalved diamond norm**.

## 2. The full-output covariance that is needed

Let g be a tensor product of one-qubit Pauli matrices. For each port,

\[
g^\dagger\sigma_{i,a}g=\chi_{i,a}(g)\sigma_{i,a},
\qquad\chi_{i,a}(g)\in\{-1,1\}.
\tag{4}
\]

Let \(\mathsf R_g\) be the second-quantized output phase operation that multiplies a photon in port (i,a) by \(\chi_{i,a}(g)\). It acts on every photon in the selected time interval and fixes vacuum. If \(V_H(t)\) is the actual pure source-plus-output isometry of (1)–(2), its calibrated dilation obeys

\[
(g^\dagger\otimes\mathsf R_g)V_H(t)g
=V_{g^\dagger H(\cdot)g}(t).
\tag{5}
\]

This follows directly by conjugating each source coupling in the quantum stochastic equation and compensating its sign in the corresponding vacuum field. It includes all photon sectors and arbitrary source-reference inputs. No physical Markov reservoir interaction is turned off by this identity.

For qubits, the output correction is only a known phase sign on each port and time interval. It can be performed after field capture on the retained mode registers. The proof therefore does not assume an infinitely fast optical phase switch at the source. It does assume that the finite receiver can resolve and coherently process the required intervals, and pays that resolution.

Reduced-channel covariance is insufficient. Two devices can both erase S to I/2 while exporting U|psi> and V|psi> to their environments. The source marginals are identical, but a single decoder cannot generally invert both unknown output rotations. Equation (5), for the **actual known dilation**, supplies the missing information.

## 3. A general covariant-output averaging lemma

The following statement is useful beyond depolarization.

**Lemma.** Let a known reference unitary dilation U_0(t) have bounded added source drift H(t), with \(\|H(t)\|\le\Lambda\). Suppose a finite random control group and implementable output correction realize the drift-conjugated dilation as in (5). Suppose

\[
\mathbb E_g\,g^\dagger H(t)g=0
\quad\text{for every }t.
\tag{6}
\]

For a block of duration d, after the output correction and after averaging over g, the complete source-plus-output channel \(\overline{\mathcal V}_d\) satisfies

\[
\boxed{
\|\overline{\mathcal V}_d-\mathcal V_{0,d}\|_\diamond
\le 2\Lambda^2d^2 .}
\tag{7}
\]

The reservoir Hilbert space need not be finite dimensional and its free generator need not have bounded operator norm. The drift in the reference interaction picture must be bounded as stated.

**Proof.** On the source and the field, remove the reference dilation. The remaining unitary Y_g(t) solves an ordinary bounded-perturbation integral equation with

\[
K_g(t)=U_0(t)^\dagger(g^\dagger H(t)g\otimes I)U_0(t),
\quad \|K_g(t)\|\le\Lambda.
\]

Let \(\mathcal A_g(t)=-i[K_g(t),\,\cdot\,]\) and let \(\mathcal Y_g(t)\) be the unitary channel of Y_g(t). A second-order integral expansion gives

\[
\mathcal Y_g(d)=I+\int_0^d\mathcal A_g(t)dt
+\int_0^d\!dt\int_0^t\!ds\,
\mathcal A_g(t)\mathcal A_g(s)\mathcal Y_g(s).
\tag{8}
\]

The first-order integral vanishes after averaging, because U_0 does not depend on g and (6) holds pointwise in time. Also \(\|\mathcal A_g(t)\|_\diamond\le2\Lambda\) and \(\|\mathcal Y_g(s)\|_\diamond=1\). The averaged remainder has norm at most \((2\Lambda)^2d^2/2\). Restore U_0 and append the vacuum input. These are complete-norm contractions. The result is (7). This argument uses no bath cutoff, weak-coupling expansion, source-only trace, or convergence assumption for a Magnus series. QED.

Uniform independent tensor-product Paulis satisfy (6) for every traceless n-qubit H. Although the group has 4^n elements, one sample costs exactly 2n independent fair bits and n local choices; enumeration of the group is unnecessary.

Now divide a useful collection time T into B blocks of duration d=T/B. Choose a fresh independent frame g_j in each block. In the logical frame, each block is a channel acting on S while all earlier output is retained as a reference. Composition and the hybrid inequality yield

\[
\boxed{
\|\overline{\mathcal V}_{T,B}-\mathcal V_{0,T}\|_\diamond
\le \frac{2\Lambda^2T^2}{B}.}
\tag{9}
\]

This is a whole retained-output estimate, not only an estimate on S. It remains uniform when earlier source-output entanglement is present.

### 3.1 What is and is not averaged

The random key is used to implement the output-frame correction. The target of (9) excludes that classical key; it is discarded after use. There is no per-seed diamond guarantee. Retaining the key as an additional output and requiring it to be independent of the recovered state is a different, generally false quadratic claim.

For example, with no reservoir and H=omega Z on one qubit, a uniform Pauli frame yields the average of the +omega and -omega unitary channels. Its diamond distance from the identity is

\[
2\sin^2(\omega d).
\]

If the sign key is also returned, the joint classical-quantum distance is

\[
2|\sin(\omega d)|
\]

for \(|\omega d|\le\pi/2\). The accepted operation averages a physical randomized channel and preserves arbitrary input-reference correlations in that channel. It does not condition on a lucky key.

Fresh randomness can be generated just before the relevant pulse. A finite random generator with total distribution error nu adds at most 2nu to the unhalved diamond error. The proof does not replace true randomness by an unproved pseudorandom generator. Classical memory and eventual disposal of 2nB key bits are resources; no energy cost for their erasure is claimed to be zero.

## 4. Why the noise-only decoder completes recovery

For H=0, the reduced one-qubit channel at useful time T is

\[
\mathcal N_T=e^{-rT}\,\mathrm{id}+(1-e^{-rT})\mathcal D.
\tag{10}
\]

The accepted pure-output reset/export instrument is a physical operation on the calibrated Stinespring environment of (10). It has a payload-independent flag: with probability \(e^{-rT}\), no export; with probability \(1-e^{-rT}\), it exports the exact input qubit, including every reference correlation, and leaves a maximally mixed source with its accessible purifier. It is not inferred from a classical jump record.

Use that instrument independently on the n H=0 local output factors. On the all-export branch, the receiver obtains the exact joint initial state, including arbitrary entanglement across sites and with R. On every other branch return a defined n-qubit state. The branch probability is input independent. Thus the complete, unconditional decoder \(\mathcal D_T\) satisfies the direct bound

\[
\|\mathcal D_T\circ\mathcal V_{0,T}-\mathrm{id}\|_\diamond
\le2\bigl[1-(1-e^{-rT})^n\bigr]
\le2ne^{-rT}.
\tag{11}
\]

The output correction first concatenates the useful physical-time intervals as known mode labels. This is relabeling of stored temporal modes, not a source-side delay line or a free buffer. In the H=0 logical reference, the intervals compose to exactly (10).

Combining (9) and (11) gives the ideal randomized recovery estimate

\[
\boxed{
\|\mathcal R_{T,B,H}-\mathrm{id}\|_\diamond
\le2ne^{-rT}+\frac{2\Lambda^2T^2}{B}.}
\tag{12}
\]

Every r>0 is permitted. There is no condition that r exceed an operator-growth coefficient. The price appears in T, B, and the control demands below. The exact finite-time flag law is asserted for the H=0 reference instrument. When the instrument is applied to the actual controlled unknown-H output, its complete channel is close by (12); exact payload-independent flag probabilities or an exact actual stopping certificate are not separately claimed.

## 5. Finite source pulses and real discarded intervals

An instantaneous pulse is not part of the physical theorem. Insert P=B+1 pulse windows of duration at most w, including the initial frame, the changes between frames and the final return. All windows have the same scheduled length, even for an identity local operation, so block times do not depend on the random key. The source continues to evolve during each pulse. Discard the output in those windows; only the dwell output is retained for (12).

During a pulse, the actual source generator consists of the intended known local control plus H(t) and the depolarizing generator. In the control interaction picture, the latter two terms have complete norm at most

\[
2\Lambda+2nr.
\]

Tracing the pulse output produces precisely this reduced Markov channel, also when S is correlated with every earlier retained output. Duhamel's formula therefore compares it with the intended noise-free local unitary at cost at most \(2(\Lambda+nr)w\). Summing over windows yields

\[
\epsilon_{\rm pulse}\le2(\Lambda+nr)Pw.
\tag{13}
\]

This charge includes the quantum information actually lost to the discarded pulse output. That loss has not been hidden by assuming that the reservoir is switched off. Its linear form is justified because this interval's output is traced; an unproved full-field time-translation bound is not used.

A smooth one-axis pulse on each affected qubit is

\[
H_{c,i}(t)=\frac{\pi}{w}\sin^2(\pi t/w)\,\sigma_{i,a},
\qquad 0\le t\le w .
\tag{14}
\]

Its area is pi/2, hence it implements the required Pauli up to an irrelevant phase. Its maximum one-site Hamiltonian norm and slew are

\[
G=\frac\pi w,\qquad S=\frac{\pi^2}{w^2}.
\tag{15}
\]

Parallel local pulses implement a tensor-product Pauli. Unknown drift during the pulse is already included in (13); it is not silently calibrated away. The total source control action is at most \(nP\pi/2\), and there are at most nP nonidentity local rotations. Electrical dissipation and conversion from Hamiltonian action to laboratory energy depend on the actuator and are not supplied by these numbers.

Calibration error in pulse axes and areas is additional. If, conditional on every prior history, the complete error of pulse round j after removing its bounded drift/noise charge is at most e_j, then \(\sum_j e_j\) adds to the recovery error. Independence between repeated pulse errors is unnecessary. For an area error a_{i,j} about the correct axis, the elementary sufficient charge is \(2\sum_{i,j}|a_{i,j}|\); axis or leakage errors need their own calibrated complete-channel envelope. A faithful calibrated control port is substantive access, not a property inferred from this unknown specimen.

Clock uncertainty can be handled with guard intervals around pulse boundaries. Outputs in the guards are also discarded, and their total physical duration adds to Pw in (13). Retained intervals must lie where the logical frame is certified constant. Receiver mode/timing errors are separately charged as in Section 7. The clock's bit count is not a certificate of its physical phase or drift accuracy.

## 6. Explicit finite prescription

Fix 0<epsilon<1, with Lambda>0. Take

\[
T=\frac1r\log\frac{8n}{\epsilon},\qquad
B=\max\left\{1,\left\lceil\frac{8\Lambda^2T^2}{\epsilon}\right\rceil\right\},
\quad P=B+1,
\]

\[
w=\frac{\epsilon}{8(\Lambda+nr)P}.
\tag{16}
\]

Then the three ideal mathematical charges are each at most epsilon/4:

\[
2ne^{-rT}\le\epsilon/4,
\qquad 2\Lambda^2T^2/B\le\epsilon/4,
\qquad 2(\Lambda+nr)Pw=\epsilon/4.
\tag{17}
\]

Allocate the remaining epsilon/4 to control calibration, finite coherent receiver, port calibration, memory, key distribution, gates, timing and classical arithmetic. A small initial receiver guard can be carved out of the pulse/lost-interval allocation by shortening the individual windows; it is not an additional free interval. With these allocations the returned quantum channel has diamond error at most epsilon. If a calibration envelope is established only on a confidence event of probability at least 1-delta, state that separately; unconditional failure mixtures can cost another 2delta in this norm.

The known-H noise-only case Lambda=0 can omit the randomized control completely and use (11). The recipe's B=1 branch is not a claim that a pulse is necessary there.

At fixed per-site bound J, with Lambda=nJ, the prescription has

\[
B=O\!\left(\frac{n^2J^2}{r^2\epsilon}\log^2\frac n\epsilon\right),
\]

\[
G=O\!\left(\frac{n^3J^2(J+r)}{r^2\epsilon^2}
\log^2\frac n\epsilon\right),
\quad S=G^2,
\tag{18}
\]

up to fixed pi constants. These are sufficient bounds, not lower bounds. Fixed installed strength G_max and slew S_max need w at least \(\max\{\pi/G_{\max},\pi/\sqrt{S_{\max}}\}\) for the chosen waveform. If that contradicts (16), this prescription is unavailable at that hardware budget. Nothing here proves that a better control sequence cannot work.

The source-operation wall time is T+Pw, plus supplied guards and propagation. Expected useful output photon count is 3nrT/4. These small counts do not imply that the required temporal modes are cheap to collect or process.

## 7. The finite coherent receiver remains a real resource

The accepted P1 bounded-component receiver has a passive splitter array, cascaded two-level capture cells, finite response poles, actual propagation, stationary processing, protected quantum memory, and finite timing/phase errors. It can be applied here; it is not replaced by an ideal instruction to save a field.

The required interface is uniform capture of the selected temporal modes of the **actual controlled** Weyl output. The original receiver proof's photon-count argument is independent of H: each marked Weyl-jump Kraus operator is a scalar times a product of unitary source propagators and Pauli operators, giving the state-independent Poisson intensity 3nr/4. It therefore still bounds all actual outputs, including during the finite pulses and readout guards.

For the mode/source approximation, use the known bound

\[
\|H(t)+H_c(t)\|\le\Lambda+nG
\tag{19}
\]

and a finite partition containing every pulse/dwell boundary. The pulse waveform and all selected mode labels are known; unknown source coefficients are not needed to choose norm-based bin sizes. The finite capture maps act on the field independently of those coefficients. The receiver's normalized one-jump-per-bin and mode estimates use norm bounds, not a fitted H. Its decoding stage here uses H=0; no inverse of the unknown source evolution is requested.

The earlier source-start omission was sometimes undone by a known U_H inverse. That step is unavailable here. Instead discard the initial receiver guard of duration t_0 and pay \(2(\Lambda+nr)t_0\), as in (13). Place it in the finite lost-interval budget. The required t_0 is positive and may be inverse polynomial; the accepted fixed-response capture prescription supports this by a growing array. One must retain the exact original guard/hardware closure and its actual propagation costs.

For fixed q=2 and a finite polynomial source-control schedule (16), all supplied norm, time, bin-count and inverse-accuracy arguments to that receiver are polynomial. Its resulting array, classical compiler, protected storage and processor costs therefore remain finite and polynomial in those arguments at the accepted scope. This is a composition statement; the receiver's already enormous sufficient constants are not improved. The prior one-qubit greater-than-10^112-cell recipe is not reinterpreted as practical hardware.

A convenient conservative way to understand temporal precision is to use a physical photon cap Q and M selected flat-bin modes. A shift of at most eta_t in a bin endpoint changes its normalized mode by at most \(\sqrt{2\eta_t/d_{\min}}\), up to the analogous allowance for both endpoints. Bounding the resulting one-particle map error by a Frobenius norm gives a sufficient scale

\[
O\!\left(Q\sqrt{M\eta_t/d_{\min}}\right)
\tag{20}
\]

for the complete-channel error on the capped sector. The exact accepted mode/guard bounds govern implementation. Equation (20) illustrates why timebase accuracy is a physical condition and why finite inverse-polynomial timing suffices for a polynomial schedule; it is not a uniform norm estimate on unrestricted white-noise fields. Photon overflow, cutoff, start edges, response tails and propagation errors retain their separate allocations.

Port-rate calibration can also be explicit. If the only port uncertainty is r versus r_hat, comparing the pure Weyl dilations over T gives

\[
\|\mathcal V_{0,r,T}-\mathcal V_{0,\hat r,T}\|_\diamond
\le\sqrt{3nT}\,|\sqrt r-\sqrt{\hat r}|.
\tag{21}
\]

Indeed their vacuum isometry overlap is
\(\exp[-3nT(\sqrt r-\sqrt{\hat r})^2/8]I\); the isometry-to-channel inequality gives (21). A certified r_min determines T, and r_max can replace r in the lost-interval bound. Learning those port bounds, phases and control axes requires actual calibration data and services. They are prior resources in the main statement. No claim says they can be learned without exposure, or that source output can be photon-counted and also retained coherently in the same degrees of freedom.

Required costs thus include: the first specimen and declared model; calibrated source control hardware; at most nP pulses with peak G and slew S; 2nB random bits and their memory/disposal; the 3n physical pure output ports; finite field capture and all associated rails/cells/phase/timing/propagation; quantum memory during capture and processing; H=0 flagged export processing and receiver reset; instrument calibration and stability; and any actual energy or fabrication bill of the chosen devices. There are **zero Hamiltonian-coefficient learning trials** in this architecture. That does not set the other lines to zero.

## 8. Comparison with the strongest applicable approaches

1. **Random dynamical decoupling.** Viola and Knill's random-group framework already cancels unknown Hamiltonians, and bounds random control performance. Their bounded-control work and later Eulerian constructions already replace ideal impulses by finite control paths. These mechanisms are not novel here.

2. **Quadratic twirling improvements.** Yi, Kim and Marvian, *Faster Randomized Dynamical Decoupling*, prove that sequence randomization removes terms linear in an unwanted coupling and obtain complete-channel estimates. Their work is closer than a source-only spin-echo comparison. Lemma (7) is a short bounded-perturbation specialization adapted to a known retained Markov output, not a claim of a new general random-decoupling advantage.

3. **Complementary-channel recovery.** Information-disturbance and Stinespring-continuity theorems already connect source forgetfulness with existence of an environment decoder. Such an existence result alone does not provide one decoder for an unknown H, or the finite actual output receiver. The present physical control, dilation covariance, (9), and the known H=0 instrument jointly construct that decoder.

4. **Accepted Astra unknown-H acquisition.** The output-only calibration route uses no new source pulse access, learns H from later output, and decodes an earlier archived first input. Its actual calibration and receiver bills remain earned. The present route purchases source control and never learns H. It works for every r>0 because its reference Hamiltonian is zero. The source access is stronger, so this is not a same-access lower-bound separation from that theorem.

5. **Direct coherent transfer.** If clean source-to-protected-memory SWAPs, sender-controlled state emission, or known entangling transducers are supplied, those ordinary transfer protocols can be stronger and cheaper. They are not granted by the one-site rotations and fixed Weyl ports used here. A same-access ordinary construction combining modern random DD with the accepted H=0 export instrument is precisely the applicable comparator; this report has supplied its missing coherent-output and finite-pulse composition. It does not claim that an optimal such protocol was previously impossible or that this schedule is best.

The earned deduction is that Hamiltonian identification is **not a necessary prerequisite** to arbitrary-input export once this additional, finite but growing, source-control resource is available. Unknown-H acquisition and strong control are exchangeable resources in this explicit model. Coherent noncommuting reservoir access is still indispensable to this particular operation, and the hidden-Z all-strength acquisition obstruction is unaffected.

## 9. Executed checks and their limits

`audit_covariant_export.py` executes two finite-dimensional diagnostics and evaluates the analytic schedule for a scalable family. The first uses a two-qubit source and a pure partial-SWAP depolarizing collision environment. It averages all 16 source Pauli frames for several block lengths and computes the normalized Choi trace distance on the **joint source-plus-environment output**. The collision model is a finite mathematical instance of Lemma (7), not a finite-band replacement for the continuous reservoir. Its global output dimension grows with the source and environment; the implementation avoids claiming that tracing the source checks the joint statement.

The second checks the exact key-kept versus key-discarded one-qubit identity in Section 3.1. Schedule values are reported for n=1,4,16,64 with Lambda=n, r=1 and epsilon=0.1. No smallest instance is used to claim a competitive hardware regime. These checks are not experimental calibration, a receiver simulation, a full stochastic quantum-field execution, or a validation campaign of accepted sources. The proof governs the result.

The executed finite dilation covariance residual was at most 2.32e-16 in ordinary floating arithmetic. At the smallest tested dwell d=0.00625, the normalized joint-output Choi error divided by d^2 was approximately 1.1713 for the one-qubit example and 1.6844 for the two-qubit example. These values support the implemented second-order calculation but are not interval certificates. The analytic upper bound is proved independently of them.

| n | Useful time T | Blocks B | Pulse width w | Per-site peak G | Random key bits |
|---:|---:|---:|---:|---:|---:|
| 1 | 4.3820 | 1,537 | 4.064e-6 | 7.731e5 | 3,074 |
| 4 | 5.7683 | 42,591 | 3.669e-8 | 8.564e7 | 340,728 |
| 16 | 7.1546 | 1,048,341 | 3.726e-10 | 8.431e9 | 33,546,912 |
| 64 | 8.5409 | 23,903,319 | 4.085e-12 | 7.690e11 | 3,059,624,832 |

Time is in units with r=1 and hbar=1, and the unknown drift bound is Lambda=n. The receiver and calibration costs are additional. This table exposes the paid strong-control resource; it is not evidence that the construction is economical.

## 10. Retained failed routes and exact limitations

- Reusing a reduced-system dynamical-decoupling bound was insufficient: an unknown environment unitary could still defeat the decoder. The joint-output covariance and estimate (9) close that interface.
- Bounding the full Markov bath generator by an operator norm would introduce an invalid finite-band assumption. The interaction-picture proof bounds only the added source drift.
- Keeping the random key in the promised output would invalidate the quadratic statement in general. The target explicitly discards it after the frame correction.
- Treating finite pulses as free while keeping their emitted field would leave an unresolved output-frame interface. The present construction discards and quantitatively charges those intervals. This is conservative and not a lower bound on better continuous-control schemes.
- The bounded-component receiver does not erase source timing and control costs. Its full finite array, guards, propagation, calibration and protected-memory bill stays in the composition.
- A finite per-site source-control strength is supplied for each instance but grows with n and requested accuracy in the recipe. This is not a fixed aggregate bounded-bandwidth or microscopic hardware theorem.
- A Markov dilation invariant under calibrated Pauli frame changes is substantive. Arbitrary natural decoherence, unknown extra outputs, drifts reacting to the current key, uncontrolled many-level leakage and unavailable bath purifiers are outside the model.
- Historical priority for this combined control/export consequence is not established. The report identifies the applicable established machinery and does not claim a civilization-scale practical advance.

## Sources

1. Lorenza Viola and Emanuel Knill, *Random decoupling schemes for quantum dynamical control and error suppression*, Physical Review Letters 94, 060502 (2005). Primary full text: https://arxiv.org/pdf/quant-ph/0511120 .
2. Lorenza Viola and Emanuel Knill, *Robust dynamical decoupling with bounded controls*, Physical Review Letters 90, 037901 (2003). Primary full text: https://arxiv.org/pdf/quant-ph/0208056 .
3. Changhao Yi, Leeseok Kim and Milad Marvian, *Faster Randomized Dynamical Decoupling*, Physical Review Letters 136, 010601 (2026), DOI 10.1103/fk7j-y1vl. Primary preprint read: https://arxiv.org/pdf/2409.18369 .
4. Accepted Astra P1 bounded-component construction at fixed revision 2d22b00d4ec6ce4cd894a345c900d53de79ea631. Exact files read and retained in `sources/`: `bounded_local_field_interface_diluted_absorber_cascades_2026-11-04.txt`, `bounded_qubit_receiver_compiler.txt`, and `final_receiver_composition_audit.txt`. Their source URLs and hashes are in `source_provenance.json`.
5. Accepted no-burn-in/deferred-calibration proof and pure reset/export instrument, read from the unchanged preceding package: `preserved_first_event/preserved_correlated_reliability/preserved_passive_calibration/preserved_deferred_calibration/proofs/no_burnin_deferred_calibration.md`. Its exact original provenance remains in that package.
6. Dennis Kretschmann, Dirk Schlingemann and Reinhard F. Werner, *The Information-Disturbance Tradeoff and the Continuity of Stinespring's Representation*, IEEE Transactions on Information Theory 54 (2008), 1708–1717, DOI 10.1109/TIT.2008.917696. Primary abstract: https://arxiv.org/abs/quant-ph/0605009 . Used for the established comparison, not as a substitute for the explicit proof above.

All preceding originals remain unchanged. This is a new independent construction, with no external publication or physical deployment.
