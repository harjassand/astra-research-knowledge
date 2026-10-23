# Finite-inventory regenerative cycle: independent formulation

## Result and recommended minimum
A one-way, equal-mass-flow isobaric cascade is not a generally valid transient model of these fixed-volume beds. A fixed-pressure cascade **can** preserve inventory if its outlet mass flow is solved from the equation of state, but the resulting flow can be negative and then its assumed upstream donor is wrong. The minimal broadly usable next model is a fixed-volume gas/solid cell network with conservative species masses and gas internal energy, local ideal-gas pressure, signed donor-aware face fluxes, and an explicit pressure/flow closure. Both beds and the heater must form one connected network. This derivation does not assert a physical cycle benefit or simulate a bed.

## 1. Fixed-volume conservative cells
Let a bed cell have bulk volume V=A dx, void fraction phi, gas volume Vg=phi V, species masses m_i, total gas mass m, gas internal energy U, and solid stored energy Hs. Define Y_i=m_i/m and rho=m/Vg. The caloric state satisfies

U = sum_i m_i u_i(T),
p = rho Rmix(Y) T,
Rmix = sum_i Y_i R_i, R_i=Ru/W_i.

Use full formation-plus-sensible u_i and h_i=u_i+R_i T from the same source thermochemistry. There is no additional chemical heat source when formation energy is already in U. Reaction sources omega_i are kg per gas-volume per second and must conserve elemental mass exactly to the numerical tolerance being claimed.

For a positive face mass rate F from cell j to j+1, use donor cell j. For negative F, use donor j+1. The same face flux, species vector and enthalpy must enter its two adjacent balances with opposite signs:

 d m_i /dt = F_left Y_i,left-donor − F_right Y_i,right-donor + Vg omega_i,
 d U/dt = F_left h_left-donor − F_right h_right-donor + Qsg + Qext,g,
 d Hs/dt = −Qsg + q_s,left A − q_s,right A − Qloss,s.

Here Qsg=Uv V (Ts−T), with Uv per bulk volume, and q_s is positive in the spatial positive direction. The reaction volume is Vg, whereas the film exchange volume is V. Mixing these factors changes the model.

Summing cells cancels every internal mass/species/enthalpy/solid-conduction flux and Qsg exactly. This cancellation is independent of flow direction. The resulting complete-system energy derivative equals boundary enthalpy inflow minus outflow plus actual external heat/work minus external heat loss. Stored species and energy remain continuous at valve reversal. Swapping boundary connections does not authorize resetting gas to fresh air or equilibrium.

This energy equation is the low-Mach thermal internal-energy balance with enthalpy transport and pressure work included in the flux. If resolved kinetic energy or momentum inertia is non-negligible, retain its storage and flux consistently instead of calling this an exact compressible-flow model. A separate frictional heat source must not be added without reconciling it with that mechanical-energy approximation and gas/solid dissipation partition.

## 2. Pressure/flow closure
For a minimal resistive low-Mach network, a signed quasisteady packed-bed closure can be stipulated at each face:

(p_j−p_(j+1))/ell = a G + b |G| G,
 a = 150 mu (1−phi)^2/(phi^3 dp^2 rho),
 b = 1.75 (1−phi)/(phi^3 dp rho),
 F=A G.

Use one face density/viscosity convention consistently and solve the signed scalar quadratic. This is an Ergun-type constitutive approximation, not an exact momentum theorem. Cell pressures still evolve through conservative mass/energy storage and EOS; they are not reset to1atm after every step. Quasisteady momentum needs a stated small-Mach and momentum-relaxation regime. Rapid valve/acoustic dynamics outside that regime require a momentum equation or bounded pressure-relaxation model. Film coefficients should use the actual local flow, not a permanently frozen G=1 during large transient dilation.

Reservoir pressures and/or mass-flow controls must be specified. One cannot prescribe both independent bed inlet flows and atmospheric pressure everywhere while also claiming inventory-conserving transients. Pump/controller work is not zero merely because pressure differences are small. A boundary supply of prescribed mass flow is an ideal controlled port whose required pressure/work remains to be counted. Air compression followed by heat rejection needs the compressor input and rejected heat, not a fictitious change in ideal-gas enthalpy alone.

## 3. Exact fixed-pressure, fixed-volume cascade identity
For one cell with positive known inlet F_in, presumed nonnegative outlet F_out, upstream state Yin,hin, and heat input Q, let omega_i denote reaction mass per time for this whole cell. Then

 m dY_i/dt = F_in(Yin_i−Y_i)+omega_i,
 m cp dT/dt = F_in(hin−h)+Q−m sum_i h_i dY_i/dt.

The constant-pressure/fixed-volume EOS imposes

 dm/dt = −m[(dT/dt)/T + sum_i R_i dY_i/dt /Rmix],
 F_out = F_in−dm/dt.

These equations follow by differentiating U=m u, using dU/dt=F_in hin−F_out h+Q, and differentiating m Rmix T=pVg. They include pressure work. Enthalpy storage may replace internal-energy storage in this special case only because d(pVg)/dt=0.

