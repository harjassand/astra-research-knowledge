ROOT FLOATING METAL GROWTH, CONNECTIVITY CHANGE, AND REDOX REGENERATION
14 November 2026 Brisbane / 13 November UTC
Science contracts; all numerical kinetics and controls below are INTRODUCED.

Question: can stock metal become an electrically floating useful geometry, while earlier features are retained, and subsequently return to a renewed stock state? The useful operation needs growth, connection, selective erasure, protection and restoration. The calculation below constructs only conditional charge-transfer and retention operations. It does not construct a three-dimensional wire, a useful circuit, a deposition head, a passive output, or a manufacturing advantage.

Owned executable:
ROOT_FLOATING_METAL_GROWTH_AND_REDOX_REGENERATION_SCREEN_20261114.py
18712 ASCII bytes, SHA256 30cfbf8e913f81c6c80358435848554a7fc64fa7c6b436bd70486bc076665465.
Owned output:
ROOT_FLOATING_METAL_GROWTH_AND_REDOX_REGENERATION_SCREEN_20261114.json
157310 ASCII bytes, SHA256 ece6dba50aa76091ff81f141bcc9789f0b003b579fe5ebab0ca78199624912a0.
Both are in work/astra-renewed-pro-programmes-20261103. They use serial standard-library Python, no external code, experimental data, installation, network or physical apparatus.

Actual source scope and ordinary constructions

Braun--Schwartz 2016, DOI10.1149/2.0031612jes, exact
https://pdfs.semanticscholar.org/c37e/ba1724cfd8a57b3dcd722d0d22b2fad73201.pdf
main lines0--469/pp0--5 read. Its moving microjet patterns metal on a prepared floating gold surface using counter-oxidation elsewhere. Electrolyte design can retain earlier deposits; other operation erases copper. Reported nickel current fractions include0.05%,2.8%,7%. This supplies an existing wireless localized deposition construction. Supplementary material, images and cited originals were not followed. Rendering gaps in equations11/13 were not reconstructed or used.

Percoco etal2026, DOI10.1002/admt.202502555, exact DOI followed to
https://advanced.onlinelibrary.wiley.com/doi/10.1002/admt.202502555
actual main2.1--4.4/lines199--455 read. A modified extrusion printer combines a wetted sponge, conductive brush, pumping and plating before polymer encapsulation. Functional demonstrations retain external wires, components and soldering. Characterization is offline; the sponge is replaced after approximately3h. This is an existing route to embedded conductors, not a supplied rewritable closed-volume factory or a full-cost quote. Supplementary material, figures, source code and cited originals were not followed.

These two constructions are distinct from other held electrodeposition sources. No failed source was recovered. The equations and parameter examples below are independently introduced and are not fits to either source.

1. Current closure is a physical constraint

Let V be the electronic potential of ONE connected floating metal body and phi_i the electrolyte potential at each exposed patch. Positive metal current means oxidation/dissolution. Put v_T=RT/F, z=2, c=N_Cu/N_Cu0, and use this declared symmetric mass-action kinetic law:
  J_i(V) = I0_i [ exp(z(V-phi_i)/(2v_T))
                   - c exp(-z(V-phi_i)/(2v_T)) ].
Its zero-current potential is phi_i+E_Cu, where E_Cu=(v_T/z)ln(c).

Let a distinct common collector support R -> O+e, with r=N_R/N_R0, o=N_O/N_O0 and introduced formal potential E_R0:
  J_R(V) = I0_R [ r exp((V-phi_R-E_R0)/(2v_T))
                   - o exp(-(V-phi_R-E_R0)/(2v_T)) ].

An electrically floating connected body obeys
  sum_i J_i(V) + J_R(V) = 0.
For positive stocks every derivative with respect to V is positive; the current sum tends to opposite infinities as V tends to opposite infinities. Hence this specified model has exactly one floating potential. One cannot assign separate electronic potentials to old branches AFTER they become connected. This is a standard lumped electrochemical constraint, not a new electrochemical law, field solver or general obstruction.

Geometry, ion transport, finite resistance within the body, capacitance, contact resistance and morphology are omitted. Each patch is uniform and has a fixed aggregate kinetic coefficient even as its nominal inventory changes. This is a finite kinetic screen, not a shape-growth simulation.

2. A conditional regenerative material circuit

Introduce a SEPARATE external regenerator with two selective interfaces:
  O+e -> R;
  Cu(donor) -> Cu(ions)+2e.
