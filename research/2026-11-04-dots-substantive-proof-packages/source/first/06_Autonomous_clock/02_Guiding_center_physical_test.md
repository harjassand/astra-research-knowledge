# Physical attempt: guiding-center clock and a Coulomb target

This follows the parent's constructive suggestion after the finite-reserve action-angle clock was built. **It advances the physical mechanism beyond an arbitrary angle-only potential, but does not earn that potential, a complete gate, or an advantage over energy-recovery logic.**

## What a magnetic clock genuinely changes

For a charge in a strong perpendicular B field, guiding-center coordinates are conjugate up to orientation, with |{X,Y}|=1/|qB|. Thus J=|qB|R²/2 and theta are an action-angle pair made from two physical spatial coordinates. A quadratic positive radial potential gives linear H_clock=omega J at leading guiding-center order. This evades the earlier restriction to one natural coordinate-only oscillator coupling: spatial angular patterning can act on the canonical clock angle.

But an ordinary Penning trap is NOT automatically this positive-energy clock. Axial electrostatic confinement entails radial anti-confinement; its slow magnetron mode has negative energy, and dissipation increases its radius. Positive radial confinement needs an independently paid axial/2D mechanism. An ideal planar constraint was supplied in the tests below, not derived from electrodes.

For a positively confined planar massive charge, the exact quadratic radial frequencies are

    Omega_s=(sqrt(omega_c²+4omega_0²)-omega_c)/2,
    Omega_f=(sqrt(omega_c²+4omega_0²)+omega_c)/2.

Finite-cyclotron corrections depend on Omega_s/omega_c; thermal gyroradius smears an angular harmonic n by order n² rho_L²/R². A classical thermal estimate is rho_L²~kT/(m omega_c²), up to the convention for mean-square radius. Very strong B is a resource, and quantum/cryogenic regimes need their actual occupation law. No thermal ensemble or refrigeration bill was simulated here.

Primary checks: Imperial's Penning-trap description https://www.imperial.ac.uk/ion-trapping/research/current-research-topics/penning-trap/; the primary experiment https://link.springer.com/article/10.1140/epjti/s40485-017-0039-4 explicitly discusses negative magnetron energy and collisional radial growth. These support the confinement caveat, not the new gate.

## Concrete action coupling, rather than an arbitrary gI

A clock charge at (R cos theta,R sin theta,0) interacts with a symmetric target pair at (u,0,h) and (-u,0,-h), h>0. The target's collective displacement u has effective mass m_t and harmonic frequency omega_t. The clock-target electrostatic potential is exactly

    V_C=C/[R²+h²+u²-2Ru cos theta]^(1/2)
       +C/[R²+h²+u²+2Ru cos theta]^(1/2).

The finite layer separation prevents coincident target charges. A symmetric mode constraint, target confinement and its internal Coulomb contribution must be included in a real apparatus. Our effective harmonic target is a favorable approximation, not an ion-trap design.

Expanding in |u|/sqrt(R²+h²), then averaging the fast target oscillator with <u²>=I/(m_t omega_t), gives

    <V_C> = 2C/sqrt(R²+h²) + I h_eff(R,theta) + O(<u⁴>),
    h_eff = C[3R² cos² theta-(R²+h²)] /
            [m_t omega_t (R²+h²)^(5/2)].

This is a defensible physical origin for action-dependent angular coupling. It also explicitly shows the unwanted radial dependence and the static monopole term. Real Coulomb-mode cross-Kerr shifts and spectator-mode dephasing are established experimentally, e.g. https://doi.org/10.1103/physrevx.14.021003; that experiment does NOT implement this geometry or its clock.

For h/R tending to zero,

    h_eff = [C/(m_t omega_t R³)] (1/2+3/2 cos 2theta).

Consequently partial_J h_eff=-3 h_eff/(2J). The magnetic bridge changes what is accessible spatially but does not remove the actual load dependence of this Coulomb realization.

## Backreaction tested before claiming a gate

Grant exact static monopole compensation and the leading guiding-center and fast-target approximations. Set omega_clock=1, J0=1 and C/(m_t omega_t R0³)=1. Start at theta=-pi/2. Then

    H=J+I J^(-3/2)(1/2+3/2 cos 2theta),
    theta_dot=1-(3I/2)J^(-5/2)(1/2+3/2 cos 2theta),
    J_dot=3I J^(-3/2) sin 2theta.

The target's extra phase is the integral of h_eff along the actual orbit, not a prescribed-time integral. For rho=I/J0 small, expanding energy conservation and the actual dt/dtheta gives

    extra phase/pi = 1 + (39/4)rho + O(rho²),
    traversal time = 2pi + (3pi/2)rho + O(rho²).

