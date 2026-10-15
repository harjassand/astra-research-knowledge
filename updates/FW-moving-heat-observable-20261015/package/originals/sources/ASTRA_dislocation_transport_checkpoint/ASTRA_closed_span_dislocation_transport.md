# ASTRA — Closed-span dislocation transport

Research checkpoint, 15 October 2026.

## Status

A proposed physical operation, conditional analytic model, and executed dimensionless checks. No new material response, device, defect-removal result, energy advantage, or historical priority has been established. The proposed same-loop response is not supplied by the existing photoplasticity measurements. Repository files were read; no GitHub update was made.

## Intended operation

Translate an existing surface dislocation half-loop while restoring its span, shape, and integrated slipped area, by combining an expansion/contraction cycle with reversible modulation of the relative glide response of its two threading endpoints. The prospective control is mechanical loading plus optical carrier manipulation. The specific experimental lead is the ZnS/GaP platform described by Montenegro et al. (S1).

This is not an assertion that light-driven defect manipulation, plasticity control, or geometric locomotion is new. The proposed distinguishing endpoint is retained translation of the same loop after closure of its shape cycle. Generic geometric/crawler principles have prior art (S2). The novelty of the physical realization remains unknown.

## Independent selection and rejected shortcuts

The broader investigation considered warm forming of brittle semiconductors (S3), nanodiamond deformation (S4), optically written dislocations (S5), and other manufacturing/energy effects. These already demonstrate their respective operations and are not new Astra discoveries. Plastic deformation through amorphization does not establish preservation of the desired crystalline material. An optical change in misfit-segment length does not establish annihilation, removal, or retained relocation.

The initially considered switch between orthogonal dislocation families was not retained: conventional multiaxial stress is a necessary comparator, and family-specific speed is not the missing endpoint. The selected hypothesis instead exploits unequal responses of two arms of one loop.

## Minimal mathematical contract

Let x_C < x_N be the two interface endpoint coordinates, where C denotes a charged-core threading arm and N the other arm. Define span ell = x_N - x_C and center c = (x_N + x_C)/2. The left/right naming is a convention, not a claim about all loop geometries.

Assume:

1. A planar loop with a fixed topology, Burgers vector, film thickness and reproducible shape family; its geometry is determined by ell and c.
2. In the interior region of interest, the energy and loading are translation-invariant, so the two endpoint forces are equal and opposite.
3. An overdamped diagonal endpoint law with finite nonnegative coefficients m_C and m_N, not both zero, applies over each stroke. No claim is made that this is already validated for ZnS.
4. The prescribed expansion and contraction are physically accessible without cracking, multiplication, cross-slip or permanent arrest.
5. Switching settles to reproducible optical/charge states, and switching transients either have negligible displacement or are separately measured and counted.
6. The span cycle closes. Claiming closure of integrated plastic strain further requires closure of the full shape/slipped area, not merely the measured endpoint separation.

Writing F for the force that expands the span:

    dx_C/dt = -m_C F
    dx_N/dt =  m_N F
    dell/dt = (m_C + m_N) F
    dc/dell = A = (m_N - m_C) / [2(m_N + m_C)].

For an expansion by a > 0 in optical state D, and contraction by a in state L, with constant coefficients:

    Delta c = a (A_D - A_L)
            = a (m_N^D m_C^L - m_C^D m_N^L)
                / [(m_N^D + m_C^D)(m_N^L + m_C^L)].

Thus changing the overall clock speed is insufficient. The relative endpoint mobility must change. Fixed optical state, common multiplicative rescaling of both endpoint mobilities, or one permanently pinned endpoint all give zero displacement for this closed-span cycle under the stated model. Interchanging the optical states assigned to expansion and contraction reverses the displacement.

For span-dependent coefficients measured reproducibly on both branches:

    Delta c = integral(ell0 to ell1) [A_D(ell) - A_L(ell)] dell.

This offers an operational experiment: determine dc/dell directly rather than infer unavailable atomistic activation barriers. Hysteresis, extra shape variables, position-dependent pinning and stress-dependent response must be retained in a more complete path description. A nonzero integral is a prediction only for the measured accessible paths.

