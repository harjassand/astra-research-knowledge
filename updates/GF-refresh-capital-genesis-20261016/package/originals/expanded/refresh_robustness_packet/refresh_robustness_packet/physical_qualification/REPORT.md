# A bounded physical qualification route for stabilizer refresh

16 October 2026. Read-only public-source assessment and proposed qualification design. **No reviewed experiment currently qualifies the full Astra refresh contract.** The useful positive result is a concrete, modest-device route to a *bounded, model-explicit* physical refresh module. It does not require a native many-body phase Hamiltonian. The required engineering boundary and residual are stronger than an average parity or gate fidelity.

## 1. Recommended primitive: an uncorrected, physically applied random Pauli string

For a Pauli stabilizer S, privately sample b in {0,1} and physically implement S^b. With p=Pr(b=1), forgetting the seed gives

    E_p(rho) = (1-p) rho + p S rho S.

At p=1/2 this is exactly Pinch_S; for p<=1/2 it is D_eta with eta=1-2p. This identity holds on an arbitrary joint state when the branch operation is S^b tensor identity on the persistent bath. Uniform independent generator bits implement the stabilizer-group pinching channel. No many-body exp(-i theta S/2) is needed at the endpoint: S is a product of ordinary single-qubit Pauli rotations.

Three conditions must not be replaced by software semantics:

1. The selected branch changes the physical state relative to a fixed, independently controlled phase reference. A terminal virtual-Z frame change, or relabelled measurement, does not itself act on the lab-frame memory.
2. The random stabilizer is not subsequently undone or propagated into a compensating pulse sequence. Randomized compiling normally preserves the intended logical computation; that is a different operation from deliberately forgetting an applied random stabilizer.
3. The seed and any copy or physical carrier of it do not later become available to baseline dynamics. This is a controller/interface assumption to audit and test; hiding a column in an analysis file is insufficient.

A useful lab diagnostic is Ramsey interferometry with the analysis pulse driven from a fixed phase reference outside the randomized frame. Compare physical I, physical S, and their unconditioned mixture. This rules out a vacuous terminal frame change, but does not alone certify arbitrary-bath privacy.

## 2. Finite-pulse repair, with all harmful baseline terms charged

**Endpoint equivalence is insufficient.** During product rotations, an intermediate control C_b(t) can fail to commute with other stabilizers even though C_b(t_end)=S^b. An otherwise unrestricted stabilizer-preserving baseline can exploit this excursion. The exact finite constant-pulse counterexample in the companion `finite_pulse_obstruction` packet has zero original baseline odd action yet average bad probability 2/9 for fair I/S. This is an obstruction to the *unqualified compilation*, not a lower bound for all pulse designs.

Here is a conservative physically meaningful sufficient contract. Declare a finite retained Hilbert space (data, explicitly retained spectators, couplers, leakage levels, and relevant bath modes), fixed controller windows, and the actual branch Hamiltonian

    H_b(t) = H_safe(t) + H_ctrl,b(t) + K_b(t).

Require [H_safe(t), C_b(s)]=0 for all relevant t,s; a simple safe choice is drift supported strictly outside the expanded control footprint. H_safe is independent of b. H_ctrl,b generates a known endpoint C_b(t_end)=S^b up to a global phase. **K_b includes all omitted baseline interactions, all branch-dependent pulse/crosstalk errors, couplings across the footprint boundary, and leakage terms in the declared model.** The baseline may remain active throughout the real pulse.

If a uniform, joint-system envelope gives

    d_b = integral_window ||K_b(t)|| dt,

Duhamel's bound gives ||U_b-U_ref,b|| <= d_b and hence

    (1/2)||E_actual-E_reference||_diamond
        <= sum_b p_b min(1,d_b).

The reference is the hidden physical Pauli channel composed with the common H_safe evolution. The bound holds with an arbitrary reference and arbitrary initial state in the declared retained space. It controls the retained bath as well as the memory, so bath changes cannot be silently discarded. It is conservative: calibrated baseline terms commuting with the entire path can remain in H_safe, and better pulse-dependent comparison bounds may be used when proved.

For a compiled product of calibrated one-qubit rotations with angle errors |e_j|, the endpoint mismatch can additionally be charged by (1/2) sum_j |e_j| in operator norm. For a Z-frequency residual bounded by |delta f_j(t)|, its coherent phase contribution is pi integral |delta f_j(t)|dt. These conversions require an actual uniform bound on the retained model, not a best-fit Ramsey frequency or a standard error alone.

This route replaces the impossible demand that arbitrary parity-preserving drift be harmless during arbitrary compiled paths. It does **not** establish a small numerical d_b on any inspected device. The existing theorem for the special physical Hamiltonian u(t)S/2 is still valid on its own assumptions; this is a different, more conservative interface.

## 3. Strongest inspected empirical building blocks

### 3.1 Physical phase control: Hellings et al. (2025), building on Cryoscope

