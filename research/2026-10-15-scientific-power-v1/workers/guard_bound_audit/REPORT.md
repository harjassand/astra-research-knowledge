# Independent audit: morphology-free conductance bound and guard-volume closure

**Scope.** This audits only the proposed guard/isolation candidate. It does not select it as the campaign's leading mechanism. The result is a conditional mathematical bound plus an unclosed physical inventory premise; it is not a cell-level safety certificate or experimental result.

## Finding

The bound

\[
G\leq \sigma_{\max}\,V/d^2
\]

is correct and sharp for a linear, passive, reciprocal Ohmic conductor confined to a slab of thickness \(d\), when its electronic-conductivity support has volume at most \(V\), its conductivity tensor satisfies \(0\preceq\sigma(x)\preceq\sigma_{\max}I\), the two terminals are equipotential parallel planes at \(z=0,d\), and every other boundary is electronically insulating. It does not require identifying the metal morphology or requiring a single connected filament. It does require the whole path and contacts to fit this boundary-value model.

With these hypotheses, the conductance theorem is a useful sufficient test: if a verified upper bound \(V_{\rm max}\) on conducting metal volume obeys

\[
V_{\rm max}<G_{\rm crit}d^2/\sigma_{\max},
\]

then no such metal path can have conductance \(G\geq G_{\rm crit}\). The bound is worst-case sharp: a straight full-conductivity prism of length \(d\) and cross-section \(V/d\) attains equality.

The proposed volume closure does **not** follow from guard alarm charge alone. A valid charge-to-volume bound must include every positive Li-reduction equivalent deposited in the target region, plus any initial and mechanically/chemically supplied metal. In particular, pre-existing metallic lithium can creep or extrude into the separator after electrical isolation with zero new external Faradaic charge. Physical measurements of Li-foil creep under battery-relevant pressure and temperature make this a concrete counterexample class, not a morphology-identification issue.

## Proof and boundary assumptions

Let the separator remainder be \(\Omega=A\times(0,d)\), with terminal planes \(\Gamma_0=A\times\{0\}\) and \(\Gamma_d=A\times\{d\}\). Set terminal voltage difference to one. Let \(\sigma(x)\) be a symmetric positive-semidefinite electronic conductivity tensor, zero off the metal support \(M\), and obeying \(\sigma(x)\preceq\sigma_{\max}I\) on \(M\). For a passive linear Ohmic problem, the unit-voltage conductance equals the minimum dissipated power:

\[
G=\min_{u|_{\Gamma_0}=0,\,u|_{\Gamma_d}=1}
\int_{\Omega}\nabla u\cdot\sigma(x)\nabla u\,dx,
\]

with insulating sides represented by the natural zero-normal-current condition. Use the admissible trial field \(u(x)=z/d\). Then \(|\nabla u|=1/d\), so

\[
G\leq\int_M\nabla u\cdot\sigma\nabla u\,dx
\leq\sigma_{\max}|M|/d^2
\leq\sigma_{\max}V/d^2.
\]

The actual minimizer can only reduce power relative to this trial. No connectedness or shape assumption on \(M\) is needed; disconnected components contribute zero unless they join both terminals. If a bounded electronic background \(\sigma_b I\) fills the entire cross-section in parallel, a safe addition is \(\sigma_b A/d\), giving \(G\leq\sigma_bA/d+\sigma_{\max}V/d^2\).

An ideal full-area guard plane pinned to the anode potential can be added at the near face of the remainder. For a passive resistor/conductivity network, adding this ideal connection cannot decrease two-terminal conductance (Rayleigh monotonicity). Therefore the original anode-to-cathode conductance is at most the conductance of the remainder between the guard plane and cathode. The remainder bound applies only if the plane truly spans the full electronic cross-section, is held at the claimed potential, and there is no edge bypass or alternative electronic path around it.

Important boundary/model qualifications:

- Electrodes must impose the fixed potentials on the stated parallel planes (or on compatible patches there); the other surfaces must be insulating in this electronic problem. A terminal contact that protrudes into the slab or fixes potentials on differently shaped surfaces may invalidate \(u=z/d\) as an admissible trial.
- Tensor anisotropy is covered when the symmetric dissipative tensor has every eigenvalue bounded by \(\sigma_{\max}\). The ordinary Dirichlet proof does not directly cover a nonreciprocal Hall tensor with an antisymmetric part; a separate model is needed.
- The bound is for the electronic metal subproblem. Electrolyte ionic current, solid-electrolyte electronic leakage, interfacial reactions, and mixed transport require additional coupled state equations. Total measured conductance is not bounded by metal volume alone if another parallel conducting channel exists.
- For non-Ohmic response, \(\sigma_{\max}\) must be a certified all-field/all-state constitutive bound and the linear variational formula need not hold. A room-temperature bulk value is not a substitute for a worst-case bound over temperature, phase, pressure, and material condition.