The floating body pairs
  Cu(ions)+2e -> Cu(product)
with
  2R -> 2O+2e.
Their formal net transformation is Cu(donor) -> Cu(product), with carrier returned. Reversing all selected reactions would formally return metal to stock, but it does NOT construct selective erasure of one useful feature while retaining others.

Let I_g be regenerator current. The finite inventories evolve as
  N_R' = (I_g-J_R)/F,        N_O'=-N_R',
  N_Cu'=(I_g-J_R)/(zF),      N_donor'=-I_g/(zF),
  N_i'=-J_i/(zF).
Thus R+O is conserved, and dissolved Cu+donor Cu+ALL product/old Cu inventories is conserved, using current closure. Chemical identity, an actual compatible reversible carrier, selective electrodes, separation, migration, mixing, pumping, counterelectrode side reactions and carryover are NOT supplied. This is an explicit conditional reaction circuit, not free renewal.

The controller uses an ideal observed well-mixed stock:
  I_g=min(I_max,max(0,F(N_O-N_O0)/tau)),
with tau=5s and finite donor stock. This is an unconstructed observation/control operation. Calculated 1V regenerator work excludes feeder field power, pumps, heat, preparation and physical isolation; it is not wall power or full-cycle cost.

3. Introduced numerical instance and finite-stock threshold

At298.15K, use nominal Cu molar mass0.063546kg/mol and INTRODUCED density8960kg/m3. A20mm-long,50um-diameter DENSE-Cu volume equivalent is0.0392699082mm3,0.351858377mg,5.53706570umol and1.06849125C. Reaching that charge does not manufacture that geometry.

Initial R=O=12umol, dissolved Cu=100umol and external donor Cu=100umol. Each old patch A/B initially contains one target-volume equivalent of Cu. Introduce phi_D=.120V, phi_A=0, phi_B=-.040V, E_R0=-.100V; I0_D=20uA, I0_A=I0_B=200uA, I0_R=400uA. No operating material or electrochemical measurement supplies these values.

Before connection of B, let x mol of R be oxidized with no regeneration. Then R=R0-x, O=O0+x and dissolved Cu=Cu0-x/2. At the exact old-A dissolution threshold, V=E_Cu and J_A=0. Substitution in J_D+J_R=0 gives x=2.581577751umol and0.2490843867C of net metal conversion. This threshold concerns the stated model, not an actual bath lifetime.

With no regenerator, the target charge is reached at682.671579s, but A has lost8.88674768% of its initial mass. A starts positive oxidative current near107.1s in the finest time-step record. This is not a successful retained-feature output.

With I_max=4mA, the target is reached at434.222838s and no A erosion is sampled. However A GAINS2.31936306% metal. Preventing loss is not preserving geometry. A1mA-limited regenerator gives526.380197s and0.947922836% net A loss; it passes this introduced1% net-mass screen despite positive erosion beginning near187.81s. This is neither measured reliability nor a universal safe-current threshold.

4. Connection changes the physical boundary problem

At100s, connect an initially isolated old B patch whose local electrolyte potential is-.040V to the growing body. The contact is INTRODUCED instantaneous and zero-resistance; no joining route is supplied. Before connection the single B patch can float at its own zero-current potential. After connection it shares V with A and D.

With4mA regeneration, V jumps from-.00366107495V to-.00751890751V. The new B branch immediately oxidizes at.651611583mA. The growth-charge target arrives sooner,387.504443s, but B loses17.52596510% and A gains3.72964734%. The apparently faster growth partly consumes earlier structure. The regenerator's lower counted charge is not an efficiency advantage.

An INTRODUCED1000-fold kinetic block on B reduces its loss to.0242072911%, but A still gains2.32137615%. An INTRODUCED field guard setting both old patches to phi=0 prevents erosion but adds2.18200828% to A and1.64687536% to B. Neither operation alone preserves both old inventories to within1%.

5. A constructive conditional alternative: two ionic controls

Suppose a physical head/guard can put ALL exposed retained metal at one common electrolyte potential phi_A, while retaining a DIFFERENT growth-patch potential phi_D. Suppose it can independently control phi_R at the common carrier collector. Those are two unconstructed physical field/access operations, not a wire to the product, a solved inverse-field problem, or freely installed observations.

