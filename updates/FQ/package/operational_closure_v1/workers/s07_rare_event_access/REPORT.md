# S07 — physically enrich a rare catalytic state, then infer its native flux

15 October 2026, Australia/Brisbane. **Status: conditional construction; no demonstrated new capability, full-cost advantage, or novelty.** The earlier hidden-terminal-row search bound concerns a local-row oracle. It does not apply when a real catalyst offers a reversible field or ligand control that changes the population of a chemically identified intermediate, plus independent product and spectroscopic readouts. I investigated that richer interface for a molecular CO₂-to-formate catalyst. The proposed output is the *native*, per-active-site formate initiation rate and the hydride-state contribution at a specified potential, proton activity, CO₂ activity, temperature and electrode geometry. It is not a measured rate in this report.

## Operation and the access it uses

Take a catalyst whose resting state `A` interconverts with a metal-hydride state `I`; `I` can return to `A`, make formate, or make H₂. At a low operating potential, `I` may be too sparsely populated to characterize directly even though its chemical identity controls selectivity. The concrete intervention is a **paired potential-gate and release assay**:

1. Under conditions that suppress **both** formate and H₂ exits without changing the bare `A↔I` chemistry, titrate potential through overlapping windows until the `A:I` ratio is measurable by a calibrated state-resolved spectrum or electrochemical signal. Recover the rare ratio at the operating potential from the measured electrochemical free-energy difference. This physically prepares an enriched `I` ensemble; it assumes no ability to set an arbitrary microscopic state. Simultaneously suppressing both exits is itself an unverified chemical feasibility gate.
2. On matched catalyst aliquots under native CO₂/proton/electrolyte conditions, apply a brief enrichment pulse to one and a sham pulse to the other. Return both to the *same controlled operating potential*, not open circuit. Record the difference in the hydride signal and time-resolved formate and H₂ flux. The formate signal can be isotope-resolved if source attribution is needed, with the isotope effect calibrated separately.
3. Infer the native state-entry rate and formate flux from the reaction-off equilibrium odds and the native differential decay. This uses the physical ability to accumulate and read out many `I` states simultaneously. It requires state identity, electrical control, and a closed kinetic model; it does not infer the rate from a pulse burst alone.

Metal-hydride pre-equilibrium and its control of formate formation are physically motivated by Pattanayak and Berben's [primary CO₂-reduction study](https://doi.org/10.1021/jacs.2c10942): the accessible article text describes a metal carbonyl cluster, fast hydride formation, competing H₂ formation and a formate-rate law involving a hydride-formation equilibrium. It reports up to 296 s⁻¹ formate production in its conditions. **That paper does not establish that its hydride is rare at my proposed operating point, nor that the pulse protocol below works on that complex.** It also makes the central pre-equilibrium idea and much of the chemistry clear prior art. The [2018 stopped-flow metal-hydride study](https://doi.org/10.1039/C8SC02535E) reports experimental CO₂-insertion kinetics and ligand/solvent effects, supporting a possible fast continuation readout but warning that its rate depends on chemistry. A recent [IrOₓ operando study](https://doi.org/10.1038/s41563-026-02514-9) actually combines potential steps, time-resolved optical and X-ray spectroscopy, charge accounting and EC-MS oxygen measurement. Its pulse readout is an unusually strong empirical comparator; it also reports a nonlinear rate versus accumulated O⁻ coverage, so the two-state formula below must **not** simply be applied to IrOₓ.

## Exact rate identity in the smallest closed model

This is an original derivation for the stated idealized continuous-time model, not a claim that any real catalyst obeys it. Each active site is in `A` or `I`. At native conditions, `A→I` has hazard `α`, and `I→A` has reversible hazard `β`. From `I`, formate initiation has hazard `γ` and H₂ initiation hazard `δ`; each product event resets the site immediately to `A`. Rates are constant over the assay; sites do not interact; transport and site loss are absent. The product-free reversible pair has odds

\[
K_0 = {\alpha\over\beta} = {P_{\rm off}(I)\over P_{\rm off}(A)}. \tag{1}
\]

The nontrivial transport premise is that adding CO₂ and running the native reaction leaves the *bare* `A↔I` hazards `α,β` unchanged. H₂ is included explicitly because it competes with formate in a metal-hydride catalyst; any additional exit needs its own measured hazard. Under native conditions, if `m(t)=P(I,t)`,

\[
\dot m=\alpha(1-m)-(\beta+\gamma+\delta)m
       =\alpha-Rm,\qquad R=\alpha+\beta+\gamma+\delta. \tag{2}
\]

