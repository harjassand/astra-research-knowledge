# Second construction: a finite-window oxygen-conditioned feed valve

This is a change of attack after the unfavorable matched-budget result for flowing adaptive viscosity. It remains directed at recovering oxygen-starved complex tissue. It is a hypothetical solid mechanical device, not a demonstrated perfusate or treatment.

## Why a different physical interface

The first construction cannot defeat a uniform-low-viscosity comparator at fixed pressure. In the synthetic broad networks, large adequate-territory gains also require substantial pressure/power premiums; equal-power gains are small. A steep local fluid switch cannot evade spatial averaging. Rather than reverse the chemistry of an existing oxygen-responsive gel, consider reversing its mechanical action.

Matsuhira and Sakai (2025, DOI 10.1021/acs.biomac.5c00669) establish a synthetic hemoglobin–PEG gel with much longer **stress-relaxation time** on deoxygenation. This is not a measurement of oxygen-conversion time. Nor is its zero-shear gel viscosity an injectable microvascular viscosity. The second device would keep the gel outside the flowing perfusate, behind an oxygen-permeable membrane.

## Mechanical sign inversion

A compliant feed channel is held open by a mechanically coupled gel pad against a compressive bias. During a finite load interval, an oxygenated rapidly relaxing pad creeps and permits closure. A deoxygenated slowly relaxing pad temporarily bears the load and keeps the channel open. Thus the experimentally observed deoxy-state strengthening in time can produce **lower hydraulic resistance under hypoxia**, without requiring deoxy-state low bulk viscosity.

The simplest finite-window operation is:

1. Establish an unloaded open reference configuration; tissue oxygen and gel oxygen must be allowed to equilibrate or their actual transient state must be known.
2. Apply a common mechanical compressive bias while continuously perfusing. Over an intermediate time window, oxygenated territories acquire more gate resistance and hypoxic territories retain more opening.
3. End the recovery interval by removing the bias and placing the supply channel in a mechanically held-open state, or transfer to an ordinary controlled supply circuit. No steady autonomous recovery or repeatable gel reset is assumed.

This is a finite restorative operation, not a Maxwell material claimed to sustain a static gate forever. A repeatable version must explicitly restore the reference strain and account for actuation work; unloading alone does not reset a Maxwell element.

## Where the oxygen signal comes from

Two distinct architectures must not be conflated:

* **Engineered tissue microdomains:** an upstream feed gate is fabricated next to the tissue microdomain it supplies, with a thin oxygen-permeable but protein-impermeable sensing interface. The gel reads local tissue oxygen by diffusion, not arterial luminal saturation. The spatial arrangement and maximum tissue-to-gel distance are part of the device. It could be incorporated while manufacturing perfusable thick tissues/engineered organs; inserting it throughout an intact native organ is not an available operation.
* **Accessible arterial/venous territory pairs:** an extracorporeal valve at an arterial feed can be mechanically coupled to an oxygen-sensing chamber on that same territory's separately collected venous return. This explicitly routes downstream information upstream, but requires separately identifiable arterial and venous access. Mixing all venous returns destroys territory-specific information. It cannot resolve hidden microvascular shunts within one collected territory, and extraction still does not equal latent recoverability.

The first architecture is the stronger route for a truly local controller; the second is a bounded external comparator/interface. Neither is an acquired native-organ repair capability.

## Constitutive calculation to perform

Use a permanent elastic skeleton G_inf in parallel with a Maxwell branch (spring G_1 and dashpot eta=G_1 tau). Under an applied stress step sigma,

    epsilon(t)=sigma/G_inf [1-(G_1/(G_inf+G_1)) exp(-t/tau_c)],
    tau_c=tau (G_inf+G_1)/G_inf.

The permanent skeleton avoids claiming unbounded creep is a useful equilibrium gate. Let geometric leverage convert epsilon to gap reduction:

    h(t)=max(h_min, h_0-ell_eff epsilon(t)),
    R_gate(t)=12 mu L_gate/(w h(t)^3).

The geometry, effective stress, oxygen-dependent G_1 and tau, finite gap, and feedback of channel pressure on membrane force all require an explicit mechanical design. A macroscopic gel modulus cannot simply withstand kilopascal perfusion pressure without a force-balanced membrane, leverage, or sufficiently large actuator area. The computation will keep these as visible physical design parameters.

## What could make this consequential

A sufficiently fast, thin, nonobstructing oxygen-to-mechanics transducer could provide many local feed controls in a fabricated vascular network, preventing macro-scale shunts from determining which microdomains remain viable. This would be an enabling component for recovering or building complex perfusable tissue, while leaving biochemical reperfusion injury and native-vessel reopening as separate tasks.

