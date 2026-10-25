# Independent frontier findings: restoring spatial oxygen delivery

25 October 2026. Scientific result at this checkpoint: a set of model-specific analytic constraints, an explicit oxygen-to-mechanics construction, and discriminating negative/comparative results. New biological recovery, a validated material/device, and a civilization-scale capability are **NOT_ACHIEVED**. External novelty and external specialist correctness are **UNKNOWN**.

## Chosen question and consequence

Can local physical feedback prevent open vascular shunts from deciding which parts of oxygen-starved complex tissue receive restorative perfusion, without requiring a separately instrumented control channel for every microscopic territory?

Success would enable local allocation in fabricated perfusable tissues/engineered organs and, if a native-organ interface were separately invented, could support recovery after severe ischemia. It would still have to preserve biochemical function, reopen obstructed vessels, and control reperfusion injury. A fraction of well oxygenated territories is a diagnostic metric; it is not successful recovery of an organ whose critical territories must all function.

The brief opportunity comparison and first independent construction are in `first_construction.md`. The investigation started with a flowing oxygen-responsive viscosity and changed to solid mechanical transmission after its limitations became explicit.

## Analytic results

1. **Transport averages a local fluid switch.** For q c'=-M f(c), uniform hydraulic resistance per uptake coordinate, and nonnegative local viscosity mu(c), write z(c)=integral_c^c_a ds/f(s), g(z)=mu(c(z)), and A(e)=e^-1 integral_0^e g. Then

       p/kappa=q A(M/q),
       d log(p/kappa)/d log(q)=2-g(M/q)/A(M/q)<=2.

   Desired-sign monotonicity gives a slope between 1 and 2. At equal uptake scale, a 100-fold geometric resistance disparity retains at least a ten-fold flow disparity. Arbitrarily steep constitutive switching cannot eliminate it.

2. **The spatial escape is explicit.** If h(a) is hydraulic resistance density against cumulative uptake and H its cumulative distribution, a local monotone fluid switch has slope at most 1+sup_a a h(a)/H(a). A localized gate can evade the uniform bound, but it requires a genuine spatial interface. Moving resistance from arterial to venous side raises intervening capillary pressure by q delta_R at fixed total resistance/flow.

3. **The budget matters.** A fluid whose viscosity is everywhere at least a matched uniform-low-viscosity reference cannot increase branch flow at fixed pressure. An oxygenated common feeder with the high-state viscosity does not repair this dominance. Under a finite total-flow budget it can redistribute, while consuming more pressure/power.

4. **Work and oxygen storage cannot be omitted.** In the specified lumped tissue model, sustained oxygen above c_min requires mean q_i>=M_i f(c_min)/(1-c_min), retaining a finite storage boundary term for finite windows. Jensen gives a sustained intrinsic hydraulic-work requirement sum R_i q_req,i^2. Root supplied an independent more general oxygen-mass conservation crosscheck; both derivations and their different scopes are retained in `hydraulic_bounds.md`.

5. **A mechanical sign inversion is possible in a stated model.** A Maxwell gel driven periodically in series with an output spring has H=i omega tau/[beta+i omega tau(1+beta)]. Longer deoxy-state stress relaxation can yield larger hypoxic valve stroke. An opposed-port spool converts oscillatory stroke into higher average conductance, with a finite delivery floor. The time-domain equation and actuator-energy identity are explicit. A static-preload version was rejected because slowing creep cannot reopen an already crept gate.

6. **The missing sensor interface has a constructive repair and a residual cost.** Parallel thin gel ribbons preserve total axial stiffness/gel volume while shortening the oxygen diffusion path. Binding-buffered oxygen transport can make a water-only estimate wrong by orders of magnitude. Thin subdivision reduces internal equilibration as thickness squared, but does not remove oxygen charge. For the direct series-transmission topology,

       V_gel >=4 F A_y/(G epsilon_max^2),
       Delta_n_O2 >=4 B_max Delta_s F A_y/(G epsilon_max^2).

   This prevents arbitrarily reducing sensor inventory while retaining mechanical force/stroke. The illustrative load requires about 9 nL and 18 pmol oxygen per phase. The pressure-bias, oxygen-charging and direct-pump-power constraints are derived in `sensor_mechanical_constraints.md`.

These are internal derivations. Root independently reconstructed the initial slope/heterogeneity/spatial-profile arguments at their stated model scope. Later device/interface derivations have numerical self-checks but have not received an independent specialist review.

## Discriminating computation

All tissues, geometries, demands and devices in these calculations are synthetic. The initial low tissue/sensor oxygen states are also supplied; a real operation must establish or measure them. No parameters were fitted to an organ or a candidate actuator, and no physical equipment was operated.