For a pulse and sham sample that differ only in initial `I` fraction, `Δm(t)=Δm(0)e^{-Rt}`. The excess product initiation rates are `Δj_F(t)=γ Δm(t)` and `Δj_H(t)=δ Δm(t)`. Thus `R` comes from the common exponential, while `γ=Δj_F/Δm` and `δ=Δj_H/Δm` come from calibrated differential products; these ratios can use an integrated burst if detector impulse responses are deconvolved. Solving (1)–(2),

\[
\beta={R-\gamma-\delta\over 1+K_0},\qquad
\alpha={K_0(R-\gamma-\delta)\over1+K_0},\qquad
\boxed{j_F^{(0)}={\gamma K_0(R-\gamma-\delta)\over(1+K_0)R}}. \tag{3}
\]

Here `j_F^(0)` is the *unperturbed/native* steady formate initiation rate per available site. Equation (3) does not use a pre-equilibrium approximation such as `γ≪β`; it explicitly accounts for product removal of `I`. A negative reconstructed `β` or a non-single-exponential difference is an immediate model-failure diagnostic. If product release or catalyst recovery consumes appreciable time, a third state is required and (3) is not the turnover frequency.
If a parallel formate route leaves directly from `A`, (3) estimates only the hydride-mediated component; total formate flux needs that route's separate rate. This distinction makes pathway attribution the scientifically useful output when direct bulk formate is already countable.

At potentials `E₁` where the reaction-off odds are measurable, thermodynamic transport to `E₀` uses the acquired conjugate charge, activities and temperature:

\[
\log K_0=\log K(E_1)-{1\over k_{\rm B}T}
                 \int_{E_0}^{E_1}\Delta Q(E)\,dE. \tag{4}
\]

`ΔQ(E)` is the equilibrium charge difference of the identified `I` and `A` states, including proton/electrolyte linkage if these change. The common Nernst simplification `ΔQ=e` is valid only for a single fixed one-electron transition at fixed relevant activities. A field-created hydride with a changed ligand, oxidation state, solvation shell or site distribution is not the native `I`. Equation (4) is a thermodynamic identity within the specified equilibrium family; the applicability of that family is an experimental burden. Its uncertainty is additive in `log K₀` and becomes multiplicative in the rare rate.

This separates two physical ways to gain access: potential control increases `I` population during measurement, and parallel catalyst sites make the product burst measurable in a short window. Neither is free. If `K₀≪1` and `γ/(β+γ+δ)` is order one, an ideal native product counter needs exposure of order `1/[M j_F^(0) ε²]` for relative error `ε` on `M` independent sites. The pulse can yield order `M Δm(0)γ/R` extra product molecules in one relaxation, while equilibrium titration obtains a tiny `K₀` through intermediate-occupancy windows. This comparison is only an information-scale illustration. It excludes chemical drift, correlated sites, detector background and the full apparatus costs below; it does not prove a practical speedup. If `γ/R` is also tiny, product-burst counting still needs order `1/(γ/R)` enriched site-continuations per observed product.

## What an easier trap would and would not identify

I first examined adding a state-specific stable chemical trap at pseudo-first-order hazard `cκ`. In the same two-state cycle it produces

\[
j_T(c)={\alpha c\kappa\over\alpha+\beta+\gamma+\delta+c\kappa}.
\]

