# Measured Zeno response: bounded experimental evidence

Date: 2026-10-15. Scope: two primary experiments, their published figures, and one supplement. Includes the later **unread exact-measurement refinement**. No author outreach, accounts, software installation, or author-code execution. This is an empirical foothold, **not an experimental certification of either corollary**.

## Decisive finding

**Measurement-induced suppression is experimentally established.** Slichter et al. directly resolve slower *coherently driven* transitions under stronger continuous single-transmon energy measurement. Kalb et al. demonstrate the more relevant *discrete repeated joint-spin projections*: joint X projections on two or three nuclear spins prolong coherence and preserve encoded states under natural quasi-static dephasing. Kalb also exposes substantial finite-duration/control overhead and fidelity loss.

**Kalb is the closest demonstrated physical interface to the refined theorem:** its nonselective joint-X projection has precisely the ideal channel form D_G(ρ)=Σ_s P_sρP_s. The lack of physically recorded intermediate outcomes is **not** an obstruction under the unread refinement: latent fresh-reservoir labels suffice. What neither experiment establishes is exact pinching on the full joint data–persistent-bath channel, isolated never-reinteracting discarded reservoirs, a bounded full error Hamiltonian J, or joint-parent operator bounds. Kalb's single joint-X check also fails the corollary's full-Pauli completion-support requirement for a footprint containing its data spins. The two experiments must remain separate capabilities. Neither is measurement-based feedback correction.

## 1. Slichter: direct continuous-measurement response