If F_out<0, the presumed outlet donor is invalid: incoming gas composition and enthalpy must come from the next cell or external reservoir. Simply clipping F_out to zero violates EOS/energy; continuing with the old donor is an inadmissible branch. A bidirectional isobaric network requires a simultaneous sign-consistent flux/donor solution, not a forward one-way recurrence.

A simple exact example makes the inventory issue unambiguous. With constant composition/cp, no inflow, heat Q>0 and a vent holding p and Vg fixed, mT=C. Then T=T0 exp[Qt/(C cp)], m=m0 exp[−Qt/(C cp)], F_out=Q/(cp T), and U=C cv is constant. All supplied heat leaves as vented enthalpy. Equal inlet/outlet flow would instead falsely hold mass fixed and violate the stipulated pressure condition.

## 4. Review of the parent's actual reversal diagnostic
Read, but did not rerun, reversal_isobaric_screen.py and its saved JSON. Its isobaric species, temperature, EOS and storage-ledger equations agree with the identities above. Its use of enthalpy-storage derivative is valid for fixed p,Vg. Its G=1 films are explicitly frozen diagnostic coefficients, not a transient transport model.

For the saved2700K bed becoming the cold bed, the first attempted negative outlet occurs at zero-based cell index15: −0.0073179106035kg/(m2 s). That is the first contradiction of the one-way closure. Values after that cell, including the displayed downstream negative outlet, cannot be interpreted as a physical trajectory. Changing the frozen film closure or solving pressure globally can change this first-invalid index; it is not a universal backflow prediction.

The other reversed bed's one-way instantaneous outlet reaches14.73411684kg/(m2 s), under its separately imposed inlet1. This is not a joint two-bed flow solution. The hot bed inlet must be the actual heater outflow; heater/header storage must account for any difference from cold-bed outflow. The source already labels these limits, and the parent explicitly retains the failed closure instead of promoting it to a cycle.

## 5. Central heater closure
Preferred finite model: a finite-volume heater/header node with the same species/internal-energy inventory equations, connected to both beds. A controller supplies Qh(t) to meet a stated temperature trajectory. For an ideal exactly isothermal heater at Tstar and fixed volume, species masses still evolve and pressure follows EOS; required thermal power is

 Qh = sum_i u_i(Tstar) d m_i/dt − sum_ports(F_in h_in−F_out h_out).

This counts reaction formation energy through species inventory. Any ramp/startup additionally contributes sum_i m_i cv_i dT/dt. Finite residence and kinetics must be retained if equilibrium is claimed.

A zero-volume instantaneous-equilibrium heater is an explicit favorable limiting map only: F_out=F_in, elemental inventories unchanged, actual inlet composition determines the equilibrium output, and Qh=F_in(h_out−h_in). It has neither heater residence nor inventory and cannot validate the actual finite heater. Independently prescribing hot inlet F=1 despite a transient upstream outlet different from1 creates an unaccounted mass source/sink.

Negative Qh means heat removal. It is not negative electrical input unless a specified recovery device actually exports work. Count positive heater input divided by its supported efficiency, pumping, valves, capture and reset. Do not add or subtract chemical formation energy twice.

## 6. Periodic reset and admission boundary
Use physical bed labels. The full valve sequence has period2 tau unless a shorter symmetry-reduced map is explicitly reconstructed. At matching phase after a complete cycle compare all gas species masses, gas energy, solid stored energy, and heater/header inventories. Equality of solid temperature alone is insufficient. Require integrated total mass and N/O elemental balances, the complete energy ledger, nonnegative species/density, gas and grain temperature limits, admissible pressures/flows, and controlled numerical discretization error.

Retained NOx is net exported product over the full boundary, after counting inlet recycle, purge and capture exactly once. Product normalized only by a hot half-cycle outlet can conceal inventory depletion. Startup energy and discarded reset streams are separate when evaluating finite campaigns. There is no generic guarantee that a small ratio of gas holdup to blow duration bounds product or energy error; kinetics, phase mixing and inventories determine that error.

## 7. Actual independent diagnostic and scope
conservation_diagnostic.py uses Python Fraction arithmetic, no chemistry package or bed solver. It verifies:
- the isobaric cell's species, EOS and energy balances exactly;
- a nontrivial example where F_out=0.918 while F_in=1;
- omission of composition enthalpy produces a61.5W residual in that example;
- forcing equal flow gives a−12.3Pa/s pressure derivative under the claimed fixed-pressure constraint;
- signed interior face flux cancellation and two elemental balances in a two-gas/two-solid network, for both flow directions;
- the analytic heated-vent identity.

The exact small diagnostics establish these algebraic conservation identities only. They do not validate the nitrogen kinetics, pressure constitutive law, material properties, numerical discretization, or a useful regenerative cycle. Runtime and Linux peak RSS are in the JSON; CPU and host overhead are unmeasured. No large solver, new experiment, spending, hardware or source acquisition was performed.
