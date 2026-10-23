Astra next16 small regenerator/electrical interface (supersedes v1 only where stated)

Read coupled_bound/physical_coil_RESULT.json and physical_coil_voltage.csv for
the SAME concrete circuit/thermal operation. The proposed replacement loses
to TE even under favorable ideal electronics/material limits. Do not optimize
this point further. Other electrical geometries need a new coupled comparison.

Geometry and area
Each bank has footprint A; pair area is2A. Ten260nm FE films are electrically
parallel, active thickness2.6um, heat capacity7.8J/m2K atzeroV. Known passive
allocation:90nmSiC*.3e7=.270 and110nmmetal*2.5e6=.275J/m2K.
Two100nmAl2O3 layers (eps9,cvol3e6) and two10nmextra metal layers add.65J/m2K.
FE zero-V plus passive C=8.995; atnonzeroV use source_envelope.props CV,
which varies with T,V. Thin optical metal PEC behavior is unqualified.
No water, fluid header or ideal thermal selector is present in replacement.
Use conditional rib support409W/m2K to338K. Original10.81post figure is not
substituted. Physical coil example A=.001m2, L1.19709mH,20turns,80mm2Cu,
Cu1.6334kg,core1.555kg; all geometric data accompany the result.

Exact constitutive source
material/source_envelope.py + envelope_data.json + supplied digitized CSVs
define Q=-G_V,S=-G_T,C=Q_V,alpha=Q_T,CV=T*S_T,U=G+TS+VQ.
Reference temperature348.15K; only338..348.15K and0..23.27V admitted.
shape=0 is a representative identifiable family member, not measured G;
shape[-.5,1] tests preserve the entropy integral. It is not valid to assign
the field-averaged p=-.004827 to every localfield while retaining measured
field-resolved P(T) derivatives. The actual published PDF/text is supplied.
The extra absorption states seen in source current are NOT yet in this G.

Electrical/optical assembly
FE outer electrode |100nm isolator| extra optical backmetal |45nmSiC|
graphene |25nmvacuum|reservoir. Graphene electrochemical reference staysfixed;
mu>.0 is electron doping. Independent gate control uses mu=.1695 or.6eV.
Reservoir effective phi=.38475V as inherited compensation; changing global
electrode references invalidates vacuum forces. A shared-terminal gate cannot
be independently clocked without this separation. Single23V operation avoids
unrealized series-tiling/segmented-reservoir reference changes.
isolation/gate_stack.py adds BOTH real optical-gas G and
Giso=-.5Ci(VFE-Vg)^2, Ci=.0007968769F/m2 perface. Thus gate current contains
-Ci*dVFE/dt. These charges/work are included, not independently chosen.
It also includes Cgap=eps0/25nm and finite quantum capacitance; use its API.
The maximum SiC field remains near4.83MV/cm, FE895kV/cm; dielectric repeated
cycling/leakage and thin-metal optical equivalence are unqualified.

Reservoir laws into each bank
qh=hh*(348-T);qc=hc*(338-T); (hh,hc)=(2111.152,264.262) hotON,
(168.69,4813.078) coldON, (168.69,264.262) bothOFF, W/m2K.
Support adds409*(338-T). These are inherited linear10K-span ports, not a
new calculation for an altered optical metal. Gating transition heat is not
fabricated: transitions in this upper screen are zero-time adiabatic limits.
Finite gate duration requires its real h(mu,T) and heat/driver losses.

Protocol and circuit
At start A highFE23V/hotON, B lowFE.1V/coldON. Hold3ms atregulated rails.
Switch both banks opticalOFF with all gate/isolation chargework included.
Disconnect bias rails, join two FE banks through L and antipolarity current
commutator for a direct zero-current LCswap (~.994ms). Keep finiteOFF heat.
After I returnszero, a bidirectional partial-power converter corrects voltage
to(.1,23)V over30us; the correction energy is explicitly computed.
Swap opticalstates; identities swap eachhalf. Fullperiod~8.04844ms.
The large FE capacitive energy circulates in L; it is not useful output.
During LC, useful bus work removes ALL I^2R heating from terminal FEwork.
High/low finite charge buffers plus regulated bidirectional catch/gate ports
are the intended circuit. Stiff rails and reversible converters here give
necessary favorable limits, not an implemented finite-buffer/control loop.
Output must be withdrawn while all buffer voltages/charges are restored;
unrestored stored/trapped charge is never useful work. Losses are UNKNOWN.

