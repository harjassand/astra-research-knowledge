# Temporary clearance topology: graph and hydraulic audit

15 October 2026. Independent internal audit for the manufacturing lead. No Capital
files were edited. The universal graph construction survives after selected edges
are split into lanes. Its proposed manufacturing advantage does not follow: a
much simpler gate schedule defeats the Wheatstone necessity example, the serial
route pays substantial resistance, and chemical erasure can destroy distal
reagent delivery. A true blind branch is a better test of changed steady net
throughflow accessibility, but that statement has a narrow physical model.

**Status:** graph statements proved below by ordinary reasoning and checked on
finite fixtures; hydraulic statements conditional on the stated continuum model;
physical fabrication, orthogonality, residue clearance, superiority and novelty
**UNKNOWN**. The U-turn baffle geometry is established prior art. The hypothesis
remaining to test is a useful sacrificial topology change under a fixed material,
temperature, access and residue contract.

## 1. Exact junction-only obstruction and universal repair

Let the final network be a finite connected undirected graph G with distinct
external fluid ports s,t. Assume one positive-width conduit per final edge, and
that removable junction partitions can only pair incident halfchannels. A single
unbranched clearance path using every conduit exactly once exists precisely when
Odd(G)={s,t}. Pairing changes which halfchannels communicate, not their number.

Concrete obstruction: G={AB,BD,AC,CD,BC}, ports A,D. Its odd vertices are B,C,
while A,D have degree two. No junction-only A-to-D Euler trail exists. This is
also the balanced hydraulic bridge: with identical edge resistances and terminal
pressures 1,0, pB=pC=1/2 and qBC=0. Parity and hydraulic stagnation are different
statements; neither proves material cannot diffuse out.

**Universal repaired construction.** Define T=Odd(G) symmetric-difference {s,t}.
T has even cardinality. Pair its vertices arbitrarily, choose a path for each
pair, and take the symmetric difference D of those path edge sets. Then
Odd(D)=T. Add one extra copy of every edge in D, obtaining a connected multigraph
H with Odd(H)={s,t}. H therefore has an s-to-t Euler trail. Each final edge needs
one lane if outside D and two separated longitudinal lanes if in D.

At every visit to a junction, join the arriving and departing halfchannels and
isolate this pair from every other visit. At s,t one halfchannel is attached to
the external port; repeated internal visits are separately partitioned. The
resulting *physical* stage-one graph is a single interval. H is its quotient
under later junction merging; merely doubling G while leaving common junctions
open does not force flow. Erasing the junction partitions and longitudinal septa
recovers G. A blind leaf uses an out-and-return lane pair with a U-turn where
the septum ends short of the distal cap.

The root's simpler repair, H=2G minus one s-to-t path, is a valid special case.
It can duplicate more edges than necessary. Given fixed per-edge lane geometries,
minimize a positive weight c_e over T-joins. For straight-duct resistance use
c_e=2R_half,e-R_full,e. The minimum weighted T-join gives the least straight-duct
series resistance in this one-or-two-lane class. One can find it by shortest-path
distances on T and minimum-weight perfect matching, then cancel duplicated cycles.
This optimization does not include junction geometry, material volume, or erosion
time, and does not minimize total clearance time by itself.

For Wheatstone, D={AB,CD} is a minimum-cardinality repair. One valid trail is
A-B-D-C-A-B-C-D, with AB and CD each traversed through distinct lanes.

**Manufacturing boundary.** This is a graph construction, not a universal fixed
resolution fabrication theorem. It assumes room for sealed, disjoint junction
passages of positive width, including isolated repeated terminal visits. Given
minimum surviving septum thickness delta_min and minimum useful lane width b_min,
a duplicated final width w requires w >= delta_min+2b_min. A usable final channel
with b_min <= w < delta_min+2b_min is a concrete countermodel to a fixed-resolution
universal implementation. Three-dimensional junction routing also needs explicit
clearance; an abstract pairing does not supply it. Disconnected final cavities
cannot be rescued without temporary connections outside this construction.

