# ASTRA controlled-matter continuation: material audit and disposition

Research date: 13 October 2026.

## Status

No specimen-level lattice pump, retained matter-transformation process, or new exceptional physical capability was established. K beta-alumina remains a microscopic experimental hypothesis. The prior independent-ion pumping identity is preserved with its assumptions; it is not a material prediction. Alternative driven superionicity and electronically assisted SiC repair were investigated, but neither was qualified here as a new manufacturing mechanism.

No density-functional, molecular-dynamics, nonadiabatic, or experimental calculation was performed in this continuation. The supplied Python program checks algebra on explicitly synthetic fixtures. It does not validate a material, assess experimental priority exhaustively, or reproduce the cited papers.

Astra was inspected selectively at commit f437df815bef12f123ae4fe313d861ec1c862bc4. No Astra or openai/math result is a load-bearing material premise. No repository content was changed.

## 1. Material evidence and prior-art correction

Minami et al. [S1] measured polarity-dependent THz-driven current in **Na**, not K, beta-alumina in 2020. Their experiment used 15–300 kV/cm fields and a 1 kHz repetition rate, reporting an approximately 50 kV/cm threshold and picoampere current. Their illustrative activated model required an adjustable enhancement factor of 62. Consequently, ordinary THz-driven net ionic current is neither a new target nor a calibrated microscopic coupling model for K beta-alumina. A structural-cycle claim must distinguish itself from this direct-field baseline.

Negi et al. [S2] model Na/K beta-alumina with space group 194, whereas beta-double-prime has a different stacking and symmetry. Their calculated K beta barriers are 0.72 eV for vacancy motion and 0.08 eV for a cooperative interstitial route. These are static calculations, described as lower bounds, not measured finite-temperature driven rates. The low-energy K-beta route involves collective configurations rather than one independently hopping ion. Their much smaller K-beta-double-prime vacancy barriers cannot be transferred to beta.

Colomban and Lucazeau [S3] studied stoichiometric beta crystals including K. In-plane cation vibrations occur below 100 cm^-1; the prominent Raman feature is E2g. The narrow 2 cm^-1 versus broader 10 cm^-1 widths discussed in the accessible abstract refer to framework/spinel modes, not a supplied dephasing rate for an identified K control-mode pair. The exact K-specimen eigenvectors, frequencies, damping, coherent amplitudes, and constrained transition-state responses needed here were not recovered.

The nonlinear-optical memory study [S4] supports treating ionic history and correlations seriously. Its orientational-memory observable must not be substituted for a population-relaxation rate or an unwrapped displacement. Mode assignments or timescales of beta-double-prime, Na-beta, and K-beta must retain their original material labels.

The LLTO phonon-ion work [S5] is an independent example of lattice-sensitive conduction in another material; it does not supply K-beta site and saddle derivatives. Conductivity enhancement or a resistance response per pump power does not itself establish directional pumping or retained processing.

## 2. Symmetry: a real restriction, not proof of controllability

Assume an ideal bulk D6h crystal, long-wavelength electric-dipole excitation, an initially symmetry-respecting ensemble, and a bilinear response in two lattice amplitudes.

An in-plane polar current transforms as E1u. An in-plane infrared coordinate P=(Px,Py) transforms as E1u; a c-axis infrared coordinate transforms as A2u. An E2g Raman coordinate can be represented by

    R = [[r1, r2], [r2, -r1]].

The product R P is a polar in-plane vector. Thus E2g x E1u contains an allowed E1u current channel. In contrast, E2g x A2u = E2u, which is neither an in-plane nor a c-axis polar-vector representation. The latter pair cannot supply this bilinear bulk current. Two inversion-odd IR coordinates alone also cannot supply an inversion-odd bilinear bulk current.

For an impulsive Raman excitation with a calibrated E2g coordinate proportional to (cos 2theta_R, sin 2theta_R), and an in-plane IR coordinate oriented at theta_I, the allowed mixed vector points along

    (cos(2theta_R - theta_I), sin(2theta_R - theta_I)),

up to its scalar dynamical coefficient and sign. Raman polarization rotation by 90 degrees changes the E2g coordinate's sign; rotation by 45 degrees rotates this vector by 90 degrees. This statement assumes the relevant degenerate mode and Raman tensor have actually been calibrated, not that any pair of beams implements it.