[Hellings et al., Phys. Rev. Research 7, 043142](https://doi.org/10.1103/1qhb-r4fb), [open preprint](https://arxiv.org/abs/2503.04610), and [supporting-data DOI](https://doi.org/10.3929/ethz-c-000783499).

The experiment calibrates real flux-induced frequency changes using in-situ spectroscopy and Ramsey phase measurements, including long pulse tails. It reports sub-permille residual frequency errors over broad timescales, with an early transient around 10 ns; the calibration assumes approximately linear control-line response. This is a much closer match to a physical phase kick than a virtual-Z benchmark. Supporting data are explicitly cited by the published paper. The public landing page returned HTTP 429 in this assessment, so no raw flux-data contents were verified. The open manuscript was acquired.

**Use:** waveform/phase calibration, pulse-tail reservation, and a practical route to confidence bands under a declared transfer-function model. **Not supplied:** hidden-seed isolation, full retained-bath operator norms, whole-refresh tomography, or a correctable spatial footprint.

[Rol et al., Cryoscope, Appl. Phys. Lett. 116, 054001 (2020)](https://arxiv.org/abs/1907.04818) gives the earlier experimentally implemented phase-reconstruction method and predistortion, including systematic limitations near pulse edges. This supports experimental attainability of phase metrology, not worst-case channel certification by itself.

### 3.2 Most directly relevant modern process model: White et al. (2025)

[White et al., Phys. Rev. X 15, 021047](https://doi.org/10.1103/PhysRevX.15.021047), [full preprint](https://arxiv.org/html/2312.08454v2), [author repository](https://github.com/gwhitequantum/process-tensor-network-tomography).

This work models background memory, correlated control errors, and control-to-environment spillage. Actual IBM demonstrations include 18 steps on one qubit and four steps on four qubits. The repository contains experimental job-result objects, fitted process tensors, and separate validation data. Its optimized gate diamond distances are predictions from characterized models; the paper explicitly distinguishes these forecasts from live optimized-control execution. The fitted reconstructions use restricted interventions and chosen low tensor-network bond dimensions. Self-consistent estimates retain gauge freedom, and the paper discusses underdetermination of fully correlated instruments.

**Use:** the strongest inspected practical framework for testing whether a proposed local pulse module has memory/crosstalk outside a naive gate model. **Limit:** a cross-validation score and a fitted model's diamond distance are not a confidence-bounded, gauge-fixed, arbitrary-bath refresh residual.

### 3.3 Cleanest acquired multi-time count dataset: Giarmatzi et al. (2024)

[Multi-time quantum process tomography on a superconducting qubit](https://arxiv.org/html/2308.00750v2), [author data and reconstruction notebook](https://github.com/Christina-Giar/NMN-tomo).

The experiment uses sequential measure-and-prepare interventions to reconstruct a full three-time process, rather than only a unitary-restricted process. Public JSON files contain four-outcome counts for 324 settings in each of ten process datasets. Both were acquired and structurally checked. However, the experiment initializes a specified bath, characterizes idle intervals rather than random refresh, and explicitly assumes system-environment interaction is negligible during tomography operations. Its displayed uncertainty concerns sampling, not all model/systematic errors.

**Use:** a real replayable template for finite-horizon memory tests and transparent counts. **Limit:** no existing refresh residual can be inferred because the proposed random pulse module was not performed in these records. A complete controlled process for one initialized bath is not a bound on the physical dilation for every bath state.

### 3.4 Randomized compiling and virtual-Z evidence

See `rc_experiments.md` for the separate source/compiler audit of Ware, Hashim, and Winick. The strongest inspected randomized-GST raw-data lead is [Ware et al. data, Zenodo 4609459](https://zenodo.org/records/4609459). It demonstrates real randomized compiled sequences, but a logical terminal random Z may be only a frame update. The public compiler can implement logical Id and Z with the same physical pulses followed by different zero-duration updates. This is exactly why the fixed-reference physical witness is necessary.

[McKay et al., Efficient Z gates for quantum computing](https://doi.org/10.1103/PhysRevA.96.022330) explicitly describes virtual Z operations through drive phase updates. This is useful compilation technology; it does not by itself create an irreversible lab-frame dephaser before a subsequent uncontrolled interaction.

## 4. The smallest credible qualification experiment

The following is a proposed design, not an authorized or completed hardware run.

1. **Choose the proof boundary first.** Start with one accessible Pauli or a low-weight stabilizer on a small code patch. Fix the exact data, spectator, coupler, leakage, controller and bath boundary; the allowed bath initialization/energy range; the intervention times; the recovery deadline; and the residual target. Do not claim the original arbitrary-bath theorem when these are restricted.
2. **Implement two physical branches.** Use actual flux-induced Z phases or microwave Pauli rotations, a common reservation window, and a fresh private bit. Disable cancellation of the selected endpoint by the compiler. Audit emitted waveforms and phase accumulators. Run the fixed-reference Ramsey control, including a deliberate software-only random-frame negative control.
3. **Characterize simultaneous operation.** Sweep all affected neighbor/spectator preparations; run the actual parallel schedule, not isolated gates. Calibrate pulse tails and branch-dependent detuning, exchange, ZZ, drive crosstalk, leakage and readout effects. Include operations that return information from accessible memories after the pulse, and vary the delay and recent pulse history. Classical controller buffers, shared oscillators and buses belong in this audit.
4. **Obtain a residual with a named guarantee.** Either use confidence-bounded coefficients in an explicitly complete bounded Hamiltonian model and evaluate the joint K_b norm, or reconstruct an informationally complete finite-horizon operational process with calibrated intervention error. Use a conservative simultaneous statistical confidence region and systematic-error budget. A point-estimate CPTP projection or bootstrap error bar alone is not the guarantee.
5. **Keep privacy separate.** Controller design must prevent baseline access to the random bit and to a later returning carrier. Delayed seed-conditioned cancellation or echo tests can falsify isolation, but absence of a signal over a finite tested horizon is only a horizon-specific result. Certify the physical isolation assumption, or restrict the claimed continuation accordingly.
6. **Qualify the whole noisy footprint.** Include every data location the pulse or its stored bath excitation can affect before recovery. Check the code's no-local-logical/correctability condition for this expanded region. If only a tail bound exists outside it, retain that tail as an explicit residual. A small diamond error says nothing about where the error acts.
7. **Use the appropriate transfer statement.** A full-system residual allows a conservative hybrid error bound for the characterized cycle. A sharper local product bound requires its separate independence/local-tester assumptions. Shared control hardware, overlapping pulse footprints, or one common bath do not permit independent local errors to be inferred from independently sampled bits. Endpoint-good support can be handled by the companion robust support-transfer result, provided the actual noisy footprint meets its hypotheses.

For finite-horizon tomography, a transparent sufficient statistical construction is possible. Given a genuinely complete linear experiment design with dual operators D_k, simultaneous probability bounds |p_k-p_hat_k|<=beta_k imply a norm-radius bound <=sum_k beta_k ||D_k|| in the chosen operational norm. Add independently bounded calibration and truncation errors. The point-estimate process distance plus this radius is a valid conservative upper bound. Conditioning can make this bound very loose; tensor-network compression reduces cost only with an additional justified approximation/model-error budget. No such radius was computed from the reviewed studies.

## 5. What cannot be certified from these observations, even with infinite shots

There are two basic identifiability obstructions, independent of statistical precision.

**Unobserved bath states.** Take any model agreeing with all tested initialized-bath experiments. Extend the bath by an unpopulated orthogonal sector and add M X tensor Pi_hidden, where X is parity-odd and Pi_hidden projects onto that sector. Every tested probability remains unchanged, for arbitrary M; the full odd norm is at least M on a different allowed bath input. Thus reduced experiments with a fixed bath initialization cannot upper-bound a uniform arbitrary-bath interaction norm. An explicit dimension/energy/initialization/control model is necessary.

**Unobserved future seed access.** A controller can retain a copy of b in an inaccessible register and release it only after the last characterization time. It produces exactly the same finite-horizon statistics as a permanently private controller, yet a later conditional inverse can undo the intended dephasing. A finite dataset cannot establish permanent no-return without a physical interface assumption or a fixed bounded continuation horizon.

Consequently, the present broad contract is not empirically certified by any inspected dataset, and generic RC success does not fill the gap. The attainable goal is a bounded, explicitly trusted physical control module plus measured/model-bounded residual and a verified correctable footprint. There is no demonstrated numerical pass yet.

## 6. Acquired material and stopping point

- Public JSON process counts, notebook source (inspected, not executed), raw article sources, repository trees, and one representative modern process-result file are in `sources/`.
- `count_audit.json` records the ten count-file structures. The nine IBM runs each sum to 2,592,000 stored counts; the in-house run sums to 2,985,984. Per-setting totals vary. Pairing opposite second-preparation labels gives exactly 16,000 counts per pair in every IBM run and 18,432 in the in-house run (162 pairs/run). This is consistent with outcome-conditioned regrouping, but does not establish its acquisition provenance. These are published postprocessed records, not independently verified untouched shots. The paired totals still differ from the preprint's nominal 2^14-per-protocol description; acquisition and grouping details remain to be reconciled before a new confidence analysis.
- `white_frequency_audit.json` records safe static inspection of one White job-result file: 11,999 positive empirical frequencies, all on a 1/1024 grid. The source preprocessor omits absent outcome keys. This representative file is processed frequency data, not untouched shots; additional sequence/shot metadata must be reconciled for a rigorous replay.
- The White repository was pinned at e3f01b011f28c1497f7ebb3dc4f98a782a75095f; the Giarmatzi tree at 154235f8bbf5e70eb71c325370a67b1894490452. Downloaded pickles were inspected as data opcodes, never deserialized or executed.
- No hardware job, restricted dataset, contact, spend, or canonical edit was made. In particular, no reserved Willow25k data or frozen STM pilot was accessed.

The next justified step is to choose the physical boundary and acceptable residual/footprint, then acquire the proposed module's actual pulse-level and multi-time records. Reanalyzing another generic parity fidelity would not resolve the missing contract.
