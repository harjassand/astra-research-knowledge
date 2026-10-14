# ASTRA Experimental Genesis: two-history molecular interferometry

Research status: proposed operation, not an experimental result. Prepared 14 October 2026.

## Scope and provenance

This package contains original idealized calculations for a proposed modification of a demonstrated Ca+/CaOH+ trapped-ion recoil-spectroscopy platform. It does not establish historical novelty, molecular coherence, survival, practical performance or scientific/economic superiority. No laboratory measurements were performed. The public Astra repository was consulted at revision `ace0cfc4437fe91c20ccd24d69e0ee4bb335e871`; its contents are research context, not independent validation.

The proposal is to prepare an ancilla-labelled spatial superposition of one molecule, independently program the optical waveform at the two branch centres using two counterpropagating beams, reverse the spatial separation and measure the complex overlap of the two molecular histories through the atomic qubit.

Ideal observable:

    L[A,B] = Tr(U_B^dagger U_A rho)
    P_beta = (1 + C Re(exp(-i beta) L))/2.

This is a native-system implementation proposal, NOT a new Hadamard-test identity. Ancilla-assisted spectroscopy, phase-sensitive molecular forces, photon recoil, nonlinear force spectroscopy and molecular pump-probe spectroscopy have substantial prior art.

## Reproduce

Python >=3.10, NumPy and SciPy:

    python check_history_interferometer.py --output results.json

The program uses deterministic quadrature and assertions. It checks field interpolation, energy accounting, exact two-level limits, branch-swap symmetry, equal-intensity waveforms, finite wavepacket width, a frozen-isotropic-orientation scenario, phase randomization and conditional acquisition costs. `validation_log.txt` is the run output. No figure or dataset in this package is experimental data.

## Physical model and limits

A consistent starting Hamiltonian is

    H = H_molecule + H_motion - mu_molecule . E(x_m,t)
        + H_atom,IR(x_a,t) + H_cat + H_bath + H_system-bath.

The same dipole matrix elements and optical fields must determine coherent excitation, AC Stark shifts, unwanted transitions and radiative rates. Molecular dephasing and photochemical loss cannot be assigned favourable independent values. The finite-width calculation uses the full position-dependent pulse unitary in an impulsive, resonant two-level model. It thus retains spatial coherent backaction but not trap evolution during the pulses. It is not a complete CaOH+ calculation.

For a common initial motional coordinate q, ideal conditional recombination measures

    L = integral dq |psi(q)|^2 Tr[U(x_A+q) rho U(x_B+q)^dagger].

For open dynamics, the branch cross-block K, not two independently evolved density matrices, must be propagated:

    dK/dt = -i(H_A K - K H_B)/hbar
      + sum_l [J_lA K J_lB^dagger
        - (J_lA^dagger J_lA K + K J_lB^dagger J_lB)/2].

This expression assumes that corresponding l labels describe the same environment channel. Recoil and which-branch information belong inside its jump operators. For an electric-dipole line, the spontaneous-emission rate follows from the same transition dipole, with the appropriate angular/degeneracy conventions; it is not a freely adjustable lifetime.

Additional exclusions: spectator modes, full rotational dynamics, anharmonicity, photochemistry, atomic IR Stark-induced qubit/motion mixing, optical dispersion, drift and nonstationary reset are not simulated.

## Field compilation and energy

Let s = k d, with branch centres at +/-d/2. Complex beam amplitudes satisfy

    [E_A] = [exp(is/2)   exp(-is/2)] [E_+]
    [E_B]   [exp(-is/2)  exp(is/2) ] [E_-].

The determinant is 2i sin(s); the construction fails at s = n pi. For equal beam areas and pulse shapes, total incident fluence is proportional to

    |E_+|^2+|E_-|^2
      = (|E_A|^2+|E_B|^2 - 2 cos(s) Re(E_A E_B*))/[2 sin(s)^2].

The demonstrated reference scales alpha ~6.5 and eta_IR ~0.03 give s = 4 alpha eta ~0.78. Physical distances quoted by the program assume an axial beam; s itself uses the wavevector projected onto the cat axis. Eta is approximate and the output's many digits are arithmetic, not parameter accuracy.

For one addressed branch and one node, the incident-energy factor is about 1.01 relative to a travelling beam producing the same local field. This is not a photon-efficiency gain: light interferes constructively at the addressed point and destructively elsewhere.