There is a further local check. If an individually defined metastable basin is invariant under a threefold rotation, its scalar free energy cannot have a linear E2g derivative: an invariant gradient would satisfy g = g rho_E2(C3), but rho_E2(C3) has no unit eigenvalue. The same holds for a locally invariant scalar basin and an E1 coordinate. This is conditional on the symmetry of the full occupied basin, not just a crystallographic site label. Oriented split interstitials and defect environments can break that symmetry. Consequently, the globally allowed mixed current does not license assigning E2g to a nonzero scalar site-energy splitting in the old two-site model. Local basin/path symmetries must be checked explicitly. No universal K-beta no-go is asserted.

These are necessary symmetry signatures, not unique identifiers of geometric pumping. Direct electrical motion whose mobility is Raman-modulated has the same symmetry. Surfaces, disorder, static fields, and higher-order responses may produce additional channels.

A mixed observable can be isolated with four protocols:

    X_cross = [X(R,P) - X(-R,P) - X(R,-P) + X(-R,-P)] / 4.

R -> -R is implemented by an independently checked mode-sign change, not a negative optical intensity. Absorbed energy, unwanted modes, and residual fields must be compared. Delay reversal is not automatically time reversal of a damped structural trajectory.

## 3. What must be acquired from one physical model

The old static lower bound is

    E_min(y) = 1/2 y^T [A K^-1 A^T]^-1 y,
    y = (u-u0, v), A = [g^T; h^T].

It holds for positive harmonic stiffness K and rank-two A in the specified linear static subspace. It does not establish that light can reach the required y.

For mass-weighted coordinates and the exp(-i omega t) convention, a linear dynamical starting point is

    Q(omega) = [K - omega^2 I - i omega Gamma(omega)]^-1
               [Z* E(omega) + F_Raman(omega)].

The actual transfer from available fields to the two physical responses is A times this susceptibility and the available driving matrix. Raman forces are ordinarily quadratic in the optical field. Nonlinear amplitudes require the corresponding anharmonic dynamics rather than extrapolating the linear transfer. A rank-one transfer at one frequency is not a universal no-pumping theorem for arbitrary multifrequency or memory-based protocols.

For K beta, acquisition must start with the actual stoichiometry, defect ensemble and collective interstitial configurations. Freeze the same physical control coordinates at small positive and negative values; relax only the remaining coordinates. Compute constrained well free energies and forward/backward transition branching. Fully relaxing the control mode away would answer the wrong question. If a proposed phonon largely consists of the moving alkali ion, it must not also be counted as an independent host actuator without a consistent coordinate projection.

Static branching/free-energy responses are a feasibility screen. For the driven prediction, use full correlated trajectories, or a memory kernel validated against them and independent equilibrium observations. A picosecond optical anisotropy time does not justify instantaneous Arrhenius rates. Include external and self-consistent internal fields, electronic response, realistic occupations, prefactors, and transport boundaries. Pump-free polar ringdown is not field-free.

### Explicit information-insufficiency example

The following construction shows why well phonons and fully relaxed migration barriers alone cannot determine control rank. It is a counterexample, not a candidate crystal.

Consider two paths sigma=+1,-1 between shared wells s=0 and s=1, with transverse coordinates Q=(Q1,Q2):

    V_sigma(s,Q) = B sin^2(pi s)
      + kappa/2 [(Q1 - d cos(pi s))^2
      + (Q2 - sigma eta sin^2(pi s))^2].

At the wells, Q=(+d,0) or (-d,0). Their complete local Hessians in (s,Q1,Q2) are

    diag(2 B pi^2, kappa, kappa),

independent of eta. Relaxing Q at each s gives the same profile B sin^2(pi s), for every eta. Every path from s=0 to s=1 passes through s=1/2, where the energy is at least B, and the displayed relaxed path attains B. Thus the relaxed minimum barrier is B.

At fixed common Q the well-energy difference and half-difference of the two saddle energies have first derivatives

    u(Q) = 2 kappa d Q1,
    v(Q) = -kappa eta Q2,
    A = diag(2 kappa d, -kappa eta).

The saddle derivative can also be obtained by the envelope argument when the saddle shifts under a small control. With suitable positive B and small d the constrained reference wells remain stable. Eta=0 gives rank one; nonzero eta gives rank two, despite identical relaxed barriers and well harmonic Hessians. The two constructions do not have identical saddle Hessians or all transition prefactors, and no such stronger claim is made.

Therefore the decisive missing measurement is the transverse, mode-constrained transition response. Spectral peaks and a small relaxed barrier do not infer it.

## 4. Unequal frequencies and damping

For a specific unshaped ringdown, let

    q1=A exp(-gamma t) cos(omega1 t),
    q2=B exp(-gamma t) sin(omega2 t), t>=0.