## Mandatory competitors and falsifiers

- Uniform-open channels at the same pressure and oxygen capacity: the valve cannot improve absolute fixed-geometry branch flow under those conditions; its benefit must use a finite flow budget or a named pressure-protection/geometry/recruitment constraint.
- Ordinary independently controlled upstream valves supplied with the same oxygen information: these are an attainable technology at larger scales and an informed upper comparator, not an ignored incumbent.
- Purely elastohydrodynamic passive regulators and established oxygen/glucose-responsive hydrogel valves: primary prior art must be checked before any novelty claim.
- A dynamic material measurement: stress relaxation is not ligand equilibration or a flow-switching response time.
- A permanently collapsed or obstructed tissue bed: a feed valve does not remove the obstruction. A minimum delivery floor/challenge or a separately acquired reopening operation remains necessary.

State: original device-level construction formed, all material-to-organ and practical-advantage claims UNKNOWN. The reason for pursuing it is a physically explicit route around the first construction's **spatial** limitation, not a claim that the material problem is solved.

## Revealing failure of the constant-preload version

Changing a dashpot relaxation time changes the rate of creep, not its equilibrium under fixed load. Under constant positive bias, the SLS internal creep coordinate increases toward the same soft equilibrium in both oxygen states. If a gate has already closed, a later increase of tau does not reopen it. Thus the finite-window construction is not an autonomous homeostatic controller. Unloading a Maxwell branch is also not a repeatable reset. This defect changes the next construction.

## Third construction: periodically driven mechanical transmission

Replace the static preload by a prescribed zero-mean mechanical displacement U(t)=U_0 cos(omega t). Connect the gel, with complex stiffness

    K_g*(omega)=K_0 i omega tau/(1+i omega tau),

in series with a real output spring K_v attached to a pressure-balanced valve spool. Define beta=K_v/K_0. The output displacement y is

    y/U=H(omega,tau)=i omega tau / [beta+i omega tau(1+beta)].

Deoxygenation-induced long tau increases |H| at fixed frequency, so it gives a larger valve stroke. No zero-frequency elastic support or spontaneous Maxwell reset is required. In time domain,

    dy/dt + beta/[(1+beta)tau] y = (dU/dt)/(1+beta).          (8)

An opposed pair of pressure-balanced metering ports converts positive and negative spool displacement into two parallel openings. A candidate idealized aperture law is

    h_+(y)=h_min+max(0,y),
    h_-(y)=h_min+max(0,-y),
    conductance=(w/(12 mu L_gate))[h_+(y)^3+h_-(y)^3].        (9)

This is a **specified metering geometry**, not a hard stop on the mechanical spring: the spool can translate both directions while different ports are uncovered. Fabricating the aperture law, cancelling static hydraulic force, and keeping friction/load small are real design requirements. Without hydraulic force balancing, perfusion pressure may dominate the soft gel and invalidate (8).

For h_min negligible and a sinusoidal stroke of amplitude A, mean conductance is proportional to (4/(3 pi))A^3. A relaxation-time contrast can therefore be mechanically and hydraulically amplified. A finite minimum opening is essential for bootstrap, and the full finite-gap formula is to be used in computation.

The mean actuator work is not zero. At steady sinusoidal drive,

    P_act,net=(omega/2) Im[K_v H] U_0^2
             =(K_v beta/(2 tau)) |H|^2 U_0^2 >=0.          (10)

In time domain, stored elastic energy is K_v(1+beta)y^2/2 and dissipation is K_v beta y^2/tau. Drive power is K_v y dU/dt. Gross positive drive work, when returned spring energy is not recovered, can exceed the net dissipation; both must be retained. Additional spool friction, fluid drag, phase-drive losses, membrane losses and oxygen-conversion kinetics are not contained in (10).

Several phase-shifted copies can smooth the otherwise oscillatory conductance while preserving a common external actuation clock. This consumes actuator volume and fabrication area; it is not free averaging. A numerical model must propagate each phase and include actuator work.

### New tests and new failure gates

The third construction is only worth continuing if a self-consistent stroke/frequency/material window exists, actuation plus hydraulic work is acceptable, local oxygen conversion is fast enough, and minimum delivery avoids a closed hypoxic trap. The actual published gel's large contrast occurs below about 1 Torr; a healthy-oxygen setpoint would require a different threshold or a different transducer. The published stress-relaxation contrast does not itself establish such a material. Ordinary oxygen sensors with independently controlled valves remain the strongest engineering comparator when local electronics and access are available.