For the opposite-order test, two time slots have target fields (1,i) and (i,1). Each slot costs 1/sin(s)^2 in these units. With a FIXED TOTAL incident fluence equal to one reference source pulse, each local target pulse receives sin(s)^2/2 ~0.247 of that fluence, before optical losses. Reference intensity/rate gives 0.11 J/cm^2, so the proposed fixed-budget target value is 0.0272 J/cm^2 per branch per time slot. This does not imply any particular molecular excitation probability.

For a node-addressed Gaussian packet, intensity leakage is

    r_I = [1-exp(-2 sigma_phi^2)] /
          [1-exp(-2 sigma_phi^2) cos(2s)].

The selected ground-mode width eta=0.03 alone gives ~0.00182. A Gaussian node-phase noise of ~0.064 radians consumes the remaining allowance for a 1% intensity-leakage target. This is not a measured apparatus error or a general quantum-gate infidelity.

## Opposite-order calibration

Using basis (g,e), define R_phi(theta) = exp[-i theta(cos(phi) sigma_x + sin(phi) sigma_y)/2]. Programme A is Rx then Ry; programme B is Ry then Rx. For a vibrational ground initial state, resonant impulsive pulses and no intervening uncompensated evolution:

    p = sin(theta/2)^2
    L = 1 - 2p^2 + 2i p(1-p)
    P_e,A = P_e,B = 2p(1-p).

Exchanging the programmes conjugates L. Randomizing the common phase of the second time slot relative to the first gives

    average L_randomized = 1 - 2p,
    Im(average L_randomized) = 0.

Both pulse patterns have identical intensity at EVERY spatial position. This is checked numerically and follows by expressing their fields as

    f_1(x) = (1+i)/2 cos(kx)/cos(s/2) + (1-i)/2 sin(kx)/sin(s/2)
    f_2(x) = (1+i)/2 cos(kx)/cos(s/2) - (1-i)/2 sin(kx)/sin(s/2).

The coefficients of the cosine and sine have a purely imaginary product, so the real cross term vanishes in both intensities. Instantaneous intensity-only shifts therefore receive identical exposure. This does NOT show that all atomic Stark errors cancel, nor that phase reversal alone proves molecular origin. Atomic background measurements and pulse-overlap controls are essential.

For a scenario p=0.03, not inferred from observed absorption:

- point packet: L = 0.9982 + 0.0582 i;
- finite selected-mode width: L ~0.99818412 + 0.05809073 i;
- additional frozen isotropic orientation, with mean p calibrated to 0.03: L ~0.99676855 + 0.05667228 i.

The orientation calculation is not a substitute for a thermal rovibrational calculation. Away from the resonant/compensated limit, equal populations need not hold. A harmonic system can also produce coherent geometric phases; this first test does not establish complex chemistry or quantum computational advantage.

## Atomic light shifts are a substantial unresolved cost

Huang et al. inferred a static differential Ca+ polarizability of -44.32(32) atomic units. If used only as a scale estimate, its magnitude at a LOCAL fluence of 0.11 J/cm^2 corresponds to roughly 1.4 radians of differential Stark phase. The actual dynamic/tensor polarizability at 2.7 micrometres and the actual fluence at the atomic ion must be calibrated. This estimate is not a dynamic prediction.

Because the cat labels are superpositions of atomic energy states, a Stark rotation during the cat can mix labels and spoil recombination. Equal-intensity order reversal suppresses an important false-positive mechanism, but does not guarantee acceptable visibility. A successful experiment must measure the phase response AND retained contrast with the complete new pulse sequence and any compensation included.

## Decisive experiment and rejection criteria

Use phase-related replicas of one source pulse, not an assumption of coherence between separate unreferenced source pulses. Measure the actual pulse duration, spatial phase, dispersion and overlap. Apply the two pulse patterns at a position turning point of the cat, on a timescale short compared with external trap motion.

Interleave programme order, randomized inter-pulse phase, individual-pulse exposures, off-resonant exposures, common branch programmes and atomic-background controls. Record both ancilla quadratures, molecular excitation checks where feasible, reset statistics and chemical identity. Analyse actual joint response, not separately favourable fitted values of p, coherence and contrast.

The decisive observable is the order-odd molecular probability difference after matched backgrounds, Delta P = C |Im L| in the ideal calibrated model. An illustrative engineering gate is Delta P >=0.015 with controlled systematic error below 0.0015, not a universal physical threshold. Its scientific adequacy depends on the intended observable, drift and survival.

Reject this implementation as a practical measurement route if the controlled signal remains below the acquisition/survival budget, if it follows instantaneous Stark or pulse-overlap backgrounds rather than the molecular response, or if it only survives at destructive fluence. A missing coherent signal cannot be repaired on paper by assuming a longer coherence time or a larger, noiseless cat.

