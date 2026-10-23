# Expansion is a time window, not an enthalpy sink

This new calculation tests an actual nitrogen-quench construction. It is not a restarted lamella or a heat-engine design.

## Steady-flow operation and robust reset requirement
One kg original dry79/21 fresh feed traverses the same saved2700K heater at1atm. The source hot composition and enthalpy are fixed, not recomputed. Downstream final bulk state is at rest, all internal modes relaxed, T<=1700K; all plant inventories are restored. The six-species boundary permits NO+NO2 between99% and101% of hot count, N<=1e-7mol/kg and O<=.003mol/kg. These are an explicit declared retained-product/reset contract, not a measured quench performance. Subsequent300K/1atm product closure still must be supplied for a complete process.

The open-flow first law gives Q_out+W_out=H_hot-H_final when net kinetic/potential energy and other material/energy fluxes vanish at the boundary. Negative W_out means work input. Internal mode storage and nozzle kinetic energy do not disappear at complete reset. Optimize final H over atom-balanced nonnegative species, the stated NOx/radical constraints and T<=1700. Positive species heat capacities make1700 the favorable temperature; a six-variable linear program maximizes its enthalpy. Its best final state has all permitted counted product asNO, maximum allowed NOx and radicals, with remaining atoms inN2/O2.

For the actual stored thermochemical coefficients, H_hot=3096703.057425J/kg and maxH_final=1689030.351810J/kg. Therefore at least1407672.705616J/kg must cross the downstream boundary as net heat plus shaft work before this relaxed1700K state is reached. An independent rational primal-dual certificate binds the stored binary64 LP, not empirical thermochemistry or kinetics. This is a transferable energy requirement, not a claim all exported heat is lost, and not electrical SEC. For a closed rigid batch use U and all boundary work instead; this H result is not transplanted there.

The no-net-new-product cap is load-bearing. More NOx or stored radicals can change final chemical enthalpy and leave this class. Heat returned to fresh feed is a counted heat export from this quench control volume and may be valuable, subject to temperature grade, finite conductance and the wider plant balance. Radiation/work/entrained coolant/solid stores must be accounted explicitly. The result does not exclude regeneration.

## Transparent ordinary gas-dynamic reference
To illustrate where the energy goes, use frozen composition but internally equilibrated NASA caloric functions. This is a declared equilibrium-mode reference, not validated rapid-expansion kinetics. Along ideal reversible expansion:
P/P0=exp[(s°(T)-s°(T0))/Rmix], u²/2=h(T0)-h(T).
Across a normal shock: rho*u, P+rho*u² and h+u²/2 are conserved. Independent scalar inversion gives the downstream subsonic root. No chemical trajectory is integrated.

At static1000K, P≈1506Pa,u≈2055m/s. A normal shock raises T≈2628K; full adiabatic deceleration returns2700K in this reference. Lower staticT is not low stagnation enthalpy. The source experiments independently require heat removal before deceleration.

A prescribed recovery factor r defines h_aw=h_static+r(h0-h_static). At1000K a passive wall cap1700K requires r<=.39818. Ordinary air examples r=.85/.89 give2454/2520K, but their transfer to reacting nonequilibrium air is NOT qualified. The exact threshold is the reusable result; illustrative correlations are not a universal wall-temperature bound. An actively cooled wall may remain below its recovery temperature by exporting heat, which must be included.

Cold isothermal compression W=Rmix*300*ln(Pambient/Pin) is evaluated for two distinct illustrative inlet pressures: full static expansion pressure or recovered postshock total pressure. At1000K reference these give366.74 or136.25kJ/kg. They are not additive and neither is a universal bound over all cooling/diffuser layouts. The lower-pressure-recovery reference already experienced high shock temperature. No route gets both instantaneous cooling and free pressure recovery by mixing the two columns.

## Heat grade is a separate obstacle
heat_grade.py examines only a common-wall class: ALL useful heat recovery to composition-preserving internally equilibrated fresh feed crosses a wall cappedTw, with no heat pump, useful-work transformation or nonthermal feed. Then Tin<=Tw. For unchanged heater chemistry, Q_heater>=hFresh(2700)-hFresh(Tw)+Qreaction. AtTw600K the favorable perfect-retention floor is2.70070MJ/mol thermal duty, versus1.45791 at1700K. A cold final cooler plus separate upstream high-temperature recuperator is NOT in this class. No actual nozzle wallT is inferred from this parametric screen.

## Primary gas-dynamic references
NASA NACA experimental temperature-recovery report: https://ntrs.nasa.gov/api/citations/19930092100/downloads/19930092100.pdf . Its moderate-Mach air recovery correlation is illustrative, not a high-temperature reacting-air measurement.
EPA1980 probe report and2011 evaporative supersonic-quench study are documented in ../expansion_evidence/REPORT.md. Their physical heat-removal and pumping boundaries support the distinction, not a numerical retention claim for this heater.

## Decision
Reject a nozzle-only or low-static-T material-admission argument. A useful expansion quench must explicitly demonstrate sufficiently early total-enthalpy removal, intact wall hot spots, pressure restoration and retained output. Do not run another arbitrary mode-partition trajectory to evade this accounting. Evaluate direct finite wall extraction against actual ordinary hardware first.

The gas-dynamic caloric reference deliberately uses ideal-gas entropy below the helper state-evaluator pressure domain. No kinetic or transport evaluator is called at those pressures; do not inherit its validation there.
