# Independent audit: reactive thermal-NOx recuperator

## Finding

The short 2400 K handover, 0.02 m exchanger case survives an independent numerical cross-check of the stated, favorable thermal model. This does not validate a device or nonthermal plasma mechanism. Two nominally successful longer-case outputs fail their boundary/energy residuals and must not be used as successful calculations. The 0.5 m integrations remain numerical failures, not physical exclusions.

The best independently checked result is 1.130726328 MJ per mol NO+NO2 at the explicit 300 K intermediate-product endpoint, before electrical efficiency, quench actuation, pumps, wall limitations, capture, and conversion to nitrate. This is not a finished-fertilizer or plant SEC.

## Source and independent method

Audited sources were `counterflow.py`, `quench_screen.py`, `CONTRACT.txt`, `sources/air.yaml`, and their original JSON results. Frozen copies of the three code/contract files and SHA-256 hashes are included in this folder. No original solver functions were imported by the independent executable.

`check_one_case.py` uses the same Cantera 3.2.0 thermochemical/kinetic data but an independently written spatial energy formulation. Both the initial 3100-to-2400 K prescribed quench and exchanger use Radau, rather than the source BDF method. The independent quench uses relative tolerance 1e-10; exchanger uses 1e-8, compared with the original exchanger's 1e-7. Energy is integrated as absolute specific enthalpy scaled by 1e6 J/kg, not temperature.

For hot-flow coordinate x, define Q as cumulative heat transferred per kg and H as hot enthalpy. Then H = h_quench - Q and h_cold = h_cold,out - Q. Equivalently h_hot - h_cold is constant everywhere. Cantera HPY inversion obtains each temperature. This checks the original explicit chemistry-temperature energy coupling by a different thermodynamic state representation.

An initial implementation using unscaled cumulative Q as the energy state suffered finite-difference/Jacobian scaling warnings and was interrupted without accepting a result. Its source and warnings are retained. Changing to scaled absolute enthalpy resolves that numerical problem; the complete accepted check took about 2.18 seconds. This is a numerical implementation issue, not physical evidence.

## Equation and unit audit

1. Conserved mass: for steady constant-area flow G = rho*u [kg m^-2 s^-1]. Species conservation is dY_k/dx = W_k*omega_k/G. Cantera's omega_k is kmol m^-3 s^-1 and W_k is kg/kmol, so the result is 1/m. The source equation has the correct mass-flux denominator; introducing another density division would be wrong.

2. Local exchange per unit conserved mass is qprime = 4*U*(T_hot-T_cold)/(D*G), with units J kg^-1 m^-1 for equal circular channels and equal mass flows. Conductances in series give 1/U = D/(Nu*k_hot) + D/(Nu*k_cold) + wallR. The source uses the explicit favorable assumptions Nu=3.66 and wallR=0.

3. Counterflow signs are correct. In the coordinate following the hot flow, dh_hot/dx = -qprime and dh_cold/dx = -qprime. The cold stream flows in the opposite physical direction. Consequently h_hot-h_cold is invariant, not h_hot+h_cold. Both source temperature derivatives have the proper exchange sign.

4. Reactive hot temperature: dh_hot/dx = cp*dT_hot/dx + sum(h_k*dY_k/dx). Here h_k = partial_molar_enthalpy_k/W_k in J/kg. Thus dT_hot/dx = [-qprime - sum(h_k*dY_k/dx)]/cp. This source equation correctly includes reaction formation enthalpy and does not create free heat. The cold equation assumes frozen composition, so its chemistry term is intentionally absent.

5. All enthalpies are J/kg of original conserved gas mass. Retained product is 1000*sum(Y_k/W_k) for NO and NO2: mol/kg, because W is kg/kmol. Dividing net J/kg by mol/kg gives J/mol, followed by 1e6 to obtain MJ/mol. N2O is not counted as useful NOx in this denominator.

