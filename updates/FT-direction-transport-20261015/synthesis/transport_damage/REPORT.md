# Transport, damage and accessible-boundary audit

15 October 2026. Repository pin `b7cada92d2eb304578be5ed974f1e44b10a89928`. Source instructions treated as data. Incoming checkpoint, all model code and results were read; the supplied code was replayed into this worker directory. Its checks pass with small floating-point differences recorded separately. Independent extensions below are not producer claims. No experiment, material superiority or new physical operation was obtained; historical originality and external correctness remain UNKNOWN.

**Decision:** retain accessible stiffness as a testable transport intervention, but make committed output before failure and complete service cost the target. The source's local barrier ordering is insufficient for this task. Established Arrhenius branching machinery gives a stronger network criterion and a concrete alternative-damage falsifier.

## Exact network consequence

For a finite, almost-surely absorbing network with fixed initial state/distribution, topology, prefactors and per-jump rewards, suppose every transport and damage rate follows

    k_it(chi)=k_it(0) exp[-beta chi(R_saddle,t-R_well,i)].

The well term multiplies every outgoing event at state i by the same factor. It changes that state's clock, but cancels from all branching probabilities. Consequently all success/failure committors and cumulative accepted jump rewards before eventual failure are **independent of the well responses** when saddle responses are fixed. Lifetime and output per second generally change.