## 2. Exactly what terminal pressure and edge gates can reach

Consider a steady incompressible scalar resistor network with every open edge
having a finite positive resistance, Kirchhoff conservation at interior vertices,
and only s,t as pressure terminals. Allow arbitrary deletion of whole edges by
ideal valves, but no new ports, storage, wall slip, or junction splitting.

**Accessibility theorem.** An edge e can have nonzero net flow in at least one
such valve state if and only if e lies on some simple s-to-t path in G.

Proof of necessity: orient every nonzero edge flow from higher to lower pressure.
Potential strictly decreases, so there are no directed cycles. Conservation lets
one extend any flowing edge backwards to s and forwards to t. The monotone
potential prevents vertex repetition, producing a simple s-to-t path containing
e. Detached components or components touching only one terminal have constant
pressure and no flow. For sufficiency, open a simple s-to-t path containing e,
close all other edges, and impose a nonzero pressure difference. Every path edge
then carries the same nonzero flow.

Equivalently, the accessible edges are the edges in blocks on the unique
s-to-t path of the block-cut tree, treating a bridge as a one-edge block. A path
cannot leave this block chain and return through the same articulation without
repeating a vertex. Conversely, any edge in a block on the chain lies on a simple
path between that block's entry and exit vertices. To see the latter fact,
subdivide the edge with a new degree-two vertex; biconnectivity gives two
internally disjoint paths from that vertex to the entry and exit, and their union
contains the subdivided edge. Stitch the block paths along the chain.

Consequences are concrete:

| Final graph | Fixed balanced flow | Any terminal pressure plus edge deletions | What temporary routing adds |
|---|---|---|---|
| Wheatstone | BC has zero flow | Every edge is reachable | A convenience, not new reachability |
| s-v-t with leaf v-cap | Leaf has zero flow | Leaf remains unreachable | An out-and-return lane can force distal traversal |
| s-v-t plus cycle v-b-c-v | Whole attached cycle has zero flow | Whole cycle remains unreachable | Junction pairing alone can put the cycle in series |

The attached-cycle example is a cheaper conditional design than a blind leaf:
G already has Odd(G)={s,t}. A root-junction partition pairing s-to-b and c-to-t
forces the full-width route s-v-b-c-v-t. Only the local root partition needs
erasure, avoiding a long distal septum. With five identical ducts its ideal
route has R=5R0 and V=5V0, so one pore volume costs 25 tau.

