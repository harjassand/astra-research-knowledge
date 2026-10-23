**There is now a coherent model-level result: retained sleeve order can encode a binding preference while the active attachments remain free to slide.** Removing every connection between rail assemblies leaves that internal order unchanged. The result comes from one contact construction and one equilibrium ensemble, with whole-assembly translation, rotation and unbound arms included.

I’m retaining the thermal sleeve architecture. The useful operation is **persistent internal identity carried through exchange of external connections**. Its molecular realization remains open, and the calculation does not yet establish a branching material or a repair process.

### The shared construction now has consistent contacts and statistics

The test components have identical inventories: two active sleeves \(A\), one passive spectator \(B\), and the same capped rail. They differ only in retained order:

- \(U:\ B\!-\!A\!-\!A\)
- \(C:\ A\!-\!B\!-\!A\)

Every \(A\) has the same exterior connection chemistry; \(B\) has none.

The model uses a straight, rigid guide with radius \(3\) nm, sleeves with outer radius \(12\) nm and axial contact length \(35\) nm, and spherical end stops of radius \(8\) nm. The usable rail length is \(220\) nm. Each active sleeve rotates freely around the guide and carries a radial stem ending at radius \(20\) nm, followed by a freely hinged, \(6\)-nm arm. Arm thickness, joint volume, unused arms and collisions between assemblies are included.

**A contact correction was necessary.** A rounded sleeve drilled through its axis does not retain the axial contact length of its filled outer envelope. For contact length \(a\), outer radius \(R\) and bore radius \(\rho\), the corrected capsule spine half-length is

\[
h=\frac a2-\sqrt{R^2-\rho^2}.
\]

The stopper positions require the corresponding bore-edge correction. With these corrections, the same surfaces determine both the allowed sliding gaps and collisions with another assembly. In the zero-clearance bearing limit, the sleeve’s own guide fills its bore, so the union of guide and drilled sleeves has exactly the filled exterior envelope used in the collision calculation.

This also closes the earlier gap between a crossing coordinate and a statistical weight. Uniform ordered axial coordinates emerge from the normalized, narrow-clearance bearing measure; they are not assigned merely because an axle passes through a ring. For \(M\) spectators, with \(n\) between the two active sleeves, their axial separation obeys

\[
S=a+nb+FT,\qquad
T\sim\operatorname{Beta}(n+1,M-n+2),
\qquad F=L-2a-Mb.
\]

No Gaussian-chain assumption enters this result.

Order retention follows from contact obstruction. A sufficient nonpassing condition at positive bore radius \(H\) is

\[
3H<R+2\rho.
\]

Here that permits \(H<6\) nm, while the larger end stops prevent escape. **This is a retention bound, not a bound on the error in the binding calculation.** The equilibrium integrals converge to the calculated bearing limit as clearance tends to zero, so a strict preference persists for sufficiently small positive clearance. A numerical fabrication tolerance has not been established.

### Two contacts can read information that one contact loses

The one-contact construction exposed a consequential failure. If its only readout is a positional binding kernel, freely translating the two components washes out the positional preference:

\[
\int d\delta\,K_{mp}(\delta)=\int ds\,w(s).
\]

Whole-body exclusion can leave a residual shape-dependent effect, but a registered one-contact result cannot be promoted directly to freely assembling components.

Two contacts can instead read an **internal separation distribution**, which survives translation and rotation. The calculation integrates the actual radial stems, sleeve azimuths, arm configurations and assembly poses; it does not substitute axial separation for the full three-dimensional contact geometry.

For the three-sleeve construction, the completed contact calculation gives the following coefficients. They are normalized by the unbound arm partition; uncertainties are one standard error from sampling.

| Pair | Single-bond coefficient \(B_1\) | Double-bond coefficient \(B_2\), nm\(^{-3}\) |
|---|---:|---:|
| \(U,U\) | \(0.3433\pm0.0005\) | \((4.378\pm0.023)\times10^{-8}\) |
| \(U,C\) | \(0.3492\pm0.0006\) | \((2.999\pm0.035)\times10^{-9}\) |
| \(C,C\) | \(0.3550\pm0.0006\) | \((6.625\pm0.041)\times10^{-9}\) |

Each entry used two million independent trials. An independent deterministic calculation of the contact-ablation model agrees with the corresponding Monte Carlo results and checks the translation, rotation and closure weights.

The double-bound coefficients favor both matching pairs. Their normalized pair-weight ratio is

