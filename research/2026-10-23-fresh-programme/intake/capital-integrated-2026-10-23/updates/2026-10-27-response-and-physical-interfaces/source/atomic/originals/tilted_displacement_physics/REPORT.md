# Tilted CrSBr writing: a physical interface screen

**Status: NOT_ACHIEVED for a retained, layer-selective physical write or a depth-preserving reset.** This branch acquired a substantially sharper route decision: ordinary reuse of the demonstrated scanning actuator destroys most of the favorable parked-ray fluence separation. A parked, oblique 200-keV actuator remains physically possible and is the better acquisition target. A counter-propagating 60-keV interstitial-return actuator is a plausible ordinary recovery alternative under explicit dynamical priors. Neither operation has been acquired from the public data.

The executed results are in [RESULTS.json](outputs/RESULTS.json), [corrected_scan.json](outputs/corrected_scan.json), and [validation_and_reset.json](outputs/validation_and_reset.json). The [figure](outputs/tilted_interface.png) displays the principal screens. These are mathematical/physical diagnostics, not measurements of layer hazards.

## What the available sources constrain

The exact starting source is [Klein et al., Nature (2026)](https://www.nature.com/articles/s41586-026-10431-9), public SI, public review, and [GitHub revision 6844cc568271d448704a0eb6ee55ddfd5246d242](https://github.com/KleinAtomLab/Mesoscale-atomic-engineering/tree/6844cc568271d448704a0eb6ee55ddfd5246d242). Main-article body access was not acquired. Local source hashes are retained in `sources/used_source_manifest.json`.

* SI PDF pp31–33: the reported ground-state path gives a 0.672-eV return barrier from δ2 and about 0.3 eV from δ1. Interstitial formation energies are 2.473 eV for δ2 and 2.724 eV for δ1. Their sum gives an approximately 3.1-eV forward-path saddle proxy for δ2. This is not an impulsive displacement threshold. The source also reports finite-cell dependence near 2.5 eV; three-decimal arithmetic is not physical threshold accuracy.
* SI pp35–37: S-vacancy-assisted structures have different formation energies, return barriers of roughly 0.3–0.8 eV, and stronger distortions. Those are alternative final states, not a measured dose-resolved damage exclusion.
* SI pp38–44: 200-keV ±b scans exhibit projected reversible population behavior. Seven energies, 80–200 keV, have ensemble intensity panels; decreasing energy reduces directional steering relative to other changes. Only 200-keV effective transition cross sections are printed. There is no angle-resolved, layer-resolved cross-section surface.
* SI pp17–18: after Cr removal, channeling in the donor column weakens and dose leaks to neighbors; simulations use 0, 4, 8, 12, and 16 removed entrance-side atoms. This does not supply the field or transition kernel following one specified layer edit.
* SI pp45–46: alternating neighboring interstitials reduce the incremental formation energy from 2.54 to 2.30 eV by the fourth defect; same-direction increments stay near 2.55–2.59 eV. The source describes a possible chain tendency. Formation-energy changes do not establish impulse thresholds or a dynamical chain reaction.

The public response, PDF p15, explicitly says no MD calculation is presented; PDF p30 also leaves surface displacement thresholds for future work. Thus no acquired angular impulse-to-final-state kernel can certify the tilted write. This is a source boundary, not a negative result about the source's demonstrated projected-column engineering.

The source SI/code rate versions, clock ambiguity, dose normalization, and population/first-event conversion remain unresolved here. No reported cross section is divided by sixteen or promoted to an independent layer hazard.

## Exact kinematics and what the review's number does not establish

Let E be the electron kinetic energy, m its rest mass, M the target mass, and n its incident unit direction. Two-body elastic kinematics gives

\[
T_{\max}=\frac{2Mc^2 E(E+2mc^2)}{(Mc^2+mc^2)^2+2Mc^2E}
\simeq\frac{2E(E+2mc^2)}{Mc^2}.
\]

This is consistent with [Oen's primary displacement calculation, equations 1–2](https://digital.library.unt.edu/ark:/67531/metadc1035569/m1/10/). The exact finite-mass/heavy-target ratio for Cr at 200 keV is 0.9999706. Isotopic average masses were used.

| Electron energy | Cr Tmax | S Tmax | Br Tmax |
|---|---:|---:|---:|
| 60 keV | 2.681 eV | 4.348 eV | 1.744 eV |
| 100 keV | 4.633 eV | 7.514 eV | 3.015 eV |
| 140 keV | 6.717 eV | 10.894 eV | 4.371 eV |
| 200 keV | 10.092 eV | 16.367 eV | 6.567 eV |

The public review PDF p14 calls 2.52 eV the maximum Cr kinetic energy at 200 keV. That is not the full stationary-atom backscattering maximum. It equals one quarter of the latter, also the maximum energy in a purely transverse Cartesian recoil component. The quote does not state such a component restriction; its cause is not identified here. It must not be used to prove that the 3.1-eV path is ballistically inaccessible.

For heavy M, available recoil momenta lie on a sphere of radius p centered at p n. For recoil **parallel to a specified unit direction u**, radial intersection gives

\[
T(u)=T_{\max}(n\cdot u)^2,\quad n\cdot u>0.
\]

The maximum energy in the u coordinate, allowing other recoil components, is instead

\[
T_{u,\mathrm{component}}^{\max}=T_{\max}\left(\frac{1+n\cdot u}{2}\right)^2.
\]

These are different questions. Neither converts a relaxed migration path into an impulsive success law. A lattice trajectory may bend or exchange momentum among atoms; a net displacement vector need not equal the initial successful impulse direction.

The propagation notebook's schematic displacement is b/2 in plane and c/4 out of plane. Taking the sign toward the electron propagation as positive gives u proportional to (0, 2.385, 1.999) Å, 50.04 degrees from c. Reversing the out-of-plane sign reverses the corresponding directional availability; the SI's coordinate sign and propagation convention do not identify a measured recoil direction.

| b tilt toward the +b destination | Parallel recoil at 200 keV | Electron energy where 3.145-eV proxy opens |
|---|---:|---:|
| −10 degrees | 2.517 eV | 242 keV |
| −6 degrees | 3.149 eV | 200 keV |
| 0 | 4.163 eV | 157 keV |
| +6 degrees | 5.215 eV | 128 keV |
| +10 degrees | 5.915 eV | 114 keV |

Tilting therefore need not destroy the displacement direction; its sign can change the available impulse energy by more than a factor of two. But the apparent angular threshold is not robust to an unacquired destination geometry. The pristine CIF places Cr1 2.978 Å from the ideal vdW-gap center. Using that geometric anchor gives a 38.69-degree net vector, 6.149 eV on-axis parallel recoil, and a 110-keV proxy opening. At +10-degree b tilt, both lateral branches then remain above the 3.145-eV proxy. No relaxed defect coordinate or initial reactive tangent was acquired that selects between these anchors.

Even holding the c/4 proxy fixed, changing the assumed impulse threshold by ±0.5 eV moves the on-axis opening from 134 to 178 keV. The source convergence angle is 32 mrad, or 1.83 degrees. Thus a sharp angular veto with a margin of a degree or less cannot be treated as an acquired branch selector.

## Elastic cross-section consequences under declared capture priors

I integrated the [McKinley–Feshbach differential elastic cross section](https://geant4.web.cern.ch/documentation/dev/prm_html/PhysicsReferenceManual/electromagnetic/elastic_scattering/elecnuc.html), using Cr Z=24. For recoil cosine μ=n·u, the electron-to-recoil solid-angle Jacobian is 4μ. The recoil density is

\[
\frac{d\sigma}{d\Omega_u}=
\frac{Z^2r_e^2(1-\beta^2)}{\beta^4\mu^3}
[1-\beta^2\mu^2+\pi Z\alpha\beta\mu(1-\mu)].
\]

The **unmeasured prior** is unit capture into the desired stable defect whenever recoil lies inside a circular cone about the c/4 proxy vector and exceeds a uniform 3.145-eV threshold. At 200 keV on axis, half-cones of 2, 5, and 10 degrees give 1.30, 8.32, and 27.0 barn. Those are not predicted physical CrSBr write cross sections: cone size, reaction threshold, energy dissipation, and capture probability are unacquired.

This calculation nevertheless establishes two useful consequences. First, sub-barn/barn magnitude alone cannot identify a mixed excitation mechanism; a sufficiently small elastic capture basin can also give that scale. This does not establish a purely elastic mechanism. Second, increasing energy transferred toward the reaction direction does not monotonically increase useful cross section: stronger electron backscattering is rarer. For a 5-degree capture cone at 200 keV, b tilts −10, 0, +10 degrees give approximately 0.67, 8.32, and 4.31 barn. A good route must maximize retained capture per damage, not only Tmax.

A separate classical 300-K velocity prior smooths the threshold using energy spread sqrt(2 T kBT), roughly 0.46 eV for the on-axis proxy recoil. It changes the preceding values to 1.84, 7.81, and 4.31 barn. This is not a phonon calculation and omits zero-point motion and excited states. It demonstrates how fragile a hard angular veto is.

The recoil Jacobian and prefactor were checked against the analytic isotropic energy-integrated cross section: both give 573.0467 barn for the declared threshold, agreeing to floating-point precision. Near a cone boundary, quadrature refinement gives 0.662–0.667 barn; the displayed conditional cross sections should be read at about percent precision, far below their physical prior uncertainty.

## The demonstrated scan does not inherit the parked-ray advantage

The previous report used a parked, 0.8-Å FWHM Gaussian ray crossing a chosen native Cr. I computed the actual source sinusoidal scans: +b goes from native Cr to the adjacent S/Br projection, and ±b goes between the two adjacent S/Br projections. The same current, elapsed time, crystal, and Gaussian width are used. All in-plane periodic translations, both Cr bases, all 16 layers, and exact distance perpendicular to the ray are included. These are vacuum fluence comparisons; scattering, channeling, excitation transport, and changing potentials are absent.

At the existing sixteen parked-optimal tilts:

| Beam motion | Chosen atom / all native Cr fluence | Chosen atom fluence per same elapsed exposure, relative to parked peak |
|---|---:|---:|
| Parked | 0.763–0.906 | 1 |
| Source +b | 0.171–0.253 | about 0.27 |
| Source ±b | 0.0744–0.0896 | about 0.115 |

A finite 26×51 angular-grid reoptimization also fails to retain the parked advantage. For layer 8, best +b and ±b fractions are 0.265 and 0.152. For the entrance layer they are 0.467 and 0.125. This is a finite grid screen, not a global certificate. At the same layer-8 parked optimum, the +b scan delivers about four times the target's fluence to other Cr atoms; ±b delivers about 11.7 times. These remain fluence ratios, not event rates.

Tilting also changes the required scan endpoints. With the c/4 destination proxy, a 5.4-degree a tilt shifts the destination transversely from the uncorrected +b scan by about 19 pm; at 7 degrees the shift is 24 pm. This is comparable to the source's 15–20-pm empirical positioning tolerance. I therefore also computed the ordinary corrected two-dimensional scan joining the projected native site and projected destination. Its best finite-grid layer-8 fractions are 0.276 and 0.284 for the two c signs; entrance-layer values are 0.485 and 0.445. Correct endpoint registration does not restore the parked-ray separation in this screen.

At nonzero a tilt, a native site and two same-gap ±b destinations are generally not collinear in projection. A single original ±b line cannot simultaneously pass exactly through all three; a bent trajectory would be a distinct actuator.

A parked ray has a potentially useful retention property: at the layer-8 parked optimum, the source-proxy destination fluence is only 1e−12–3e−10 of the native peak. The demonstrated scans expose the desired interstitial at order-one fluence relative to native Cr. Thus, **acquiring directional displacement with a parked oblique probe** is physically more consequential than simply tilting the demonstrated scan.

A concrete acquisition candidate for layer 8 is 200 keV with tilt a=1 degree, b=+10 degrees, parked on the selected native Cr. Its target/all-Cr vacuum fluence fraction is 0.678, and source-proxy destination fluence is below 3e−8 of native peak. Under the narrow capture priors it can favor +b over −b; that directional preference disappears or weakens under broader cones, thermal velocities, and the alternate gap-center vector. This candidate is selected for testing the missing actuator, not for claiming high-fidelity writing.

The same parked optimum also delivers total S and Br fluences comparable to or greater than the native target's. Their true defect cross sections are unknown; formation energies are not displacement thresholds. The 200-keV kinematic maxima do not exclude their damage. Surface sputtering is explicitly acknowledged as plausible in the public review. No all-species collateral guarantee follows from the favorable Cr ratio.

## Electronic excitation is not an acquired local hazard law

The source response invokes long-lived dark excitons. The cited [Sears et al. PRL (2025)](https://markdean.info/assets/pdf/sears2025observation.pdf) establishes dark-exciton dispersion in both in-plane directions, mainly at 30 K. Its low-energy dark feature weakens strongly by 200 K. It does not measure the lifetime or local bond-softening population under a room-temperature 20-pA electron probe. Neither a local accumulation law nor a diffusion kernel is supplied by that citation.

A different direct optical study, [Meineke et al., Nano Letters (2024)](https://doi.org/10.1021/acs.nanolett.3c05010), measures about 15-ps bulk exciton lifetime at room temperature. That is a different prepared excitation population and does not disprove another long-lived electron-generated state. Its practical consequence is conditional: at 20 pA, electron interarrival time is 8.01 ns and Rτ=0.00187 for a 15-ps state. A steady mean of one such excitation in the relevant volume would require an effective local yield of about 534 excitons per incident electron. Neither that yield nor an appropriate long-lived alternative was acquired. Same-electron correlated excitation/impulse and rare nonlinear events remain possible.

A tilted ray's total geometrical path length grows by only sec(theta), about 0.7% at 6.6 degrees and 3% near the largest combined allowed tilt. That does not preserve the local channeling/excitation environment. The decisive quantities are the spatial and temporal excitation kernel and the resulting reactive capture basin, including the one-defect state.

## Reversibility, rollback, and the stronger ordinary recovery route

The source's projected reversibility must be retained as positive evidence of atom mobility. But the public response PDF p13 describes repeated imaging moving interstitials into random sites, calling the visible pattern erased. SI S21 demonstrates beam-induced mobility and reduced pattern visibility. It does not demonstrate restoration of the original vacancy, unchanged other layers, or bounded S/Br damage. The fitted reverse Γ20 is under ±b exposure, not a parked-interstitial reset measurement.

Moreover, an interstitial moving into a different layer vacancy can restore projected native-column population without restoring the original three-dimensional configuration. The available projected observations do not identify this distinction. No depth-preserving reset kernel is acquired.

In the straight c/4 reaction-coordinate prior, the reverse net direction points backward relative to the writing electron. A recoil exactly along it is unavailable from the same incidence. Even the maximum kinetic energy in that backward coordinate is only 0.323 eV at 200 keV on axis, below the reported 0.672-eV return barrier. This does not forbid actual return: the real path can bend, involve collective motion, use excitation, or restore a different depth. It does explain why seeing a projected return does not identify a simple opposite ballistic write.

A stronger ordinary alternative is **opposite-side irradiation of the detected interstitial at lower voltage**. Flipping incidence makes the reverse coordinate forward. Under the c/4 proxy, the return-barrier opening is about 37 keV, whereas native-write opening is about 157 keV. At 60 keV the parallel return recoil is 1.106 eV. A stricter energy-only screen keeps Cr Tmax below the 3.145-eV native forward-path proxy below about 70 keV; the resulting differential window is about 37–70 keV, still conditional on the two reported-path barriers being relevant dynamical thresholds. The ideal gap-center vector changes the two openings to about 25 and 110 keV. Thus 60 keV is a source-informed candidate for selective return across both geometric anchors; it is not a calibrated reset. At 60 keV, S Tmax is still 4.35 eV, and surface/defect damage remains unbounded.

Specimen flipping, re-registration, opposite-side access, low-energy focusing, readout, and any replacement must be charged. An ordinary tilt holder does not automatically provide opposite incidence. No claim of an available fast reset or manufacturing advantage is made. Nevertheless this conditional energy window is a more specific acquisition target than indiscriminate pattern erasure.

Failure of a 99% direct first-event target is not failure of all internal programming routes. Lower-fidelity writing could become useful with depth heralding and a sufficiently faithful, low-damage rollback. The source does not yet supply the required rollback, so the heralded-write pathway remains open rather than established or ruled out.

## Decisive acquisition and completion boundary

The next useful acquisition is an angle- and state-conditioned transition kernel, not another focus-only library. It should distinguish, from the same initial geometry: retained desired δ2 complex; wrong layer or wrong interstitial; return to the original vacancy; transfer to another vacancy; S/Br loss; surface ejection; and other irreversible changes.

The smallest source-informed comparison is: ordinary source +b scan at 200 keV; parked oblique 200-keV native-site irradiation; and detected-interstitial return under opposite-side 60-keV incidence. Their budgets must include identical registration/read assumptions and their actual total electrons, lost specimens, retained defect verification, and flip/recovery costs. Ground-state impulse trajectories must first reveal whether the actual reactive basin is broad enough to make the parked route useful; excitation-conditioned trajectories or measurements are needed if it is not. A one-defect state must be included because both the potential and nearby defect energetics change after the first event.

If the parked oblique pulse produces retained δ2 capture with manageable competing fates, the source's scanning penalty can be avoided with ordinary beam control. If the source operation requires the moving excitation pattern or on-axis channeling, the favorable parked-ray geometry cannot be promoted to a write actuator. If opposite-side low-energy irradiation restores the exact original vacancy with low irreversible damage, depth-heralded retry becomes an actionable alternative even below a 99% direct-write probability. None of these conditional branches is resolved by the acquired public data.

The two executed main batches took 17.20 and 11.02 seconds; the follow-up algebra/plotting is small. No multislice propagation was run here. Additional successful source downloads total about 8.15 MB; failed/blocked attempts and exact hashes/timings are recorded. The Oen direct HTTP response was a CAPTCHA challenge and is labeled accordingly; its scientific formula was read through the web tool, without bypassing the challenge. All outputs and new files are confined to this owned branch directory. No physical experiment, outreach, public write, purchase, automation, or descendant agent was used.

**Achieved:** executed source-scan transfer, anisotropic kinematic bounds with geometry sensitivity, conditional elastic capture integrals, damaged-state/rollback discrimination, and a quantitative ordinary recovery candidate. **Not achieved:** measured tilted-write cross section, layer-addressable retained defect, all-species damage bound, verified depth-preserving reset, functional capability, or practical advantage.

Reproduce with the sibling source runtime, setting `PYTHONDONTWRITEBYTECODE=1`, `OPENBLAS_NUM_THREADS=2`, and `OMP_NUM_THREADS=2`: run `analysis/tilted_interface.py`, `analysis/scan_transfer_refine.py`, then `analysis/summarize.py`. Set `MPLCONFIGDIR` to this branch's `tmp/matplotlib` for plotting.