6. Net model heat is h_hot,3100K-equilibrium - h_fresh,300K - recovered_heat. Heat removed in the very fast initial quench is not credited, nor is downstream cooling after the finite recuperator. The independent explicit 300 K tail confirms that distinction.

7. Negative nominal hot-minus-cold temperature gaps are not, by themselves, a sign error or second-law violation. At the quenched inlet the stream still contains radicals; reaction can reheat it. Local qprime reverses when the cold-feed side is hotter. Local conduction still transfers heat from the locally hotter to locally cooler gas. Rejecting every crossing would incorrectly exclude these reacting solutions. Conversely, this means handover temperature is not a guarantee that the reacting gas will remain below that temperature.

## Independent numerical case

Parameters: dry 79/21 molar N2/O2, 1 atm chemistry, 3100 K equilibrium initialization, initial quench 1e8 K/s to 2400 K, D=1 mm, G=1 kg/m2/s, L=0.02 m, zero wall resistance.

- Hot outlet: 654.210945732 K. Original: 654.211063219 K.
- Cold outlet: 2570.634879584 K. Original: 2570.634870738 K.
- Hot maximum: approximately 2676.407 K, demonstrating reheat above the 2400 K handover.
- Minimum local hot-minus-cold gap: -170.634880 K.
- Recovered enthalpy: 2,694,307.012 J/kg. Original difference: +0.011408 J/kg.
- Retained NO+NO2: 1.23322721449 mol/kg. Difference from original: 7.33e-9 mol/kg.
- Recuperator NOx survival: 0.780515284 of the post-quench amount.
- Net model heat: 1.13072632825 MJ/mol. Difference from original: -1.60e-8 MJ/mol.
- Cold inlet boundary residual: +8.06e-10 K.
- Terminal global energy residual: -8.13e-7 J/kg.
- Maximum reconstructed enthalpy-invariant residual: 0.003370 J/kg, below 1e-9 of gross heat, including HPY inversion tolerance.
- Hot mass-fraction sum drift: 7.77e-16. Minimum species fraction: -3.44e-16, numerical roundoff.

Outlet and delivered species vectors are included in `one_case_result.json`, not just scalar yields.

## Explicit delivery endpoint and cold-feed validity test

The original finite exchanger terminates above 300 K and therefore does not by itself meet the contract's delivered endpoint. An explicit downstream cooler at 1e4 K/s was added only in the independent check; its removed enthalpy receives no heat-recovery credit.

For the checked case, cooling from 654.211 K to 300 K rejects 367,001.200 J/kg. NO+NO2 remains 1.23322721449 mol/kg within the reported precision. This confirms this case's intermediate-product denominator at 300 K under the same small air mechanism. It does not validate realistic tail oxidation, capture, or nitrate conversion kinetics.

Frozen fresh air at 2570.635 K deserves a chemistry check, not an assumption of perfect inertness. A one-way diagnostic reacts fresh inlet air along the computed frozen cold-temperature profile, in its correct flow direction, with G=1. It is not a fully coupled replacement and receives no additional yield or energy credit:

- Cold residence time: 6.272 ms; hot residence: 4.520 ms.
- Cold-side NO+NO2 generated: 0.000929780 mol/kg, 0.0754% of the checked hot product.
- Largest cold mass-fraction change: 0.000124095.
- Additional outlet enthalpy at the prescribed same temperature: 1832.258 J/kg, 0.0680% of recovered heat.
- As a distinct limiting comparison, equilibrating the same frozen-air outlet enthalpy adiabatically gives 2478.356 K, about 92.3 K lower. That is an equilibrium comparison, not the millisecond finite-rate prediction.

Thus frozen cold composition is not exact, but this one-way kinetic test does not expose a large spurious benefit in this short case. It is not a certificate for all lengths, temperatures, rates, alternative mechanisms, or a fully coupled reactive cold channel.

## Root acceptance failure

