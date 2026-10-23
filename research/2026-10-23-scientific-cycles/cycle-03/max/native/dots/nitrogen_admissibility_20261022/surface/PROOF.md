# Surface retention is not identified by passivity, detailed balance, and reset

## Decision

Do not admit a quantitative NO+NO2-retention guarantee for the actual zirconia bed from the existing constraints. Do not infer fatal actual loss or physical exclusion either. The missing material response is a kinetic/coverage observable, not an additional atom or heat balance.

The decisive statement is constructive: a finite, regenerated catalyst can destroy useful NOx by returning nitrogen to N2 while dissipating the chemical free energy stored in NO. Detailed balance, atom conservation, passivity, finite site count, and complete surface reset permit that route. They also permit an arbitrarily slow version of the same route. Therefore they cannot, by themselves, certify a useful finite-time retention threshold such as 95%.

This is stronger than merely finding no source: it identifies a null direction of thermodynamic identification, the common forward/reverse kinetic scale, and constructs energy-coupled completions on opposite sides of a retention decision. It is weaker than an admitted uncertainty range for real zirconia. None of the illustrative kinetic values is a measured or otherwise material-qualified zirconia value.

## 1. What reset does and does not constrain

Write surface state as finite site inventories z. If b_N is its nitrogen content, a true periodic/reset surface obeys b_N·[z(t1)-z(t0)] = 0. Thus storage alone cannot account for a persistent cycle-to-cycle fixed-N deficit. This excludes treating indefinitely accumulating adsorbed nitrogen as a catalytic loss sink.

It does not imply that the time integral of a catalytic turnover is zero. For a network S_s r = dz/dt, reset constrains S_s ∫r dt = 0. Any nonzero cycle vector v with S_s v = 0 can still have nonzero gas stoichiometry S_g v. Site count bounds instantaneous occupancy, not the number of repetitions of such a cycle. A rate/encounter/time bound or a known absence of such a cycle is needed to turn site capacity into a turnover bound.

The useful product here is NO+NO2, not all nitrogen-bearing species. NO↔NO2 preserves the count. NOx→N2 destroys fixed nitrogen; NOx→N2O can destroy useful-product count without destroying all fixed nitrogen. The six-species source does not contain N2O, so it cannot exclude that alternative. None of these distinctions is removed by atom conservation.

At complete gas/solid/header/surface reset, global nitrogen conservation still holds, but both output NOx and output N2 are allowed. Its mass-conservation upper bound is trivial compared with a small allowed product-loss fraction. In a general reacting bed, an incident-NOx collision integral is not even a complete bound on surface-mediated changes because radical recombination can alter subsequent homogeneous production/destruction.

## 2. Minimal regenerated mechanism and detailed balance

Consider the reversible effective surface event

2 NO(g) + C ⇌ N2(g) + O2(g) + C.

C is a finite population of catalytic centers. It has exactly the same chemical state before and after each event. No solid atom, reductant, stored oxygen vacancy, external reagent, current, or surface nitrogen reservoir is consumed. Its gas stoichiometric vector, in the pinned order N2, O2, N, O, NO, NO2, is

ν = (1, 1, 0, 0, −2, 0).

Both N and O atom vectors annihilate ν. The center count and its chemical energy cancel identically. C can be understood as a thermodynamically reversible effective scattering/catalytic channel with no resolved stable occupied intermediate; it is not asserted to be a known elementary zirconia event.

For positive ideal-gas activities a_i = p_i/p°, the gas standard thermochemistry supplies

K_d(T) = exp[−(g°_N2 + g°_O2 − 2g°_NO)/(RT)].

Let F = a_NO² and B = a_N2 a_O2/K_d. Any positive common mobility L produces rates r+ = L F and r− = L B. Their ratio is exactly K_d a_NO²/(a_N2 a_O2), not an arbitrarily chosen irreversible sink. At equilibrium F=B both rates match. The reaction affinity is A = RT ln(F/B), and the entropy production is

(r+−r−) A/T = R L (F−B) ln(F/B) ≥ 0.

Multiplying L by any positive factor preserves every statement above and preserves all equilibrium thermodynamics. The small-rate completion is strictly reversible, not an assumption of zero/inert surface kinetics.

### Finite-intermediate version, if a resolved adsorbate is required

The atom- and site-balanced reversible steps

1. NO + 2* ⇌ N* + O*
2. 2N* ⇌ N2 + 2*
3. 2O* ⇌ O2 + 2*

sum to the same gas reaction when step 1 occurs twice per occurrence of steps 2 and 3. At a fixed gas state with total decomposition affinity A>0, choose fixed positive coverages and adsorbate standard free energies such that all three step affinities are A/4. This is possible: set μ_N*−μ_* = μ_N2/2+A/8 and μ_O*−μ_* = μ_O2/2+A/8 at that state. Then 2A_1+A_2+A_3=A, and every step is dissipative. Detailed-balanced forward/reverse constants can be given positive common scales such that the net rates obey r_1=2J, r_2=r_3=J. The coverages and finite surface inventory then remain exactly stationary while the catalyst turns over.

