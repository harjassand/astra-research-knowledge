# Independent heat-recovery bound and finite-rate challenge

## Scope and conclusion

Rapid product-preserving cooling and heat recuperation are physically compatible. Useful recovery must satisfy local temperature matching while the gas traverses its NO-destruction window sufficiently quickly. A freely assigned recovery fraction does not establish that these requirements can be met simultaneously.

This note derives an optimistic heat-allocation bound, independently verifies its discrete optimization formula, and supplies a separate nonreacting sensible-enthalpy calculation. It is not another chemical-kinetics simulation, a validated recuperator design, or a full wall-plug fertilizer process model. No other agent's kinetics grid was rerun.

## 1. Conserved basis and process energy balance

Normalize to a conserved mass or specified amount of fresh feed, rather than a mole of hot gas. Dissociation changes total molar flow, so hot NO mole fraction is not automatically retained moles of NO per mole of fresh feed.

Use these quantities on the same feed basis:

- Hh: reactor-exit total enthalpy relative to ambient fresh feed, including sensible, chemical formation and dissociation enthalpy.
- Qr: heat actually transferred back into the reactor's incoming feed.
- L: reactor thermal losses not already included in Hh.
- B: external heating required by downstream segments whose total enthalpy increases.
- eta_p and eta_B: electrical-to-thermal conversion efficiencies, kept symbolic unless measured.
- Wa: auxiliary electrical energy, including compression, oxygen preparation, pumping and cooling.
- Wx: actual recovered/exported work, not exported heat.
- yr: retained moles of NO, or explicitly stated NOx-N, per feed basis.

For an electrically heated front end with these boundaries:

E_retained = [(Hh - Qr + L)/eta_p + B/eta_B + Wa - Wx] / yr.

Exported heat is a separate product. It is not both a credit against electrical consumption and a source of feed preheating. If energy is valued economically, state the displaced use and value separately.

Let A be total heat released along downstream segments. On a consistent enthalpy basis, Hcold = Hh + B - A. Consequently the ideal thermal input Hh - Qr + B equals Hcold + (A - Qr). Chemical recombination energy is already included in the actual segment enthalpy drops and must not be added again.

NO formation enthalpy at ambient conditions is approximately 90.29 kJ/mol (NIST), but this alone is not a universal minimum electrical work: a complete reversible-work calculation must specify chemical potentials, mixing, separation, product state and possible heat exchanges. Do not substitute standard formation enthalpy for the full process boundary.

For fertilizer, use:

E_nitrate = total net process electricity / moles of captured nitrate-N.

NO/NOx concentration is not captured nitrate production. If an overall capture yield xi is defined consistently, E_retained/xi plus appropriately normalized downstream duties is a useful rearrangement. A single-pass absorber fraction is not automatically the overall capture yield in a recycle process. Count recycle reheating, purge losses, oxidation/absorption, concentration and neutralization where applicable.

## 2. Staged quench, then sensible recuperation

Suppose a rapid nonrecuperative quench takes hot gas from Th to Tq. The subsequent countercurrent recuperator can transfer no more than either its available hot-stream heat or the capacity of its cold feed:

Qr <= min[available post-quench effluent heat,
          h_feed(Tq - delta_T_min) - h_feed(T0)].

This endpoint expression is necessary but can be weaker than internal-pinch constraints, derived below. It becomes a favorable sensible-recuperation screen if the cold feed is assumed nonreacting. If cold-side chemistry occurs, its actual composition-dependent enthalpy must replace the nonreacting feed expression.

The Th-to-Tq quench duty cannot also be credited to the downstream recuperator if it was rejected externally. If a direct-mixing quench retains that enthalpy in a larger combined stream, model the extra stream, dilution, pressure drop and cold-feed capacity explicitly instead of treating the mixing as heat recovery.

The independent NIST-Shomate calculation in this folder gives sensible enthalpy increments for 79/21 N2/O2, relative to 298.15 K:

| Feed temperature | kJ/mol feed |
|---|---:|
| 2100 K | 60.41793960547889 |
| 2000 K | 56.77490098666668 |
| 1800 K | 49.544496489742656 |
| 1500 K | 38.86573512578124 |
| 3100 K | 97.59442158582993 |

Using gross energy 2.7 MJ/mol NO and the explicitly illustrative yr=0.045 mol NO/mol feed, the zero-pinch, lossless 2100 K preheat credit is 1.3426208801217533 MJ/mol NO. The residual is 1.3573791198782468 MJ/mol NO. Reaching 1.5 MJ/mol requires 89.37742722213436% of that maximum credit at perfect retention and electrical-to-thermal efficiency. Reaching 1.0 would require 126.6180218980237%, outside this particular sensible-recuperation screen.

These are not parent-solver predictions. The assumed yr is not an exact conversion from hot mole fraction, and cold feed is nonreacting. The separate calculation using an independently rounded gross value of 120 kJ/mol feed produces 1.3240457865449136 MJ/mol NO; the difference exposes the rounding/basis sensitivity and is not a second physical result. Use the parent solver's consistent enthalpy and retained yield instead of combining rounded literature numbers.

