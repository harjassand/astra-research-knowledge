# Independent rapid-cycle regenerator boundary check

## Decision
The implemented rapid-cycle, equal-phase, two-reacting-stream equations have a consistent mass/element/formation-enthalpy ledger. The saved geometry-linked results are credible conditional averaged-profile calculations at the reported engineering tolerance. They are **not** a demonstrated cyclic nitrogen-fixation device or finished-product electrical SEC. No full BVP was rerun in this check.

## Independent derivation
Let x increase with hot-phase flow, G denote mass flux per total bed cross-section, phi void fraction, q_s=-k_eff dT_s/dx, and U_v=h a_s with a_s=6(1-phi)/d_p. Gas reaction production is per void-gas volume, hence

G dY_hot/dx = phi W omega_hot,
-G dY_cold/dx = phi W omega_cold.

The total specific enthalpy includes species formation enthalpies. Therefore

G dh_hot/dx = -U_hot(T_hot-T_s),
G dh_cold/dx = +U_cold(T_cold-T_s).

The code's temperature equations subtract sum_i h_i dY_i/dx before dividing by cp. No additional reaction heat belongs in the total-enthalpy equation. For equal hot/cold phase durations the zero-average-storage solid equation is

dq_s/dx = [U_hot(T_hot-T_s)+U_cold(T_cold-T_s)]/2.

Consequently G(h_hot-h_cold)+2q_s is spatially constant. With insulated ends, hot enthalpy decrease equals cold enthalpy increase. With q_s(0)=0 and a radiating cold end, the pair loses **2q_s(L)/G per kg through-flow**. The factor2 is necessary: at any time there are two physical beds. It is not an erroneous double charge. Heater duty h_hot,in-h_cold,out divided by the hot outlet NO+NO2 mol/kg is consistent for one through-flow through cold bed, heater and hot bed. The cold stream's already formed NOx is internal, not an extra output to add again.

The state q_s/1e6 and T_s/1000 scaling is internally consistent. The radiation k=16 sigma T^3/(3 beta) has units W/(m K); U_v uses actual sphere area per bed volume, while Reynolds number uses superficial mass flux. No missing extra porosity factor was identified in these terms.

## Actual independent saved-data operation
check_saved_ledgers.py imports the common native Cantera thermochemistry via paper_model.py, not either parent BVP or the vector kernel. It reconstructs all six mass fractions, native gas enthalpies and molar NOx at every saved node, checks the energy invariant and element drift, and independently calculates Ergun pressure and gas holdup. This is an independently implemented ledger check with shared physical source data, not an independent thermochemical validation.

Ten saved checkpoints were checked: the geometry-linked3100K result, eight hot-inlet continuation states3050 through2700K, and the radiating2700K state. Local invariant drift is about0.118–0.152J/kg against duties near1MJ/kg; elemental mass-fraction drift is at most2.22e-16. Tiny raw negative mass fractions remain, down to about-3.6e-10 in the3100K state. Native/kernel normalization clips these; they must not be called strict positive certified solutions. The check examines all six species, whereas the parent scalar receipt only reports the five independent fractions. The omitted N2 is benign in these actual saved states, but that receipt field is incomplete in general.

Radiating2700K actual values independently recovered:
- Heater gas duty914859.7602031655J/kg fresh feed.
- Outlet NO+NO2:0.9795828183670688mol/kg fresh feed.
- Quotient0.9339279365150621MJ/mol exchanger-outlet NOx.
- Cold-end pair loss33897.63126666872J/kg.
- Endpoint energy residual after that loss0.1369161724J/kg.
- Saved-node solid maximum2259.39105565K.
- Hot/cold bed Ergun diagnostic1245.49/869.53Pa.
- Hot/cold gas-holdup times0.0080310/0.0135978s.

The quotient is not300K product yield, captured nitrate yield, electric efficiency or a matched conventional-process comparison. The calculation's source thermochemistry has a small1000K piecewise-polynomial discontinuity; the finite energy residual and tolerance changes must remain recorded rather than hidden by an exact-energy claim.

## Concrete receipt issue
cold_end_radiation.py and radiating_2700_result.json inherit scope text saying 'insulated radiative ends', although the actual cold boundary radiates. The actual equation is unambiguous and its ledger passes; the stale textual scope needs an explicit corrected receipt rather than silently overwriting prior evidence.

The max_boundary_residual field mixes dimensionless species/temperature and scaled heat-flux conditions. A value near3e-8 is not3e-8W/m2: its heat-flux component corresponds to roughly0.03W/m2. Report dimensional residuals when using this as an admission gate.

## Dominant missing device boundary
The averaged calculation simultaneously assumes gas profiles are quasi-steady in each phase and the solid has negligible cycling amplitude. A real phase period must make both assumptions compatible. Each reversal changes the flow and composition of nonzero residual gas inventory. At2700K this is approximately0.008/0.0136kg per m2 of hot/cold bed for G=1kg/(m2 s), excluding headers/heater/valve dead space. A1s blow therefore has bed-inventory scales of about0.8%/1.36% of its through-flow; a0.1s blow has8%/13.6%. These are inventory ratios, **not** computed losses: displacement, purge, recycle and transient chemistry determine the actual yield/energy. They cannot be set to zero merely because the averaged solid resets.

A finite-period reacting calculation must track those inventories and solid storage to periodic state, plus provide particle heat capacity/conductivity to test the isothermal-grain approximation. Current models stipulate opaque-black Rosseland diffusion and source-derived geometry, not measured high-temperature effective conductivity of this material/geometry. Insulated hot end, finite-particle gradients, gas/solid reaction at surfaces, heater formation residence, electrical coupling, capture and startup/reset remain process obligations. The nonzero cold-end radiation test addresses one obligation only.

This is not a universal rejection of thermal nitrogen fixation, zirconia beds, or the lower-temperature candidate. The immediate scientific value is a consistent favorable averaged model and an explicit next discriminating finite-period/inventory boundary, not proof of practical superiority.

## Resources and provenance
The independent operation took0.0643349s internal wall time, peak process RSS40888KiB on Linux; CPU accounting and host-wide overhead were not measured. No spending, external source acquisition, full BVP, hardware or physical experiment occurred. saved_ledgers.json pins SHA-256 identities of every inspected checkpoint and equation source. Common Cantera/model source remains a shared assumption.