This is useful: stable adducts can integrate a fleeting-state signal, and a dose series can infer `α` and `α+β+γ+δ` if `κ`, trap specificity and response are independently calibrated. It cannot split `β`, `γ` and `δ`, so trap signal alone cannot determine unperturbed formate flux. High-dose trapping also changes occupancy and diverts product. At low dose the mark rate vanishes with `c`, so an apparent sensitivity gain must pay in site-time. Spin-trap research supplies a real warning: [an isotope-order artifact experiment](https://pmc.ncbi.nlm.nih.gov/articles/PMC3859841/) found false signals arising from non-radical addition followed by oxidation under some conditions. The trap is therefore a discovery/identity control, not a sufficient kinetic estimator. The gated equilibrium plus native release is the substantive redesign after this identification failure.

## Exact counterexample to an unjustified transport

The inference fails even when the off-equilibrium measurement and the entire pulse *difference* look perfect. Let the reaction-off pair have `α_off=10⁻⁵ s⁻¹`, `β_off=10 s⁻¹`, so `K₀=10⁻⁶`. Set `γ=1 s⁻¹`, `δ=0`. In world 0, the native pair equals the off pair and `R=11.00001 s⁻¹`; (3) gives `j_F=1/1,100,001 s⁻¹`. In world 1, CO₂ subtly changes `α_on` to `2×10⁻⁵ s⁻¹` and `β_on` to `9.99999 s⁻¹`. Then `R`, `γ`, the off `K₀`, and every normalized pulse/sham difference are *identical*, but the native formate flux is `2/1,100,001 s⁻¹`. The target rate differs by exactly two. The native intercept `m_∞=α/R` would distinguish the worlds if measured with sufficient sensitivity; that returns the assay to acquiring the rare occupancy. The exact fractions and reconstruction are replayed by [`exact_fixture.py`](exact_fixture.py), which uses only the Python standard library; its output is saved as [`EXACT_FIXTURE.json`](EXACT_FIXTURE.json). This is an analytic toy, not an observed substrate effect.

A second failure mode is hidden heterogeneity: an enriched potential pulse may populate two hydride conformers in a different mixture from spontaneous native formation. A single aggregate optical band and single apparent exponential do not show equality of these entrance distributions, and product branches can differ. Operando Rh-hydroformylation work reports simultaneous mono- and bis-phosphine acyl intermediates and their ratios changing with CO/phosphine conditions ([primary FlowNMR study](https://doi.org/10.1039/C9FD00145J)); that is a concrete chemical reason to audit state mixtures rather than equate a signal with a single state. A physically successful version needs resolved spectra/labels or a bound on hidden fractions and their branch hazards. Preparing many sites is not preparation of the correct *conditional* microstate distribution by definition.

## Complete acquisition and control bill

The native input contract includes identified active-site count and turnover availability; measured potential at the catalytic interface (not only potentiostat set point); proton/CO₂ activities; temperature; catalyst age and site distribution; state-resolved signal-to-population calibration; formate/H₂ detection efficiency, lag and background; and proof that the pulse and titration preserve the same active chemistry. The apparatus consumes catalyst, electrolyte, substrate, electrodes, reference standards, isotope tracer if used, spectrometer/MS acquisition time, pulse and return time, mixing/washout time and control samples. Electrical cost includes double-layer charge, Faradaic charge and dissipation over the complete pulse train; computational fitting, deconvolution and uncertainty propagation are additional. `M` parallel sites reduce wall time while increasing total charge, reactants and readout load. No measured wall time, joules, calibration error or hardware throughput exists here.

Equation (4) can be an expensive precision gate. As a **toy scale**, if `K₀=10⁻⁹`, one ideal electron and 298 K, moving to `K(E₁)≈1` takes about 0.532 V. A 5.7 mV systematic error in the integrated potential corresponds to about 0.22 error in `log K₀`, roughly 25% multiplicative uncertainty. A one-percent error in the integrated charge/free-energy gap gives about 0.21 error in `log K₀`. Such systematic error does not disappear by collecting more pulse sites. Over 0.532 V the chemical system may oxidize/reduce other species or restructure, invalidating the two-state identity. This numerical illustration is derived from constants and assumptions, not an experimental potential window. Equal free-energy overlap across a sequence of windows, reference-electrode stability, local pH/IR-drop correction, reversibility checks and activity controls must be budgeted.

For measured windows `E_0<...<E_L`, (4) is an explicit reweighting bill: if the estimated charge differences have covariance matrix `Σ`, then to first order `Var(log K₀)` contains `(k_BT)⁻² vᵀΣv`, where `v_l=E_{l+1}-E_l`, in addition to the uncertainty of `log K(E_L)` and their covariance. Bias from missed slow states is not in this variance. Directly reweighting one highly biased ensemble back to `E₀` can have a vanishing effective sample size, `n_eff=(Σ_i w_i)²/Σ_i w_i²`; overlapping windows and independent equilibration are the proposed remedy, with their full mixing/measurement time charged. An `O(log(1/K₀))` number of windows is conceivable for a benign fixed-charge two-state system but is not a complexity guarantee for a real catalyst with hysteresis or phase changes.

The decisive comparison is against an **equally informed** laboratory that can use the same enriched intermediate, spectra, transient products and titration. It can fit the conventional full kinetic model directly, or use fast operando spectroscopy and product analysis. The Pattanayak–Berben hydride work already uses a pre-equilibrium hydride-rate relation; the IrOₓ work already performs potential-pulse state/product accounting. No exclusive estimator advantage is established. In simulation with an accurate acquired generator, [umbrella sampling](https://doi.org/10.1016/0021-9991(77)90121-8) can measure the equilibrium rare-state ratio, while [transition-path sampling](https://doi.org/10.1039/A801266K) and [forward-flux sampling](https://doi.org/10.1103/PhysRevLett.94.018104) can obtain reactive paths/rates; [weighted ensemble](https://arxiv.org/abs/0810.1963) can preserve path weights under resampling. They still pay for a trustworthy physical model and score/restart access. A physical assay may be useful when those are unavailable, but a matched comparison must charge its own calibration and perturbation costs. No source inspected here establishes the proposed combination's novelty or its superiority.

## Decisive remaining test and status

On a molecular catalyst with resolved `A` and `I`, conduct blinded random-order potential pulses and sham pulses at the native operating potential across a CO₂-activity series. Independently measure `K₀` with overlapping reversible titration windows. Pre-register (3) and its uncertainty before measuring the native formate rate by a separate long, direct product assay. Verify single-exponential `Δm`, constant `Δj_F/Δm` and `Δj_H/Δm` over pulse amplitudes, unchanged catalyst/site spectrum and mass/charge balance, plus an off-versus-on test of `α/β`. An isotope product label must agree with the unlabeled chemistry after a measured isotope-effect correction. If the inferred native rate misses the direct rate outside the joint uncertainty, or if hidden state mixtures/transport make the interval vacuous, the operation fails. No such experiment was performed here.

| Item | Status |
|---|---|
| Equations (2)–(3) and exact two-world counterexample | Derived and finite-rational replayed for the stated two-state model |
| Potential-gated preparation, hydride-resolved pulse release, full calibration | Proposed, unperformed |
| Existence of related hydride pre-equilibrium, stopped-flow continuation and potential-pulse readout | Supported in the cited primary systems, which are different systems/conditions |
| Transfer of reaction-off `K₀` to native `α/β`; identical pulsed and native `I` | Unverified decisive assumptions |
| Native rare rate, rate advantage, historical novelty, external validation | **UNKNOWN / NOT ESTABLISHED** |

Capital context, read at local checkout revision `5611ad3fc9aa31b6bd09738d1831020ca4235e49`: dossiers `N490`–`N492` treat finite-state rare-path variance and acquisition as scoped and unreviewed, and explicitly leave high-dimensional certificate acquisition and physical-time conversion open. Those dossiers do not prove that a reversible laboratory control cannot add the information used here. The earlier campaign's hidden-channel lower bound likewise covers a different local-row acquisition contract. Neither is used as a premise for the chemical identity or the kinetic transport.

### Sources actually inspected

- [Pattanayak & Berben, JACS 2023](https://doi.org/10.1021/jacs.2c10942): accessible indexed article introduction/abstract and primary paper record; hydride pre-equilibrium, fast formation, CO₂-to-formate versus H₂ and reported rate scale. I did not independently reanalyse its supplementary data.
- [Primary metal-hydride stopped-flow study, Chemical Science 2018](https://doi.org/10.1039/C8SC02535E): accessible indexed abstract/record; CO₂ insertion measured by rapid mixing and chemistry dependence. Full experimental traces were not inspected.
- [Liang et al., Nature Materials 2026, full PDF](https://www.nature.com/articles/s41563-026-02514-9.pdf): inspected abstract, potential/spectroscopy and pulse/O₂ passages including Figure 4 explanation; potential steps, O⁻/O₂ quantification, and the paper's own nonlinear rate warning. This is adjacent empirical prior art, not validation of (3) on IrOₓ.
- [Primary Rh FlowNMR study, Faraday Discussions 2021](https://doi.org/10.1039/C9FD00145J): accessible indexed article excerpt; concurrent catalyst intermediates and CO/phosphine-dependent ratios. Full data were not reanalysed.
- [Spin-trapping artifact experiment](https://pmc.ncbi.nlm.nih.gov/articles/PMC3859841/): indexed full-text excerpts; isotope-order artifact and false-positive mechanism. It is a caution for the abandoned trap-only proposal, not evidence against every trap.
- [Torrie & Valleau, umbrella sampling](https://doi.org/10.1016/0021-9991(77)90121-8), [Bolhuis–Dellago–Chandler, transition-path sampling](https://doi.org/10.1039/A801266K), [Allen–Warren–ten Wolde, forward-flux sampling](https://doi.org/10.1103/PhysRevLett.94.018104), and [Zhang–Jasnow–Zuckerman, weighted ensemble](https://arxiv.org/abs/0810.1963): inspected accessible primary abstracts/records for the competitor capabilities; no implementation benchmark was run.