These are **net edge flux statements**, not no-exchange theorems. A finite-width
junction is not literally equipotential: two loop mouths can experience different
local pressures. For example, a pressure difference epsilon*DeltaP between the
mouths of a three-duct loop produces q=epsilon*DeltaP/(3R0), rather than zero.
In a blind finite-width cavity, recirculation can exchange material while net
mouth flux stays zero. Wall compliance, liquid compressibility, gas displacement,
diffusioosmosis and diffusiophoresis supply further mechanisms outside the graph
reduction. Primary work explicitly derives zero-net-flux diffusioosmotic
countercirculation in dead-end channels. [Shin et al., PNAS 2016](https://www.pnas.org/doi/10.1073/pnas.1511484112).

The strongest pressure-actuated competitor may also split a junction, rather
than merely delete edges. A deformable roof pressed against a barrier-shaped
floor contact can impose the same pairings and then release them. That lies
outside the theorem's valve class and can reproduce the attached-cycle operation
in a suitable compliant host. It requires acquired seal geometry and actuation
hardware; it cannot be dismissed by the edge-deletion theorem. Pneumatic
elastomeric switching valves are established, although the original demonstrated
devices and cure process are not automatically compatible with this candidate's
particular host and temperature contract. [Unger et al., Science 2000](https://web.mit.edu/thorsen/www/113.pdf).

## 3. Resistance, cross-section, pressure and length costs

Assume constant-viscosity Newtonian liquid, no slip, rigid straight ducts,
constant cross-sections and fully developed laminar flow. Junctions, U-turns,
entrance losses, deformation and material-dependent rheology are additional
obligations. Pressure-driven rectangular duct solutions and their strong shape
dependence are classical. [Mortensen, Okkels and Bruus, PRE 2005](https://backend.orbit.dtu.dk/ws/files/4757131/Asger.pdf).

For a rectangle w>=h the exact resistance used in `hydraulic_audit.py` is

    R(w,h,L) = 12 mu L / [w h^3 F(w/h)],
    F = 1 - (192 h/(pi^5 w)) sum_{n odd>=1} tanh(n pi w/(2h))/n^5.

The script retains 1,000 terms; the omitted correction-factor tail is bounded by
192/[4*pi^5*(1999)^4] when w>=h. A square side a has
R0=28.45415377 mu L/a^4. Splitting its width with a septum delta makes two
rectangles of width (a-delta)/2 and height a. These lanes are **serial** in the
clearance route, despite being physically parallel in the final edge footprint.

| delta/a | Each lane R/R0 | Two serial lanes R/R0 | Remaining primary-core area/A |
|---:|---:|---:|---:|
| 0 | 4.917823 | 9.835647 | 1 |
| 0.05 | 5.610095 | 11.220189 | 0.95 |
| 0.10 | 6.455533 | 12.911066 | 0.90 |

For any cross-section of area A, the torsion/Poiseuille conductance is at most
A^2/(8*pi*mu*L). This is the classical equal-area disk optimum, in the
normalization where -Laplacian(u)=1. [Huang et al., section 5](https://arxiv.org/html/2502.09485v1).
Thus m serial lanes with areas A_j and sum A_j<=A obey

    sum R_j >= 8 pi mu L sum A_j^(-2)
            >= 8 pi mu L m^3/A^2 = m^3 R_circle(A).

The last step is Jensen's inequality. A finite septum reducing total lane area
to A-A_septum worsens the bound by [A/(A-A_septum)]^2. **This is relative to an
equal-area circular duct, not an m^3 penalty relative to every original shape.**
For a very wide shallow rectangle, splitting its width into two still-wide
lanes makes 2R_half/R_full tend to 4. Splitting its height instead makes that
ratio tend to 16. Shape and septum orientation must be retained in comparisons.

For duplicate set D, neglecting junctions,

    R_route = sum_{e notin D} R_full,e + sum_{e in D} 2R_half,e,
    V_primary = sum A_e L_e - sum_{e in D} A_septum,e L_e,
    Q = DeltaP/R_route,       T_PV = V_primary R_route/DeltaP.

The route length is sum L_e + sum_{e in D} L_e. A desired flow Q requires the
full DeltaP=Q R_route; a pressure cap limits Q directly. Hydraulic pump work for
N displaced primary pore volumes is N*DeltaP*V_primary, before pump efficiency,
cooling, chelation or actuation. Thin-wall deflection and seal leakage can limit
pressure long before the host fails. In a blind loop the cross-septum pressure
difference is largest near the mouth and can approach its entire allocated
pressure drop, not merely the small pressure difference over one wall thickness.

## 4. Strong Wheatstone gate counterexample

Let every final edge have resistance R0 and volume V0, and define
tau=R0*V0/DeltaP. The minimum square-lane Euler repair duplicates AB,CD:

    R_E/R0 = 3+4(R_half/R0),
    V_E/V0 = 5-2 delta/a.

An explicit equally informed comparator places small temporary gates at AB and
CD, near readily exposed junction faces. Close both and flush the full-width
path A-C-B-D. In a one-dimensional equal-viscosity plug model q=DeltaP/(3R0).
At six tau, the fresh-fluid front has traversed AC and BC. Open the gates. The
final outer paths each have q=DeltaP/(2R0); four further tau displace their two
edge volumes. BC is already clean and becomes stagnant. The total is **10 tau**,
with six V0 of clean feed. This is a feasible schedule, not a claim of global
optimality over all pressure or valve programs.

| delta/a | Euler ideal plug clock/tau | Explicit gate plug clock/tau | Ratio |
|---:|---:|---:|---:|
| 0 | 113.356469 | 10 | 11.335647 |
| 0.05 | 124.657852 | 10 | 12.465785 |
| 0.10 | 138.346231 | 10 | 13.834623 |

This rejects necessity and a hydraulic time advantage on Wheatstone. It does
not show physical Pareto dominance: at delta=0 the gate schedule consumes six
V0 versus five V0, hence 20% more hydraulic pump work at the same pressure, plus
gate actuation/erasure overhead. EDTA dissolution times and residue tails remain
unmeasured for both architectures. Gates occupy primary-core volume too; their
small-volume idealization must be checked. A prior intermediate 11-tau volume
accounting was corrected before this report because support from AB can
recontaminate BD; the correction is retained in `CORRECTIONS.md`.

Local pressure-operated membrane gates, external pinching where feasible, or
small chemically erased gates should all be included. Calcium-alginate valves
chemically erased with EDTA have already been reported; the exact combined
F127/alginate/silicone process is not established by that precedent.
[2016 primary article](https://doi.org/10.1016/j.snb.2016.04.140).

There is also a strong **F127-only thermal gate comparator**: leave AB/CD locally
warm and gelled while cold-liquefying the desired path, then cool/open everything.
This uses the primary support's own reversible phase transition instead of
introducing alginate and EDTA. Local thermogel valves using F127 are established.
[Stoeber, Liepmann and Muller, microTAS 2003](https://www.rsc.org/binaries/loc/2003/volume1/046-161.pdf).
Its adaptation to millimetre channels, host heat transport, attainable pressure
resistance and the exact temperature ceiling remains conditional. It nevertheless
belongs in the matched comparator set, rather than assuming every temporary
valve must introduce a second material.

## 5. Blind-branch opportunity and diffusion/pressure tradeoff

For s-v-t with one identical blind square duct, the repair duplicates only the
blind edge. At delta=0 its loop resistance is 9.835647R0; with the two backbone
ducts R_total=11.835647R0 and total primary volume 3V0. One whole-path pore volume
costs 35.506941 tau. At delta/a=0.05 these become 13.220189R0, 2.95V0 and
38.999558 tau. The stage-one path reaches the cap without adding a final port.

For an isolated intact blind loop, let c=279.865... be twice the square half-lane
coefficient, so R_loop=c mu L/a^4 at zero septum thickness. Then

    T_loop,PV = c mu L^2/(DeltaP a^2),
    U_lane = 2 DeltaP a^2/(c mu L),
    Pe_L = U_lane L/D = 2 DeltaP a^2/(c mu D).

The baseline one-dimensional diffusion model has absorbing mouth c(0,t)=0,
closed distal end c_x(L,t)=0, and uniform initial solute. Direct separation of
variables gives

    M(t)/M(0) = (8/pi^2) sum_{k>=0} (2k+1)^(-2)
               exp[-(2k+1)^2 pi^2 D t/(4L^2)],
    t_1percent = 1.78128799 L^2/D.

This is a valid finite-clearance diffusion countermodel to removal impossibility,
and a useful baseline if its assumptions match. At fixed pressure and
cross-section, both diffusion and loop advection clocks scale as L^2. The gain
is a Péclet-dependent coefficient, not an improved length exponent. Maintaining
a length-independent lane speed instead requires pressure growing with L.
Other network resistance reduces the pressure available to the branch.

An illustrative calculation, **not acquired F127 properties**, uses a=1 mm,
L=10 mm, mu=1 mPa s, DeltaP=10 Pa and delta/a=0.05. It gives a whole-path pore
volume clock of 11.10 s and lane Re=3.60. Pure diffusion to 1% at that L takes
49.5 h if D=10^-9 m^2/s and 20.6 days if D=10^-10 m^2/s. These numbers do not
compare actual residue removal: viscosity, effective diffusivity, wall uptake,
gel dissolution, pressure tolerance and stage-two erasure all need measurement.

Liquid-only pressure strokes scale with the compressive or compliant storage
DeltaV; rigid incompressible graph theory sets this to zero. A bubble, membrane
or cavitation cycle can make it large, and reciprocal flow plus diffusion can
exchange solute. Such mechanisms must be tested as competitors rather than
excluded by changing the graph model. Same-mouth needle/baffle insertion and
extraction are also competitors wherever geometry allows them.

**Current lower-burden fixture supplied by the manufacturing lead:** an 80 mm
centerline loop with 1x1 mm cross-section attached through a 3x3x1 mm root chamber.
A 0.5 mm thick diagonal calcium-alginate wall pairs inlet-to-loop-start and
loop-return-to-outlet. In an assumed 1 mPa s Newtonian liquid the loop alone has
R=2.27633e9 Pa s/m^3 and V=80 microlitres. Allocating 10 Pa to it gives an ideal
one-pore-volume clock of 18.21 s; this excludes mainline/root losses and all
chemistry. A full chamber diagonal has ideal wall volume about 2.12 microlitres,
far less than a long loop septum. Erasing the root wall changes the common
junction connection. A rigid acoustic side-lobe could supply a meaningful host
stiffness constraint, but the specific application need and sub-40 C requirement
have not yet been acquired. In silicone, temporary external junction pinching
remains a particularly strong comparator. The final finite-mouth pressure and
countercirculation caveats remain unchanged.

## 6. Concrete residual and self-erasure countermodels

**A pore-volume clock is not a clearance certificate.** In a circular duct with
fully developed Poiseuille flow, uniform initial miscible support, equal constant
viscosity, a clean inlet step, zero diffusion and no wall adsorption, put
theta=Qt/V. Cross-sectional integration of the parabolic velocity profile gives

    M/M0 = 1-theta               for 0<=theta<=1/2,
           1/(4theta)           for theta>=1/2.

One pore volume leaves 25% of the initial material in this exact model. A 1%
mass endpoint takes 25 pore volumes. This calculation is not a prediction for
F127, but directly defeats the inference from dye arrival or one nominal volume
to support removal. Adsorption, corner films and fragmented septa create further
possible residue; diffusion changes the tail and must be measured.

**Erasure can starve its own distal target.** The blind-channel adversary supplied
the following countermodel, independently checked here algebraically. Equal
lanes have resistance per length r; the eroding septum has distributed
cross-conductance per length g. Let Delta=p_forward-p_return and q be the forward
lane flow. Conservation and Poiseuille relations give

    q'=-g Delta,       Delta'=-2r q,
    kappa=sqrt(2rg),   Delta(0)=DeltaP, Delta(L)=0,
    Delta(x)=DeltaP sinh[kappa(L-x)]/sinh(kappa L),
    q_tip/q_intact = (kappa L)/sinh(kappa L).

At kappa L=5, distal delivery is only 6.74% of the intact value; at 10 it is
0.0908%. Proximal EDTA attack or imperfect initial seals can create shortcuts
that drain reagent before distal septa are dosed. This is an explicit hydraulic
countermodel, not a measured erosion law. Orthogonal chemistry alone does not
preserve the path during erasure. A fill-stop-dwell protocol needs evidence that
the full loop receives sufficient EDTA before routing is lost. Afterwards the
final blind branch has no net throughflow, so residual alginate products require
their own evacuation test. The root-only attached-cycle partition avoids a
long distal erasure target, but still needs full root residue and final geometry
checks.

## 7. Prior-art boundary

The proposed blind-loop geometry is not new by itself. US4800953A already
describes a baffle dividing a one-opening passage into supply and return
conduits, connected at its closed end, with a root barrier forcing the main flow
through them. That particular baffle locks in place; it is not evidence of
chemical erasure. [1989 patent, description and claims 1,6](https://patents.google.com/patent/US4800953A/en).
US20080003325A1 likewise explicitly shows an elongated U-shaped passage in a
blind cooling hole. [2008 patent, detailed embodiment](https://patents.google.com/patent/US20080003325A1/en).

Support-removal difficulty is real, but prior numerical endpoints must be read
literally. Hornik et al. report approximately 40–75% optical clearance for their
particular printed channels, using sonication/NaOH, an 80 C bake and manual
pressure flushing. That is neither complete clearance nor a same-temperature
F127 comparator. [Primary author-hosted article](https://nps.edu/documents/141875175/141876408/Hornik_etal_Micromachines_2022.pdf/a69507eb-7858-9393-450b-7283e6be913a?t=1683062430885).

No chemical-erasure manufacturing novelty follows from the bounded search here.
The narrower combination of sacrificial routing, orthogonal removal, final
geometry, material contract and demonstrated residual advantage remains UNKNOWN.

## 8. Complete operational cost ledger and decisive test

Charge CAD acquisition and graph routing; junction embedding and mold/print
resolution; sacrificial-core and partition preparation; host cure and interfacial
adhesion; cooling/heating the whole embedded core; calibration of viscosity,
diffusivity, swelling, adsorption, seal leakage and pressure tolerance; pump,
lines, valves, pressure sensors and fluid waste; stage-one dilution/displacement;
stage-two chelator delivery, stoichiometric demand and erosion time; debris and
product evacuation after the graph opens; final dimensional and hydraulic
inspection; rejected parts and reset. Actual labor, yield, energy, fabrication
resolution and F127/alginate response are UNKNOWN. Inference energy is UNKNOWN.

The next test should compare three matched geometries: a stagnant Wheatstone
bridge, an attached-cycle junction, and a true blind leaf. Fix final dimensions,
host, temperature ceiling, exterior access, total pressure cap and a predeclared
residual endpoint. Compare ordinary cold flushing; optimized local gate or
junction actuation; the candidate sacrificial routing; and at least a feasible
diffusion/pressure-cycle protocol. Include an intact permanent baffle as a
transport positive control. Measure primary-core mass/volume residual and
partition residual separately, along the entire cap/loop/root, with independent
geometry or destructive confirmation. Record full pressure/flow traces, distal
reagent exposure, wall displacement, shortcuts, chemical consumption, final
conductance, time, waste and failures. Dye breakthrough is insufficient.

Do not promote the graph theorem to a manufacturing result. A useful positive
result would be a measured final cavity meeting its residue and geometry contract
at lower complete cost than the strongest compatible comparator. This audit has
not supplied that result.

## 9. Reproduction and certificate scope

Run from this directory:

    python3 graph_audit.py
    python3 hydraulic_audit.py

`graph_certificate.json` checks all 27,475 connected labelled simple graphs on
2–6 vertices with fixed terminals 0,n-1. For each it compares the simple-path
union with the block-cut criterion and constructs a valid one-or-two-lane Euler
repair. There were zero mismatches. A separate exact rational calculation on all
1,024 graph masks on five vertices unions nonzero-flow witnesses over every edge
deletion state, using 874 source-sink-connected exact solves, again with zero
mismatches. It also preserves the explicit Wheatstone, blind-leaf and attached
cycle witnesses. These finite checks validate the scripts' fixtures, not the
universal proofs or a physical device.

`hydraulic_certificate.json` records the duct coefficients, gate schedule, blind
branch clocks, diffusion series, no-slip residue countermodel, leakage ratios and
explicitly assumed dimensional examples. `CORRECTIONS.md` preserves the gate
timing correction. `SOURCE_NOTES.md` records inspected primary evidence and
access limitations. No laboratory outcomes were generated.