## Acquisition and survival

For two equally sampled Bernoulli conditions, the conservative shot-noise planning estimate for five-sigma separation is

    N_total ~25/(C R)^2,    R = |Im L|.

At the REFERENCE, not guaranteed, C=0.52:

- R=0.01: 924,557 completed trials;
- R=0.03: 102,729 completed trials;
- R=0.10: 9,246 completed trials.

At an ASSUMED 50 full trials/second, these correspond to approximately 5.14 hours, 34.2 minutes and 3.08 minutes. These are conditional arithmetic scenarios, not measured instrument throughput. Controls and calibration increase them. The 100-kHz laser rate is not the full-trial rate.

For one molecule to survive N trials with probability at least 0.9, independent per-trial irreversible loss must satisfy q_loss <= -log(0.9)/N. At N~10^5, this is about 10^-6. Zero losses in 10^5 trials only bounds q_loss to roughly 3x10^-5 at 95% confidence; approximately 3 million failure-free independent trials are needed for a 10^-6 bound. Internal quantum-state preservation is not claimed.

## Scientific extension and limitations

The target beyond calibration is selected native-system multi-time response and comparison of alternative control histories, without first implementing a known molecular Hamiltonian on a simulator. Derivatives of L with respect to short, calibrated dipole-pulse areas yield ordered dipole correlators; derivatives of log L yield connected correlators. For an ideal harmonic Gaussian system with linear controls, log L is quadratic, so fourth connected derivatives vanish. Rotational mixtures and other classical mixtures can also generate non-Gaussian signatures and must be distinguished from anharmonic dynamics.

Higher-order response is not free: a fourth-order weak signal often scales as p^2, giving trial costs of order p^-4, with phase-cycle overhead. Full Hamiltonian or process reconstruction is not promised. Increasing mass at fixed trapping frequency/participation reduces eta as M^-1/2, requiring larger cats for fixed s. Chemical survival, coherence and contrast must therefore be re-established for each larger species.

## Primary research and closest prior art

- Wu et al., *Infrared absorption spectroscopy of a single polyatomic molecular ion*, Nature 657, 364-368 (2026). DOI: 10.1038/s41586-026-10915-8. Author version: https://arxiv.org/html/2511.19687v2 . This work already proposes pump-probe extensions. It reports a mismatch between its simple excitation model and measured absorption; its lifetime estimate is not a measured coherence time.
- Associated experimental code/data: https://github.com/quantum-molecules/absorption-spectroscopy . Only selected content was inspected; it was not independently reproduced or repackaged here.
- Najafian et al., *Identification of molecular quantum states using phase-sensitive forces*, Nature Communications 11, 4470 (2020). DOI: 10.1038/s41467-020-18170-9.
- Calvin et al., *Nondestructive inelastic recoil spectroscopy of a single molecular ion*, Physical Review A 108, 062819 (2023). DOI: 10.1103/PhysRevA.108.062819.
- Ricci Vasquez et al., *Control of an atomic quadrupole transition in a phase-stable standing wave*, Physical Review Letters 130, 133201 (2023). https://arxiv.org/abs/2210.02597 . This is not a demonstration of the present ultrafast molecular protocol.
- Huang et al., *Measurement of infrared magic wavelength for an all-optical trapping of 40Ca+ ion clock* (2022). https://arxiv.org/abs/2202.07828 . Used only for an explicitly static polarizability scale.
- Zhai et al., *Generalised quantum computational spectroscopy on a quantum chip*, Nature Communications (2026). DOI: 10.1038/s41467-026-74936-7. Ancilla-assisted Hadamard spectroscopy is prior art, not an invention claimed here.
- Saurabh and Mukamel, *Communication: Atomic force detection of single-molecule nonlinear optical vibrational spectroscopy*, Journal of Chemical Physics 140, 161107 (2014). DOI: 10.1063/1.4873578. A theoretical nonlinear force-detection proposal.
- Ma et al., *Two-Dimensional Infrared Spectroscopy of Isolated Molecular Ions*, Journal of Physical Chemistry Letters 14, 9683-9689 (2023). DOI: 10.1021/acs.jpclett.3c02661.
- Ma et al., *Coherent Vibrational Dynamics in an Isolated Peptide Captured with Two-Dimensional Infrared Spectroscopy*, JACS 147, 9556-9565 (2025). DOI: 10.1021/jacs.4c17464.

The specific two-branch waveform protocol is a candidate contribution requiring specialist priority review. No first-in-history claim is established.
