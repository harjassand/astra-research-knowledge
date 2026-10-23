# Independent challenge: aerodynamic cooling and complete reset

## Finding

The load-bearing endpoint inequality survives an independent, exact-arithmetic check. In the declared six-species, fixed-inventory, fully relaxed steady-flow reset contract, static expansion alone cannot finish the reset without transferring stagnation enthalpy out of the processed stream. The required net outward heat plus shaft work is at least **1.407672705615 MJ/kg fresh**, using the stored binary64 endpoint data.

This is **not** a lower bound on irrecoverable loss, electrical energy consumption, or the whole-cycle energy input. Heat exported from the processed stream may be recovered by another stream. Nor does it exclude a cooled nozzle, a turbine, staged regeneration, or a changed material/energy contract.

The separate experimental comparator has a significant interpretive caveat: conditional ballast-power lower bounds can be calculated, but their ratio does not bound the actual improvement in wall-plug SEC.

## Independent methods and checks

Run `python nitrogen_cycle5_20261022/nozzle_independent/check.py` and `python nitrogen_cycle5_20261022/nozzle_independent/comparator_check.py` from the workspace root.

Neither script runs a flow trajectory or chemical integration. The principal checker does not import the original admission calculation, `ThermoKernel`, SciPy, or an LP solver.

1. An exact `Fraction` primal/dual LP certificate is constructed directly from the binary64 numbers stored in the admission result. The original atom and count matrices are checked explicitly.
2. The pinned NASA7 coefficient table is evaluated independently with scalar 80-digit arithmetic. The normal shock is solved for downstream temperature, rather than the original calculation's downstream velocity.
3. Fifteen separate closed-form calorically perfect nozzle/shock cases cover three heat-capacity ratios and five upstream Mach numbers, including weak shocks. They test mass, momentum, energy, total-pressure and entropy identities independently of the NASA implementation.
4. Exact Bernstein-basis positivity certificates establish positive species heat capacities on the model's 200–1700 K domain. Branchwise monotonicity and a direct splice-to-cap comparison establish that each species' largest endpoint enthalpy in that interval occurs at 1700 K. N2 below 300 K remains the source's existing extrapolation, not newly validated physics.
5. Exact-decimal experimental-table arithmetic checks the four-species flow contraction and conditional ballast inference. A counterexample tests the validity of comparing the resulting lower bounds.

## Exact endpoint certificate

Let c be the six stored molar enthalpies at 1700 K, and n the endpoint mole inventory ordered N2, O2, N, O, NO, NO2. Let aN and aO be the stored atom totals, Nmax the upper allowed NOx count, and Ncap and Ocap the atom-species caps.

An exact dual witness is

- λN = cN2/2 and λO = cO2/2;
- μ = cNO − λN − λO;
- νN = cN − λN and νO = cO − λO.

All inequality multipliers are positive. Their species-wise majorant is exact for N2, O2, N, O and NO. Its NO2 slack is cNO + λO − cNO2 = 56,522.23425404456… J/mol, also positive. Therefore

c·n ≤ λN aN + λO aO + μ Nmax + νN Ncap + νO Ocap = B.

A primal witness attaining B exactly sets N=Ncap, O=Ocap, NO=Nmax, NO2=0 and assigns the remaining atoms to N2/O2. It is nonnegative and satisfies the lower NOx count. Thus the rational primal–dual gap is exactly zero, not a numerical solver residual.

The exact stored-data bound is

H0 − B = 1,407,672.7056155034297744616113316971413380231410184… J/kg fresh.

The reported floating bound differs by about 2×10⁻¹⁰ J/kg. The optimum is deliberately favorable: it permits 101% of the original hot NOx count and the most enthalpy-rich allowed endpoint allocation. It is an endpoint envelope, not an attainable chemistry claim.

This is rigorous arithmetic for the stored LP inputs. It is not a rigorous uncertainty interval for thermochemical coefficients, atom inventories, omitted species, or physical model validity. The `T≤1700 K` statement is established on the declared caloric-model temperature domain; it does not license extrapolating the polynomials to arbitrary lower temperatures.

## Nozzle, shock, entropy and recovery

Independent properties agree with the reported hot and 1700 K enthalpies to better than 5×10⁻¹⁰ J/kg. Across the five expansion examples, every reported checked quantity agrees within 9×10⁻¹⁰ in its displayed SI unit. The independent shock states are compressive and subsonic downstream, with positive entropy production and lower total pressure. Conservation/entropy identities close to about 2.4×10⁻⁷⁹ in the independent high-precision arithmetic.

The source's ordinary ideal-gas relations are consistent:

- nozzle: h(T)+v²/2=H0 and s°(T)−R ln P=constant;
- shock: mass, momentum and stagnation enthalpy are conserved;
- shock entropy: Δs=−R ln(P02/P0)>0;
- ideal downstream diffusion restores the same 2700 K stagnation temperature, not a relaxed cold endpoint.

The shock temperatures remain about 2580–2642 K even when the incident static temperatures range from 1700 down to 500 K. Those values are reference-model results, not reacting-flow measurements.

