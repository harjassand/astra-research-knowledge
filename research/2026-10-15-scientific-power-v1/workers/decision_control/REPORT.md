# Direct control without hidden-mechanism identification: guard, inventory, and conductance

15 October 2026, Australia/Brisbane. Worker: decision_control. **NEW OPERATIONAL CAPABILITY: NOT_ACHIEVED.** No physical cell was built, no laboratory experiment was run, and no new foundational conductivity theorem is claimed.

The best precise interface found is a separator interception alarm combined with a physically bounded downstream metal inventory. It would certify that no electronic short with conductance at least a declared threshold can form, without reconstructing a dendrite's morphology or identifying its growth mechanism. The exact mathematical ingredient is valid and sharp but classical. The missing physical operation is not more statistical fitting: it is closure of every source of metal entering the protected gap, including stored metal transported mechanically after electrical isolation. Published physical evidence makes that omission consequential.

## Physical obstruction and proposed operation

Terminal voltage, charger current, and surface temperature do not measure all internal metallic lithium or stored chemical/mechanical energy. An early warning can therefore arrive before a short while still failing to make that short preventable. Stopping external charge is not equivalent to stopping all internal transport or exothermic chemistry.

The attempted device has an anode, a separator, a third-terminal sensing/interception layer inside the separator, and a cathode. A genuine interception layer would meet every hazardous electronic path before it reaches the cathode. At the alarm, an isolator stops charge delivery. The controller then issues an explicit decision: **no modeled electronic short of conductance at least Gcrit can occur during the specified isolation horizon**, provided the certified upper inventory bound passes the inequality below. A failed bound returns **UNKNOWN**, not a prediction that a short will occur.

The initially considered actively biased stripping layer was not retained as a safety mechanism. A positive measured strip charge can coexist with local plating in another region; a single signed guard-current integral does not measure the positive deposition current in every local branch. A porous conductive layer also does not form a literal geometrical cutset, because a fine or insulated filament may cross a pore without sufficient electronic contact. A dense mixed conductor would change ionic transport and can itself change lithium nucleation; that material interface has not been acquired. The final mathematical certificate does not assume that an aggregate stripping current heals the dangerous branch.

This is distinct from a dissipation-inference operation: the intended output is a forward conductance exclusion after intervention, not a hidden entropy-production lower bound.

## Exact conditional result and proof

Let Ω be the slab A×(0,d). The two electronic terminals are equipotential subsets of the planes z=0 and z=d; all remaining boundaries are electronically insulating. An arbitrary metal region M inside Ω has volume at most V. Electronic conduction is linear, passive, reciprocal, and Ohmic. Its symmetric conductivity tensor obeys 0≤σ(x)≤σmax I on M and vanishes elsewhere. Ionic/faradaic branches are outside this electronic subproblem.

At unit voltage, electronic conductance equals the minimum Dirichlet energy:

    G = inf ∫Ω ∇u·σ(x)∇u dx,

where u takes values 0 and 1 on the two terminal planes. The trial potential u=z/d is admissible, so

    G ≤ ∫M σmax/d² dx ≤ σmax V/d².                    (1)

The statement covers many branches, tortuous shapes, disconnected metal, and anisotropic conductivity bounded by σmax. A straight prism of conductivity σmax, length d, and cross section V/d attains equality. Thus no universally smaller coefficient is available using only the slab gap, volume, and conductivity bound in this continuum class. This sharpness statement is a mathematical lower bound on morphology-independent certification, not a lower bound on every physical battery controller or estimator.

For a full anode–cathode path, adding a virtual ideal plane at the guard location pinned to the anode potential can only increase conductance by Rayleigh monotonicity. Equation (1) applied to the remaining slab therefore upper-bounds the original path conductance, provided every path actually crosses that slab and no edge, tab, or other electronic bypass exists. The plane used in this comparison is mathematical; it does not establish that a fabricated porous sensing layer detects every crossing.

If the separator has known electronic background σb throughout area A, an immediately safe looser version is

    G ≤ σb A/d + σmax V/d².

When the metal replaces background rather than being an additive conductivity, the sharper correction is σb A/d+(σmax−σb)V/d². Electronic leakage, ionic transport, interfacial reactions, nonlinear conduction, Hall response, and protruding contacts require the appropriate different model; they cannot silently be assigned to zero background.

This mathematical ingredient is **established-method specialization**. Milton's primary 2011 paper explicitly reviews the affine-potential upper bound e0·σD e0≤〈σ〉e0·e0 in section 3, equation (3.4). Equation (1) is the finite-slab zero-background case. The proof above was independently derived here, but it is not historically new. [Milton, full paper](https://arxiv.org/pdf/1105.0954).