## 3. Discrete trajectory-wise pinch bound

Let a prescribed hot trajectory have boundaries i=0,...,N, ordered from hot inlet to cold outlet. All Hi values use the same conserved feed basis.

For segment i define:

ai = max(Hi - H(i+1), 0),
bi = max(H(i+1) - Hi, 0).

ai is available heat; bi is required heating. Negative heat segments are not discarded from the energy balance: B=sum bi. This formulation assumes any bi is supplied externally; a bidirectional internally coupled heat network requires a different explicit model.

Let qi be recovered heat from segment i, so 0 <= qi <= ai. A cold stream flows countercurrently. At boundary i it has accumulated:

Di = sum(qj for j >= i), with DN=0.

For an invertible cold-feed enthalpy function, the local pinch requirement is:

Di <= ci = h_feed(Ti - delta_T_min) - h_feed(T0).

All ci in the active exchange domain must be nonnegative. Trim or bypass hot portions below T0+delta_T_min. Artificially allowing negative ci would make even zero recovery infeasible. Clamping to zero is only a shorthand for excluding unsuitable exchange portions, not for forcing heat transfer across a temperature cross.

The objective is Q= D0. The exact optimum of this fractional heat-allocation linear program is:

Q* = min over i=0,...,N of [sum(aj for j<i) + ci],

where cN=0.

### Proof by cuts

At any boundary i, no more than sum(j<i) aj can be recovered upstream of that boundary. Recovery downstream cannot exceed ci. Thus each bracketed expression is an upper bound.

### Achievability proof

Let Mi be the maximum feasible recovery from segment i onward, with MN=0. By continuous curtailment, the achievable downstream recoveries fill an interval [0,M(i+1)]. Adding a continuously selectable qi in [0,ai] yields all values in [0,ai+M(i+1)]. Imposing the local cap gives:

Mi = min(ci, ai + M(i+1)).

Unrolling this recurrence yields the cut expression. This proof does not require caps to be monotone, only nonnegative in the defined active domain.

### Continuous version and discretization caveat

For a continuous trajectory parameter s from hot inlet 0 to cold end L, let da(s) be its nonnegative recoverable heat-release measure and c(s) the cold-feed enthalpy capacity imposed by local pinch. With the same ideal continuously curtailable heat-allocation assumptions:

Q* = inf over s of [integral from 0 to s of da + c(s)], with c(L)=0.

A discrete set of sampled boundaries can miss an interior pinch, especially when reaction enthalpy or heat capacity changes rapidly. Its optimum is therefore optimistic relative to the continuous problem unless interior constraints are checked or convergence/refinement is established. Prescribed hot trajectories do not themselves prove that a physical recuperator can produce them.

### Executed independent verification

The exact source of the already-run inline checker is saved as lp_check.py. It used seed 182052, generated 1000 cases with 1-30 segments, and compared the formula against scipy.optimize.linprog using HiGHS. Every optimization succeeded and every discrepancy was below 1e-8. The maximum absolute discrepancy was 5.684341886080802e-14.

The additional illustrative case uses a=[50,30,20] and c=[80,15,8]. Its maximum recovery is 65, while checking only total available heat and hot-end capacity would falsely permit min(100,80)=80. The retained solver solution was q=[50,15,0]. Other optima can exist.

Original command wall time was 1.444439171 s according to tools.exec_command. CPU time and maximum RSS were not metered. The receipt explicitly records that limitation. Original random-case inputs and per-case optimizer outputs were not saved during execution; the exact source and seed reproduce them. This persistence step did not rerun the checker or any chemical grid.

## 4. Finite-rate challenge to independently selected recovery and quenching

Consider an ideal balanced constant-heat-capacity counterflow recuperator as a diagnostic, not a reactive design model. The hot and cold temperature profiles have the same slope when viewed along the hot-flow direction, hence their local difference is constant. With effectiveness epsilon:

DeltaT_local = (1-epsilon)(Th-T0).

Let Uv be overall conductance per hot-flow volume and kappa=Uv/(rho*cp). A hot gas element obeys:

-dTh/dt = kappa*DeltaT_local.

Therefore the time required to traverse a critical interval Th-to-Tq is:

tau_critical = (Th-Tq)/[kappa*(1-epsilon)*(Th-T0)].

At finite conductance density, epsilon approaching one sends this traversal time to infinity. Increasing epsilon from 0.90 to 0.99 while holding quench speed fixed requires ten times kappa in this balanced constant-property diagnostic. Thus high recovery and rapid cooling cannot be freely specified as independent knobs.

For reactive gas the temperature balance must include chemical heating. With r=-dT/dt and q_chemical positive for exothermic chemical heating:

Uv_required = [rho*cp*r + q_chemical]/(Tgas-Tcold).

The numerator can be obtained from the actual trajectory's enthalpy-removal rate. If the numerator is negative, the segment requires heating rather than ordinary heat rejection. Use actual state-dependent properties and composition; the constant-property diagnostic is not a replacement for that calculation.

