# Retained atomic operations without exact layer addressing

2026-10-27. **New consequential device or scientific operation: NOT_ACHIEVED. Physical experiment: NOT_PERFORMED.** The useful result is a concrete replacement for an unnecessarily strong prerequisite, followed by source-specific tests of its limits. Exact depth addressing is unnecessary for an empirical experiment on lateral defect-pattern policies. It is also unnecessary in the first-Born projected-density formula. Neither statement supplies a calibrated quantum Hamiltonian, a predictable electron-optical transfer function, or an advantage over ordinary platforms.

The strongest acquired starting point is a retained structural pattern with an independently demonstrated in-microscope diffraction response. The proposed extension is an equal-cost, deliberately correlated material intervention, with its final response measured rather than inferred from an unobserved atom arrangement. This is a useful experimental model class. Its new functional result has not been acquired here.

## What the source actually supplies

[Klein et al., Nature (2026)](https://www.nature.com/articles/s41586-026-10431-9) demonstrate many selected Cr-column modifications in multilayer CrSBr. Their larger pattern occupies roughly 150 × 100 × 13 nm and involves over 4,000 target columns; the reported approximately 40,000 displaced atoms are not 40,000 independently addressed sites. The [public peer-review response](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-026-10431-9/MediaObjects/41586_2026_10431_MOESM2_ESM.pdf), PDF pp10, 22–24, expressly distinguishes the demonstrated interface from exact atom-number/depth control and from future optical/spin measurements.

The [49-page supplement](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-026-10431-9/MediaObjects/41586_2026_10431_MOESM1_ESM.pdf) supplies two particularly useful observations:

- S7, PDF pp28–29: defect superlattices with spacing 5a by 4b give new nanobeam electron diffraction spots at 60 keV, 50 pA, approximately 50 nm beam diameter. Two displacement orientations were tested.
- S8, PDF pp29–30: a patterned region was recovered after one hour in ambient conditions and seven hours in the microscope. Further high-energy imaging moved defects. This demonstrates structural retention at the reported interval, not a read-endurance specification. The identical diffraction transfer function before and after ambient removal was not established by this experiment.

The custom positioning, lattice walking, directional scanning and automation software is not publicly released; the source attributes this to ongoing IP protection. Public CIF/simulation notebooks therefore do not acquire the actual fabrication workflow. The full main article body was not acquired in this branch; the abstract, data/code availability, complete supplement, peer-review response and deposited figure material were available.

## A weaker operational contract that survives hidden depths

Use a fixed fabrication grid, a fixed beam-action protocol and a fixed number of actions. Choose between two in-plane masks, then measure a specified final observable, such as a diffraction spectrum. The object of study is the distribution

`P(final measured response | mask, complete fabrication/read protocol)`.

Hidden layers are included in that distribution. Randomly assigning masks to independently prepared, matched patches permits a causal comparison of the **whole mask policies**, assuming independent treatment assignment, consistent protocols and no interference between patches. It does not require a reconstructed layer for every defect.

This is weaker than claiming the masks produce identical final defect populations or differ only in pair correlations of a known Hamiltonian. Equal action count/dose does not imply equal final defect density: neighbouring writes, drift and defect-dependent channeling can change yield. Isolating geometry at fixed finished density requires population calibration and appropriate controls. A measurement of a mask-policy effect could nevertheless be scientifically useful even when its microscopic mechanism remains unresolved. This removes exact layer addressing as a universal prerequisite for materials experiments; it does not remove measurement or calibration costs.

The source already supplies the basic patterning and diffraction ingredients. No physical mask-policy comparison or new retained functional response was performed in this branch. An autonomous optimizer would obtain an empirical response surface, not silently acquire specified couplings. Ordinary Fourier optimization and ordinary experimental design receive the same observations and actions.

## Executed construction: an actual source-grid mask and its uncertainty bill

`analysis/projected_operation.py` compiles two 2,000-action masks in an 80 × 50 grid. With the deposited CIF, their spacings are 17.5295 Å and 19.0812 Å, covering 140.236 × 95.406 nm. Coordinates lie on the native Cr sublattice with origin `(a/2, 0)`. The output CSVs are **computed, unwritten coordinates**, not acquired material. One mask is random; the other uses an ordinary fixed-cardinality greedy Fourier swap method. Both prescribe the same +b action, allowing the stronger directed interface rather than restricting the comparator to symmetric ±b motion.

For a common in-plane displacement d, projected column count n_j and first-Born scattering, the *change* in elastic amplitude is

`ΔA(q) = f_Cr(q) [exp(i q·d) − 1] Σ_j n_j exp(i q·R_j)`.

This formula is independent of which layers supply n_j when q_z is neglected. It is not independent of counts, displacement signs, host relaxation, charge redistribution, illumination or multiple scattering.

Let `v_j = exp(i q·R_j)`, common mean count μ and count covariance C. Then

`E |Σ_j n_j v_j|² = μ² |Σ_j v_j|² + v† C v`.

Thus a designed mask zero does not specify a physical zero. Mean count alone cannot determine its noise floor. For `L=16` and an **unvalidated sensitivity value** `p=0.625`, both of the following models have μ=10:

| Count model | Variance per written column | Additive normalized floor |
|---|---:|---:|
| Independent Bernoulli displacement in each layer | `L p(1-p)` | `(1-p)/(L p) = 0.0375` |
| All layers within each column switch together; columns are independent | `L² p(1-p)` | `(1-p)/p = 0.6` |

Normalization is by `μ² M |f_Cr(exp(iq·d)−1)|²`, away from form-factor zeros. Spatial cross-column correlations contribute further off-diagonal terms. Neither covariance model was inferred from the experimental data. The approximately ten displaced atoms per column discussed in the source is not a fitted per-layer Bernoulli probability.

The computed mean target mask power falls from **0.6721913 to 0.0001812493**, a geometric ratio of **3,708.7**. Adding the two declared floors changes the expected ratios to **18.83** and **2.120**, respectively. Two independent 2,000-draw Monte Carlo moment checks are within 0.49 estimated standard errors of their analytic means. These are checks of the declared probability models, not physical calibration or evidence of a device gain. An equally informed ordinary controller gets the identical optimized coordinates.

The source-size illumination matters separately. A 50 nm hard-disk illumination model, translated over 15 locations, reduces the geometric mask improvement to **3.797**. This calculation compares centered density fluctuations after removing the common half-fill aperture amplitude; it is not a calibrated measured intensity subtraction. A global cancellation across a 140 nm field cannot be assumed visible in a 50 nm patch. The true beam profile and coherence would have to enter the actual design.

Local atom conservation also supplies a useful but limited observation: `[exp(iq·d)−1]` vanishes at q=0 and is linear in small q. Under a bounded iid-count model the displacement-induced diffuse term therefore has a q² factor, unlike unpaired random atom removal. This is not proof of actual material hyperuniformity or transparent electronic/phononic disorder. Defect electronic potentials are not the Cr number density, and long-range correlations, other displaced species and non-kinematic scattering need separate treatment.

## A source-informed counterexample to a count-only diffraction operator

It would be tempting to close the previous chain by noting that the Ewald depth phase is small. At the first 5a and 4b superlattice orders the computed `q_z T` is only 0.0636 and 0.0537 radians at 60 keV, and smaller at 200 keV. That controls one first-Born phase effect. It does not eliminate dynamical scattering in a 13 nm crystal.

`analysis/multislice_projection_test.py` executes a finite abTEM test using the deposited CIF, 5 × 4 × 16 host cell, and the authors' approximate +b interstitial displacement `(0, b/2, −a/2)`. Exactly ten Cr atoms are moved in one selected column, with four different depth assignments: first ten, last ten, spread ten and seeded random ten. All four have **numerically identical summed projected potential**. Ten Å of vacuum on each side prevents truncating atomic potential tails. The grids are commensurate with the lateral host cell.

| Numerical setting | Max/min first b-superlattice Fourier intensity, 60 keV | Same ratio, 200 keV |
|---|---:|---:|
| 320 grid, 1 Å slice | 1.4647 | 1.2138 |
| 640 grid, 1 Å slice | 1.4800 | 1.2129 |
| 320 grid, 0.5 Å slice | 1.5265 | 1.2226 |
| 640 grid, 0.5 Å slice | **1.5239** | **1.2189** |

At the final setting the 60-keV chosen-order fractions range from `9.9011e-5` to `1.5088e-4`. These are fractions of the calculated elastic exit-wave Fourier norm, **not measured absolute diffraction efficiencies**. The projected-phase approximation gives an identical response for all four depth assignments; multislice does not. The qualitative discrepancy persists across the declared grid/slice refinements. This is a finite numerical counterexample inside the assumed model, not a numerical certificate or a validated physical error bar.

The model omits relaxed defect coordinates, charge changes, temperature, inelastic scattering, partial coherence, finite-array edges, instrument response and damage. The public displacement construction is approximate. Its purpose is to reject the inference “small q_z and known projection automatically give a predictable device,” not to predict a real mask's efficiency. An initial 256-grid diagnostic without vacuum padding is retained but excluded from conclusions.

## Exact depth is also not identical to known aggregate couplings

There is a simple count-only bound that can sometimes replace layer assignment. If two columns contain n_1 and n_2 defects among L possible matching layers, their common-layer count satisfies

`max(0,n_1+n_2−L) ≤ overlap ≤ min(n_1,n_2)`.

For 10 and 10 defects in 16 layers this is 4–10. For 8 and 8 it is 0–8, including an entirely disconnected same-layer pair with the same projection as a fully aligned pair. Explicit witnesses are in the JSON output.

This bound can protect an aggregate contrast if occupancy lower bounds and suitable couplings are acquired. As an algebraic sensitivity example only, SI Table S1 gives partial-DFT+U dxy hopping magnitudes 10.6 meV at 10.5 Å and 0.5 meV at 14 Å. Under an additional independent matching-layer `Σ|t|²` response model, the worst overlap ratio would still leave `(4/10)(10.6/0.5)² = 179.8`. This is **not** a transport result: the count bounds, compatible interstitial orientation, actual many-orbital response, magnetic configuration, charge filling and detector coupling were not acquired. The source's Hamiltonian/screening approximations do not supply these interfaces. It demonstrates why exact layer identity is not logically necessary for every aggregate contrast, while exposing the weaker sufficient measurements that remain absent.

## Strong ordinary alternatives and what they erase

| Intended operation | Acquired ordinary comparator | Consequence for this route |
|---|---|---|
| Arbitrary electron wave shaping or beam splitting | [Harvey et al., NJP (2014), author manuscript at NIST](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=918165): measured phase gratings, 80 nm periods over 50 µm diameter, periods down to 20 nm; one table reports 0.17 ± 0.04 incident-normalized and 0.34 ± 0.07 transmitted-normalized first-order efficiency. Coated gratings remained usable in the beam for weeks. | The broad operation is already real. Electron optics maps these masks to Å-scale probes, so atomic mask pitch alone is not a new output-resolution capability. CrSBr lacks the corresponding calibrated efficiency, phase fidelity and endurance. |
| Known tight-binding graph and electronic-state readout | [Drost et al., Nature Physics (2017)](https://arxiv.org/abs/1611.01049): atomically fabricated Cl-vacancy lattices, measured LDOS, dimer-chain domain-wall and Lieb-lattice states. | Reproducing a computed SSH/flat-band diagram for CrSBr would not establish a new simulation operation. Buried, retained host remodeling is a different fabrication interface. |
| Controlled disorder with calibrated local potentials and quantum dynamics | [Choi et al., Science (2016), full author paper/SI](https://oar.princeton.edu/bitstream/88435/pr1k06x136/1/1604.04178.pdf): DMD disorder, site-by-site microwave calibration, measured correlation length 0.6(0.1) lattice spacings, single-site atomic readout. | Generic programmable-disorder discovery is established. Its loading, cooling, optics and repeated-shot costs must be charged, but CrSBr must supply an observable/model class that the ordinary simulator does not already implement. |
| Many individually controlled quantum sites | [Manetsch et al., Nature (2025)](https://www.nature.com/articles/s41586-025-09641-4): over 6,100 trapped atoms with defined qubits and measured coherence/readout. | Tens of thousands of Cr movements cannot be counted as tens of thousands of known qubits or couplings. Atom cooling and continuous trapping are real costs; retained structural memory is not qubit coherence. |
| Change CrSBr magnetic order despite stochastic depth | [Pfister et al., Nano Letters (2023)](https://krasheninnikov.de/publ/Cr-S-Br.pdf): nonmagnetic ion irradiation produces measured remanence/hysteresis and ferromagnetic behavior up to about 110 K. | “Defects alter magnetism without exact depth control” is already demonstrated in the same host. The possible new variable is selected nanoscale geometry at matched defect population, whose functional advantage is still unmeasured. |
| Atomic pattern storage/rewrite | [Kalff et al., Nature Nanotechnology (2016)](https://arxiv.org/abs/1604.02265): automated 8,000-bit Cl-vacancy memory, read/rewrite and stability to 77 K. | CrSBr's room-temperature structural retention is attractive, but no completed capacity, bit-error, read-disturb, rewrite-endurance or full-cycle storage benchmark was supplied. |

These are scope comparators, not an assertion that all platforms implement the same CrSBr solid. Their full economic costs were not measured here. The same-host ion experiment is particularly important: retained stochastic defect populations are already sufficient for some magnetic operations, so exact-depth failure does not imply that all consequential material control is blocked.

## Physical resource and completion account

The source response gives about 1 s at 20 pA per column, or 0.5 s when the current is doubled for the larger array, plus roughly 10 ms positioning. At 200 kV this is approximately **1.248e8 incident electrons, 20 pC and 4 µJ incident kinetic energy per target column**. For 4,000 actions it is about **34 minutes including the stated positioning overhead and 0.016 J incident kinetic energy**. This is not deposited heat, wall-plug consumption or the cost of producing a usable array. The 2,000-action candidate mask inherits a nominal 17-minute action/positioning bill before preparation, reads or repairs.

At the source's 50-pA read current there are 3.121e8 incident electrons/s. Treating 50 nm diameter as a uniform disk gives about 1,589 electrons/Å²/s and illuminates approximately 587 eligible source-grid columns. Actual beam shape, exposure and dose response were not acquired. One diffraction image does not establish unlimited nondestructive reads, especially when other imaging conditions visibly move defects.

The full comparison still owes crystal growth/exfoliation, thickness selection, suspended-membrane transfer, cleanliness, vacuum/instrument setup, aberration/drift calibration, acquisition of the proprietary control workflow, write/read registration, count/covariance calibration, every read and read-induced change, recovery/replacement, any contact or cavity fabrication, and retained functional characterization. Rewriting a pattern under the beam is not yet a measured erase/rewrite cycle with bounded collateral change. Correlation measurements across independent patches also require replication; one optimized mask is not a material response distribution.

This branch downloaded **23,089,005 bytes** of new public material: Figure 5 notebook, Figure 5c array and a comparator manuscript. The two deposited files match their advertised MD5s; that verifies transport only. The Figure 5c array is a 310 × 310 floating image without acquisition-clock/incident-normalization metadata; its plotting code uses a logarithmic display. It was inspected without executing notebooks or deserializing pickled objects. It does not acquire absolute diffraction efficiency. The four quoted multislice runs cost approximately **191 seconds** in aggregate; an excluded initial diagnostic cost another approximately 12 seconds. No experiment, paid service, purchase, outreach or external write was performed.

## Evidence tiers and handoff

| Item | Tier/status |
|---|---|
| Large selected-column structures, structural ambient retention, and insitu diffraction peaks | Published experimental source; retained spectrum/endurance not jointly established |
| Projected-amplitude/covariance identities and overlap bounds | Derived at explicitly declared interfaces |
| Concrete masks, covariance moment checks, finite-aperture sensitivity | Executed local computations; no physical pattern or advantage |
| Same-projection dynamical-scattering discrepancy | Executed finite source-informed multislice model; not physical calibration |
| Geometry-dependent optical, magnetic, transport or correlated-state operation from these masks | NOT_ACQUIRED |
| New efficient electron-optical device or new calibrated quantum simulator | NOT_ACHIEVED |
| Practical advantage or civilisation-level capability | NOT_ESTABLISHED / NOT_ACHIEVED |

The usable correction is to pursue an explicitly measured **mask-policy response**, or an aggregate observable with experimentally supplied count/covariance bounds, without making exact depth addressing a universal gate. The computations also show why projected geometry cannot be substituted for a predictable microscopic operator. A new result would have to be an acquired response unavailable or materially better under the equally informed ordinary alternatives above. This branch has not acquired it.

Reproduce with the sibling `empirical_operation_invention/.venv/bin/python` runtime: run `analysis/projected_operation.py`; run `analysis/multislice_projection_test.py` at grids 320 and 640 with slice thicknesses 1 and 0.5 Å; then run `analysis/finalize.py`. All new files are confined to this owned directory. `outputs/RESULTS.json` is the compact machine-readable handoff; `outputs/projected_operation.png`, `outputs/depth_projection_counterexample.png`, the coordinate CSVs, public input copies and individual numerical JSONs retain the evidence.