## What follows for Joule heat

For the same stationary Ohmic two-terminal slab, if a known voltage \(U(t)\) is imposed across the exact terminals, then

\[
P_{\rm J}(t)=G U(t)^2
\leq\frac{\sigma_{\max}V}{d^2}U(t)^2,
\qquad
E_{\rm J}\leq\frac{\sigma_{\max}V}{d^2}\int U(t)^2dt.
\]

Thus a verified voltage cap and duration can give an upper bound on modeled Ohmic dissipation. This does not upper-bound electrochemical reaction heat, heat from other parallel branches, stored-energy release, or temperature rise without thermal and source models. At fixed current, the same conductance cap gives

\[
P_{\rm J}=I^2/G\geq I^2d^2/(\sigma_{\max}V),
\]

which is a lower bound; it supplies no upper bound without a lower conductance or source-compliance/energy bound. No HEAT or complete energy-safety conclusion follows from the conductance cap by itself. The proposed decision-control interpretation—rule out a short above a specified \(G_{\rm crit}\)—is the conservative direct consequence.

## Charge-to-volume audit and exact counterexample

For deposition \(\mathrm{Li^+ + e^-\to Li(s)}\), Faraday's law gives the solid-metal addition from charge actually consumed at the target plating interface:

\[
\Delta V_{\rm plated}=\frac{M_{\rm Li}}{F\rho_{\rm Li}}Q_{\rm plated}^{+}.
\]

The charge must count all positive Li-reduction equivalents delivered to the target, regardless of whether electrons came through the external circuit, an internal electronic path, or chemical reduction. A signed aggregate guard current is not this quantity: plating and stripping can cancel in a net-current integral, internal paths can bypass the sensor, and chemical or remote redox sources need not be captured by that measurement.

**Exact counterexample:** metallic Li already present on the anode side of the guard creeps or extrudes through/around the guard into the separator remainder under stack pressure after charger isolation. The external post-isolation charge can be \(Q_{\rm res}=0\), while the metal volume in the target remainder increases. Therefore

\[
V_{\rm target}\leq V_0+Q_{\rm res}M/(F\rho)
\]

is false if \(V_0\) counts only metal initially in the target and \(Q_{\rm res}\) is inferred from external or guard current. It can be repaired by taking \(V_0\) as an upper bound on **all** pre-existing metal that can enter the target over the isolation interval, or by separately bounding incoming advective/creep metal volume and all other source terms. A general accounting form is

\[
V_{\rm target}(t)\leq V_{\rm target}(0)
+\frac{M_{\rm Li}}{F\rho_{\rm Li}}Q_{\rm plated,target}^{+}(0,t)
+V_{\rm metal,in}^{\rm mech}(0,t)
+V_{\rm metal,in}^{\rm other}(0,t),
\]

where the final terms require certified bounds rather than assumptions. Remote stripping must not cancel positive plating elsewhere in \(Q_{\rm plated,target}^{+}\). If volume means a porous deposit envelope instead of actual conducting lithium, its void fraction and electronic connectivity also need treatment.

The physical counterexample is supported by Ding et al.'s primary measurements: Li-foil creep at 30–60 °C and 0.6–3.6 MPa was typically a few \(\mu\mathrm m\,\mathrm h^{-1}\); the paper explicitly reports extrusion around electrolyte/separator and shorting under relevant conditions. This does not prove that a particular proposed guard fails; it shows that a no-inflow assumption must be demonstrated for the actual guard geometry and pressure/temperature range.

The separate mixed-transport concern is also real: Han et al. used operando neutron depth profiling to observe Li deposition inside LLZO and amorphous Li\(_3\)PS\(_4\), and attributed it to high electronic conductivity in these solid electrolytes. That result requires a coupled ionic/electronic/reaction model if such materials or paths are present; it is not captured by the metal-only \(\sigma_{\max}V/d^2\) statement.

## Physical scale check (illustrative, not a certificate)