## What the inventory must actually bound

For one-electron lithium reduction, charge Q consumed at a plating interface creates solid-metal volume QM/(Fρ). A safe all-source accounting over a declared horizon is

    Vprotected(t) ≤ Vinitial
                   + M/(Fρmin) Qpositive_reduction,all_sources(0,t)
                   + Vmetal,in,mechanical(0,t)
                   + Vmetal,in,other(0,t).             (2)

Here Vinitial includes all conducting metal initially in the protected remainder. The positive reduction charge counts local plating without cancellation by stripping elsewhere, and includes electrons from the guard, internal electronic leakage, chemical reductants, and external wiring. The last terms include imported pre-existing metal and any other uncounted source. Alternatively, one can conservatively include all pre-existing metal that can enter the remainder in the initial inventory allowance. That often destroys the useful numerical margin.

If independently certified bounds give Vprotected≤Vmax and

    Vmax < (Gcrit−Gbackground)d²/σmax,

then G<Gcrit. In the unusually restrictive case of no initial metal or metal inflow and only one fully monitored source of reduction equivalents, the charge reserve is

    Qmax < (Fρmin/M) (Gcrit−Gbackground)d²/σmax.         (3)

Equation (3) is not a general statement about charger charge. None of the missing all-source terms is paid for by naming it an oracle or a calibration parameter.

Under an independently known voltage cap Umax, the stationary Ohmic model also gives P≤Umax²G. It supplies no whole-cell temperature or thermal-runaway guarantee. At current control, P=I²/G and an upper bound on G gives a lower bound on P. Even a small total modeled power may be concentrated locally; chemical energy and post-isolation internal energy are separate hazards.

## Exact countermodels and physical alternatives

1. **Zero-charge metallic inflow.** Pre-existing lithium below the guard is displaced into the protected gap by pressure after charger isolation. External and guard charge can both be zero while protected metal volume increases. A volume 10^-17 m³ rearranged into a straight 10 μm path has conductance 125/116 S under the explicitly nominal conductivity used in the script. Thus the simplified implication V≤Vinitial+QM/(Fρ) is false when it omits mechanical transport. This countermodel does not claim every real guard permits that exact shape.

2. **Net-current cancellation.** One region plates ΔV while another strips an equal lithium amount. The signed total current integrates to zero; the protected region gains ΔV. This defeats a certificate based on net guard current even when the sensor itself is exact. An internal electrochemical redistribution can be powered by stored free energy, so no external charging current is required. The artifact encodes the equal and opposite charge equivalents exactly.

3. **Hidden initial downstream metal.** A disconnected metal inclusion or a remote nucleus can exist beyond the sensing layer before the first connected front arrives. Contact by the observed front can connect an already extensive conductor after arbitrarily little new deposited volume. A no-downstream-metal premise cannot be inferred from the front alarm alone. This is an idealized switch/contact countermodel; no specimen-specific electrical equivalence experiment was performed.

4. **Late energetic appendage.** For any finite observation/intervention record, a model class permitting an initially uncoupled stored-energy module that couples only after that record contains two systems with identical records and different later hazards. This is the ordinary causal indistinguishability argument: every adaptive choice is the same up to coupling, so an algorithm cannot infer the hidden energy bound from those observations. It is not an impossibility theorem for a physically restricted, acquired device class. A bound on coupling, inventory, or release rate must come from an actual additional operation.