\[
\mathcal R_2=\frac{B_{2,UU}B_{2,CC}}{B_{2,UC}^{\,2}}
=32.24\pm0.79.
\]

**Single bonds substantially dilute that preference.** For labeled rails, the complete association volume is

\[
K_{ij}=4\lambda B_{1,ij}+2\lambda^2 B_{2,ij},
\]

where \(\lambda\) is one common intrinsic junction association volume. The factors count four single-contact choices and two complete matchings.

At the illustrative, uncalibrated value \(\lambda=10^8\ \mathrm{nm^3}\), the corresponding total pair-weight ratio is about **6.97**, rather than 32.24. In the weak-binding limit it is approximately one. These are equilibrium pair weights, not predicted sorting yields. The common junction weight, local hinge rule and sticky-contact approximation remain explicit model inputs; they do not supply reaction rates.

### A decisive control separates accessible geometry from its statistical weighting

I kept the total spectator length at \(70\) nm and compared:

- one independently sliding spectator of length \(70\) nm;
- two independently sliding spectators of length \(35\) nm each.

The allowed active-sleeve separation intervals remain identical between these controls: \(35\)–\(115\) nm for the outside-spectator arrangement and \(105\)–\(185\) nm for the inside-spectator arrangement.

Nevertheless, splitting the spectator changes the probability of occupying those accessible separations. In the calculation with binding obstruction suppressed, mismatched double closure falls by a factor of **21.60**. With all physical body and arm contacts restored, it falls by **\(19.90\pm0.27\)**. The latter result includes the changed spectator surfaces as well as their additional sliding freedom.

The mechanism is identifiable. Splitting the spectator suppresses the large-gap tail required from the outside-spectator component and the small-gap tail required from the inside-spectator component. The relevant average is taken over the **correlated, doubly bound ensemble**. Multiplying unloaded mean gaps would miss it.

This establishes something beyond a forbidden-spacing explanation: **retained inventory changes the weights of configurations that remain geometrically possible**, and that effect survives the common-contact calculation. It does not imply that a twentyfold change in double closure produces a twentyfold change in total association; the single-bond contribution remains present.

### What this changes about the materials opportunity

The general design lesson is now more specific:

> Retained internal information becomes useful when it changes a correlation of active attachment positions that survives the component’s free motions—and when that correlation remains consequential after all competing bond states are included.

Existing work already establishes entropic control of affinity, steric communication between fluctuating DNA components, and assembly effects from mobile binding groups. Those are strong conventional precedents, not capabilities to claim anew. An ordinary bivalent binder with the same internal separation distribution can reproduce the equilibrium recognition calculated here. The architectural opportunity is to store that distribution in **captive, sliding inventory**, while external partners exchange. :chatgpt-content-reference{index="0"}

The physical evidence also narrows the implementation choices:

- **DNA origami** provides a demonstrated capped rail, mobile slider and reversible positioning chemistry. Benson’s device does not establish the combined operation of several ordered mobile sleeves with exterior inter-sleeve connections. Its rail compliance and released positioning handles must remain in a material-specific model. :chatgpt-content-reference{index="1"}
- **Carbon nanotubes provide stronger direct bearing evidence than I initially credited.** Beyond telescoping cores, Barreiro and colleagues demonstrated a short outer sleeve carrying exterior cargo while translating and rotating on an inner nanotube. Thus attachment to a moving sleeve is already physically demonstrated. The outstanding interface is several independently translating retained sleeves, selected reversible exterior connections, and their equilibrium positional free energy. Their demonstrated motion was thermally driven; low friction does not establish uniform equilibrium occupancy. :chatgpt-content-reference{index="2"}

I have not combined DNA’s binding control with nanotube bearing data and treated the combination as a realized material. The missing interactions—rail deformation, atomic or molecular corrugation, sleeve adhesion, residual handles and linker contacts—could change the predicted weights. That is a physical interface to resolve, distinct from lacking experimental equipment.

The present two-site component also has a clear network limitation: strong double binding consumes both active sites and favors saturated dimers. It does not supply a branching elastic network, an autonomous writer of sleeve order, a reset time or a global repair guarantee.

The earlier contact argument, elastic-energy floor, two-spectator distinction, counterexample and correlated loaded-ensemble criterion remain at their stated scope. This construction adds a concrete equilibrium readout of retained inventory. The next material-level question is whether that persistent