The passive recovery-temperature threshold r≤[h(1700)−h(Tstatic)]/[H0−h(Tstatic)] is algebraically correct. It rises from zero at static 1700 K to approximately 0.52217 at static 500 K. Recovery factors 0.85 and 0.89 remain illustrative low-temperature-air inputs, not validated reacting-gas bounds. Adiabatic recovery temperature is not the actual temperature of an actively cooled wall.

NASA's [normal-shock equations](https://www.grc.nasa.gov/WWW/BGH/normal.html) and [isentropic relations](https://www.grc.nasa.gov/WWW/BGH/isentrop.html) provide the independent perfect-gas reference. The broader calorically imperfect conservation formulation appears in [NACA Report 1135](https://www.nasa.gov/wp-content/uploads/2023/03/equations-tables-charts-compressibleflow-report-1135.pdf). These references do not validate the source's reacting, rapid-expansion or surface physics.

## Meaning of the compression columns

Rmix×300×ln(Pout/Pin) is reversible isothermal compression work at 300 K for the assumed unchanged composition. It is not adiabatic compressor work, measured electrical power, or a universal floor over all nozzle/cooler/diffuser architectures.

The static-pressure-cooling route and normal-shock-plus-ideal-diffuser route are alternatives. Their costs must not be added. In the second reference route, the pressure-restoration expression is exactly 300Δsshock. This identity is a useful algebra check, not an admission of the cooling hardware or a whole-cycle result.

All nozzle pressures are below the helper state evaluator's 0.5 atm pressure domain. The admission script uses pressure-independent ideal-gas caloric polynomials rather than that evaluator, so this is an explicit ordinary thermodynamic extension, not an admitted low-pressure kinetic or transport closure.

## Smallest scientific correction

State the result as a **steady-flow stagnation-enthalpy transfer requirement**, with net outward heat/work signs, the complete material contract, and no uncounted carrier or stored-energy accumulation. Do not call it energy “lost,” unavoidable external heat rejection, or net electrical SEC.

For a closed material batch, internal energy U rather than H is the relevant state function, and all pressure-volume/boundary work must be included. An illustrative calculation using the same stored conventions gives U0−Ufinal,max≈1.113411431 MJ/kg rather than 1.407673 MJ/kg. This does not weaken the stated steady-flow result; it prevents applying that number to a different boundary convention.

## Experimental comparator challenge

For the supplied 80/20 triplicates, arithmetic group means are 158.913333 W with the nozzle and 198.583333 W without it. The reported discharge power is not total supply input.

If 135 mA is the time mean of the same current flowing through the 25 kΩ ballast over the matching averaging interval, Jensen gives Pballast≥R(mean I)²=455.625 W. A 135 mA RMS interpretation gives equality. A setpoint, peak, or current averaged only over active discharge intervals does not establish that lower bound. The series-current identity and effective resistance must also hold.

With only N2/O2/NO/NO2 products and no uncounted flow, atom balance gives Fin=Fout(1+xNO2/2), where xNO2 is the outlet mole fraction. Thus inlet-flow-based SEC is multiplied by 1+xNO2/2. This gives:

- Discharge-only, flow-corrected SEC: 2.967792 versus 3.830736 MJ/mol, a 22.5268% reduction.
- Arc plus constant-135 mA ballast reconstruction: 11.476835 versus 12.619888 MJ/mol, a 9.05755% reduction.

The latter comparison is conditional, not measured wall-plug performance. **The ratio of two independent lower bounds is not a bound on actual relative savings.** The checker supplies a concrete counterexample: nozzle current alternating equally between 35 and 235 mA has the same 135 mA mean but 705.625 W ballast loss, versus 455.625 W for constant 135 mA without the nozzle. The corresponding SEC ordering reverses, while both Jensen lower bounds remain true. This waveform is a mathematical counterexample, not an assertion about the experiment.

The displayed 2.967792/3.830736 figures apply the contraction formula to the mean percentages. Averaging each separately corrected replicate production rate first, then dividing mean power by that rate, instead gives 2.96779317794252 and 3.83073687434212 MJ/mol. Both definitions are retained in the checker; this tiny aggregation difference is not an arithmetic disagreement. The counterexample uses the latter, mean-corrected-rate definition. These calculations retain the paper's 24 L/mol convention and are not substituted for its weighted statistics. The paper and SI are identified by DOI [10.1016/j.cej.2022.136529](https://doi.org/10.1016/j.cej.2022.136529). The portable checker reads only the source manifest for the historical SI PDF hash and does not locally reverify the PDF or extracted text. The numeric rows are exact decimal transcriptions embedded in code. The original text-hashing checker and result are preserved as `comparator_source_text_hash_v1.py` and `comparator_source_text_hash_v1_result.json`.

## Heat-grade formula review

The parent's `heat_grade.py` was inspected, not rerun. Its formula hFresh(2700)−hFresh(Twall)+saved positive isothermal reaction duty is correct for the explicitly fixed heater history and passive, composition-preserving fresh-feed preheat class. Differences between caps reduce exactly to hFresh(1700)−hFresh(Twall).

Use “internally equilibrated fresh feed,” not “chemically equilibrium fresh feed”: the code preserves 79/21 N2/O2 composition during preheat. The wall-temperature ceiling applies only when all useful passive recovery to that feed is through walls no hotter than the cap, without chemical heat release or work/nonthermal conversion. It is not a bound on upstream hotter recovery stages or on a design containing only a local cold spot.