If a simple first-order loss diagnostic is adopted, retained fraction S=exp[-integral k_loss(T,composition,p) dt]. The allowed residence time and transfer density are therefore coupled. Gross destruction rates plus formation need a full kinetic balance; a fitted net-loss coefficient is not a universal reaction rate. A nominal freeze temperature such as 2100 K is residence-time- and pressure-dependent, not a discontinuous chemistry switch.

A realizable design still needs finite area/conductance, allowable local wall temperature and heat flux, acceptable pressure drop, suitable materials, and checks on wall/surface chemistry. The fractional LP proves only an optimistic heat-allocation bound allowing recovered and rejected heat to be selected independently along the path.

## 5. Ordinary physical alternatives and boundary traps

### Direct mixing

A mixing quench can be fast without a solid heat-transfer surface in the hottest region. It retains heat in a larger mixed stream while diluting NO. It does not transfer that heat into the reactor inlet by itself. Account for extra gas flow, recycle/jet pressure, capture burden and combined-stream enthalpy.

For the restricted equal-heat-capacity, chemically frozen illustration, the cold/hot mass-flow ratio required to mix from Th to Tq is (Th-Tq)/(Tq-Tc). That expression is not an adequate reactive-plasma design calculation because dissociation/recombination enthalpy and unequal capacities matter.

### Expansion/nozzle

An adiabatic nozzle converts static enthalpy into kinetic energy. Lower static temperature is not an equal loss of stagnation enthalpy, and subsequent shocks/diffusion can reheat the gas. Heat or work recovery credit requires the full downstream path, pressure supply and actual recovery equipment. Do not count a nozzle as free refrigeration plus free recuperation.

### Pressure and enrichment

Ideal isothermal compression requires at least R*T0*ln(p/p0) per mole compressed. At 298.15 K, 1-to-10 bar corresponds to 5.708009502430058 kJ/mol feed, before inefficiency; normalization requires the actual pressurized-process retained yield. Net pressure-work accounting must also include any genuine expansion work recovery.

For the isolated reaction N2+O2 <=> 2NO, total stoichiometric mole number is unchanged. Pressure benefits involve the wider dissociation/recombination network and kinetic pathways rather than a simple pressure shift of that isolated reaction.

Oxygen-enriched results need oxygen-preparation energy and the same product boundary before comparison with air-fed processes. No assumed compressor or oxygen-separation efficiency is introduced here.

## 6. Evidence and strongest ordinary comparator

The appropriate comparator is optimized thermal NO formation plus realistic product-preserving quench and heat integration, not an inefficient unoptimized plasma torch. Rapid quench followed by slower feed-heat recovery is already proposed in the main contemporary source, so that architecture alone does not establish novelty.

1. Albrechts et al., Energy Conversion and Management 349 (2026), 120842. The paper's thermal/flow model is validated against reactor experiments. It proposes near-uniform optimal-temperature operation, rapid quench, then slower heat recovery; it does not demonstrate a recuperator delivering that combined performance. https://medialibrary.uantwerpen.be/files/7783/685e44c1-b0c3-424d-a9d5-ab9a2e2d8755.pdf

2. Vikash et al., Chemical Engineering Journal 543 (2026), 178575. The authors' university-hosted abstract describes experimentally validated CFD and split-feed impinging-jet quenching that improves retained production. This supports thermal-trajectory engineering, not validated high-grade recuperation. https://research.chalmers.se/en/publication/552709 ; DOI https://doi.org/10.1016/j.cej.2026.178575

3. Zinchenko, Serbin and Chernyak, Ukrainian Journal of Physics 67 (2022), 44-53. A mixing-quench section followed by a heat exchanger was experimentally studied; reported heat flux agreement supports the transport treatment. Its CFD is chemically unreactive, so it is not a full validation of retained-NO chemistry. https://ujp.bitp.kiev.ua/index.php/ujp/article/download/2021064/2437/21209

4. Shen et al., 2025. A thermal/vibrational atmospheric model uses an artificially enhanced wall-cooling factor and finds temperature-dependent effects of cooling. The modeled special vibrational behavior near the energy-optimal operating point does not outperform its thermal perfect-quench limit. Model quench factors are not demonstrated recuperator performance. https://arxiv.org/html/2504.20952v1

5. McKinney et al., Nitrogen 6(3) (2025), 51. The pilot reports recovery of approximately 60% of plasma energy into water heated to 60 degrees C, alongside nitric-acid production. This demonstrates useful low-temperature cogeneration, not an equal reduction of plasma electricity. https://www.mdpi.com/2504-3129/6/3/51

For context only, heat supplied entirely at 60 degrees C against a 25 degrees C environment has maximum reversible heat-to-work fraction 1-298.15/333.15 = 0.10505778177997904. A finite tank that warms to that final temperature has less available work than treating all heat as supplied at the final temperature. This exergy illustration does not replace the local pinch/finite-rate arguments above.

Primary property inputs and exact source URLs are preserved in nist_shomate.inputs.json. The original calculation output is in nist_shomate.original.results.json. No unsupported material temperatures or real equipment efficiencies are assumed.