Choose V*=phi_A+E_Cu+epsilon. Let L(V*) be the sum of ALL metal currents at V*, q=-L(V*)/I0_R, r=R/R0 and o=O/O0. The positive solution of
  r u-o/u=q
is
  u=(q+sqrt(q^2+4ro))/(2r).
Choose
  phi_R=V*-E_R0-2v_T ln(u).
Then J_R=-L(V*) exactly, and uniqueness of the floating potential gives V=V*. At epsilon=0, every old patch at phi_A has zero current, while the growth patch carries current. This constructs a conditional control law in the stated model. It does not supply independent control of these electrolyte potentials around a growing3D object.

With both controls and4mA regeneration, the target charge is reached at500.585357s, including the100s connection. Old net-mass changes are numerical roundoff. A+1mV setpoint error gives520.449579s with A/B losses.758327427%/.612619884%;+2mV gives541.102552s with1.57805620%/1.28641698%, exceeding the introduced1% tolerance.

For arbitrary time-dependent errors satisfying |eta_old|<=e, duration<=T_max and c<=c_max, the declared law gives
  |Delta Q_old| <= 2 I0_old sqrt(c_max) sinh(z e/(2v_T)) T_max.
Therefore1% net-mass retention over600s with c_max=1.01 is ensured WITHIN THIS LAW by e<=1.137797036mV. This bound is not installed sensor accuracy, a morphology/adhesion certificate, functional resistance, dimensional stability or a real3D guard. Guarding only a measured terminal voltage is insufficient unless the local solution potentials and activities also satisfy the contract.

6. Drive-off is not chemical stop; restoration must follow protection

The introduced E_R0=-.100V is downhill relative to Cu, so the ideal reaction law permits electroless deposition without an external spatial drive. This is an important limitation of this parameter instance, not a measured property or a conclusion about every electrolyte.

At the two-control case's endpoint, removing all spatial fields and active guards while leaving the metal wet gives an instantaneous V=-.0324669632V and A current=-.650762986mA. It is MORE deposition, at an initial old-A fractional mass rate.000609048495/s. No constant-rate extrapolation or passive lifetime is claimed. The B passivation factor is retained when calculating the corresponding coated case.

A conditional sequence is: physically isolate ALL product reaction paths WHILE guards remain effective, THEN disable guards and finish external regeneration. Isolation is a missing real operation: residual films, inaccessible liquid, rinsing, contamination and waste cannot be assigned zero time or free perfect blocking.

For the two-control case, restoring R/O and dissolved Cu after such PERFECT isolation needs.0106723886C additional recharge,2.66809716s at4mA and.0106723886J at an INTRODUCED1V. Together with growth-stage regeneration, total carrier recharge is1.06849125C and counted regenerator work1.06849125J. R/O return to12/12umol, dissolved Cu returns to100umol, donor Cu falls to94.4629343umol, exactly paying the target Cu volume. The sum500.585357+2.668097s EXCLUDES physical protection/clearing and is not full ready-to-ready time. No required stock is silently reset.

7. Comparator, verification and unresolved operation

A matched ideal WIRED localized head with the same tip law at-.120V overpotential supplies2.13506822mA and reaches the same nominal charge in500.448294s. Its electrical contact and local wetting are assumptions, not a purchased machine. The two-source physical constructions above supply brush/nozzle plating and embedded polymer-Cu electronics as comparators. Eliminating a direct product wire has not established an advantage once the remote method's guard, collector, stock, fields, head access and isolation are paid. No full-cost advantage is claimed.

Nine cases at three time steps(.2,.1,.05s) retain full finite carrier/Cu histories. The initial regulator-limit kink produced a.000105533s coarse-step target-time span; the implementation was corrected to split that event explicitly. Final maximum span is1.70348e-8s, carrier-balance error1.08421e-19mol, Cu-balance error4.82470e-17mol and sampled current-closure residual2.0e-15A. Refinement and conservation are meaningful finite numerical checks; they are not rigorous continuum error bounds or physical validation.

The conditional construction is specific: an independent ionic boundary control plus a regenerable charge carrier can retain earlier connected metal while driving local growth in the model. The unresolved physical operations are the actual field/collector/stock implementation around changing geometry, unwanted-background suppression, protection before withdrawal, selective erasure, and useful qualified3D function against matched ordinary methods. No qualified material, sensor, source, freeform path, passive device, continuous renewal campaign, new algorithm, novelty verdict or invention is supplied.