This fixed-state construction demonstrates why stable intermediates do not supply a reset-capacity bound. It is not the numerical mechanism below, and its standard free energies must not be silently retuned as gas conditions change. It establishes no zirconia-specific adsorbate free energy or rate.

## 3. A collision-capped common mobility, not an unlimited fictitious rate

The numerical effective channel additionally respects conservative gas-collision caps. Per geometric area, define

J* = [p°/(RT)] sqrt[RT/(2π M_max)],
D = 1 + a_NO + (a_N2+a_O2)/K_d,
r+ = λ J* F/(2D),
r− = λ J* B/(2D), with 0<λ≤1.

M_max is the largest molecular mass among the six pinned species, so its one-sided thermal speed is no larger than the speed of any reactant. The positive common denominator does not change detailed balance. On nonnegative states,

2r+ ≤ λ J_NO,
r− ≤ (λ/2) J_N2,
r− ≤ (λ/2) J_O2,

where J_i = c_i sqrt[RT/(2π M_i)] is the Maxwellian one-sided collision flux. Thus the adverse example is not created by allowing an infinite number of reactions per incident gas molecule. These are a deliberately specified admissible continuum channel and encounter cap, not an identified real-material reaction law.

The hypothetical center inventory is 10⁻⁵ mol per square meter of geometric area, identical in all completions. It cancels from the effective rate once the per-center collision normalization is defined. Any positive finite center count would serve the logic, with a corresponding per-center turnover frequency; this numerical value is not a measurement or capacity estimate of zirconia.

## 4. Coupled finite-energy counterexample

The supplied t=11 s snapshot's final gas cell, index 27, has gas T=1047.01993 K, solid T=778.14578 K, and p=101336.13 Pa. It provides a positive six-species gas inventory. Use its original void volume 0.003333333 m³ per m² bed cross section, geometric grain area 3.1496063 m²/m², and finite solid heat capacity C_s=20,833.333 J m⁻² K⁻¹.

The numerical test is NOT a rerun of that cell in the bed. It deliberately creates a small isolated common-temperature contact problem. Its initial gas composition is the snapshot's; its initial common T=778.157966 K is the unique finite-capacity adiabatic thermalization value from the source gas/solid energies. This initialization raises entropy by 0.0465291 J m⁻² K⁻¹. It is an energy-matched initial-condition construction, not a simulated two-temperature catalytic thermalization history. In particular, actual catalysis is not claimed to wait while that source cell equilibrates. Constant volume means the resulting pressure is lower than the source pressure. No original flow, residence-time distribution, particle conduction history, or heater performance is predicted.

During the one-second test, all six gas inventories and the common temperature evolve together. Existing seven-reaction homogeneous chemistry is retained. The added channel supplies νr_s. Define

U(n,T) = Σ_i n_i u_i(T) + C_s T,
u_i(T) = h_i(T)−RT,
(C_s + Σ_i n_i c_v,i) dT/dt = −Σ_i u_i dn_i/dt.

The pinned NASA formation energies are included in u_i. There is no external heat, work, or uncounted reaction heat during the exposure. Reaction chemical energy becomes finite gas/solid sensible energy. The gas entropy plus C_s ln T increases. Surface C is chemically reset at all times, not only at the endpoint.

The resulting retained NO+NO2 fractions are:

- λ=10⁻¹²: 0.9999999972. Negligible direct destruction, although both directions remain present.
- λ=10⁻⁶: 0.997192693. About 0.281% loss.
- λ=10⁻⁴: 0.780121345. About 21.99% loss.
- λ=10⁻²: 0.0376904924. About 96.23% loss.

These four values are an explicit family of mathematical completions. They are NOT a zirconia uncertainty distribution, measured confidence interval, material admissibility envelope, sensitivity fit to the bed, or a claim that the actual material achieves any member.

For the high-turnover completion, direct surface NO destruction is 0.00102956149 mol/m², from 0.00106988602 mol/m² initial NOx. The finite catalyst executes 16.3443 net turnovers per site and has zero site-inventory change. Total temperature rises only 0.00451515 K, because the finite solid absorbs the approximately 94 J/m² chemical energy release. The total contact entropy rises 0.0774170 J m⁻² K⁻¹. The largest forward NO-collision conversion fraction is 1.61518×10⁻⁴, much smaller than one.

### Reset and heat bookkeeping