`perfusion_model.py` evaluates 1,920 budget/geometry/material cases and 48,000 branch root/elasticity checks. The exact pressure-flow root error is below 5e-16 relative; finite-difference elasticity agreement is about 1e-9. In the broad independent lognormal fixture, the best adequate-territory fraction increases from 38.9% to 47.6% at fixed total flow and about 1.68 times pressure/power. At matched hydraulic power the best value is only 39.5%. A severe 100-fold two-path disparity remains unrescued. The first fluid construction has no established practical advantage.

`phase_valve_model.py` propagates 24 synthetic territories, eight mechanical phases per territory, local oxygen stores, separate sensor-conversion lag, pressure/flow/power caps, and actuator dissipation. Harmonic input work equals dissipation to about 9e-16 relative error. In the selected hypothetical tuned-threshold case, 18/24 territories stay above the model oxygen threshold throughout the final 300 seconds, compared with 13/24 for uniform-open supply, at about 2.02 times the uniform-open hydraulic power. Actuator net loss is small in the ideal pressure-balanced model; real clock, friction and membrane losses are excluded.

The informed comparator is stronger: at the original uniform-open power budget, ideal independently set ordinary upstream valves can keep 19/24 territories adequate under the steady count objective, while the selected phase-driven candidate keeps only 12/24 continuously adequate in its final interval. The steady comparator uses supplied true geometry/demand and assumes control access; it is not an acquired microscopic control system. An ideal independent-pump architecture on the bare tissue beds can satisfy the modeled oxygen threshold everywhere at that work budget. The candidate has not beaten the informed alternative. A critical-pressure floating-point eligibility error was caught in an independent small-network check and repaired; the count optimizer now agrees with all 256 subsets in each of 100 random eight-branch problems. The main 19/24 result is unchanged by the repair.

The selected stable numerical case changes median terminal oxygen by only 3.4e-6 when dt is halved. A different high-gain regime is delay-sensitive: adding a five-second sensor lag changes final-window continuous adequacy from 23/24 to 2/24 while time-averaged adequacy remains about 62%. Refining dt .1 to .05 preserves the low continuous-adequacy fraction and mean power, but terminal phases shift. This supports a persistent excursion problem in the model; it does not establish a Hopf theorem or physical instability. See `delay_resolution_checks.json`.

`interface_constraints.py` evaluates the binding/diffusion and mechanical inequalities. With explicitly illustrative immobile-site inputs, a 50 micrometre slab half-thickness has about 248 s small-signal 90% equilibration, compared with 9.93 s at 10 micrometres. Bound-carrier mobility can shorten this, and intrinsic ligand kinetics can lengthen it. Those are predictions to discriminate, not measured gel response times. The small-signal diffusion, load-power optimum and force/stroke volume bound have numerical checks. `mechanism_diagnostics.png` shows the main constraints.

## What has and has not survived

The useful explanatory framework is the combination of extraction-coordinate hydraulic gain, the location of resistance, sustained oxygen/work balance, and the sensor's mechanical/oxygen inventory. It identifies the exact physical operations that would change the obstruction: changing intrinsic patency/resistance, routing acquired tissue oxygen information to upstream actuation, supplying localized work, or acquiring safe reversible demand control.

The surviving invention candidate is an oxygen-conditioned periodic mechanical transmission, built as thin load-bearing ribbons and coupled to a specified pressure-balanced metering geometry. Its chemical threshold, ligand-conversion speed, force balance, friction, cyclic stability, biological compatibility and practical advantage remain unacquired. Existing oxygen-sensitive gels and hydrogel valves prevent a broad novelty claim. The present synthetic valve parameters do not justify advancing to an organ-recovery claim.

The decisive next scientific operation is a standalone thin-ribbon oxygen-to-stroke unit, compared with a bulk specimen at matched binding inventory and with an ordinary sensor/actuator. It must measure ligand state independently of stress relaxation, acquired force/stroke versus frequency, pressure bias, total work, and cycle drift. This would resolve a specific enabling-interface question. A missing laboratory does not refute the conditional mechanism; the current mathematics and computation already identify several ways it could fail.

Primary comparisons, actual source access and APA references are in `primary_comparison.md`. Mathematical proofs are in `hydraulic_bounds.md`; construction changes and rejected assumptions are in `mechanical_valve_construction.md`. Reproduce the numerical work by running the three named model scripts, `allocation_check.py`, `delay_checks.py` and `plot_results.py` with Python 3 and NumPy; plotting additionally uses Matplotlib. No protected corpus or another owner's files were modified.
