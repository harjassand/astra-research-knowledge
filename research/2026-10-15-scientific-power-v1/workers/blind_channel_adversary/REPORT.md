# Independent adversary: sacrificial return septum in a final blind channel

15 October 2026. Status: **conditional manufacturing proposal; no laboratory demonstration; novelty of the complete erase-to-merge process UNKNOWN**. This worker edited only its assigned directory. No Capital edits were made.

The strongest result of this audit is an explicit partial-erasure countermodel: small distributed openings in the septum can reduce distal wash to less than 1% of its intact value while maintaining the same root pressure. The return-divider geometry itself is old mold-cooling-baffle practice. The remaining opportunity is a useful, acquired sacrificial-removal schedule that outperforms vacuum cycling and a removable tube under the actual geometry and temperature constraints.

**Adaptive update:** after this audit, the manufacturing lead changed the leading design to a lollipop loop with only a short root partition. The long-septum failure above does not reject that changed geometry. The final section records the new finite-mouth countermodel and remaining gate; retain the original audit as lineage evidence.

## Scope received from the continuing leads

The manufacturing lead's current target is a final 80 mm tortuous blind channel of square 500 micrometre cross section, connected through its one mouth to a main line with two external ports. The host must be rigid, impermeable and nonphotocurable, processed below 40 C, with no extra final holes. During support clearance, a 25 micrometre longitudinal septum makes two 237.5 by 500 micrometre lanes joined at the distal tip. A root partition routes main-line flow down one lane and back through the other. Primary Pluronic F127 is cold-flushed; Ca-alginate septum is subsequently erased by EDTA. The complete materials implementation has not been acquired.

The topology lead is separately calculating a 10 mm long, 1 mm square proof fixture in silicone. That is not the same rigid/impermeable target. All numerical examples below identify which geometry is used. Neither fixture has been physically built here.

The proposed manufacturing acceptance criterion is at most 1% residual primary support plus separator mass, with intact final blind geometry. The denominator and whether mass means dry polymer, hydrated gel or all initial support need specification before testing. Assay the two materials separately: a small initial separator mass can otherwise be entirely retained while passing a pooled percentage threshold. Geometry, local obstruction and end-use performance remain additional observables.

## What the graph obstruction does establish

For a fixed, rigid, impermeable blind branch in steady incompressible flow, with no internal volume sources, conservation gives Q'(x)=0 and the capped-end boundary gives Q(L)=0. Therefore the net section flux Q(x) is zero. The same conclusion holds in a passive resistor graph for a source-free subtree attached at one vertex.

This is a no-net-throughput result, not a no-mass-exchange or no-local-velocity result. It does not apply unchanged to chemical wall slip, two phases, compressibility, time-dependent storage, a tool inserted through the mouth, or a temporary return divider. The continuing leads now state this narrow distinction correctly.

### Exact countermodel 1: diffusion clears soluble material at Q=0

Consider a solute already dissolved at uniform concentration c0 in 0<x<L, with constant D>0, perfectly maintained clean mouth c(0,t)=0, reflecting distal end c_x(L,t)=0 and no adsorption, reaction or velocity. Separation of variables gives

    M(t)/M(0) = (8/pi^2) sum_{n>=0} (2n+1)^(-2)
                 exp[-(2n+1)^2 pi^2 D t/(4L^2)].

Thus clearance is possible despite identically zero volumetric flux. The 1% remaining-mass time is approximately 1.7812879939 L^2/D; higher modes at that time are negligible. This is an exact ideal transport model, not a lower bound for all cleaning methods or a measured F127 dissolution law.

| L | Assumed D (m^2/s) | Time to 1% remaining mass |
|---|---:|---:|
| 10 mm | 1e-9 | 2.06 days |
| 10 mm | 1e-10 | 20.6 days |
| 80 mm | 1e-9 | 132 days |
| 80 mm | 1e-10 | 1,319 days |

These assumed diffusivities are illustrations, not measured material properties. Initial solid dissolution, concentration-dependent diffusion, boundary saturation and binding can make this model inapplicable. For the 80 mm target it refutes impossibility without providing a competitive manufacturing process.

### Exact countermodel 2: zero-net-flux countercirculation

In a slit with half height h, a solute gradient can induce equal wall slip U_s. The Stokes solution with its induced balancing pressure gradient is

    dp/dx = 3 mu U_s/h^2,
    u(y) = (U_s/2)[3(y/h)^2 - 1].