The original code's `mismatch` uses the last point of an integration even when an event terminates it early. A sign bracket and Brent x-tolerance do not alone certify a valid boundary-value solution. The final assertion checks only full length, not the endpoint boundary residual or energy residual. In a stiff shooting problem, tiny changes in shot or integrator error can spoil the endpoint condition despite nominal root convergence.

The original saved outputs include:

- Tq=2400 K, L=0.1 m: cold-inlet residual -32.791681 K; heat imbalance +33,066.698 J/kg. This is not an accepted solution and its 1.182175 MJ/mol must not support a claim.
- Tq=2100 K, L=0.1 m: cold-inlet residual -0.015154 K; heat imbalance +15.143570 J/kg. It also fails a strict 1e-3 K boundary / 1e-6 relative-energy gate.
- All three L=0.5 m cases: final length assertions failed. These are numerical failures only, not no-go physics.

Recommended acceptance requires successful full-length integration, explicit endpoint-temperature tolerance, explicit energy-invariant tolerance, species conservation/nonnegativity within specified numerical tolerances, and a convergence or independent-method check for any candidate conclusion. Event-truncated shots may help search, but must never themselves be treated as solutions. A multiple-shooting or collocation formulation is a reasonable route if longer lengths remain ill-conditioned.

## Actual 1800 K length tradeoff

This subsection is a read-only calculation from the two accepted original 1800 K profiles, not an additional independently solved grid.

Increasing length from 0.02 to 0.1 m:

- Recovery rises from 2.012590 to 2.198796 MJ/kg, +186.205 kJ/kg or +9.252%.
- Retained NOx falls from 1.548673 to 1.447977 mol/kg, -6.502%.
- Net heat per retained mol falls only from 1.340605 to 1.305237 MJ/mol, -2.638%.
- Hot peak rises from 2139.102 K at x=1.4 mm to 2394.636 K at x=5.25 mm. Reheat above handover rises from 339.102 to 594.636 K.
- The initial reverse-transfer interval extends from about 0.562 mm to 4.315 mm.
- Friction-only hot pressure-drop estimate grows from 134.899 to 740.589 Pa, a factor of 5.490.

This directly challenges the simplistic statement that a quench to 1800 K keeps subsequent NO destruction negligible. More recovery can lengthen residence, increase reheating, and sacrifice product; the model's energy-per-product improvement is much smaller than its recovered-heat improvement.

## Pressure and transport diagnosis

The source accumulates 32*mu*G/(rho*D^2) along each side, the fully developed circular laminar friction-pressure-gradient magnitude. Its units and sign as a positive diagnostic are correct. It is not a self-consistent variable-pressure solution, total device pressure loss, or pump-work calculation.

In the independently checked case:

- Friction-only drops: hot 237.488 Pa; cold 202.048 Pa, small compared with 101325 Pa.
- Reynolds ranges: hot 12.30–30.94; cold 12.40–53.68. Laminar flow is internally plausible.
- Hot-stream momentum-acceleration correction G^2*(1/rho_out - 1/rho_in) is -5.179 Pa, a modest pressure-recovery term not included in the original friction-only number.

Temperature-dependent properties are used. However, inlet/thermal development, manifold and turning losses, actual walls/contact resistance, axial conduction, leakage, materials limits at 2000–2700 K, heat loss, pressure feedback on chemistry, and pumping work remain outside this calculation. Nu=3.66 should be presented as an idealized fully developed assumption, not a demonstrated exchanger conductance. Zero wall resistance is a favorable bound.

## Bottom line

The independently checked short-case heat-recovery benefit is not an arithmetic or counterflow-sign artifact. The larger unsupported claim would be practical competitiveness or robust preservation merely from the handover temperature. The audit finds a real shooting-acceptance bug, supplies one trustworthy same-model numerical cross-check, closes that case's 300 K endpoint explicitly, and quantifies reaction-driven reheating and the recovery-versus-product tradeoff. It does not establish a realizable reactor/exchanger, reproduce a seven-reaction 2026 plasma/CFD model, or establish electrical/finished-product superiority.
