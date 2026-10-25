# Oxygen transport, pressure bias, and material-volume constraints

These are conditional engineering derivations for the third construction. They do not assert that the published Hb–PEG gel meets the device's threshold, conversion-speed, cyclic, or load requirements.

## Oxygen binding makes a water-only diffusion estimate inadequate

Let p be oxygen partial pressure, alpha p the dissolved oxygen concentration, and B(p) bound oxygen per gel volume. If the oxygen-binding sites are locally equilibrated and immobile, conservation in a thin gel gives

    [alpha+B'(p)] partial_t p = D_free alpha Laplacian(p).

For small excursions around a reference pressure, the effective diffusivity is

    D_eff=D_free/[1+B'(p)/alpha].                          (13)

If bound oxygen can diffuse with its carrier at D_bound, the numerator becomes D_free alpha+D_bound B'(p), giving

    D_eff=[D_free alpha+D_bound B']/(alpha+B').            (14)

The immobile case is an explicit hypothesis, not a proven property of a dynamic Hb–PEG network. Carrier exchange/facilitated transport can change the answer; slow ligand kinetics can add another limitation. The actual material needs a transient oxygen uptake/release measurement.

Use B(p)=B_max p^n/(P50^n+p^n) as an illustrative Hill isotherm. At p=P50,

    B'=n B_max/(4 P50).

The 2025 paper uses [Hb]=0.50 mM in its pO2 rheology series; four oxygen sites per Hb tetramer give a nominal B_max=2 mM. Its measured dilute-conjugate P50=3.3 Torr is an input proxy, not an independent binding measurement inside the loaded actuator. Taking alpha=1.3 micromolar/Torr, D_free=2e-9 m2/s, and n=2 as **illustrative aqueous/Hill inputs** gives a retardation factor of about 234 near P50. These are not a fitted material diffusivity or measured Hill coefficient.

For a slab of half-thickness a supplied at both faces, the leading linear diffusion relaxation time is

    tau_1=4 a^2/(pi^2 D_eff).

Its mean residual response has leading amplitude 8/pi^2; the first-mode estimate for 90% equilibration is tau_1 log(80/pi^2). Under the preceding immobile-site illustrative inputs, a=50 micrometres gives about 249 s, while a=10 micrometres gives about 10 s. The exact small-signal series, rather than only this approximation, is used in the calculation file. No water-only estimate can certify a five-second ligand conversion in this material.

## A constructive way to shorten the diffusion path

Make the load-bearing pad a bank of parallel thin gel ribbons, each with short lateral oxygen diffusion distance and all carrying axial mechanical load in parallel. For length L, total load-bearing cross section A_total, and material modulus G,

    K_0=G A_total/L,       V_gel=A_total L.

Splitting the same area/volume into N thinner ribbons does not reduce axial stiffness in this ideal mechanical model, while the binding-limited lateral diffusion time falls as ribbon half-thickness squared. A hundred-micrometre-wide pad divided into ten equally thick oxygen-accessible ribbons could therefore reduce this internal diffusion contribution by about 100-fold. Boundary fluid channels/membranes must actually supply all ribbon faces at the sensed tissue pO2; external oxygen transfer, binding kinetics, added volume, and mechanical support cannot be ignored.

This is a concrete interface architecture, not an assumption of instant oxygen conversion. It addresses one missing interface without claiming to solve the material's very-low-oxygen switching threshold.

### A kinetics floor that thin ribbons cannot evade

The local-equilibrium calculation can be tested against explicit finite binding kinetics. Linearize an immobile binding system around a reference state, with free oxygen perturbation u and bound perturbation v:

    partial_t u=D Laplacian(u)-a u+b v,
    partial_t v=a u-b v,

where a,b>0 are chemical relaxation coefficients. For a spatial mode with d=D k^2, its two decay rates are

    lambda_±=[d+a+b ± sqrt((d+a+b)^2-4 d b)]/2.             (19)

At chemical equilibrium v/u=a/b, so the buffering factor is 1+a/b. In the fast-binding regime the slow mode is d/(1+a/b), reproducing (13). As the specimen becomes arbitrarily thin (d→infinity), the slow bound-state rate approaches **b**, not infinity. A clamped free-oxygen step therefore retains an intrinsic ligand-state conversion time, with ideal one-mode 90% conversion ln(10)/b. A separate network-association conversion state can introduce another slow mode.

Neither a nor b is the measured stress-relaxation time. The proposed thin-ribbon/bulk comparison has a clear interpretation: quadratic thickness scaling supports internal diffusion/buffering control; a thickness-independent floor points to ligand/network kinetics or external boundary transfer. External mass transfer must be independently controlled to distinguish those explanations. Equation (19) is a linearized reaction/diffusion model, not an identified kinetic mechanism for the published gel.

## Thin ribbons cannot eliminate the oxygen inventory

The oxygen charge needed for a saturation change Delta_s is

    Delta_n = B_max V_gel Delta_s.

For the illustrative 10 nL gel pad, B_max=2 mM gives 20 pmol per full saturation change; eight phase copies require 160 pmol. Thin subdivision changes the path length, not this inventory. If only J_reserve mol/s of oxygen delivery is available beyond tissue uptake, then charging requires at least Delta_n/J_reserve seconds. The sensing element can perturb the tissue it senses; its oxygen budget must be coupled to that of the tissue, rather than granted as a clamped infinite reservoir.

## A force/stroke/oxygen-inventory inequality

For the series Maxwell-gel/output-spring architecture, let the admissible input strain be epsilon_max=U_max/L, gel volume V, and instantaneous modulus G. At any sinusoidal frequency, |H|<=1/(1+beta). If A_y is output stroke amplitude and F=K_v A_y the spring-force amplitude, then

    F A_y=beta K_0 |H|^2 U_max^2
          <= [beta/(1+beta)^2] G V epsilon_max^2
          <= (1/4) G V epsilon_max^2.

Therefore this architecture requires

    V >= 4 F A_y/(G epsilon_max^2),
    Delta_n >= 4 B_max Delta_s F A_y/(G epsilon_max^2).    (15)

At nonnegligible viscoelastic loss the volume requirement is stronger. This is not a bound on every sensor or an externally powered latch. It is a topology-specific bound on the proposed direct mechanical transmission. Optical sensing plus a separate powered actuator need not satisfy it, which makes that an essential comparator.

For the illustrative model F=40 nN, A_y=20 micrometres, G=100 Pa, epsilon_max=.06, (15) gives V>=8.9 nL and about 17.8 pmol full-saturation oxygen charge per phase. The chosen 10 nL pad is already close to this ideal series-transmission volume bound. Reducing pad volume freely while retaining force and stroke is not an admissible repair.

## Residual hydraulic pressure can destroy the conductance contrast

Let a pressure-balanced spool retain unmatched hydraulic area delta_A. At pressure difference Delta_P it has static bias force F_h=delta_A Delta_P. A Maxwell gel transmits no static elastic force after relaxation, so the output spring develops mean displacement

    y_bias=-F_h/K_v.

Because the opposed-port conductance depends on |y|, a substantial bias opens the nominally low-conductance state and removes selectivity. To hold |y_bias|<y_tol,

    |delta_A| < K_v y_tol/Delta_P.                         (16)

With K_v=.002 N/m, Delta_P=1900 Pa, and y_tol=1 micrometre, the mismatch must be below about 1.05e-12 m2. Against a nominal 1e-9 m2 pressure area this is about 0.1% residual area. Dynamic pressure, spool friction, seal drag, membrane bending, and mechanical-clock losses can demand still more. This calculation names a fabrication/force-balance requirement; it does not establish that it can be met in a biocompatible microdomain array.

## Why simply replacing the valve with a local pump is not free

A local pump could avoid dissipating common high pressure across healthy territories, but the gel would then have to transmit useful hydraulic work. With input velocity amplitude omega U and gel mechanical impedance Z_g=K_0 tau/(1+i omega tau), the maximum power delivered to a purely viscous linear load is attained at load coefficient C=|Z_g|:

    P_load,max=(omega U)^2 |Z_g|^2/[4(|Z_g|+Re Z_g)].        (17)

For the model's K_0=.001 N/m, tau=600 s, omega=.02/s and U=60 micrometres, this is about 1.7e-14 W per phase. Eight copies supply only about 1.3e-13 W through this direct linear coupling. A 100 Pa, 1 nL/s hydraulic duty is 1e-10 W. Thus a direct local-pump replacement at that duty would need a much larger material/drive budget or a distinct powered clutch/latch interface. Treating the gel as a low-power controller of a larger external energy source is a different, potentially useful construction, but the source, force routing, and switching operation have to be invented explicitly.

## Decisive next scientific operation

The smallest informative physical unit would be an isolated oxygen-to-stroke transducer, with oxygen activity independently clamped and measured, not an organ experiment. The decisive measurements are the transient ligand state, frequency-dependent force/stroke, hysteresis, pressure bias/friction tolerance, cyclic degradation and total input work. A thin-ribbon specimen and a bulk specimen at matched Hb inventory can discriminate diffusion/binding retardation from intrinsic ligand/network conversion. Passing that operation would acquire a transducer at its measured conditions; it would not establish tissue recovery, novelty, or whole-organ feasibility.