## Mobility-matching constraint

Suppose the N endpoint has the same mobility m > 0 in both optical states. Let m_C^D = p > q = m_C^L > 0. Then

    |Delta c|/a = m(p-q)/[(m+p)(m+q)].

Its derivative with respect to m is

    (p-q)(p q - m^2)/[(m+p)^2(m+q)^2].

The maximum occurs at m = sqrt(p q). Defining R = p/q:

    |Delta c|/a <= (sqrt(R)-1)/(sqrt(R)+1).

This bound concerns displacement per span excursion, NOT speed, energy efficiency, success probability or manufacturing throughput. If the nominally unaffected endpoint is much slower or faster than the switchable endpoint, translation is small even when R is large. There is no evidence here for a measured same-loop R or for the neutral endpoint being optically insensitive.

## Energy and transformation boundary

The reduced model has nonnegative glide dissipation

    P_glide = (m_C + m_N) F^2.

Closing the span or mean plastic-strain cycle does not imply zero mechanical work. Complete paid input includes optical wall-plug energy, actuator losses, heating/cooling, metrology, preparation, repeat failures and replacement. Recovered mechanical work may be credited only when actually recovered.

In a fixed planar shape family, integrated slipped area scales with span. Closing span and full shape can restore its integral while relocating the local plastic-distortion field. The local field is NOT unchanged. No defect is annihilated by interior translation alone.

Export to a perimeter or guard region creates a separate boundary-accounting problem. Removal of a misfit segment changes strain accommodation. The operation does not promise elimination of all strain-relieving dislocations while keeping the same mismatch relaxation. Guard capacity, backstress, surface slip, later renucleation and propagation back into the working region must be measured.

## Earliest decisive experimental gate

Use an existing-loop imaging platform, with independently calibrated reversible substrate loading and controlled illumination. Begin at the published platform conditions (S1), not an assumed room-temperature high-mobility regime. Identify the two endpoints and the same loop through the whole sequence.

Before attempting transport, measure both endpoint responses under each optical state for outward and inward motion. Stop if one arm cannot move, the relative response does not change, or contraction requires destructive loading. Nominal film mismatch, relaxed-film mobility and critical thickness do not by themselves establish a reversible loading window.

To test a cycle: expand to a registered ell1, change optical state while holding or explicitly measuring shape, contract to ell0, and restore loading, temperature and illumination. Measure signed center displacement against stationary substrate fiducials and independent full-shape/strain checks. Reverse optical phase order and compare the direction and magnitude with the independently measured geometric integral.

Controls must include fixed-light closed-span cycles, an optimized stress-only waveform at the same constraints, matched-temperature controls, phase-scrambled equal-dose illumination, beam-dose controls, and position-dependent stress checks. Electron-beam imaging can perturb carrier populations; use beam-off actuation and count all imaging interruptions. Apparent disappearance of contrast is not disappearance of a defect. Use multiple diffraction conditions and appropriate independent structural checks.

A successful elementary demonstration needs reproducible nonzero retained displacement, closure of span and relevant shape/strain observables, phase-order reversal, prediction from independently acquired endpoint responses, and separation from matched controls. Counts, confidence levels and power should be preregistered after a noise pilot rather than based on an arbitrary invented sample size. Report the entire accessible loop population, including pinned/damaged loops.

## Technological output and comparators

The prospective task is selective post-growth clearing or relocation of threading defects from a predefined active region with a constrained strain budget. Local motion is not sufficient: measure remaining defects, newly generated defects, cracks, surface roughness, retained electrical/optical performance and operational stability.

A proposed accounting unit is cost or joules per accepted device area after this full qualification, compared to the best available route for that device. Native substrates, bonding, growth/buffer design, thermal/stress treatment and established optical processing must not be excluded by choosing an artificially narrow baseline. Relevant primary comparators include S5-S7. Results in Ge/Si or PMN-PT are not ZnS parameters and cannot establish a head-to-head ranking.

For a measured cycle drift d and full cycle duration t_cyc, interior mean translation speed is d/t_cyc. Reaching a guard a distance L away requires at least approximately L/|d| successful cycles in a constant-response idealization. This does not include arrest, interactions or failures. Whole-wafer uniform control may drive different loop orientations differently; it is not automatically selective parallel routing.