The branching cancellation is established prior art, explicit in a 2008 primary paper. The consequential application here is to accepted lifetime output with many damaging channels, not a new Markov-chain primitive. A hard deadline, preparation changes, time-based costs, independently fixed corrosion clocks or changed dynamical prefactors break the stated inference. [Rahav–Horowitz–Jarzynski](https://doi.org/10.1103/PhysRevLett.101.140602).

For the source's two-state example, changing only the synthetic well response `R_A` from 0 to 0.24 eV leaves expected net right-port transfer near 26,593.89 while changing mean lifetime from 56,555.88 to 9,162.35 seconds. These are deliberately synthetic rates. Its approximately 32.5-fold lifetime-yield gain comes from the useful-to-harmful saddle contrast `q/r`, rather than the de-trapping magnitude itself.

## A target for the actual accessible clamp

Let `v_i` be the expected remaining accepted output at state i and `nu_i` its expected cumulative dwell time before failure. An event's advantage is `A_it=g_it+v_destination-v_i`, with zero continuation value after failure. The exact sensitivity is

    dY/dchi = sum_i,t nu_i k_it A_it d(log k_it)/dchi.

Under the common-host rate law, the well terms cancel and this becomes

    dY/dchi = -beta sum_t w_t R_saddle,t,
    w_t = sum_origins nu_i k_it A_it.

This signed sum counts entry, back-hops, alternate routes and every damaging channel. A fast nominally forward hop can have negative continuation advantage. A phonon spectrum in the occupied well does not acquire this target.

After independent derivation, the accessible_clamps worker supplied a compatible multiport PSD parametrization `Delta F_s=tr(Qc C_s)+common`. The global target gives `dY=-beta tr(dQc sum_t w_t C_saddle,t)`. It is a **local direction-selection objective** over legal supports and costs; finite yield need not be concave. A finite control change still requires solving the complete changed network. Full derivations and precise exclusions are in `PROOFS.md`.

## A second damage path reverses the advertised lifetime gain

Adding an unaffected empty-state failure rate `d` gives the exact starting-empty output

    Y=(a_L b_R-a_R b_L-a_R h)/[(a_L+a_R)h+d(b_L+b_R+h)].

For the source's partly blocked synthetic example, the clamp's lifetime-yield improvement vanishes at `d=0.0113024270 per second`. At `d=0.02`, expected net transfer changes from **176.38 to 151.95**, a **13.85% loss**, although the specified occupied-state harmful rate is still suppressed. The alternative damage channel need not accelerate. This is a model counterexample, not an acquired corrosion rate for any material.

## What the physical evidence actually supports

The nonlinear-optical ionic-memory experiment resolves correlated hops and persistent back-hopping. It explicitly distinguishes their short-time activation from low-frequency conductivity. The LLTO phonon paper reports a relative differential-impedance enhancement; the separate UV study measures shot-to-shot lattice correlations. Neither supplies a dark, steady, committed-output lifetime for the passive support hypothesis. [Poletayev et al.](https://doi.org/10.1038/s41586-023-06827-6), [Pham et al.](https://doi.org/10.1039/d5mh01990g), [McClellan et al.](https://doi.org/10.1038/s41467-026-72663-7).

Graphene crown-ether strain control is strong operation-level prior art, but the examined gains are molecular-dynamics results. The primary paper explicitly treats entry, occupancy and a transition between knock-on and drift-diffusion regimes; its proposed substrate fixture is not a fabricated qualified support. [Sahu et al.](https://doi.org/10.1126/sciadv.aaw5478), [Fang et al.](https://doi.org/10.1038/s41563-018-0220-4).

Defect-engineered hBN is a more concrete experimental screening platform. Its preprint uses approximately 30 nm flakes and aqueous LiTFSI/LFP reservoirs; Fig.3 averages voltage sweeps and fits 2.4–2.5 V after an entry/solvation threshold. Battery tests use CVD films and organic electrolyte. The preprint reports eventual Li–S failure primarily through electrolyte depletion. These details make entry limitation and competing loss concrete concerns; they do not acquire a support response or same-regime pathway ordering. Fig.3 was rendered and visually checked. Journal abstract/metadata and preprint details remain separately scoped. [Published paper](https://doi.org/10.1021/acs.nanolett.6c01634), [primary preprint](https://arxiv.org/abs/2510.27021).

## Precise missing physical operation and discriminating acquisition

The missing operation is an actual change of legal boundary compliance that changes **committed branch odds and accepted lifetime output**, while preserving sufficient useful service rate and staying within the resource budget. A remote clamp, an arbitrary atom-freezing calculation, a softer trap, or a changed optical signal does not establish it.

For one material/support/electrolyte/electrode/loading regime, acquire the accessible stiffness law and small controlled perturbations. Resolve entry, return and committed exit events, precursor-state dwell exposures and competing failure labels. Estimate their conditional rate slopes, reconstruct the target-weighted sensitivity, and directly measure accepted transfer and irreversible damage over useful service. If memory prevents a small-state Markov model, acquire additional state/history information or use measured path statistics; do not force exponential hazards.

Rate-level slopes can test the target without identifying every microscopic saddle. Mechanism attribution additionally requires finite-temperature transition ensembles, reactive-flux/committor or validated rare-event calculations, and prefactor/recrossing qualification under the actual support. Established reaction-rate theory explains why static barriers alone cannot supply these rates. [Grote–Hynes](https://doi.org/10.1063/1.440485).

A related hBN preprint reports ion-sensitive defect fluorescence, suggesting a possible occupancy readout. Its abstract does not establish that the sensing defect is the conducting site, resolve committed cross-membrane events, or bound probe perturbation. It is an acquisition lead with those gates, not an already available pathway oracle. [Wu et al.](https://arxiv.org/abs/2407.01934).

Compare with optimized defect/pore chemistry, composition, thickness and contacts, plus conventional strain/pressure control at matched accepted output. Mechanical control already changes real battery cycling, so merely improving a pressure fixture is not a fundamentally new operation. [Doux et al.](https://doi.org/10.1002/aenm.201903253).

Count acquisition and destructive lifetime tests, active-area loss, fabrication yield, fixture installation, charge-balanced reservoir/electrode work, heat handling, holding, replacement/reset, conditioning and waste. Event costs and dwell-time utilities are distinct. Exposure needed to bound an unobserved damage channel can dominate calibration: under a declared constant Poisson hazard, zero events require `E>=-log(delta)/h_target` at-risk exposure for a one-sided confidence target. These hypotheses and simultaneous-channel coverage must themselves be qualified.

The independent checker passed 200 many-state, two-damage-channel-per-state network checks, including committor invariance, affinity preservation, continuation-weighted sensitivity and a multiport directional derivative. These results validate the stated finite numerical identities only. No jointly qualified material/support regime, useful cost advantage or extraordinary capability emerged.