These countermodels have concrete source support. Ding et al. measured lithium-foil creep at battery-relevant temperature and pressure and describe extrusion around an electrolyte/separator as a shorting route. Their reported rates are not assumed to be universal instantaneous speed bounds for our guard. [Primary creep study](https://doi.org/10.1016/j.jpowsour.2020.229404).

Doux et al. provide a more direct zero-new-charge physical example in a specified substrate: their Li|Li6PS5Cl|Li symmetric cell at 75 MPa shorted before plating/stripping began. The approximately 82%-dense electrolyte had connected pores into which lithium could creep. They also report no zero-current short over prolonged durations at 25 MPa, where cycling was needed. This is a counterexample to universal charge-only closure, not evidence of rapid zero-current failure at ordinary pressure in our proposed guard. [Primary preprint, PDF pages 5–6](https://arxiv.org/pdf/1910.02118).

Han et al. used neutron depth profiling to observe lithium accumulating inside bulk LLZO and Li3PS4. At 25°C they report shorting attributed to thin dendrites with total lithium below the measurement's detection limit. This directly challenges the assumption that all metal starts as one observable connected front. The raw data were not acquired or reanalyzed here. [Primary paper, author PDF](https://bpb-us-e1.wpmucdn.com/blog.umd.edu/dist/7/477/files/2019/01/Han_et_al-2019-Nature_Energy-wp3t4s.pdf).

## Reproducible exact calculation and scale

`verify_guard_bound.py` uses standard-library rational arithmetic. It solves 300 finite resistor-network fixtures with exact Gaussian elimination, verifies G≤trial energy≤σmax V, and checks an equality-attaining straight rod. Those checks passed normally and under Python -O. The random seed is 20261015. These are finite mathematical fixtures, not a dendrite simulation or experimental battery result. The continuum proof does not depend on their success.

The same script computes explicitly nominal room-temperature scales using bulk lithium density 534 kg/m³ and electrical resistivity 9.28×10^-8 Ωm from the NIST-hosted evaluated compilation, nominal molar mass 0.00694 kg/mol, and exact SI F=NAe. They are not specimen-wide certified bounds over temperature, pressure, phase, purity, and nanostructure. The standard atomic-weight interval also reflects composition variability. [NIST evaluated data](https://srd.nist.gov/jpcrdreprint/1.555598.pdf), [CIAAW lithium](https://ciaaw.org/lithium.htm), [CODATA constants](https://physics.nist.gov/cuu/pdf/all.pdf).

| Remaining gap d | Gcrit | Metal volume at sharp bound | Li charge equivalent | Time at 1 A if all source charge can enter the remainder |
|---|---:|---:|---:|---:|
| 10 μm | 1 S | 9.28 μm³ | 68.896 nC | 68.896 ns |
| 20 μm | 1 S | 37.12 μm³ | 275.582 nC | 275.582 ns |
| 100 μm | 1 S | 928 μm³ | 6.890 μC | 6.890 μs |
| 1 mm | 1 S | 92,800 μm³ | 0.689 mC | 0.689 ms |

At d=10 μm and Gcrit=1 S, the straight circular rod radius is about 0.5435 μm and mass about 4.956 pg. This sharp continuum example is not atom-scale. At 1 μA instead of 1 A, the same nominal charge allowance lasts 68.9 ms; a small, source-limited laboratory device is therefore a different regime from ampere-scale cell charging. Lower Gcrit tightens all the volume and charge budgets linearly. The hazard threshold itself is UNKNOWN for a real proposed specimen.

These numbers demonstrate a tight sufficient-certificate budget. Failing that sufficient certificate does not prove that a real cell fails, that all Li takes the worst-case geometry, or that every preventive design is impossible. A physically enforced small local current fraction could improve the residual budget, but that fraction cannot be assumed from the total current or from a mean deposition model.

## Strongest equally informed competitors and novelty status

The strongest competitor receives the same internal layer, calibration, current/voltage access, initial inventory information, isolation latency, and material bounds. It can apply equation (1), use stronger established composite bounds, directly measure electronic leakage, and implement conventional cell segmentation or local current limitation. No information or computation advantage over that competitor has been shown.

Early interception sensing itself has direct primary prior art: Wu et al. demonstrated a third-terminal bifunctional separator in 2014; Wang et al. report a distributed reference electrode and spatially informed charging protocol in 2025. These precedents defeat novelty claims for merely adding a reference mesh or separator alarm. [Wu et al., author PDF](https://web.stanford.edu/group/cui_group/papers/Hui_Cui_NCOMMS_2014.pdf), [distributed reference electrode study](https://doi.org/10.1016/j.cej.2025.162990).

The stronger active comparator is Gonzalez et al.'s 2021 iongate: a 300 nm PPy:PDA membrane on a conductive separator terminal reversibly changes ion transport. The reported added areal ionic resistance changes from 255 to 2443 Ωcm²; full-cell shutoff after externally shorting the iongate to lithium takes tens of seconds in the demonstrated discharge trial. Most full-switching measurements used 30-minute potential holds. Its thickness/pinhole tradeoff is explicit. This is physically demonstrated active control, but its roughly tenfold resistance change is not complete instantaneous isolation or an all-path damage guarantee. [Primary author PDF, pages 3–6](https://liugroup.ucsd.edu/wp-content/uploads/2021/07/adfm.202102198.pdf).

Their 2020 Janus separator is a particularly close passive preventive competitor: a cathode-facing partially conducting layer intercepts dendrites, controls short resistance, and gradually drains charge. The primary report describes mitigation in lithium-metal pouch-cell charging-abuse trials, including lower short current and temperature rise than the single-layer control. Those source-reported outcomes must remain scoped to their tested devices; they do not close our universal inventory or hazard premises. They do rule out presenting interception plus bounded discharge as a new idea. [Primary Janus study](https://doi.org/10.1002/adma.201906836).

Reversible electrochemical dendrite healing in a nanoscale LLZO device is also reported prior work. It is a meaningful comparator, but its demonstration does not certify every branch's retreat in an unknown bulk battery. [Lu et al., primary preprint](https://arxiv.org/abs/2010.01624).

The retained synthesis—guard alarm plus all-source inventory cap plus a sharp conductance exclusion—is an unbuilt conditional interface. Its combination may be a useful design specification, but historical novelty, practical advantage, and physical implementation are all **UNKNOWN**. The mathematical cap is established prior art; it should not be promoted by renaming it.

## Complete resource and premise ledger

| Item | What would actually be needed | Current evidence/cost |
|---|---|---|
| Acquisition | Specimen-specific gap, background electronic leakage, initial mobile metal inventory, all-source inflow bounds, pressure and temperature range | UNKNOWN; no acquired specimen |
| Fabrication | Cutset layer with edge sealing, qualified ionic transport, third terminal, isolator and local source limitation | UNKNOWN; no fabricated device |
| Preparation | Bounded initial metal in and able to enter protected remainder; controlled state of charge, pressure, prior cycling and defects | UNKNOWN; no perfect reset assigned |
| Calibration | Worst-case σmax and ρmin; alarm misses and SEI contact; isolation latency, residual capacitive/inductive/chemical sources | UNKNOWN |
| Readout | Sufficient bandwidth and charge resolution over every relevant electronic source; separately constrained mechanical/chemical transport | UNKNOWN; net current is insufficient |
| Control energy | Bias, sensing, switching, stripping if attempted, pressure release, losses and external energy storage | UNKNOWN; no energy telemetry |
| Reset and endurance | Restore the guard, electrolyte, metal distribution and geometry after an alarm; repeatability and false alarms | UNKNOWN; no repeated device test |
| Comparison | Same geometry/inventory/instrumentation, optimized conventional control, guard-only and isolation-only arms | Not executed |
| Computation | Exact proof and 300 small rational resistor fixtures; nominal charge arithmetic | Executed; script/results saved; no measured inference energy/token usage |
| Data | Source-reported experiments versus independent measurements | No laboratory outcomes or public raw-data reanalysis by this worker |

## Decisive next operation, if allocated

The narrow next experiment is a transparent, low-energy, micrometre-gap electrochemical cell with a third-terminal guard and a separately bounded current source. Preload a known amount of metal on the source side, interrupt external current at the alarm, and vary stack pressure while imaging downstream metal. Log all current ports and pressure/displacement. The falsifier is a downstream volume increase exceeding the complete electrical allowance after isolation. A companion deliberately preloaded remote-inclusion specimen tests whether the alarm constrains initial downstream inventory. A chemically reducing control and an SEI-insulated contact control test the other bypasses.

Before a positive cell-level claim, the experiment must acquire the actual all-source inequality (2), show the guard does not create a new plating route, and validate a consequential Gcrit/thermal threshold. Compare with the same guard and isolator using an established controller and the same sensor bandwidth; compare pressure-limiting and local-current-limiting architectures at identical usable energy, gap, throughput, and total cost. This is a proposed discriminating experiment, not a reported result or a reason to continue conditional simulation indefinitely.

## Artifacts and review scope

- `verify_guard_bound.py`: exact finite-network checker and nominal scale computation.
- `GUARD_BOUND_RESULTS.json`: exact rational values, nominal grid, cancellation and mechanical-inflow countermodels.
- `NIST_resistivity.pdf` and `.txt`: acquired authoritative evaluated property source, with original source caveats retained.
- `iongate_2021.pdf` and `.txt`: acquired primary active-intervention comparator, with switching-time and leakage qualifications retained.
- `SOURCE_RECEIPTS.json`: URLs, access scope and relevant sections.
- Independent internal audit: `../guard_bound_audit/REPORT.md`; physical adversary collaboration independently identified mechanical metal inflow and local cancellation issues. Same-team audit is not external review or formal verification.

The useful outcome is a sharp, reproducible conditional design rule and a concrete reason an early alarm is not yet preventive controllability. A new reliably obtainable scientific or technological operation remains **NOT_ACHIEVED**.