A second research tranche is justified by newly measured same-loop ratio switching and safe reverse glide, not by another uncalibrated optimization. A device programme requires retained functional improvement and matched complete-resource advantage. Generalization to other compounds requires new acquisition in those compounds.

## Astra capital consulted after selection

Pinned repository revision: a6190a1083f688a7e4bf64adbc5244ef150ff2c4.

Read N854's dossier and the first 94 lines of the N852 transport/damage proof source. N852's row-clock invariance under its finite absorbing-network assumptions warns that faster local processes need not improve total output. This informs the output boundary and interest in relative responses; it is not a theorem about a moving crystal line. N854's calibrated fixed linear-response acquisition contract is not established for a nonlinear, history-dependent dislocation system. No query-count or robustness guarantee was transferred.

## Executed checks

`check_model.py` uses only Python's standard library. It verifies the drift formula against endpoint integration, fixed-mode and common-scaling nulls, the pinned-endpoint null, phase reversal, the sharp mobility-matching bound, and a span-dependent geometric integral. `model_results.json` contains the exact outputs from this run.

The dimensionless example m_C^D=10, m_C^L=0.1, m_N=1 gives Delta c/a=-9/11. The independently integrated displacement is -0.8181818181791247, versus -0.8181818181818181 analytically; the final span is 4.000000000004806 from an initial span of 4. This checks arithmetic and model implementation, not physical assumptions. These numbers must not be described as ZnS simulation results or measured contrast.

## Primary-source ledger

S1. A. F. Montenegro et al., A common origin of photoplastic and electroplastic effects in ZnS, Physical Review Materials (2026), DOI 10.1103/c2hc-lyp2. Readable author preprint and appendices: https://arxiv.org/html/2506.07908v2 ; publication https://link.aps.org/doi/10.1103/c2hc-lyp2 . The HTML and its embedded appendix text were inspected. No raw trajectory dataset was reproduced.

S2. J. E. Avron, O. Kenneth, D. H. Oaknin, Pushmepullyou: An efficient micro-swimmer (2005), https://arxiv.org/abs/math-ph/0501049 . Used to delimit generic geometric locomotion prior art, not as a dislocation material model.

S3. Z. Gao et al., Warm metalworking for plastic manufacturing in brittle semiconductors, Nature Materials (2025), https://www.nature.com/articles/s41563-025-02223-9 . Public abstract and extended-data descriptions inspected.

S4. Plastic deformation in nanodiamonds, Nature Communications (2026), https://www.nature.com/articles/s41467-026-70189-6 . Public article inspected.

S5. Reversible writing of high-density dislocations with multidimensional controllability in PMN-PT crystal, Nature Communications (2025), https://www.nature.com/articles/s41467-025-61095-4 . Public full text inspected, including reported thermal dependence and residual amorphous region.

S6. Y. A. Bioud et al., Uprooting defects to enable high-performance III-V optoelectronic devices on silicon, Nature Communications (2019), https://www.nature.com/articles/s41467-019-12353-9 . Full text, characterization limits and process conditions inspected.

S7. O. Skibitzki et al., Reduction of threading dislocation density beyond the saturation limit by optimized reverse grading, Physical Review Materials (2020), https://link.aps.org/doi/10.1103/PhysRevMaterials.4.103403 . Publication page inspected; no independent replication performed.

Repository proof read: https://github.com/harjassand/astra-research-knowledge/blob/a6190a1083f688a7e4bf64adbc5244ef150ff2c4/updates/FT-direction-transport-20261015/synthesis/transport_damage/PROOFS.md

Repository acquisition dossier read: https://github.com/harjassand/astra-research-knowledge/blob/a6190a1083f688a7e4bf64adbc5244ef150ff2c4/frontier/dossiers/N854.txt

The targeted literature search did not establish priority for the proposed exact operation. No exhaustive patent, archival literature or repository novelty audit was completed. No physical experiment, material-calibrated simulation, or industrial cost benchmark was performed.