After the parcel has been withdrawn, restoring the solid from its final temperature to its contact-start temperature requires removal of 94.0656 J/m² in the adverse completion, versus only about 0.000055 J/m² in the slow completion. Rejecting this heat to a 300 K environment has nonnegative total entropy production, 0.192670 J m⁻² K⁻¹ in the adverse case. No heat-engine work credit is claimed. The chemical surface state is already identical. Hence finite solid thermal reset does not reverse the NO destruction or demand a compensating supply of fixed nitrogen.

This is a repeatable contact-and-solid-reset boundary argument, not a complete plant cycle. The source gas/solid two-temperature state, original bed fields, gas filling/withdrawal, pumps/valves, gas quench to 300 K, capture and finished product are not simulated or costed. Gas is withdrawn as the altered output stream, not reset by secretly regenerating NO. Restoring the solid to the source snapshot's lower solid temperature would additionally reject the common initial thermalization heat, identical for all completions. The comparison's incremental reset heat remains approximately 94 J/m².

The point is not that a whole zirconia regenerator has been proved to attain the adverse output. It is that entropy and finite/reset surface inventories cannot supply the missing favorable retention theorem. A downstream dissipative catalytic contact can defeat such a theorem without spending a consumable surface inventory.

## 5. What is and is not held identical

Identical among the completions: six-species standard thermochemistry; seven-reaction homogeneous mechanism; initial gas composition; initial common temperature; finite gas volume; finite solid heat capacity; geometric area; finite center count and center state; site and atom conservation; equilibrium constant; collision cap; exposure time; energy equation; and reset boundary.

Different: only the common forward/reverse kinetic coefficient of an otherwise identical effective catalytic channel. This represents missing kinetic information. Standard free energies do not determine activation barriers or their prefactors.

For a specified exact microscopic material and history there is one physical response, not four freely selectable ones. To argue that a particular λ belongs to real dense/stabilized zirconia requires independently applicable evidence. Deliberately changing composition, defects, catalyst loading, porosity or surface preparation would be changing the material; it would not certify a property of the already specified material. This work makes neither move. It establishes non-identifiability from the supplied macroscopic constraints, not the joint physical realizability of every constructed member on the actual zirconia. Neither constructed rate law has been fitted to AVCO's unquantified qualitative observation or demonstrated to reproduce that apparatus. Thus “identical known information” here means the explicitly enumerated thermodynamic, geometric, inventory and initial-state constraints, not a claim of empirical agreement with all unknown or incompletely specified material observations.

## 6. The honest admission boundary

Thermodynamics can constrain feasible directions, equilibria, heat and entropy, and coarse inventory limits. With a specified encounter law it can join kinetic collision upper bounds. It cannot fix the kinetic scale or prove that an unqualified surface leaves a chosen amount of metastable NO intact over a finite cycle. A very weak maximum-destruction bound is not the needed high-retention guarantee.

The required additional observable remains a species-resolved, geometric-area net NOx loss/formation rate or integrated response on the actual material under applicable gas and surface temperatures, oxygen activity, loading, cycling and reset. It must distinguish N2, N2O, NO/NO2 interconversion and temporary adsorption, and include uncertainties sufficient for the claimed retained-product margin. The prior frozen collision exposure gives a screening scale, not that observable.

Consequently: park numerical admission of the inert-surface complete-cycle construction until this load-bearing response is qualified or an alternative robust construction removes the dependence. Do not extend an unqualified bed trajectory merely to improve its quotient. Do not replace the missing response with a favorable free parameter. Do not infer physical exclusion from its absence.

## 7. Reproduction and numerical checks

From /workspace/scratch/57d8dd795b13:

python nitrogen_admissibility_20261022/surface/coupled_counterexample.py
python nitrogen_admissibility_20261022/surface/validate_counterexample.py

The first script writes coupled_counterexample.json and four small full histories. The second uses a tighter Radau solve versus the BDF calculation and independently inverts conserved total energy for every accepted state. Maximum retention disagreement is 3.39×10⁻¹⁰ absolute. Maximum element residual is below 5×10⁻¹⁶ mol atoms/m²; common-temperature disagreement with the energy root is below 9.6×10⁻¹² K. The BDF run has maximum absolute energy residual 3.8×10⁻⁸ J/m² on a 1.62×10⁷ J/m² stored energy, not a global solution-error bound. Small signed trace species reach roughly −4.2×10⁻²¹ mol/m² in the independent solve and are reported, not hidden. No positivity theorem is asserted.

The source-bound homogeneous reactions and the added surface channel have nonnegative computed entropy-production rates on resolved positive states. No generic web search, long trajectory, whole-bed parameter fit, material-rate assignment, paid resource or hardware action was performed. The test and cross-check take about 1.3 and 9.4 seconds respectively on this environment. A minor validation-report list-to-array error was corrected before the successful check; it did not affect the differential equations or primary results.