NIST's evaluated alkali-element resistivity data give solid lithium total resistivity \(9.28\times10^{-8}\ \Omega\,\mathrm m\) at 293 K (nominal conductivity \(1.08\times10^7\ \mathrm{S\,m^{-1}}\)); the compilation gives about ±5% uncertainty in the 60–1500 K band. NIST lists lithium density as 0.534 g cm\(^{-3}\); lithium's standard atomic weight is about 6.94 g mol\(^{-1}\); 2022 CODATA gives \(F=96485.33212\ldots\ \mathrm{C\,mol^{-1}}\), exact under the SI definitions. These numbers are a room-temperature scale, not a certified global \(\sigma_{\max}\) for a cell.

They imply

\[
M/(F\rho)\approx1.347\times10^{-10}\ \mathrm{m^3/C}
=0.1347\ \mathrm{mm^3/C},
\]

or about 0.485 mm\(^3\) per mAh of one-electron Li plating. For \(d=20\ \mu\mathrm m\), a \(1\ \mathrm S\) target short needs, in the ideal straight-filament limit,

\[
V_{\min}=G_{\rm crit}d^2/\sigma_{\max}
\approx3.71\times10^{-17}\ \mathrm m^3
=37.1\ \mu\mathrm m^3,
\]

corresponding to about 19.8 pg of Li or 0.276 \(\mu\)C of ideal Li-plating charge equivalent. A circular straight filament at that threshold has radius about 0.77 \(\mu\)m. At \(d=10\ \mu\)m the charge equivalent scales as \(d^2\) to about 69 nC. These are geometric/stoichiometric scales only: they do not say that 1 S is the actual hazardous threshold, that all lithium reaches this geometry, or that an alarm responds within that coulomb amount. They do show why a claimed short-exclusion certificate needs a measured \(G_{\rm crit}\), specimen-specific \(d\), and a very tight inventory/latency bound.

## Required closure before operational promotion

The theorem is established, but the physical premises needed to apply it are still **UNKNOWN** for a real cell: a worst-case conductivity bound over state and temperature; verified full-area guard/electrode geometry without edge or pore bypass; bounded electronic background and mixed ionic/electronic reaction pathways; initial mobile Li inventory; all-source positive plating charge; pressure-driven incoming Li; post-alarm latency and residual energy; and a validated short threshold \(G_{\rm crit}\). No physical measurements or instrumentation receipts for a particular specimen were provided in this audit.

## Primary sources inspected

- T. C. Chi, “Electrical Resistivity of Alkali Elements,” *Journal of Physical and Chemical Reference Data* 8, 339–438 (1979), NIST-hosted evaluated data and recommended lithium resistivity table, including \(\rho(293\,\mathrm K)=9.28\times10^{-8}\ \Omega\,\mathrm m\): https://srd.nist.gov/jpcrdreprint/1.555598.pdf. NIST's reprint index identifies the work and PDF: https://www.nist.gov/srd/nist-standard-reference-database-journal-physical-and-chemical-reference-data-reprints.
- Shaochen Ding et al., “Compressive creep deformation of lithium foil at varied cell conditions,” *Journal of Power Sources* 488 (2021), 229404, DOI: https://doi.org/10.1016/j.jpowsour.2020.229404. Publisher abstract and article text: https://www.sciencedirect.com/science/article/pii/S0378775320316888.
- Fudong Han et al., “High electronic conductivity as the origin of lithium dendrite formation within solid electrolytes,” *Nature Energy* 4, 187–196 (2019), DOI: https://doi.org/10.1038/s41560-018-0312-z. Publisher article: https://www.nature.com/articles/s41560-018-0312-z.
- NIST lithium density (0.534 g cm\(^{-3}\)): https://physics.nist.gov/cgi-bin/Star/compos.pl?matno=003&mode=text.
- NIST lithium isotopic composition / standard atomic-weight interval: https://pml.nist.gov/cgi-bin/Compositions/stand_alone.pl?ele=Li.
- E. Tiesinga et al., “CODATA recommended values of the fundamental physical constants: 2022,” *Reviews of Modern Physics* 97, 025002 (2025), NIST-hosted article; Faraday constant: https://physics.nist.gov/cuu/pdf/RevModPhys.97.025002.pdf.

**Audit status:** theorem passes conditionally; Q-residual-to-volume implication fails unless all mechanical, chemical, remote, and latency sources are bounded. Most defensible consequence is the conditional \(G<G_{\rm crit}\) exclusion for the stated electronic slab model. No cell certificate, HEAT claim, or campaign-lead selection follows.