D. H. Slichter et al., *Quantum Zeno effect in the strong measurement regime of circuit quantum electrodynamics*, New J. Phys. **18**, 053031 (2016), [DOI](https://doi.org/10.1088/1367-2630/18/5/053031), [author-hosted published PDF](https://circuitqedsherbrooke.ca/wp-content/uploads/2024/07/74_ZenoCQED.pdf), [arXiv](https://arxiv.org/abs/1512.04006). Main references below are journal page numbers.

### Compatible operating point and measured quantity

- **Observable:** one transmon's energy, effectively σz in {|g>,|e>}, via dispersive cavity homodyne readout. This is continuous readout, not a sequence of multi-qubit projective checks.
- **Drive:** resonant transverse coherent microwave drive, Hamiltonian amplitude Ω/2 (ℏ=1); Ω/2π is quoted in MHz. The drive is resonant at the *ground-state-conditioned* ac-Stark-shifted transition. Different cavity occupations in g/e make the excited-state drive off-resonant; the driven-response analysis is consequently restricted to g→e. The selected measurement traces illustrate Ω/2π=0.8 and 3.6 MHz; Fig. 4 covers a wider sweep (about 0.2–9.2 MHz, panel dependent).
- **Device:** qubit 5.3556 GHz; anharmonicity −258 MHz; cavity 6.2724 GHz; coupling g/2π=105.3 MHz; cavity linewidth κ/2π=7 MHz; readout 6.282 GHz; 50 mK (p. 3).
- **Measurement:** Γm=2Γd, with Γd calibrated from spectroscopic linewidth after drive-power broadening correction. Ten Γm values: 134, 179, 203, 226, 248, 270, 297, 334, 364, 393 μs⁻¹; ground-conditioned cavity occupation n̄g=3.4–37. Γd therefore spans 67–196.5 μs⁻¹. These are dephasing/information-rate conventions, not a count of exact projective readouts.
- **Timing/data:** 17.5 μs measurement pulse, drive during 10 μs starting after 3 μs cavity preparation; only the joint drive/readout interval enters Zeno-rate analysis. 10,000 iterations per point, 100 μs apart, 100 MS/s (10 ns sampling), 14 MHz raw-data 3 dB noise bandwidth (pp. 3–5).

### Response and controls

The reported driven excitation rates are consistent over much of the sweep with Γ↑,drive=Ω²/[2(γ2+Γd)], approaching Ω²/Γm. Fig. 5 displays the Ω² dependence; Fig. 4 compares all ten strengths. Deviations occur above roughly Ω/2π=6 MHz. The authors identify strong-measurement and dispersive-approximation limitations; Γm is already larger than κ, and n̄g crosses the usual critical-photon estimate near Γm≈340 μs⁻¹ (pp. 6–7). The fitted curve is not a proven upper envelope.

**Same-device controls:** (i) Ω is calibrated from Rabi oscillations with measurement off, including frequency dependence; (ii) Ω=0 runs at each measurement strength measure excitation background, which is subtracted to isolate driven excitation; (iii) no-drive decay versus readout power distinguishes the response from changes to T1/Purcell decay. No equal-resource sham-measurement memory experiment is reported here.

The extracted background excitation is **0.018–0.022 μs⁻¹**, not zero. With readout off, **T1=575 ns, Tφ=7.9 μs**, giving γ2≈1 μs⁻¹ (p. 3; PDF text extraction corrupts μ in some places, so these units were visually checked). The no-drive T1 change under readout is inconsistent with the inverse-Γm Zeno scaling and is analyzed separately as Purcell/nonlinear physics (pp. 7–8). This is not evidence that arbitrary irreversible errors are Zeno-suppressed.

### Readout, leakage, and analysis costs

- The chosen amplified quadrature cannot separate |e> from higher transmon levels. A separate, lower-SNR quadrature dataset measured **about 1–5% population above the computational manifold** (p. 6). It is not a per-measurement leakage probability or a uniform leakage bound.
- Finite-bandwidth filtering misses short excursions. Gaussian filtering and hysteretic thresholding supply dwell times; maximum-likelihood estimation includes finite-bandwidth and censoring corrections. Median simulated-calibration systematic bias/uncertainty were −3.5%/2%; magnitude was below 20%/10% for all experimental points (p. 5). The experiment's 95% rate intervals are not exact event records.
- Strong σz measurement dephases superpositions at Γd. Preserving an unknown unencoded qubit is not the demonstrated task. No protected classical record, comparator/reset reliability, or multi-parent cross-talk budget is supplied.

### Acquired numerical foothold

`derived/slichter2016_fig4_experimental_digitized.csv` contains **114 red-square experimental point estimates and their plotted vertical 95% intervals**, reconstructed from the licensed PDF's vector geometry by `extract_slichter_figure4.py`. Black simulation points and blue theoretical curves were excluded. This is **derived publication-figure data, not author source data or raw quantum-jump traces**. The script and tick calibration are retained for reproduction. Values below about 0.05 μs⁻¹ are especially poorly resolved on the linear axis; do not use their apparent precision.

Examples (approximate digitized coordinates; drives differ slightly across panels):

| Γm (μs⁻¹) | Ω/2π (MHz) | Γ↑,drive (μs⁻¹) | Plotted 95% interval |
|---:|---:|---:|---:|
| 134 | 3.04 | 3.26 | 2.88–3.62 |
| 203 | 2.99 | 2.31 | 2.23–2.39 |
| 270 | 2.87 | 1.55 | 1.49–1.60 |
| 393 | 3.21 | 1.44 | 1.40–1.47 |

These are illustrative published mean-response estimates, **not a same-Ω ratio, independent reanalysis, confidence bound on a channel norm, or bath-uniform probability bound**.

## 2. Kalb: the closer discrete multi-spin intervention

N. Kalb et al., *Experimental creation of quantum Zeno subspaces by repeated multi-spin projections in diamond*, Nat. Commun. **7**, 13111 (2016), [article](https://www.nature.com/articles/ncomms13111), [supplement](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fncomms13111/MediaObjects/41467_2016_BFncomms13111_MOESM496_ESM.pdf).

### Operation and environment

- **Observable:** O=X, XX, or XXX on one to three ¹³C nuclear spins near a single NV electron ancilla. The ideal nonselective operation is M_O(ρ)=(ρ+OρO)/2. Controlled rotations map the joint eigenspaces onto the electron; optical pumping projects and resets it, followed by an electron π pulse.
- **Error process:** natural slowly varying nuclear-bath dephasing, modeled per shot by H=ΣᵢΔᵢZᵢ/2, independent Gaussian quasi-static Δᵢ with σᵢ=√2/T2,i*. There is **no calibrated injected coherent-error drive sweep** analogous to Slichter's Ω sweep. Measured single-spin T2*: 12.4(9), 8.2(7), 21(1) ms. Supplementary Table I reports joint fitted T2*: 7.1(3) ms for spins 1–2 and 6.5(2) ms for spins 1–3; these are baseline parameters, not protected-memory lifetimes.
- **Schedule:** N equally spaced projections, weak evolution spacing t=τ/(N+1) in the ideal model. Single-spin N≤16; two-spin reported even N=0,2,4,6; three-spin N=0,2,4. Natural noise is predominantly low-frequency, and the model assumes uncorrelated static detunings. It is not an arbitrary shared-bath test.
- **Nonselective:** the paper explicitly says the optical outcome need not be extracted or recorded (p. 3). This now **matches the allowed unread interface**, rather than constituting a missing extra-readout requirement. It does not establish the refined theorem's exact full-joint pinching or no-return-reservoir assumptions. The latent u0,…,uM and OR flags are mathematical Kraus labels, not this experiment's measured data.

### Measured benefit and same-device control

With XX projections, the six-state average encoded-qubit fidelity exceeds the best individual participating spin over a time range while remaining above 2/3; the four entangled input states retain fidelity above 1/2 longer with N=2,4,6 than with N=0 (Fig. 3). For XXX, three selected logical states show prolonged decay and an absolute-fidelity benefit over a time range despite lower initial fidelity (Fig. 4). This is real encoded-state protection against the tested noise, not a theorem-level arbitrary-state/worst-bath guarantee.

Controls are N=0 on the same encoded system and the best individual participating spin, with quadrature-insensitive single-spin coherence measurement to avoid systematic-detuning bias. Supplementary Fig. 2 explicitly compares corrected and uncorrected time axes. No matched full-pulse-budget projection-disabled control or per-instrument fault characterization is reported in these sources.

### Costs that cannot be dropped

- Each optical pumping pulse lasts **30 μs**; reinitialization has a stochastic timescale about **1 μs**. Hyperfine couplings are below **2π×50 kHz**, chosen to limit extra nuclear dephasing. The initial sector is mapped to the optically dark electron state to reduce excitation (pp. 2–3).
- The plotted τ **subtracts average nuclear-spin driving time**; it is not total wall-clock reservation time. For the two-spin N=4 trace the subtraction is **5.06 ms** (Supplementary Fig. 2).
- The three-spin N=4 sequence uses **33 two-qubit gates and 1,276 electron-spin refocusing pulses** (p. 4). These are reported sequence costs, not 33 gates per projection.
- Initial encoded-qubit fidelity without projections is **0.89(1)**; added projections reduce initial amplitudes further. Fit amplitude damping parameterizes errors from sequence complexity; it does not separate measurement-induced faults from gate, reset, initialization, or leakage faults.
- Final readout is corrected with a model assuming symmetric initialization/readout and fixed ¹⁴N initialization loss. Correction factors range **0.90(2)–0.95(2)**; ¹⁴N desired-state initialization probability is **0.96(1)** (Supplementary Note 3). These numbers are not intermediate-record assignment fidelities. An independently resolved leakage budget is not supplied.

## 3. Exact relation to the measured-cell theorem and unread refinement

| Required input / conclusion | Experimental status |
|---|---|
| Repeated intervention can inhibit coherent sector-changing evolution | **Supported mechanistically:** direct driven-transition response in Slichter; repeated joint-spin-projection dephasing suppression in Kalb. Different devices/regimes. |
| Exact nonselective D_G on the full retained data–persistent-bath channel, at prescribed boundaries | **Not established, but Kalb supplies the closest operation.** Its ideal joint-X map is D_G; measured real gate/reset errors and finite duration are unqualified. Slichter is continuous single-qubit readout, not exact finite-time pinching. |
| Latent deletion-null QℓU(zℓ=0)W=0, with fresh isolated discarded reservoirs and no outcome feedback | **Not established experimentally.** No physical extra readout/comparator is required after the refinement. Kalb's optical reset is a plausible irreversible backaction route, but exact full-joint channel composition and absence of retained/reinteracting correlations were not certified. Slichter has nonzero no-drive events: deleting only its coherent drive would not delete all observed background transitions. |
| Full-footprint Pauli(A)∩Centralizer(G)⊆phase×S_code | **Not supplied and not true for a naive identification with Kalb's single parity.** For G=<XX> or <XXX>, single X factors commute with G and can act logically; even Z products also commute. First-order anticommution of the tested Z noise is weaker than completeness against all footprint Paulis. |
| Known action aℓ=∫||Vℓ||dt, or bath-uniform J | **Not measured.** Ω/2 is a known applied drive norm only in an ideal two-level reduction; it is not the norm of all hardware+bath errors. Gaussian detuning fits are ensemble parameters, not finite hard operator-norm bounds. |
| F_R≤∏ᵢ(Jᵢ²τᵢ²/Mᵢ)I for simultaneous parents sharing an arbitrary finite bath | **Not tested or inferred.** No parallel-reservation joint-subset detector acquisition, arbitrary input/bath uniformity, or higher-order joint-tail certificate. Mean rates/fidelities cannot establish this inequality. |
| Exact initial correction/controller and entering-sector preparation; finite total θ; bounded full footprints/conflicts | **Not established.** Extra comparison circuitry can be omitted under the refinement, but the original correction-controller assumptions remain. Kalb supplies valuable cost evidence, while τ omits control time; neither supplies the complete reserved hardware/latency/fault budget. |

**Reservoir qualification matters:** reuse of a physical electron ancilla is not automatically disqualifying if each reset realizes the required fixed fresh state and information is discarded into fresh external modes that never feed back. Conversely, discarding an optical outcome alone does not prove that condition. Kalb's stochastic reset and hyperfine-induced dephasing show why the full joint channel, rather than just a favorable data marginal, needs qualification. The refinement also requires an actual initial pinching or already-qualified sector preparation after exact correction; it does not create an entering sector label for free.

The formal continuous/discrete rate match Γmτcell=4 quoted by Slichter is a **model relation**, not a hardware substitution. Their Γm values would map to ideal measurement spacings of about 30–10 ns. The actual experiment has continuous cavity dynamics, 14 MHz noise bandwidth, filtering, and no such sequence of exact projective syndrome operations. Counting Γm×duration as M would be invalid. At finite rate and time, an ordinary dephasing semigroup retains residual off-diagonal coherence; it is not the exact complete pinching assumed by the refinement.

## 4. What remains for a many-qubit physical-memory claim

The missing evidence is narrowly defined: characterize the actual repeated **nonselective syndrome channel on the full joint data–persistent-bath system**, including reset/reservoir isolation, ambient noise during gates/readout/reset, correlated backaction, leakage, full reservation time and footprint; then demonstrate or justify the required joint-fault control and completion-support condition. With ignored extra outcomes, physical intermediate assignment/comparison fidelity is no longer needed; the original correction-controller and final-decoder requirements are unchanged. An observed suppression curve alone does not replace those hypotheses. Empirical average instrument errors also cannot silently become exact deletion nullness; a noisy-instrument extension would need its own proved bound.

This acquisition supplies measured response and costs, not a proposed apparatus. No rates or fidelities from Willow, Ware, Slichter, and Kalb have been combined into a synthetic device capability.

## 5. Acquisition and provenance

- Slichter published PDF: CC BY 3.0 notice on p. 1, retained with attribution/DOI. Its original multi-gigabyte jump traces were **not located in a readily accessible licensed public deposit** during this bounded check. No claim that no archive exists anywhere.
- Kalb article: CC BY 4.0 notice on p. 6; publisher article/PDF and linked supplement acquired. Its data-availability statement says data are available from the corresponding author on request. No author request was made; no raw/source numerical dataset acquired.
- PDF-derived text sometimes renders μ as m. Relevant units and key figures were checked against page images. Reported uncertainties are copied from publications, not newly estimated.
- `PROVENANCE.json` lists URLs, licenses, local paths, and acquisition classification. `SHA256SUMS` covers the saved bundle. `README.md` explains the numerical-file boundary.
