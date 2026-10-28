# Oblique parked irradiation survives elastic propagation at a reduced fluence scope

**Achieved:** a discriminating, matched calculation with a rotated finite 16-layer crystal, actual IAM elastic scattering, finite focus propagation, two distinct completions of the source's 0.8 Å effective width, and all Cr/S/Br atoms in successively enlarged crystal patches. The selected oblique beam retains substantially more nominal-site Cr fluence separation than the on-axis source scan. This is not a small-supercell omission artifact. **NOT_ACHIEVED:** a retained physical write, measured layer hazard, calibrated all-species damage advantage, or reset.

The accepted [preceding report](../REPORT.md) is unchanged; its hash matches the earlier saved artifact manifest. This continuation stays within `continuation_rotated_field_20261027/`.

[COMPARISON.json](outputs/COMPARISON.json) contains the machine-readable results, gains, conditional collateral tradeoffs, convergence checks, resources, and source hashes. [METHOD.md](METHOD.md) records the construction and coherence treatment. The [figure](outputs/field_comparison.png) displays the principal results.

## The physical question and matched calculation

The fixed candidate is the previously selected parked beam through native Cr1 in layer 8, with crystallographic tilt components `(a,b)=(1,10)` degrees. The beam direction is proportional to `(tan 1 degree, tan 10 degrees, 1)`. I rotate the atoms rigidly into an orthonormal beam frame; incidence is then along laboratory `+z`. This avoids representing a roughly 175-mrad carrier with a near-axis propagator.