Close the initial point to the origin along the q1 axis, which adds zero oriented area. Then

    Area = 1/2 integral(q1 dq2 - q2 dq1)
      = AB/4 [(omega1+omega2) 2gamma /
               ((2gamma)^2+(omega1-omega2)^2)
             +(omega2-omega1) 2gamma /
               ((2gamma)^2+(omega1+omega2)^2)].

At equal frequency omega this is AB omega/(4gamma). Detuning substantially larger than the linewidth suppresses the resonant term of this specific primitive. Shaped forcing can change the trajectory, with additional costs; this is not a universal bound on arbitrary control.

This is a geometric calculation of a prescribed waveform, not a K-beta transport prediction. No measured K-mode pair or damping values were inserted. At nonadiabatic hopping times, area alone need not determine ionic transport.

## 5. Retention and spatially useful transformation

Continuity gives d_t c = -div J. Uniform drift starting from a uniform composition does not write a composition pattern. Permuting identical ions can yield nonzero unwrapped tracer displacement while leaving every useful local structural/compositional property unchanged.

For a small nonzero Fourier-mode density perturbation in a homogeneous one-mobile-species conductor with fixed compensating background, take

    J_n = -D_chem grad(delta n) + (sigma/q) E,
    div E = q delta n / epsilon.

Here epsilon is the relevant background dielectric permittivity, excluding a second counting of mobile-ion conduction. Linear continuity gives

    d_t delta n_k = -(D_chem k^2 + sigma/epsilon) delta n_k.

D_chem and sigma are constitutive coefficients; a tracer Nernst-Einstein identification is not assumed. In an anisotropic system the electrical term is (k^T sigma k)/(k^T epsilon k). Nonlinear traps, phase boundaries, chemical reactions, additional carriers and contacts require their own model; this law is not a no-go theorem for every retained ionic material.

For an explicitly stipulated 10 nm sinusoidal pattern retaining 90 percent amplitude for one hour, this model requires

    D_chem (2pi/10nm)^2 + sigma/epsilon <= 2.9266809905e-5 s^-1.

With neutral compensated transport and no electrical term, D_chem must be no larger than 7.4133695525e-23 m^2/s. With the diffusion term set to zero, the dielectric relaxation time epsilon/sigma would need to exceed 34168 seconds, about 9.49 hours. These are target-derived limits, not measured K-beta coefficients.

Possible exits include neutral countertransport, deep trapping, a stable chemical phase transformation, or annihilation of the mobile defect at its destination. Each needs its own capacity, free-energy, transport, damage and reverse-reaction account. Merely asserting that a fast conductor becomes immobile after a pulse is insufficient.

The system metrics must include total wall-input energy per verified retained transformation, source conversion, useful and parasitic absorption, lattice damping, thermal management, field delivery, contacts, throughput, final spatial resolution and depth, fatigue, and unwanted defects. An atomic hop is not optical spatial resolution. A blocking sample cannot sustain arbitrary accumulated one-species transport without space-charge opposition or compatible boundary reactions.

## 6. Driven superionicity: a contemporary alternative, not an established solution

Li et al.'s 5 October 2026 preprint [S6] supplies a materially specific computational route in AgCrSe2: configuration-dependent effective charges and an interatomic potential, with an out-of-plane 0.03 V/angstrom AC field and a separate in-plane 0.0025 V/angstrom probe. At 0.05 THz and thermostatted 300 K they report approximately 1.7 S/cm. The 37 meV/Ag transition is collective; localized partial rearrangements have eV-scale penalties. This is simulation evidence for driven mobility, not a laboratory demonstration of unbiased pumping or retained pattern writing.

The reported probe values give, by unit conversion,

    sigma_x E_x^2 = 170 S/m * (2.5e7 V/m)^2
                  = 1.0625e17 W/m^3.

This is the electrical probe-work density inferred from the stated transport definition, not a calculation of the out-of-plane drive's total heating. The missing drive-work account involves the actual integral of E_z dP_z and other losses. A Langevin bath maintaining 300 K is not a physical cooling or wall-energy budget. Simulation duration for statistics does not imply an equally long continuous experimental pump is necessary.

## 7. Independent task: low-temperature, post-fabrication SiC defect repair

The concrete alternative task examined was removal of harmful carbon vacancies from 4H-SiC power-device material after fabrication, rather than generic ionic displacement. The desired endpoint is

    C_i + V_C -> C_C.

Annihilation can retain the result because the mobile defect disappears into a normal lattice site. This reaction and electronic assistance of annealing are not new inventions.