The section average of u is zero, although the walls and centre carry opposite velocities. Cross-sectional concentration variation, particle phoresis and transverse diffusion can then produce species exchange. A uniform species concentration across each section would cancel the integrated advective species flux; countercirculation by itself is not a universal clearance proof.

Shin and colleagues report dead-end-channel experiments and explicitly discuss the balancing diffusioosmotic and pressure-driven profiles. Their channels are about 400 micrometres long, with approximately 10 micrometre height, not the current 80 mm fixture. The experiment establishes the missing physical mechanism, not performance at the target scale. [PNAS, DOI 10.1073/pnas.1511484112](https://doi.org/10.1073/pnas.1511484112).

Kar and colleagues report transient diffusioosmosis extracting otherwise trapped material from dead-end pores, with reported speeds up to 50 micrometres/s. Their 2016 correction adds a funding acknowledgement; it does not correct the transport result. This is source-reported evidence and has not been reproduced here. [Original primary abstract](https://pubmed.ncbi.nlm.nih.gov/25559608/), [publisher correction](https://pubs.acs.org/doi/10.1021/acsnano.6b00965).

### Exact countermodel 3: pressure cycling with storage and mixing

A gas pocket within an impermeable blind cavity provides storage without wall permeation. If its low-pressure volume is fV, isothermal compression from P_low to P_high changes that volume to fV P_low/P_high. Clean liquid enters the same mouth during compression and an equal volume leaves during decompression. Net cycle volume flux is zero.

If liquid is thoroughly mixed before the outward stroke, its solute inventory multiplies each cycle by

    R = (1-f)/(1-f P_low/P_high).

For f=1/2 and P_low/P_high=1/2, R=2/3, so twelve cycles leave 0.7707% of the original solute. This explicitly states the mixing and gas assumptions. In a perfectly reversible unmixed plug, the fresh liquid can simply leave again; this formula then does not apply. Gas-pocket access and mixing in the actual solid-filled labyrinth are unresolved.

Liquid compressibility alone is much weaker. With an illustrative beta=4.5e-10 Pa^-1 and pressure swing 1e5 Pa, the fractional stroke is only beta DeltaP=4.5e-5. Even an ideal fully mixed exchange at that fraction would need about 102,335 cycles for 99% removal. Thus ordinary liquid pressure pulses are not automatically a strong competitor; nucleation and gas volume are the material distinction to measure.

## New explicit failure: partial erasure starves the distal return path

Let both lanes have hydraulic resistance per length r, and let a partially removed septum permit cross-flow per length g Delta(x), where Delta=p1-p2. Define q as outward lane flow. Equal lane geometry and incompressibility give

    q' = -g Delta,    Delta' = -2 r q,    Delta''=2 r g Delta.

With fixed root pressure difference Delta(0)=DeltaP and an ideal distal U-turn Delta(L)=0, put kappa=sqrt(2rg). Then

    q_tip = kappa DeltaP/[2r sinh(kappa L)],
    q_tip/q_intact = (kappa L)/sinh(kappa L),
    q_intact = DeltaP/(2rL).

At kappa L=5, tip flow retains 6.74%; at 10, it retains 0.0908%. The result already assumes fixed root pressure, not just a fixed total-flow pump. At fixed total inlet flow, the ideal model gives q_tip/Q_root=1/cosh(kappa L), a stronger suppression. Proximal leakage is especially damaging when upstream lane resistance is nonzero. A shunt exactly at an ideal pressure-clamped root is a special exception: it can consume unlimited extra flow without reducing a separately maintained distal pressure difference.

There is a concrete partially erased geometry behind the dimensionless example. For the 80 mm target with 25 micrometre divider, use hypothetical 10 micrometre axial-width openings extending over its 500 micrometre height, at 1 mm pitch. Model the 79 interior openings and the intervening lane segments as fully developed Newtonian rectangular resistors, with sealed divider elsewhere, and neglect entrance and turn losses. An exact discrete ladder gives q_tip/q_intact=0.009605. The continuum model gives 0.009570. The water-like viscosity cancels from this ratio when both lanes and openings contain the same Newtonian liquid.

This is a countermodel consistent with partial barrier removal, not a claim that EDTA produces those exact openings. It shows that chemical selectivity does not prove maintained distal perfusion. The decisive material quantity is time-dependent hydraulic cross-conductance, including cracks, detachment and gel permeability.

The lead independently identified another failure: after global separator erasure the distal dissolved products occupy a newly blind volume. Predosing EDTA may solve chelation access while leaving product export unsolved. Distal-first erasure with a retreating U-turn could address both failures only if the remaining septum stays sealed and each exposed segment is rinsed before the loop shortens. No physical realization of that schedule was acquired here.

## Closest prior art and strongest same-access competitors

**Exact geometric precedent.** US4800953A, published 1989, describes a two-port main passage, a one-opening blind side passage, a longitudinal baffle creating supply and return conduits joined at the end wall, and a barrier extending into the main passage to force circulation through the side passage. It explicitly avoids additional drilled access openings. Its spring-arm embodiment locks the baffle in place; the text says it can no longer be removed after positioning. This is geometric precedent, not evidence of sacrificial removal or the current dimensions. [Primary patent description and Fig. 3](https://patents.google.com/patent/US4800953A/en).

**Further baffle precedent.** US20080003325A1 describes the same blind-hole U-turn with numbered inlet lane 23, distal turn 24 and return lane 25. It discusses close-fitting surfaces to prevent bypass. DME's own FAQ describes removal of some commercial plastic baffles and warns against their reuse after removal; it separately identifies side leakage as a reason for sealing wipers. Neither source establishes chemical erase-to-merge clearance. An earlier message from this worker incorrectly associated removability with the 1989 spring-arm patent; that error was corrected directly to all leads. [2008 primary patent](https://patents.google.com/patent/US20080003325A1/en), [manufacturer FAQ](https://www.dme.net/baffles-faqs/).

**Vacuum cycling.** The 1971 patent US3563711A describes pressure reduction to induce boiling of liquid in partially leached casting passages, followed by repressurization, to replace spent leachant. Its disclosed process does not establish the present below-40-C target. [Primary patent](https://patents.google.com/patent/US3563711A/en).

**Acquired experimental comparator.** Ariyarathna's 2021 SHSU thesis studies carbon black in blind capillaries, 1.12 mm inner diameter and approximately 49 mm internal length. It reports 82 +/- 7% removal with 1% SLS solution and fifteen vacuum cycles at room temperature. Abstract/conclusions state approximately 99 +/- 1% at 40 C and twenty-five cycles, but body Table 6 labels fifteen cycles and reports orientation means of 98.3 +/- 0.7% and 98.8 +/- 0.7%. This discrepancy must remain explicit. The balance LOD is 0.21 mg; specimens were dried at 120 C for an hour. This is substantial primary evidence for blind-hole exchange, not proof of at-most-1% residue in an 80 mm/500 micrometre F127 labyrinth or a complete process below 40 C. PDF pages 39-43, 51-52, 63-67 were text-inspected; pages 40 and 64 were visually inspected. [Live university PDF](https://shsu-prod.dotcms.cloud/academics/chemistry/cleanresearch/documents/Ariyarathna,Nethmini_Vacuum-Cavitation-Cleaning.pdf).

**Very close current research lead, limited evidence.** The downloaded official Hilton Head 2026 programme, page 60, lists Kathryn J. Pacheco and Don L. DeVoe, WP-42, on vacuum-cycle nucleation cleaning of high-aspect-ratio blind holes in printed molds. The page was visually inspected. Only the programme was acquired: dimensions, materials, full paper, residue measurements and temperature history are UNKNOWN. It cannot be cited as an achieved matched-target result. [Official programme](https://hh2026.org/files/HiltonHead2026_Program.pdf).

**Removable tube comparator.** Preplace a flexible tube to the distal tip, send cold rinse down its bore and return liquid through the surrounding final lumen; then retract the tube. This avoids separator dissolution products and naturally removes material from the distal end first. It uses the same final ports. For an illustrative 100 micrometre inner diameter, 200 micrometre outer diameter and 80 mm length, ideal water flow of 0.1 microlitre/s needs 3.26 kPa across the tube alone. The tube occupies 12.6% of the 500 micrometre square cross section. Five final-channel volumes take 1,000 s, which is not a 99%-clearance guarantee. Return, bend and connector losses, cold F127 viscosity, tube kinking, pull force and extraction damage must be measured. The actual bend radii and access route were not supplied, so this incumbent has not been excluded by the word "tortuous".

For comparison, the ideal intact two-lane geometry at the same rate has 190 s loop residence, about 40.9 Pa straight-lane pressure drop at assumed viscosity 1 mPa s, and Pe_L about 67,368 at assumed D=1e-9 m^2/s. This is a real potential hydraulic advantage over the thin tube. It excludes U-turn/root/manifold losses and support rheology. One loop volume does not remove near-wall films or certify residue. The narrow-lane diffusion scale is about 56 s at that D and about 564 s at D=1e-10. Higher Pe does not eliminate the final separator-export gate.

No exact sacrificial U-turn divider later erased into a final blind channel was located in the bounded primary-source search. That is not novelty clearance. The old baffle geometry, sacrificial templating and established vacuum cleaning substantially narrow any remaining claim.

## Decisive experiment and scientific decision

The actionable decision is whether the sacrificial-divider process creates the required final blind geometry more reliably or with lower total cost than the best same-port incumbent. A dye reaching the tip is not the endpoint.

1. Fix one actual host formulation, cure history, labyrinth coordinates/bend radii, pressure envelope, temperature cap, and end-use acceptance specification. First qualify the material triad on short coupons: core flush without separator loss; separator erasure without host swelling/damage; calibrated separate assays of both polymer inventories. Failure here stops the long-device experiment.
2. Build identical final-geometry specimens using the proposed septum, a preplaced removable tube when mechanically possible, and unpartitioned sacrificial core cleaned by vacuum cycling. Give all arms the same compatible chemistry, allowed access, pressure/temperature envelope and cleanliness endpoint. Include static-rinse and standard pressure-rinse controls, plus a positive open-through-channel control. Vacuum cycling may be combined with the septum if it helps; attribute that extra operation and cost explicitly.
3. During separator removal, acquire local tip flow and root flow simultaneously, rather than infer tip flow from outlet discharge. In a transparent proxy, use particle tracking or micro-PIV at the distal turn and image cross-septum leaks. Test pressure-controlled and flow-controlled operation. Fit r and g from independently measured geometry/flow, then compare the observed tip-flow decline with the ladder prediction. The rigid target still needs its own verification; a silicone proxy does not transfer impermeability or adhesion premises.
4. At predefined removal times, destructively section replicate target specimens at the mouth, middle and distal end. Extract and quantify F127, alginate and relevant chelator/reaction residues separately using validated assays with spike recovery, host blanks and detection limits well below each local acceptance amount. Use geometry imaging or sections to detect residual walls, cracks and added leaks. Maintain an inlet/outlet/retained-material ledger; declare unexplained inventory UNKNOWN.
5. For an acoustic-cavity endpoint, measure complex input impedance and the actual resonance/loss across the required band after drying below 40 C. The simple air quarter-wave estimate for 80 mm is roughly 1.07 kHz at an assumed sound speed of 343 m/s. Bends, root loading, residue and viscothermal losses mean that number is not a measured useful device result. Compare an independently fabricated clean reference and the best manufacturable conventional geometry. A planar labyrinth that can be milled and capped must compete unless a concrete end-use constraint prohibits its seam.

Pre-register the residual-mass denominator, local obstruction limit, acceptable impedance error, total processing time and useful cost advantage before running. A source-matched vacuum positive control is needed to distinguish an ineffective incumbent implementation from a meaningful septum advantage. Failure of the target material triad, distal flow collapse before residue export, or no advantage at the matched endpoint rejects the current operation. A new externally useful capability requires the end-use result as well as clean channels.

## Complete cost and status ledger

Count template and divider fabrication/registration, host preparation/cure, tube insertion or septum anchoring, cooling/heating, clean reagent acquisition and consumption, pump/vacuum energy, fixtures, pressure and temperature calibration, online flow imaging, assay standards and spike recovery, destructive specimens, all rinses, solvent exchange, below-40-C drying, waste collection, machine cleaning/reset, failures and rework, and throughput/yield. Keep manufacturing time separate from measurement/verification time, while reporting both. Present laboratory energy and inference energy as UNKNOWN without telemetry. Reusable hardware amortization must use the same batch and reuse assumptions in all arms.

**Internally derived and checked:** ideal diffusion series; zero-net-flux slip counterflow; gas-storage compartment model; leaky-divider continuum and discrete ladder; ideal rectangular-lane and circular-tube hydraulics. Script: `check_transport.py`; saved numbers: `TRANSPORT_RESULTS.json`. These are model checks, not laboratory observations.

**Source-reported/acquired:** old baffle geometry; older pressure-cycling disclosure; blind-capillary vacuum experiments with the stated limitations; a close 2026 conference programme entry. Download receipts and hashes are in `sources/SOURCE_RECEIPTS.json`; they establish source-file integrity only.

**Unresolved:** complete material implementation; controlled separator erosion order; product export; target-scale incumbent performance; final useful acoustic or other scientific endpoint; full cost advantage; novelty of the complete process. The current operation is not demonstrated.

## Adaptive addendum: lollipop loop with local root partition

The manufacturing lead subsequently proposed an off-backbone loop, total stated length 80 mm and cross section 1 by 1 mm, attached to a 3 by 3 by 1 mm root chamber. A temporary approximately 0.5 mm alginate diagonal root partition sends main flow through the full-width loop. Only that local partition is erased; its products can leave directly via the main line. This changes the final geometry from a blind degree-one stub to a loop lobe attached at one root chamber. It substantially improves the material prospect: it removes the long thin separator and does not generate its dissolved products at a far blind tip. The original distributed-septum countermodel therefore cannot be applied as a rejection of this mutation.

**New exact countermodel to graph-level absolute inaccessibility.** A real root chamber has finite size. Two loop mouths can see different pressures even if the graph representation collapses their chamber to one vertex. Consider an explicit placement with the two mouths at the ends of a main-channel segment having resistance Rc, while the loop between the mouths has resistance Rl. Without a divider the two resistances are in parallel:

    Q_loop/Q_total = Rc/(Rc+Rl) > 0,
    Q_loop = DeltaP_mouths/Rl.

An intact partition ideally removes the main-channel shunt and makes Q_loop=Q_total. Using fully developed rectangular resistance for a 3 mm long, 3 by 1 mm root segment and an 80 mm long, 1 by 1 mm loop at assumed viscosity 1 mPa s gives Rc=1.5191e7 Pa s/m^3, Rl=2.2763e9 Pa s/m^3 and unpartitioned loop flow fraction 0.006629. A plain unpartitioned device would require about 150.85 times as much total flow to obtain the same loop flow in this ideal example. That is a potentially valuable finite pumping/reagent advantage; it is not zero-versus-nonzero physical access. For fixed pressure across these exact mouth nodes, the loop flow itself is unchanged by the parallel shunt; supplying the extra bypass flow is the resource cost. Real port resistances, pump limitations and chamber entrance flows change the calculation.

This is an explicit possible mouth placement, not target-specific CFD. If the actual mouths are in a symmetry plane that enforces equal pressure, this particular pressure-driven comparator vanishes. The leads need exact mouth coordinates, an actual root pressure field and local loop-flow measurement to determine which case applies. Zero mouth separation cannot be assumed merely from graph adjacency.

**New incumbents.** A removable root routing insert, a mechanically switched local valve, and a preplaced flexible tube deserve comparison. The operation now resembles temporary bypass blocking rather than a new long-channel access primitive. The rigid final host does not by itself forbid a removable temporary insert. Conversely, an external pinch valve is not automatically a fair comparator if there is no permitted deformable segment at the root; acquire its actual connection geometry before claiming dominance. A gate left permanently in the finished device is not equivalent if it fails the acoustic or other final-geometry requirement.

Sacrificial fluidic gating itself is established: US9295990B2 describes a sacrificial member within a microfluidic channel that dissolves on controlled fluid contact to allow subsequent flow, with a gas pocket used to delay contact. It does not establish the present support-removal use, material triad or root geometry. [Primary patent](https://patents.google.com/patent/US9295990B2/en). Bazargan and Stoeber's 2008 paper describes creating and removing a temporary gel wall between co-streaming fluids through ionic control of a thermoresponsive polymer; its demonstrated purpose is controlled particle transfer, not the target manufacturing process. [Primary publisher abstract, DOI 10.1103/PhysRevE.78.066303](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.78.066303).

**Changed scientific endpoint.** If 80 mm means total loop circumference and both loop ends couple to one compact root pressure symmetrically, the root-excited symmetric acoustic mode is equivalent to two blind arms of length 40 mm. Its elementary quarter-wave proxy is about c/(2 L_loop), or 2.14 kHz at assumed c=343 m/s. The earlier 1.07 kHz blind-stub estimate does not transfer. Antisymmetric ring modes may be dark at the root. Exact mouth coupling, loading and losses still require measured complex impedance; this is linear ideal wave reasoning, not a measured resonator result.

The decisive modified experiment is a matched final loop, first with an intact removable/inert root partition and then without it, measuring local loop flow under the same external pressure, maximum total flow, temperature and reagent budgets. Add the chemically erased partition only after that gain and final impedance tolerance are established. Assay root residues and inspect whether erosion leaves a pocket or film in the loop mouth. Complete host/cure compatibility, final geometry, local erosion products, matched incumbent comparison and cost remain unacquired. The mutation is a more plausible fabrication candidate, not an established new capability.
