# Most consequential physical opening inspected: no spanning Li path, rather than no dendrites

Status: constructive target and failed indispensable geometric construction; not a new battery design, material certificate, or safety claim.

## Proposed newly possible operation

A lithium-metal cell that tolerates bulk metal nucleation and finite dendritic growth while guaranteeing that no electronic path reaches the opposite electrode during its specified capacity/cycle window. If achieved at useful areal capacity, low stack load, thin separator and high current, this would remove a major obstacle to high-energy fast-charging metal batteries. The claim would need to concern full-cell energy and lifetime, not a single high-current pulse.

## Existing positive mechanisms that must not be rediscovered

- Ye and Li, Nature 593 (2021), https://doi.org/10.1038/s41586-021-03486-3: stable/less-stable/stable electrolyte sandwich, localized constrained decomposition, proposed expansion-screw/anchoring mechanism. Reported 10,000 cycles at 20C and 8.6 mA/cm^2 are at a small cathode loading: the source's 631.1 Wh/kg statement is explicitly cathode-material-level, not complete-cell energy.
- Di et al. (2025), https://pmc.ncbi.nlm.nih.gov/articles/PMC12366673/: graded particle-size guidance plus a less Li-stable layer producing self-limiting deposition. It combines growth-generated pressure, deposition pressure, and reaction-product expansion. This is already sequential guiding AND limiting, not only surface stabilization.
- Zhang et al., Nature 652 (2026), https://doi.org/10.1038/s41586-026-10415-9: in-plane microscopy of roughly 150-micrometre LLZTO at about 50 mV; hydrostatic Li stress around 600 MPa in the model; transverse engineered voids/Vickers cracks redirect growth. This is a stronger same-material comparator than unmodified galvanostatic plating.
- Cui et al. (2026), DOI https://doi.org/10.1038/s41586-026-10734-x: a reported bulk-nucleation/biaxial-stress result. Full primary text was inaccessible through the Nature identity redirect in this investigation. Do NOT infer thickness, capacity, duration, cycling or full-cell efficiency from its abstract-level 100 mA/cm^2 statement.

## Hardest construction personally attempted: a stress foliation that cannot be crossed

Let z be electrode-normal. In an elementary pressurized-crack model, biaxial compression is Sigma=-P diag(1,1,0). For a crack-plane unit normal n making angle theta with z, the opening traction supplied by internal Li pressure p is

    t_n = p - P sin^2(theta).

Griffith propagation additionally requires sufficient crack length, but for every fixed theta with sin^2(theta)<p/P, the opening traction is positive. For a long enough flaw, the usual stress-intensity criterion can therefore permit propagation. The admissible crack plane then has a tangent direction with nonzero z component sin(theta).

Thus finite biaxial compression does NOT create an exact invariant horizontal foliation. If the continuum model imposes no positive minimum filament cross-section, a connecting path of length ell can have arbitrarily small metal volume A ell by taking A small. A fixed lithium inventory alone cannot certify absence of a short. Atomic minimum dimensions remove the literal zero-volume limit but do not normally make total battery charge a strong restriction on one narrow conducting filament.

For a single straight crack with lateral excursion at most W and electrode separation L, a tilt theta>=atan(L/W) suffices geometrically. To rule out even all such straight crack planes using only t_n<=0 would require

    P >= p [1+(W/L)^2].

This is not a universal fracture theorem: orientation-dependent toughness, finite crack lengths, curved/branching cracks, confinement, plasticity and chemical reaction matter. It is a counterexample to treating finite steering stress as a topological no-crossing guarantee. Curvature and bulk nucleation make the full task harder, not easier.

For an illustrative geometry W=1 cm, L=150 micrometres, the factor is about 4,445. This rejects the simplistic geometric certificate before any detailed phase-field numerics. It does not contradict observed finite-time transverse steering.

## What a genuine sufficient construction would need

A separating guard region with an actual positive lower bound on the complete incremental free energy of Li insertion/propagation under the maximum allowed local electrochemical drive; or a quantitatively validated stochastic crossing law with its correlation, area, cycle and defect population costs paid. A perfectly impenetrable membrane or an exactly horizontal growth law cannot be assumed.

A pressure-only scale illustrates the burden: using lithium molar volume Vm approximately 13e-6 m^3/mol, the work F eta per mole corresponds to p approximately F eta/Vm, roughly 0.37 GPa at 50 mV and 0.74 GPa at 100 mV. These are illustrative mechanical scales, not actual stability thresholds: partial molar volumes, electrolyte stress, reaction energies, pressure relaxation and crack surface work must be included. Biaxial residual film stress is not hydrostatic confinement.

The existing self-limiting interlayers already target this thermodynamic/constriction mechanism. No newly acquired material law or fabrication establishes a stronger guard here. Therefore no positive no-spanning construction or superior operating point has been earned. Preserve this as selection evidence, not as a claimed invention.

## Later acquired source correction

The colleague acquired openly visible Cui2026 paper captions/text, separate from the blocked Nature full text. The strongest claimed stress protocol must not be conflated with its fastest current step: about330MPa biaxial compression,5MPa axial load,approximately1mm-thick LLZO; the100mA/cm^2 ramp point uses0.1mAh/cm^2 (=3.6s), while the separate2000-cycle10mA/cm^2 protocol uses1mAh/cm^2 (=6min per half-cycle). The paper reportedly acknowledges nonhorizontal dendrites, partial surface connectivity, increasing electronic contribution and eventual percolation risk. The colleague's source ledger records provenance and exact limitations. These facts weaken—not strengthen—the case for treating steering as guaranteed no-short operation.

The2022 primary constrained-ensemble paper explicitly says local K_eff can collapse when new cracks form and notes a positive feedback between decomposition and crack formation. Its demonstrated electrolytes are120+400(+240)micrometre layers at2mg/cm^2 cathode loading. The scalar effective-modulus/stability premise is therefore not a uniform acquired guard over all damaged states. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC9088294/ .