Existing comparisons are materially stronger than a hypothetical pump. Carbon-rich thermal treatment at 1250 degrees C has removed the carbon-vacancy DLTS signature below detection while producing other carbon-related traps [S7]. That study also found cap loss/oxidation, so it is not a clean isolated carbon-cap source experiment. Room-temperature recombination-enhanced removal of some SiC irradiation-defect signals was reported in 2005 [S8], but this does not identify those signals as healed carbon vacancies. A 2025 study reports approximately one-minute pulsed-current rejuvenation of commercial SiC MOSFETs and checks much of the electrical recovery after 175 days [S9]; it used only two devices and explicitly lacks microscopic defect identification. It is a strong functional comparator, not proof of carbon-vacancy annihilation.

The material-level obstacle is not removed by identifying a soft local motion. In the carbon-interstitial/M-center study [S10], the 0.11–0.24 eV barriers describe rotations. Reported C_i^- translational migration barriers are 1.8 eV in the basal direction and 2.2 eV axially. The configuration-coordinate diagram displays the lower of two inequivalent axial steps: cycling between two configurations does not establish repeated cell translation. Electronic trap depths are not optical excitation thresholds. Competing capture and charge states also matter. The paper finds low final annihilation barriers for close Frenkel pairs, but does not demonstrate an affordable route that first brings separated defects together selectively.

A simple kinetic restriction is useful. Suppose desired-vacancy and unwanted-sink capture hazards share one mobility multiplier a(t):

    h_V(t) = a(t) k_V N_V,
    h_j(t) = a(t) k_j N_j.

With fixed sink populations and those well-mixed hazards, the conditional fraction reaching the desired sink is

    P(V | capture) = k_V N_V / (k_V N_V + sum_j k_j N_j),

independent of a(t). A finite pulse changes the completion fraction, not this conditional branching. This does not claim invariance for arbitrary spatial dynamics or independently modulated charges. It identifies what an improved mechanism must do: change capture selectivity, not just accelerate every diffusion/capture pathway together.

No validated charge/optical cycle changing that branching while enabling full translation was found. This pivot was therefore not promoted to a discovery candidate meeting the mission standard. Ordinary electronic annealing was not renamed as a new physical power.

## 8. Strongest remaining K-beta experiment

1. Qualify one phase- and composition-verified K-beta crystal. Measure polarized complex IR and Raman responses and coherent host/ion trajectories on that specimen. Obtain a mode-constrained, many-ion transition-response calculation at those same displacements. Validate against independent equilibrium observations before any driven-current fit.

2. Use the four-protocol mixed response and the D6h angular prediction above. Include the c-axis-IR forbidden-channel control. Predict complete delay, frequency, field and polarization dependence from measured trajectories, without borrowing a population rate from optical memory. Equal incident energy is not equal absorption. Residual external and internal fields and Raman-induced ordinary mobility changes must be included.

3. Establish net translation independently of reversible polarization. Electrical charge detection should be paired with an appropriate tracer/composition measurement; changes in a tracer centroid and its width help separate drift and symmetric broadening. A stable K-isotope profile is a possible assay design, not a sensitivity-calibrated experiment already established here. The ideal sampling error would depend on profile variance, diffusion duration and independent effective counts; instrument resolution, drift, boundaries and thermodiffusion must also be budgeted. The existing Na experiment establishes picoampere electrical readout feasibility, not the size of a K mixed signal.

4. Any technological claim additionally needs a retained endpoint, charge/mass balance, final device or material performance, wall energy, depth, throughput and damage comparisons. A positive phase-sensitive current without these remains a transport result.

Stop this material-mode branch if the acquired second response is absent, the accessible trajectory is too small after damping/detuning, the full-field baseline explains the signal, or no retained endpoint survives. Missing parameters are not permission to enlarge assumed pump amplitudes.

## 9. Reproducibility and limits

`check_audit.py` checks 24 symmetry covariance fixtures, two information-insufficiency potential cases, 18 damped-loop quadratures, four linear-PNP modes, uniform-current continuity, and three capture-hazard doses. It reproduces the stipulated retention thresholds. These are floating-point checks on mathematical identities, not independent physical validation. See `checks.json` for residuals.

Sources are in `SOURCES.json`; it records what was read and which evidence is missing. Public-source claims retain their material, phase, temperature and evidence level. Current searches were not an exhaustive patent or priority clearance. Missing K-specific spectra/gradients and missing microscopic validation in comparator studies remain missing.

The research outcome is a tightened material/retention audit and a discriminating acquisition experiment. It is not a physically established exceptional controlled-matter operation.
