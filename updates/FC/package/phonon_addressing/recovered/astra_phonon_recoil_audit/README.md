# ASTRA: phonon-phase-addressed recoil — candidate audit

**Status:** Research hypothesis, not a demonstrated physical operation. This package
contains arithmetic and algebra checks, not molecular dynamics, a material
Hamiltonian, experimentally measured defect yields, or a historical novelty clearance.

## Proposed output
A retained sublattice-resolved occupancy bias produced by a broad electron beam
synchronized to the different basis-atom velocities of a coherent optical phonon.
Crystalline trigonal Te is an unqualified test candidate, not a recommended
manufacturing material or a proven application.

## Reproduce
`python recoil_audit.py` (Python standard library only).
The output is reproduced in `results.json`.

## Physical scope
The impulse identity is Delta K = q^2/(2M) + q.v. It is established mechanics,
not a new law. The high-mass near-backscatter approximation uses q = 2p_e.
Neither expression specifies a retained chemical or structural outcome.
An angularly integrated many-body trajectory response is still required.

For an equal-amplitude radial three-atom mode, projected velocities have the form
v*cos(theta - 2*pi*j/3). At theta=0 these are v, -v/2, -v/2.
The mean linear kinematic shift therefore cancels, while a sublattice-resolved
weighted observable can remain linear. Equal scalar damage kernels must NOT be
assumed solely from crystallographic equivalence at a fixed beam direction.

The energy bound |q.v| <= 2*sqrt(T0*K_coh_atom) follows from the impulse law.
Replacing K_coh_atom by mean absorbed energy requires the stated spatial and
mode-energy assumptions. A 100% conversion ceiling is not an efficiency estimate.
The source's optically inferred 0.24 A amplitude is not an independently calibrated
per-atom trajectory. The literal undamped harmonic energy interpretation does not
close with the quoted absorbed-energy estimate; this is an input-compatibility
flag, not a proof that the source's experiment is wrong.

No 7.9 eV Te-in-CdTe threshold is imported into elemental Te.
No Gaussian velocity width or favourable retained cross section is fabricated.
The pulse attenuation calculation is for a linear sinusoid, not nonlinear yields.

## Differential experimental benchmark (conditional)
Let Y_j(E,+v) and Y_j(E,-v) be equal-dose retained-event yields under preparations
with the same positions and electronic state but opposite coherent velocities.
In the near-backscatter, energy-shift-dominated, small-signal approximation,
D_j/S_j ~= q*v_j/T0'(E), where D_j is half their difference and S_j is the energy
derivative of their average. This neglects changing scattering prefactors,
angular weighting and direct neighbour-velocity effects on the reaction branch.
Those corrections require measurement or physical modelling. The benchmark is
not an unconditional prediction of the retained yield, and simply choosing two
different pump-probe delays does not establish matched electronic states.

## Required qualification
The minimal intended success is a **retained, sublattice-resolved** phase-dependent
occupancy change, with measured Q(t), electronic-state controls, angular controls,
a full energy/dose curve and independent post-pump retention measurements.
A transient diffraction signal or increased total damage alone is insufficient.

## Selectivity accounting
For independent irreversible events, conversion is 1-exp(-H), where H is
integrated hazard. Requiring >=99% target conversion and <=1% unwanted conversion
requires H_target/H_unwanted >= 458.2. This is an illustrative fidelity benchmark,
not a recommendation to delete an entire Te sublattice. It does not apply without
modification when healing, feedback or changes in structure alter the event model.

## Source records
- Kamaraju et al., Large-amplitude chirped coherent phonons in tellurium mediated
  by ultrafast photoexcited carrier diffusion, arXiv:1011.0090v1 (2010).
  https://arxiv.org/abs/1011.0090
- Tangney & Fahy, Density-functional theory approach to ultrafast laser excitation
  of semiconductors: Application to the A1 phonon in tellurium, PRB 65, 054302 (2002).
  https://doi.org/10.1103/PhysRevB.65.054302
- RSC, tellurium element properties (mass and density).
  https://periodic-table.rsc.org/element/52/tellurium
- Chirita Mihaila, Susi & Kotakoski, Influence of temperature on the displacement
  threshold energy in graphene (2019). Not an elemental-Te calibration.
  https://arxiv.org/abs/1811.04011
- Susi et al., Silicon-Carbon Bond Inversions Driven by 60-keV Electrons in Graphene,
  PRL 113, 115501 (2014). Existing atom-manipulation baseline.
  https://doi.org/10.1103/PhysRevLett.113.115501
- Waldecker et al., Coherent and Incoherent Structural Dynamics in Laser-Excited
  Antimony, arXiv:1608.03486v2 (2017). Joint structural/energy calibration precedent.
  https://arxiv.org/abs/1608.03486
- Gliserin et al., Sub-phonon-period compression of electron pulses for atomic
  diffraction, Nature Communications 6, 8723 (2015). Single-electron-pulse result,
  not a high-current 300-keV processing qualification.
  https://doi.org/10.1038/ncomms9723

No experimental work or atomistic simulations were performed for this package.
