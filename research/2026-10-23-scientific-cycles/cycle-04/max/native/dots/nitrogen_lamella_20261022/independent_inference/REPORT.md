# Independent inference challenge

## Defects and vulnerable inference steps first

1. **The radiation time/temperature contract needs a qualification.** The existing 1700 K / 110 microsecond calculation cannot bound radiation over the actual trajectory from its 2700 K inlet: 1700 K is not an upper temperature on that initial segment. Also, the endpoint theorem does not require its heat export to occur by 110 microseconds. That deadline must be an additional design requirement. The saved below-threshold window itself is only about 51–112 microseconds, not a full 110 microseconds. This does not rescue ordinary NO. A small read-only correction using the same finite catalogue at a 2700 K cap gives at most **1.2858 kJ/kg fresh over 110 microseconds**, versus 0.7248 kJ/kg at 1700 K, still about 42-fold short of 53.995 kJ/kg. This remains a conditional finite-model LTE NO-only inequality with the parent's unresolved catalogue-integrity warning, not an all-gas or nonequilibrium bound.

2. **Packet retention cannot be called net new product.** The initial 1.905098411 mol NOx/kg fresh consists of 1.031412321 from the hot fresh stream plus **0.873686090 from the returned stream**. N48's final packet retention is 99.945907%, but subtracting the input-return inventory gives 1.030381796 mol/kg fresh, or 99.900086% of the initial hot-stream NOx. Even that subtraction is an inventory balance, not a demonstrated steady process yield: the returned outlet stream, composition and reset have not been reclosed. The 1.01-times-packet ceiling permits 0.019051 mol/kg fresh additional NOx, about 1.847% of the hot-stream initial NOx, not a 1% fresh-product increment.

3. **Strict saved-state positivity is not established.** N24 has 2 saved states with negative mass fractions; N48 has 10. Minima are -2.62e-26 and -7.23e-16, respectively. These are tiny and do not demonstrate a physically significant failure, but they invalidate a literal all-saved-states strict-positivity claim. The initial one-sided zero O abundance also makes some logarithmic entropy expressions undefined/infinite. A finite positive-state check must exclude and count these cases rather than silently floor them. Signed Newton continuation, successful BDF termination and tiny energy residuals are not positivity or entropy theorems.

4. **Source-binding is incomplete, not demonstrably incorrect.** The saved endpoint certificate hashes its three listed sources correctly, but omits the thermo manifest from which its script reads the gas constant. The trajectory NPZ/JSON records flags and numerical states but not the generating source hashes. This audit records the current script/helper/cache/manifest/trajectory hashes. That binds the audit to current bytes, not retrospectively to the precise source bytes used when a trajectory was generated. No changed-source error was found.

## Load-bearing distinction: temporary cooling is not relaxed-endpoint admission

The N48 saved history has these observations:

- Last saved point above the initial crossing: 50.427893 microseconds, maximum 1700.071746 K.
- First saved point below: 51.427893 microseconds, maximum 1699.142859 K.
- Lowest saved maximum: 1693.628708 K at 68.427893 microseconds.
- Last saved below: 111.427893 microseconds, maximum 1699.878925 K.
- First saved above again: 112.427893 microseconds, maximum 1700.047572 K.
- At 1 ms: essentially uniform 1724.578683 K.

These are saved mesh-state values and crossing brackets, not exact event times or a continuum maximum certificate. N24 reproduces the behavior; its lowest saved maximum is 0.090623 K higher. Two grids and their close final temperatures are useful numerical corroboration, not a spatial-error bound.

During N48's saved below-1700 window, O radical inventory declines from **0.344559 to 0.225509 mol/kg fresh**, versus the endpoint certificate's **0.003** cap. N is 1.907e-7 to 1.366e-7 mol/kg fresh, also above its **1e-7** cap. At the minimum temperature O is 0.305017 mol/kg fresh, about 102 times the permitted relaxed inventory. Thus there is no contradiction between the temporary cold one-temperature trajectory and the endpoint ceiling. Chemical energy remains stored in radicals, and its subsequent release reheats the adiabatic packet. Only by 1 ms do these saved radical inventories satisfy the specified caps; the temperature then fails the cap.

## Independent finite entropy check, with full cross terms

`check_saved_path.py` reads the existing N24 and N48 histories; it never evaluates an ODE time step or writes a trajectory. It reconstructs ordinary Maxwell–Stefan flux, the same explicitly restored native thermal-diffusion vector, Soret mass flux and reciprocal Dufour reduced heat flux. For strictly positive endpoint compositions it evaluates

    sigma_face = q_reduced * Delta(1/T)
                 - sum_i j_total,i * Ri * Delta(log Xi).

Here j_total includes Soret and q_reduced includes Dufour. This is the finite-face entropy expression after the receiving enthalpy secant cancels the standard-potential jump. It is not the old no-Soret formula. Near-equal logarithms use log1p. The known source-splice/secant floating-roundoff qualification remains; this check does not independently turn the secant into an exact interval identity.

Sampling 81 saved states from each path checks 1,851 N24 and 3,783 N48 strictly positive finite faces. It excludes 12 and 24 faces with a nonpositive endpoint, respectively. No negative value larger in magnitude than the stated diagnostic tolerance is found. Raw minima are -1.35e-29 and -1.54e-29 W/(m² K) in effectively uniform late states; those roundoff-scale signs are retained rather than reported as exact positivity. The maximum local restored Schur ratio is 0.0001494371 on both paths.

