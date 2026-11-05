# Dense electrolyte opportunity audit: rejected as the selected discovery target

## Decision

The apparent failure of viscosity to predict lithium transport in high-concentration and localized high-concentration electrolytes is real, quantitatively large, and technologically relevant. It is nevertheless already addressed by measured Onsager correlations, reference-frame-aware transport, and explicit molecular mechanisms. I do **not** nominate this anomaly as a new scientific opening. The remaining shortage of transferable composition-to-coefficient prediction or complete ternary characterization is not, by itself, evidence for a new organizing principle.

Compared with the parent investigation of competitive solid-state synthesis, this branch currently has weaker grounds for selection. It offers a striking failure of a weak baseline but no demonstrated failure of the strongest applicable framework. Synthesis should also be tested against its latest kinetic competitors before selection; this rejection does not endorse an unconstructed synthesis breakthrough.

## Primary measured object and acquisition

Bergstrom and McCloskey, *Ion Transport in (Localized) High Concentration Electrolytes for Li-Based Batteries*, ACS Energy Letters 9 (2024), 373–380, DOI [10.1021/acsenergylett.3c01662](https://doi.org/10.1021/acsenergylett.3c01662), provides actual measured viscosity, ionic conductivity, mutual salt diffusion, transference number and thermodynamic factor. [Accessible full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC10863389/).

The material family is LiFSI in dimethyl carbonate (DMC), with tetrafluoroethyl-tetrafluoropropyl ether (TTE) added to make localized high-concentration formulations. The tables below preserve the paper's molar ordering **LiFSI:DMC:TTE**. Ion and solvent mobilities came from electrophoretic NMR; self diffusion from pulsed-field-gradient NMR; electrochemical methods supply the other transport quantities. Reported molality is relative to DMC mass, so it must not be mistaken for molality relative to total DMC plus TTE.

The main text was acquired and retained in `bergstrom2024_fulltext.md`. Tables 1 and 2 were manually transcribed into `bergstrom2024_tables.json` and CSV. These are a transcription of published measurements, not new experimental data or underlying instrument records. The supplement could not be acquired: the PMC URL returned captcha HTML, retained honestly as `bergstrom2024_si.response.html`, and the ACS URL was blocked. Thus the exact uncertainty convention and measurement temperatures were not verified from the supplement. The entries marked ± below are simply the authors' reported ± quantities; no confidence level is assigned here.

An important method qualification: to suppress convection in eNMR, 3–4 wt% PVDF was added as a gelling agent to the dilute 1:10:0 and 1:4:0 samples. This makes an indiscriminate six-formulation comparison of all measurements less clean. The selected 1:2:0 versus 1:2:1 comparison avoids those explicitly gelled formulations. The main paper reports the procedure but the detailed supplement remains unavailable.

| LiFSI:DMC:TTE | Salt / M, Table 2 | Viscosity / mPa s, Table 1 | Conductivity / mS cm⁻¹ | Mutual D / 10⁻⁷ cm² s⁻¹ | Lab-frame tLi | Thermodynamic factor |
|---|---:|---:|---:|---:|---:|---:|
| 1:10:0 | 1.08 | 1.81 ± 0.04 | 10.04 ± 0.50 | 35.3 ± 3.2 | 0.28 ± 0.09 | 0.67 ± 0.29 |
| 1:4:0 | 2.38 | 6.56 ± 0.06 | 10.54 ± 0.53 | 32.5 ± 2.7 | 0.32 ± 0.05 | 2.60 ± 0.69 |
| 1:2:0 | 3.90 | 34.79 ± 0.11 | 4.17 ± 0.21 | 7.23 ± 0.84 | 0.37 ± 0.07 | 2.38 ± 0.58 |
| 1:1.1:0 | 5.49 | 248.89 ± 1.20 | 1.19 ± 0.06 | 1.36 ± 0.04 | 0.52 ± 0.05 | 1.16 ± 0.15 |
| 1:1.23:0.62 | 3.50 | 45.55 ± 0.21 | 1.43 ± 0.07 | 3.14 ± 0.18 | 0.35 ± 0.07 | 1.68 ± 0.35 |
| 1:2:1 | 2.46 | 10.97 ± 0.07 | 2.85 ± 0.14 | 11.8 ± 0.91 | 0.24 ± 0.03 | 2.42 ± 0.40 |

The source has two small concentration discrepancies: Table 1 gives 5.41 M for 1:1.1:0 and 3.49 M for 1:1.23:0.62, whereas Table 2 gives 5.49 and 3.50 M. Both values are retained in the JSON rather than silently reconciled. The selected comparison is unaffected.

## Quantitative comparison: the observation survives, the novelty claim does not

Compare 1:2:0 with 1:2:1. This keeps the salt-to-coordinating-solvent ratio fixed while adding one molar equivalent of TTE per LiFSI. It does **not** keep total salt concentration fixed: concentration falls from 3.90 to 2.46 M.

Computed directly from the tables:

- Viscosity ratio = 0.315320: a **68.47% reduction**.
- Conductivity ratio = 0.683453: a **31.65% reduction**.
- Laboratory-frame lithium transference number ratio = 0.648649: 0.37 to 0.24.
- The laboratory-frame lithium contribution to the linear current coefficient, κtLi, changes from 1.5429 to 0.6840 mS/cm, a ratio of 0.443321: a **55.67% reduction**.
- Mutual salt diffusion increases by **63.21%**.
- Thermodynamic-factor point estimates differ by only 1.68%, substantially less than the displayed uncertainties.

A concentration-corrected Walden-like prediction κ proportional to c/η would predict

κLHCE/κHCE = (2.46/3.90)(34.79/10.97) = **2.000407**,

whereas the observed ratio is 0.683453. The simplistic prediction therefore overestimates the relative conductivity by a factor of **2.926911**. Correcting for concentration is essential: attributing the whole reduction to dilution would miss the stronger discrepancy.

This is a useful falsification of a viscosity-only design intuition. It is **not** a comparison with the strongest existing theory. The original paper explicitly identifies viscosity's insufficiency and uses measured correlations to interpret it.

As a nonprobabilistic sensitivity check, independently allowing each conductivity to span its displayed ± value gives a ratio interval [0.6187, 0.7551]. Allowing κ and tLi to span their displayed ± values gives a κtLi ratio interval [0.2953, 0.6795]. These are rectangular extrema, **not** confidence intervals: the uncertainty convention and covariance are not known. In particular κ and the inferred transference number need not have independent errors.

κtLi is not a battery limiting current, power density, charging speed, or concentration-polarization figure of merit. Frame choice, diffusion, activity, convection, electrode reactions, geometry, and interfacial stability all matter. Calling the product a universal lithium-conduction capability would overclaim the data.

The reproducible calculation is `compare_measurements.py`; output is `comparison_results.json`. No parameters were fitted.

## Existing operation that explains the observation

The appropriate constitutive object is a coupled Onsager transport matrix plus thermodynamic derivatives, defined in an explicit reference frame. For monovalent ions, the charge-current conductivity in a fixed frame is proportional to L++ + L−− − 2L+−. Ion self diffusivities and static coordination alone do not fix these cross-correlations. A change in viscosity or even faster self diffusion cannot establish the direction of the change in useful charge current.

Bergstrom and McCloskey already infer these coefficients from combined eNMR, electrochemistry and self-diffusion measurements. They report decreasing per-ion cation–anion correlated motion as concentration increases, despite increased static association. Their distinct cation–cation term becomes less negative in high concentration formulations; adding TTE makes it more negative. The distinct anion–anion term is approximately zero within their uncertainty. It would be inaccurate to turn 'more positive' into a blanket claim of measured positive cation–cation correlations. In the highest-concentration sample the cation–cation distinct contribution is near zero within uncertainty.

The molecular account is that structural exchange/hopping and the persistence of ion associations matter more than the mere count of associated ions. This interpretation is supported by earlier simulation and extended in Mohanakrishnan et al., *Correlated Ion Transport Governed by Dynamic Local Structure in High Concentration and Localized High Concentration Electrolytes*, Chemistry of Materials 38 (2026), 7141–7150, DOI [10.1021/acs.chemmater.6c00541](https://doi.org/10.1021/acs.chemmater.6c00541), [full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC13420536/). Full text retained in `mohanakrishnan2026_fulltext.md`.

That work already constructs a concentration-dependent graph/cluster account of connected ion-rich structures, micelle-like regions and fragments; it compares dynamics and Onsager correlations across DMC/TTE formulations. TTE is not simply an inert viscosity reducer. The simulation uses LAMMPS, OPLS-AA-type force fields and a 0.72 scaling of ionic charges benchmarked against experimental conductivity, viscosity and density. Consequently its experiment agreement cannot all be treated as independent validation. Its topology depends on the finite box, cutoff definitions and force field. These limitations qualify the molecular conclusions, but they do not create evidence that merely renaming the network is a new scientific operation.

## Stronger competitor: predictive macroscopic transport already demonstrated

Wang et al., *Potentiometric MRI of a Superconcentrated Lithium Electrolyte: Testing the Irreversible Thermodynamics Approach*, ACS Energy Letters 6 (2021), 3086–3095, DOI [10.1021/acsenergylett.1c01213](https://doi.org/10.1021/acsenergylett.1c01213), [full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC8438662/), provides a more decisive baseline than a correlation fit. Full text retained in `wang2021_fulltext.md`.

They independently characterize the composition dependence of conductivity, salt diffusivity, solvent-frame transference number, thermodynamic factor and two partial molar volumes for LiPF6/EMC. They then predict an experimental concentration field using coupled Onsager–Stefan–Maxwell charge, volume and cation balances including Faradaic convection.

The validation experiment used 3 M LiPF6/EMC between planar lithium electrodes separated by 8 mm in a sealed cylindrical PEEK cell. A 60 μA current (0.48 mA/cm²) was applied for 2 h, followed by an open-circuit hold. Vertical orientation and upward positive current minimized buoyancy effects. 19F MRI imaged the PF6 anion approximately every four minutes; lithium concentration was inferred from local electroneutrality. Voltage was recorded synchronously.

The authors explicitly state that the material parameters measured ex situ were not adjusted to achieve the validation agreement; geometry, current and pulse duration specify the test. They report theoretical and experimental concentrations within **±5% at all times**, and open-circuit voltage relaxation within **7 mV**. These error statements are the authors' comparison, **not an independent numerical reproduction here**. The open-circuit qualification is essential: the electrolyte model does not itself establish the full on-current electrode overpotential. There is a localized relaxation mismatch near the plating electrode, which the authors discuss in relation to MRI shielding by mossy lithium.

This shows that a dense electrolyte can violate dilute intuition while retaining quantitatively predictive established thermodynamics. It does not establish that an independently parameterized binary LiPF6/EMC model automatically predicts arbitrary ternary LiFSI/DMC/TTE behavior. It does establish the correct strength of the comparison: coupled measured transport and thermodynamic coefficients, not Stokes–Einstein/Walden or ideal Nernst–Planck alone.

The authors supply [code and raw MRI/electrochemical records](https://github.com/ndrewwang/EMC-MRI-model). The MATLAB/COMSOL source, repository tree, README, and raw measurement files were acquired under `wang2021_repository/`. The executable requires COMSOL; that solver was not run here. Availability of source is not a replication claim.

## The genuine remaining gap, and why it does not yet pass selection

The 2024 paper acknowledges that a ternary system has six independent Onsager coefficients, but simplifies LiFSI/DMC/TTE to a binary electrolyte with a mean solvent. This removes the explicit relative DMC–TTE transport mode. The paper motivates this by local segregation; local nanostructure alone should not be assumed to prove bulk thermodynamic phase separation.

An explicit ternary model could therefore be needed under sustained composition gradients or selective solvent motion. However, this is already a standard multicomponent transport problem. We have not acquired a held-out ternary concentration-field experiment that defeats a fully parameterized multicomponent Onsager–Stefan–Maxwell model. Nor have we constructed a new operation that predicts its transport coefficients from a cheaper independently available object with demonstrated transfer across compositions, force fields, temperatures and protocols. Measuring the missing coefficients, adding the missing species, or fitting a graph descriptor would not by itself satisfy the user's intended breakthrough.

A viable future selection would need a concrete comparison of entire concentration and current fields, independent composition-to-coefficient predictions, and a completed useful energy endpoint including preparation, formulation mass/cost, electrodes, thermal management and degradation. This audit does not provide those and does not nominate the work as an achieved capability.

## Parent-facing conclusion

Reject the dense-electrolyte viscosity/correlation anomaly as the selected opening. The measured 68.5%-lower-viscosity / 31.7%-lower-conductivity contrast is robust enough to be scientifically useful, but the field already has the relevant organizing representation and at least one stringent independent macroscopic validation. The strongest unresolved part is transferable quantitative parameterization under full multicomponent forcing, a broad research challenge without a demonstrated superior construction in this audit.