`test_guiding_center.py` independently integrates these equations. Relative extra-phase errors at rho=.0001,.001,.01,.05 are .0009758,.0098305,.10635,.90218. At .08 and .1 the orbit fails to complete before leaving the admitted annulus in this effective model. That failure is not a claim about actual Coulomb trajectories near the model singularity.

A critical comparison: a fast physical target also rotates at omega_t between modulations. At the clock's completed revolution the readable phase relative to an integer-frequency clock reference is

    phi_read = extra phase + omega_t (traversal time - 2pi).

Subtracting omega_t times the ACTUAL traversal time would silently grant another perfect clock. Thus for integer omega_t, the first-order relative error is

    phi_read/pi -1 = [39/4 + (3/2)omega_t] rho + O(rho²).

Fast-target averaging helps its own approximation while worsening phase sensitivity to clock delay. This is a genuine implementation tradeoff, not a proof that reliable devices are impossible.

## Unaveraged finite-mass test

`test_full_coulomb.py` integrates the full planar Lorentz force plus exact clock-target pair potential and target dynamics. Its original h=0 model is retained only as a mathematical diagnostic; coincident same-plane target charges make it unsuitable as a physical target.

`test_separated_coulomb.py` corrects that by using h=R0/4 and the exact separated-pair potential. It still grants an effective harmonic target, ideal planar confinement and exact static monopole compensation. Those grants must not become claims of completed electrodes, internal target forces or thermal preparation.

The clock has mass=charge=1, B=100 or300, kappa=B+1 and initial circular speed=R0, so its uncoupled slow angular rate is EXACTLY1, not a guiding-center approximation. J0=B R0²/2=1; omega_t=30. Numerical events detect a full physical clock revolution. Saved results include target-action change, total phase in the actual clock frame and Hamiltonian-energy drift. These deterministic sample trajectories are not stochastic fidelity estimates or rigorous finite-error bounds.

The earlier same-plane calculation already showed clock-frame relative phase errors of -.0377,.00628,.1081 for I=.0001,.001,.003 at B100. The superficially small error at the middle point is cancellation between approximation/calibration and load error, not amplitude-independent control. The separated-pair results are saved separately and supersede it as the geometrically admissible diagnostic.

## Electrostatic shaping and the stronger remaining operation

For a genuinely 2D charge-free annulus, a nonzero angular Fourier component of a harmonic electrostatic potential has radial form A R^n+B R^-n. One can set its first radial derivative to zero at R0 with B=A R0^(2n); then f''(R0)=n²f(R0)/R0². Thus local flattening is available, but exact radial independence over a finite annulus is not supplied by such a component. This is only a 2D Laplace restriction: 3D electrode fields can use axial curvature, and an effective target-action coefficient is not automatically harmonic in two dimensions. It is not a universal electrostatic no-go.

The next stronger operation is an actual finite electrode/charge geometry that cancels the relevant radial derivatives of the COUPLED target-action coefficient, retains stable axial and radial confinement, and supplies a useful write/hold/read interface. Its full noise, input-state, magnet, cooling and shared-clock costs must then beat the strongest admitted energy-recovery block at matched throughput and reliability. None of those comparisons follows from making guiding-center coordinates canonical.

This follow-up earns an explicit Coulomb coupling and deterministic finite-mass tests. It does not earn a physical angle-only coupler or a new computing capability. The bottleneck is now concrete geometry and a full repeated-block resource comparison, rather than a generic missing-Hamiltonian disclaimer.

## Calibrated comparison, not a strawman detuning failure

`test_calibrated_coulomb.py` gives the separated-plane model a scalar coupling calibration at I/J=.001, initial target phase0. The resulting scale1.349837745 produces pi to numerical accuracy. The SAME scale is then used at I/J=.0001,.001,.003 and initial phases-.2,0,.2. Clock-frame relative rotation errors range from about -3.6% to+8.4%, with target action changes up to1.4%. All nine outputs retain the correct NOT sign basin. Thus these deterministic data do show a working one-cycle NOT in this supplied conservative model; the phase errors are not immediate logical failures. They do not establish a repeated computation threshold, thermal fidelity, an output-hold operation or an energy advantage.

The role of calibration is important. The uncalibrated separated geometry changed the mean coupling and had a roughly27% phase offset at the smallest action. That removable offset is NOT the decisive failure. The retained challenge is variation across actual input actions, physical clock delay, finite-amplitude target distortions, noise, repeatability and the complete interface/resource comparison.