The total ideal-mixture entropy is additionally computed at every nonnegative saved state without flooring zeros. Every adjacent pair for which both states are nonnegative has increasing entropy: smallest increments 4.51e-10 and 5.32e-10 J/(m² K). End-to-end entropy rises from 0.726913059 to about 0.77482784 J/(m² K). Negative saved states are not assigned physical logarithmic entropy.

**What this establishes:** sampled accepted-state evidence for the actual restored full-cross closure, supplementing the earlier no-Soret-state coefficient tests. **What it does not establish:** universal arithmetic-face entropy stability, positivity preservation, BDF entropy stability, strict behavior at zero support, unsampled-time bounds, an independently certified chemistry entropy theorem, or experimental transport accuracy. A constitutive positive-semidefinite block is not by itself a proof of arbitrary finite-face discretization entropy.

## Endpoint theorem: supported wording and limits

The 53.995135224 kJ/kg-fresh result is supported as a **conditional relaxed endpoint heat-export lower bound** for the specified packet and isobaric enthalpy contract, with:

- the pinned six-species NASA model and admitted thermochemical temperature domain;
- every local equilibrium temperature no higher than 1700 K;
- total packet NO+NO2 no more than 1.01 times its initial packet value;
- total N no greater than 1e-7 and total O no greater than 0.003 mol/kg fresh;
- no additional species, external work port, nonthermal final reservoir or changed mechanical boundary.

The stable-species baseline at unchanged packet NOx is 56.501455 kJ/kg fresh; the relaxation of the NOx and radical caps is what gives 53.995135 kJ/kg. The exact rational script establishes signs and endpoint arithmetic for stored binary coefficient values, not experimental exactness of thermochemistry. Its temperature monotonicity premise is supported separately by float64 polynomial extrema checks over 200–1700 K; it should not be described as a wholly formally verified empirical theorem or a statement below 200 K. For internal-energy rigid boundaries, the relaxed number is different: 102.686116 kJ/kg fresh.

This necessary endpoint export is not a process energy consumption, an available-work claim, or proof that the proposed apparatus has an advantage over ideal rapid once-through quenching. Allowing greater useful NO production, other species, a work port, or a different endpoint changes the feasible set. Finite vibrational storage may change the transient but cannot erase the ultimate export requirement once the stated relaxed endpoint is reached.

## Compressible comparison and remaining physics

The terminal sparse compressible result was read, not rerun. It **did not finish the requested 150 microsecond horizon**: its explicit 120-second integration budget stopped it at 127.515380 microseconds. It nevertheless observed a minimum maximum temperature of 1693.507388 K, first saved all-gas-below at 51.058834 microseconds, and reheating to a final maximum of 1702.505569 K. This is useful partial one-temperature pressure-loaded-slab corroboration of a cool-and-recross event, not horizon completion, a steady jet, or physical feasibility. Its invariant is U+KE+P0*width, not the low-Mach enthalpy alone.

Numerical failure of alternative face laws or the dense attempt is evidence about implementation/solver conditioning under those choices, not evidence that the molecular mechanism is impossible. Conversely, a successful local one-temperature trajectory is not an admission of internal-mode equilibration. The vibrational report identifies relaxation times comparable to the cooling time and no controlled error small relative to the approximately 6 K margin. Injector formation, shear/momentum losses, surface heat exchange, finite cooling area and periodic inventory/reset remain unqualified.

The radiation result supports neither a demonstrated photon path nor all-gas exclusion. NO-only models are far too weak under their stated assumptions; NO2 completeness, N2/O2 forbidden and pair channels, atomic channels, nonequilibrium populations and density history remain relevant to a complete exclusion. Do not convert "NO is too slow" into "all gas radiation is impossible."

## Separate four ledgers

- **Internal proof/check status:** conditional endpoint algebra and exact coefficient arithmetic; local constitutive Schur admission; saved-path, not universal, finite entropy and numerical checks.
- **Historical originality:** not established by these calculations. Maxwell–Stefan transport, lamellar molecular mixing, reciprocal thermal transport and endpoint energy maximization are established ideas. A useful particular combination or implementation is not automatically a new principle.
- **Useful implementation:** explicit moving material-cell geometry, mechanical contracts, actual-source endpoints, cross-term restoration disclosure, source audit and concrete transient timing are reusable progress. Rejected numerical variants are diagnostic information, not performance gains.
- **Physical performance:** remains unqualified at whole-process level. The evidence is a conditional thermochemical burden and a local one-temperature cool/reheat calculation, not apparatus realization, net yield, energy superiority or a research-amplification result.

## Artifacts and reproduction

- `saved_path_audit.json`, `check_saved_path.py`: packet accounting, threshold timing, radical predicates, full-cross finite entropy, local Schur tests and current source hashes.
- `hot_radiation_check.json`, `check_hot_radiation.py`: finite NO catalogue cap at both 1700 and 2700 K.
- `MANIFEST.sha256`: hashes of this independent audit's files.

From the project root:

    PYTHONPATH=nitrogen_quench_recovery_20261021/deps python nitrogen_lamella_20261022/independent_inference/check_saved_path.py
    python nitrogen_lamella_20261022/independent_inference/check_hot_radiation.py

No trajectory was integrated and no old ledger or parent result was modified.