The [pinned authors' native CIF](https://github.com/KleinAtomLab/Mesoscale-atomic-engineering/blob/6844cc568271d448704a0eb6ee55ddfd5246d242/CrSBr.cif) supplies all six basis atoms in all 16 layers. A finite central patch is embedded in an orthogonal vacuum box with nonperiodic potential construction. Actual transformed and padded atom lists are checked for identity with the intended coordinates. There is no affine strain or periodic tilted-cell wrapping.

The ordinary comparator is the demonstrated one-sided sinusoidal `+b` motion from native Cr toward S/Br. A parked on-axis reference is also included. Both controllers receive identical incident electron normalization, 200-keV energy, 32-mrad available aperture, and vacuum focus at the chosen layer. Perfect target coordinates/focus are supplied equally; their acquisition is not demonstrated here. This is a comparison of specified actuators, not a global control optimum.

Every controller receives all three probe models:

* **Ideal coherent 32 mrad:** a uniformly filled circular pupil, about 0.403 Å vacuum FWHM.
* **Coherent 0.8 Å:** Gaussian pupil apodization inside the same available aperture, with 0.8 Å focal intensity FWHM.
* **Incoherent 0.8 Å:** the ideal pupil with Gaussian incoherent position spread, calibrated to the same 0.8 Å effective FWHM. The source standard deviation is about 0.296 Å.

The latter two are physically defined alternative beam completions. They are not an acquired coherence distribution or an uncertainty interval for the microscope. FWHM alone does not determine propagation through a crystal. No controller receives a narrow probe that is withheld from its comparator.

The Gaussian coherence kernel and the sinusoidal scan characteristic function are evaluated analytically in the finite reciprocal pupil. Positive component factorization retains more than `1-10^-6` incident trace without renormalizing the discarded part. The source scan average is exact within the initial-state input model, rather than an arbitrarily sparse set of scan phases. The final propagation uses 88 coherent components for the oblique three-probe batch and 254 for the on-axis batch including all reference controllers.

A preliminary 9×9 source-position quadrature was rejected as the final definition: it closely matched the FWHM but had a substantial error in the high-separation coherence characteristic function. Its output is retained as preliminary and is not the final physical input. The analytic positive kernel removes that ambiguity.

## Local fluence survives, with substantial kernel and coherence sensitivity

The primary comparison below uses **bilinear nominal-site point intensity immediately before the atom-containing slice**. It is a local diagnostic, not an acquired microscopic reaction kernel. Finite-potential contributions before the plane are included. In the refinement the plane lies between zero and 0.5 Å before the atom's longitudinal coordinate. It is not a measurement at an exactly known, motionless nucleus.

At the common 768-grid, 1 Å slice setting, the chosen native site's share of the summed nominal-site intensity at all native Cr sites is:

| Probe model | On-axis parked reference | On-axis source +b scan | Selected oblique parked |
|---|---:|---:|---:|
| Ideal 32 mrad | 0.1846 | 0.1511 | 0.7834 |
| Coherent 0.8 Å | 0.0881 | 0.0803 | 0.5868 |
| Incoherent 0.8 Å | 0.1346 | 0.1034 | 0.4355 |

The matched oblique/source-scan fraction gain is about 5.2×, 7.3×, and 4.2×, respectively. Fractions are fluence diagnostics, not event probabilities. The actual transition coefficients may change with incidence, phase space, excitation, and atomic state.

Point values are not the only functional retained. With 0.2 Å radius disks the oblique values are 0.7193, 0.5455, and 0.4126; with 0.4 Å disks they are 0.5169, 0.4471, and 0.3493. Uniform disks are declared surrogates. A physical rate would integrate over nuclear-position uncertainty and the reactive transition response, rather than inherit one arbitrary atom disk. A rigid potential with a displaced sampling kernel would still not be a complete frozen-phonon calculation.

The same incident electrons also do not imply identical target fluence. For nominal-site intensity, the oblique/source-scan target-fluence gains are approximately 4.7×, 1.06×, and 3.0×. The coherent 0.8 Å gain in absolute target intensity is small relative to other model uncertainties. The informed on-axis parked reference has a higher absolute target point intensity than the oblique beam in these runs, while strongly exposing other native Cr in its column. Thus the oblique beam does not dominate every possible resource or collateral criterion.

## The ray discrepancy is mostly propagation/coherence and kernel choice

A matched zero-potential propagation control gives oblique nominal-site fractions of 0.7844, 0.5813, and 0.4470. Adding the crystal potential changes these to 0.7834, 0.5868, and 0.4355. At the declared incoming-site scope, standard elastic scattering does not collapse the geometric separation.

The previous constant-width 0.8 Å Gaussian ray gave 0.6783 at this candidate. That number was a point-intensity calculation. Comparing it directly to a 0.4 Å disk result would mix a propagation change with a changed sampling functional. I therefore computed the matched ray kernels too:

| Constant-width Gaussian ray functional | Target / all Cr |
|---|---:|
| Point | 0.6783 |
| 0.2 Å radius uniform disk | 0.6357 |
| 0.4 Å radius uniform disk | 0.5196 |

For the coherent 0.8 Å completion, point ray → vacuum wave → scattering wave is approximately `0.678 → 0.581 → 0.587`. For the incoherent completion it is `0.678 → 0.447 → 0.435`. Finite focus propagation and mutual coherence explain most of the reduction for these models; elastic scattering is the smaller additional effect. The narrow ideal probe is a separate matched beam model and must not be treated as the acquired 0.8 Å source.

## Frame, finite crystal, and numerical checks

The main construction has 13,616 atoms in a 96 Å transverse box, sampled at 0.125 Å, with 149 finite-potential slices for the oblique specimen. The enlarged check has 23,984 atoms in a 112 Å box at the same sampling. Target depth and slice alignment are held fixed. Minimum atomic vacuum margins exceed 7 Å in the enlarged construction.

Enlarging the crystal and box changes the oblique point fractions by less than 0.07% and the 0.4 Å disk fractions by less than 0.07%. Absolute target fluences change by about 0.02% or less. This explicitly tests the previously important missing-collateral failure; all near-ray competitors and both native Cr bases are included. It is a finite domain convergence check, not a rigorous infinite-crystal bound.

The final candidate refinement uses 1024 transverse points, 0.09375 Å sampling, and 297 slices of 0.5 Å. It gives:

| Probe model | Refined point fraction | Refined 0.2 Å disk | Refined 0.4 Å disk |
|---|---:|---:|---:|
| Ideal 32 mrad | 0.7826 | 0.7075 | 0.5199 |
| Coherent 0.8 Å | 0.5860 | 0.5388 | 0.4486 |
| Incoherent 0.8 Å | 0.4312 | 0.4054 | 0.3499 |

Relative to the common-grid comparison, point fractions change by less than 1%, disk fractions by less than 1.8%, and absolute target point intensities by about 2%. These combined grid/slice checks do not establish exact microscopic intensity or provide a thermal-kernel uncertainty bound. The on-axis comparator was not repeated at every refinement setting; the primary matched comparison uses identical settings for both controllers.

Weighted final border probability is about `5.3e-4` for the ideal/incoherent candidate and `5e-7` for the coherent Gaussian. Fine-grid retained wave norms are approximately 0.9938, 0.9980, and 0.9954. Their loss is numerical high-angle antialias removal, not a measured absorption or damage probability; no wave was renormalized after propagation. Higher-angle and finite-domain limitations remain explicit.

A direct high-tilt carrier would accumulate a large longitudinal phase error under a first-order near-axis expansion over 130 Å. After removing unobservable piston and a fitted linear shift, the computed RMS residual is about 0.188 rad, or 0.109 rad after also fitting isotropic focus. In the rotated frame the corresponding incident-pupil values are about 0.00127 and 0.00032 rad. These are illustrative free-space expansion checks, not a claim that every software tilt implementation fails. Rotating the atoms and using the second-order Fresnel kinetic propagator avoids relying on the high-carrier approximation.

## All-species collateral prevents an unconditional actuator ranking

All Cr, S, and Br sites are measured. Against the source +b scan, the oblique candidate lowers each non-target species' site-intensity sum per unit target intensity for the three matched probe models. But the informed ordinary on-axis parked reference substantially suppresses S/Br exposure and gives a real tradeoff.

For the incoherent 0.8 Å beam with the nominal-site functional, the normalized site-intensity sums are:

| Controller | Other Cr / target | S / target | Br / target |
|---|---:|---:|---:|
| On-axis parked | 6.429 | 0.512 | 0.498 |
| Source +b scan | 8.670 | 10.606 | 10.259 |
| Oblique parked | 1.296 | 1.580 | 2.159 |

A useful conditional decision boundary follows. Give other-Cr fluence weight 1, S fluence weight `wS`, and Br fluence weight `wBr`. The oblique beam has smaller weighted non-target fluence than the on-axis parked reference exactly when

`1.068 wS + 1.661 wBr < 5.132`

for this input model and functional. Equal S/Br weights cross at about 1.88. This is a linear **weighted-fluence** frontier; the weights are not acquired damage coefficients. If local linear response were eventually justified, measuring its relevant species/angle/state dependence could choose between these routes. Ground-state formation energies do not supply those coefficients. A different physical sampling functional also changes the boundary.

## The minimal remaining physical interface

The calculation advances the route from favorable ray geometry to a standard elastic wave model. It selects a specific parked oblique actuator for transition acquisition; it does not establish that parked irradiation produces the source's retained δ2 defect, preserves its displacement direction, or enables rollback.

The remaining interface needs three concrete inputs:

1. **Probe:** calibrated complex pupil and mutual intensity, energy/focus spread, and registration at the write angle. FWHM alone permits materially different selectivities, as the two 0.8 Å completions demonstrate.
2. **State:** the actual 16-layer geometry and the relaxed one-edit configuration, with nuclear motion and the changed elastic/excitation environment. This run uses a rigid native neutral-atom IAM; it does not average thermal displacements or propagate after a defect is created. The exact scan average likewise assumes an unchanged initial potential.
3. **Transition:** an angle-, excitation-, and state-conditioned map from incoming electron modes to retained desired interstitial, wrong layer/site, competing Cr motion, S/Br damage, and return to the original vacancy. The present generated incoming modes can feed such a transition operator. A scalar proportionality to local intensity has not been acquired.

The field result therefore supports continued acquisition of the parked oblique route. It gives no reason to discard the route because of elastic channeling or a finite-cell omission. It also does not justify manufacturing, direct-write fidelity, or all-species advantage claims. Heralding and rollback remain separate physical operations.

The five final propagation batches consumed 1,258 recorded seconds, with two-thread limits. Peak recorded resident memory was about 3.36 GB. A rejected preliminary quadrature propagation took another 58.5 seconds; short setup/input checks add small overhead. No new source download, paid compute, physical experiment, outreach, external write, automation, or descendant agent was used. The installed abTEM 1.0.11 runtime was reused read-only with this continuation's cache paths; the actual source-file hashes are recorded.

Reproduction: run `bash analysis/reproduce.sh` with the retained sibling runtime. It sets this continuation's caches and two-thread limits, then executes the five fixed propagation cases and postprocessing. The old source-position quadrature files are preliminary; the final runner uses the analytic coherence kernel.
