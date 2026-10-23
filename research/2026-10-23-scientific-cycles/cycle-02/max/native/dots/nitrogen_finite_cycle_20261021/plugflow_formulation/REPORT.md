# Independent formulation check: finite isothermal compartment chain

## Decision
The stated closure is mathematically consistent on the equal-pressure/equal-total-molar-density manifold. It admits a zero-header-pressure-drop, low-Mach isothermal advection–reaction interpretation. It is not a complete momentum model or, without specifying thermal actuation, a demonstrated realizable heater. There is no missing explicit pressure-storage term in the proposed **internal-energy** balance.

This check uses exact rational arithmetic and no parent trajectory or chemistry implementation. It does not establish chemical accuracy, temporal/spatial convergence, stability, a performance advantage, or material feasibility.

## Derivation
Use fixed volumes V_j, fixed common temperature T, total volume V_H, total species molar density C_j, and reaction molar source S_j = sum_i omega_ij. All signed face molar flows F_j are oriented left to right. At a face choose the left donor for F_j > 0 and right donor for F_j < 0, including the adjoining bed/reservoir at an inflow boundary. A zero face has zero transported species/enthalpy regardless of donor.

With normalized donor fractions, summing conservative species balances gives

    Cdot_j = (F_(j-1) - F_j)/V_j + S_j.

Let D = (F_0 - F_N + sum_j V_j S_j)/V_H. The proposed prefix closure

    F_j = F_0 + sum_(k<=j) V_k (S_k - D)

gives Cdot_j = D and exactly reproduces F_N. Consequently initially identical C_j remain identical and Pdot = RT D. This is an invariant-manifold statement, not a mechanism that repairs an initial pressure inconsistency. Restart states must satisfy the common-C constraint; arbitrary cellwise clipping or renormalization would destroy conservation.

Each internal face must use one shared species flux, not two independently evaluated donor values. Species fluxes cancel in the total inventory ledger. Mass conservation additionally requires sum_i W_i omega_ij = 0. Boundary mass flux is F_j times the actual donor mean molecular weight. When interfacing with an Ergun **mass** flux, convert to molar flux with that same actual donor and preserve its sign. If boundary pressure/mass flux depends on the evolving state, evaluate the coupled state consistently at each RHS evaluation.

For species molar internal energies e_i = W_i u_i(T) and molar enthalpies h_i = e_i + RT, fixed-cell storage is U_j = V_j sum_i e_i c_ij. The fixed-control-volume first law is

    Udot_j = H_(j-1) - H_j + Q_j,
    H_j = F_j sum_i X_(donor,i) h_i.

Thus the proposed Q_j is correct. Reaction formation energies belong in e_i; do not add a separate reaction heat on top of these storage terms. For uniform spatial pressure, pressure work is already in advective enthalpy. Adding V_j Pdot to Q_j creates an erroneous residual. An enthalpy-storage reformulation instead has Udot_j = Hstored_dot_j - V_j Pdot; do not mix these two conventions.

## Exact diagnostic
Run: python nitrogen_finite_cycle_20261021/plugflow_formulation/exact_check.py

Three cells have volumes 1/50, 3/100, 1/20, totaling 0.1. Species A2, A, B have molecular weights 2, 1, 3. Reaction sources (-r, 2r, 0) conserve mass while changing total molecule count. Cell mole fractions differ but all total molar densities agree. Arbitrary exact molar internal energies (-7,11,3) and RT=10 test the algebra rather than a particular chemistry dataset. External right and left donor compositions differ.

Cases and exact results:
- Forward: face flows (3, 699/250, 123/50, 2), D=61/5. Local Q=(-22/25,-249/100,-1/4).
- Reverse: face flows (-2,-557/250,-62/25,-3), D=62/5. Local Q=(-17/10,24/25,-23/10). Positive heat=24/25; removal=4.
- Internal reversal: face flows (1/100,9/125,-9/200,1/100), D=-1/10. Local Q=(59/25,-93/20,2). Positive heat=109/25; removal=93/20.

All exact species, mass, energy, common-density, endpoint-flow and redistribution checks pass. Each case detects a spurious V_H Pdot addition, a fixed-molecular-weight boundary conversion, and a uniform-divergence shortcut that neglects local reaction sources. The reverse case explicitly checks right-reservoir inflow donor selection. Conservation alone cannot detect every consistently applied wrong donor, so correct donor identity is a separate check.

For the internal-reversal case the net heater heat is -29/100 despite positive heat input 109/25 and removal 93/20. Net heat alone therefore conceals simultaneous heating and removal. Summing positive Q_j and negative Q_j magnitudes separately is required. These are ideal thermal duties, not electrical power or refrigeration-work estimates.

Initial subdivision at unchanged densities and temperature preserves species inventory, mass, and internal energy exactly. It changes the residence-time/mixing model, not the physical history; do not award startup/reset credit for this redistribution.

## Limits and implementation guards
1. A directed, sufficiently resolved chain tends toward a plug-flow advection–reaction description. With reversals/stagnation it is a conservative distributed-flow model, not a single forward residence-time PFR. Do not promise monotone performance convergence with cell count.
2. Uniform thermodynamic pressure is compatible with a low-Mach approximation in which dynamic pressure gradients select flow but their pressure-loss work is neglected. This model does not establish header friction, kinetic energy, acoustic transients, or physical pressure-gradient feasibility. Mark the zero-resistance header assumption explicitly.
3. Holding every cell at T imposes distributed heating/removal. Equal total volume and temperature alone does not establish equal realizable actuator resources to a single mixed heater. Treat the chain as a favorable thermal-control limit unless wall/heater placement and heat-flux limits are supplied.
4. No extra boundary moving-wall work is present because volumes are fixed. Momentum/kinetic-energy omissions and separate bed pressure-loss/pumping accounting remain explicit.
5. Preserve positivity and equal total density numerically; source stiffness may impose integration constraints despite exact continuous-time conservation. Do not project inconsistent states without an accounted conservative procedure.
6. Finite-cell upwinding adds numerical mixing. A useful performance claim requires a mesh/time check, unchanged volume/inventory and honest local thermal duties, but none is executed here.

## Execution receipt
Source: exact_check.py. Raw output: exact_receipt.json.
Completed in approximately 0.000704 s Python calculation time; Linux process peak RSS 10,112 KiB. Interpreter launch, report writing and parent implementation cost are outside that calculation timing. No trajectory, chemical solve, tuning, paid resource or external access was used.