Coupled equations and regenerator interface
Call gate_stack.coupled_derivatives(T,V,mu_faces,mudot_faces,IFE,q,FEprops).
Its common-G matrix includes FE caloric response, optical heat capacity and
isolation crosscapacitance. Supply q=qh+qc+qsupport+qreg+qwire+Pdiss_body.
LC: LA*jdot=VA-VB-Rseries_area*j; IFE_A=-j,IFE_B=+j.
LA=1.19709e-6Hm2; Ldevice=LA/A atsingle23V. Need re-evaluate event/fieldbound
when regenerator changes T and thus capacitance/current. Prescribed voltage
and independently optimized thermal trajectories may NOT be combined.
Four normal-metal arms have sum resistance_area rarms. Their heat into each
bank is4L0/rarms*(Tnode^2-Tbank^2), L0=2.443004509e-8. Wire Joule heat splits
onequarter rarms*j^2 into eachbank, half into node; coil heat all into node.
Node has actual Cu heat capacity and returns to initial T after a fullcycle.
Coil resistance cannot be allocated to thermal arms at the same time.

Periodicity and usefulness
After fullperiod both FE T,V,Q,S, graphenes mu/charge, isolation capacitors,
inductor I and core state, regenerator T/internalstates, floating-node T,
all buffercharges and controller/material internalstates must reset.
The reversible screen resets all states it actually models; unmodeled core,
buffer/controller/material states are explicit missing physical costs.
P=Whalf/(2*half_duration); eta=Whalf/Qhhalf. Comparator te_analytic_check.py
uses same348/338K, area2A, hot2111.152/cold4813.078 ports and constant ZT1.2,
optimizing thermal conductance and electrical load at actual netpower.
The .00251259J/m2 remainder of the zero-coil floating-wire screen is ONLY a
fixed-trajectory external-bus-loss diagnostic. Internal heat changes T,Qh
and current; solve the coupled operation again instead of spending budgets.

Material obstruction (not a measured low-frequency FE no-go)
material/relaxation/actual_cycle_results.json analyzes the complete voltage
path, with each Debye state periodic, using ONE positive spectrum for BOTH
banks. Conditional T-independent positive Debye+DC interpretation of source
conditioning pulse has analytical all-tau loss>=108J/m2/bankcycle, vs source
full338..348K reversible monotone-cycle envelope<=1.10331J/m2. ZeroDC still
fails. The initial uncharged state and repeatability are NOT established by
the published pulse. A trained/nonlinear response needs explicit internal
states and coupled terminal-work/heat/reset data, not a favorable tail split.

99.74% reference
charging_reference/READ_THIS.txt states the actual definition: loss over BOTH
charging+discharging absolute energy,9.927uF constant filmcap,316.99Vpp,
20.002Hz,19.947W processed; controller and gate-driver supplies excluded.
It is a topology reference, not a transferable cycle efficiency. This cycle
is nonlinear,23V,~124Hz, and has fast1ms FE exchange/optical flips, tiny net
module power and multiple gate/electrical buffer ports.

Replay needs Python,numpy,scipy. From this folder:
 python coupled_bound/cycle.py
 python material/relaxation/actual_cycle.py
These reproduce favorable limits/conditional response-class calculations,
not physical success. Source parameters and CSVs are supplied for independent
regenerator coupling; original v1target remains in the separate v1archive.

ACTIVE SURVIVING LIMIT / ACTUAL SMALL DATA
Enlarging the winding to470mm2Cu leaves a favorable limit, NOT a physical
operating region:17.25990W/m2,eta.4091916%,TE.4002484%atsamepower. It requires
9.596kgCu+7.562kgcore(.817moutsideD) forA=.001m2bank,pairoutput34.52mW.
This material allocation and its floating thermal mass are recomputed in
active_larger_coil_RESULT.json. Unknown core/FE/switch/buffer/control losses
are not given favorable actual values. Shared remaining externalbus room
is.001805892J/m2/pairhalf (~.449mW permodule) at this unchanged trajectory.
Any internal loss requires heat/current feedback and a NEW comparison.
Use active_finite_phase_ports_halfcycle.csv for actual T,V,Q,I,allfourgate
states/charges/currents and photon/support/wire heat. Complete the second
half by exchanging bank identities. The gate-event CSV is SEPARATE: its
dimensionlessx represents an adiabatic zero-time bound, currents aredQ/dx.
A real finite gate operation must replace these events; it cannot inherit
the zero-time thermal or resistive cost. active_stage_ports.json has separate
finite-time I2 and gate-event(dQ/dx)^2 integrals plus field maxima.
Absolute gate-port energy3.59138J/m2/half is NOT an irreducible converter
processing requirement: equal-voltage opposing isolation currents can share
buses, and direct gate charge exchange/partial-power processing is allowed.
Actual routing must reproduce terminal currents, finite-voltage ripple and
full buffer/inductor/reset state, with losses counted once. No required99.x%
efficiency is inferred from blindly multiplying that absolute port energy.
The positiveLTI class attack was repeated on this SAME active voltage trace:
all-tau lowerbound108.10863J/m2/bankcycle, LP128.899ish (see exact JSON).
This exceeds the FE source envelope evenbeforeothercomponents. A nonlinear
conditioned response could escape that class, but must be supplied explicitly.
