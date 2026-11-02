# Optional native resource comparison for the exact-Clifford K13 route

Governing comparator: UNTOUCHED_K15_AND_NATIVE_DICTIONARY.md proves that the ORIGINAL source already has K≤15 with no basis/noise change. The K180 ratios below are historical sufficient-certificate comparisons, not gains over the strongest now-available method. Against K15, K13 gives only a (13/15)³≈0.651 peak-coefficient ratio and a charged edge-Clifford hook tradeoff.

Companion to DIRECT_K13_GIBBS_CERTIFICATE.md. This compares explicit sufficient implementations, not hardware minima. Geometric/source binding is independently audited in the companion finite-star receipt. Explicit native source-contact/dictionary bounds are supplied in UNTOUCHED_K15_AND_NATIVE_DICTIONARY.md; an absolute useful tolerance is not claimed.

## Fixed resources and actual changes

Same underlying abstract cells, number of data qubits, number and labels of Hamiltonian checks, source violation energies, spatial dimension/positions, onsite bath dimension, and ideal equilibrium/overwrite/read contract. The edge basis is changed by a block-local Clifford on at most3 qubits. There is no ancillary cone volume, no new gauge sector, and no source temperature penalty.

| Quantity | Previous conservative certificate | New certified bound |
|---|---:|---:|
| maximum actual check weight bound |180|13|
| Z-check weight bound |15|10|
| total checks per data qubit |64|16|
| clock overlap including itself |11341|196|
| largest clock Hilbert dimension |180|13|
| one new native prefix in old data frame |—|≤39 old qubits|
| added data qubits |0|0|
| source Gibbs cold-energy multiplier |1|1|

A clock remains one finite-dimensional native site per check. Its number of levels/transitions decreases; site-count conventions must not confuse this with removing one site per discarded clock level. For heterogeneous lengths, sum K_a and sum K_a² enter the actual total transition/onsite coefficient budgets, as in the admitted compiler.

## Uniform finite-temperature clock check (no monotonicity shortcut)

Let M=max K_a≥3. Keep the admitted heterogeneous resonant choice

 t_a=J M² K_a/(2 eta²),  g_a=eta t_a/M,
 x=Dbar eta²≤1/64,

where −J S is the effective Pauli coefficient and the violation energy is2J. Assume beta J≥1 and eta²≤1/64. The path gap obeys mu_a≥2JM/eta², while the common time tilt is b=16Dbar JM. Consequently

 mu_a−b ≥(7/4)JM/eta².

The required full-circle-wrap condition follows from

 M(M−1) exp[−(7/4)(beta J) M/eta²] ≤eta²,

which holds uniformly for M≥3 under these assumptions: the left side decreases with M, and its M=3 value is bounded by 6 exp[−21/(4eta²)]≤eta². Thus lowering M does not rely on an incorrectly assumed monotone wrap margin inherited from M=180.

The winding-tail relative error is bounded uniformly by

 exp[2/9−(beta J)M/(2eta²)] ≤ exp[2/9−3/(2eta²)].

For the ordinary excursion tail delta_a, take c_a=t_a/K_a²≤mu_a/4. The spectral resolvent bound M0,a(c_a)≤(4/3)M0,a=(4/3)J K_a gives

 beta delta_a ≤ (4/3)(beta J)M exp[−(beta J)M/(2eta²)]
               ≤4 exp[−3/(2eta²)] ≤4 exp(−96).

All thermal clock sectors, including wraps, remain in these estimates. The multi-rod margin still depends on beta J and x; the admitted heterogeneous moment bounds M0≤JM and M1≤eta²/M cancel the M factor in their product. Use a common conservative event envelope, not an unsupported zero-event approximation.

## Peak energy and source activity

At the same J and eta,

 t_peak,new/t_peak,old=(13/180)^3=2197/5832000≈3.76715×10^(−4).

Thus the sufficient peak internal coefficient is about2654 times smaller **at fixed eta**, with no compensating source cold penalty. Keeping the old eta also makes x_new≤x_old under the new overlap certificate. This comparison does not assert that the old loose certificate was a lower bound on implementation cost.

With a common admitted cold/event/tail envelope and fixed conservative source-support exponents, the generic activity remains

 q_native≤M^(b_c) d_B^(b_B) exp(beta delta_bar b_c)[exp(beta v_dict)−1].

The M-only factor decreases by (13/180)^(b_c). A new data Pauli maps to at most3 old edge qubits, and a length13 prefix to at most39. Thus this conversion fits the previous length180 data-word envelope. Source syndrome/decoder traces and check labels are unchanged. The finite source dominance check should retain the old conservative contact/adjoint/filling bounds wherever they already dominate these inputs; it must also retain the actual matrix dictionary norm and bath range. A Clifford permutes data Pauli words without multiplying their coefficients, but native clock matrix dimensions and prefix contact counting must still be entered explicitly.

Accordingly the old recorded K180 local-dimension/peak-coefficient obstacle is removed already by the untouched K15 baseline; K13 is only an optional further re-encoding. An absolute useful value of v, a laboratory operating temperature, or a simultaneous optimized total-volume/noise frontier is not supplied by these relative ratios. If common-source domination is not yet audited, report that specific remaining gate instead of declaring the old v tolerance unchanged.

## Preparation and access remain unchanged

The stabilizer source equality holds for every beta; the compiled native retention theorem is still restricted to its admitted finite-temperature parameter region and bounded local perturbations/bath. Gibbs preparation, noisy WRITE, and autonomous READ/WRITE are not made easier by this algebraic certificate alone. The quantum memory is still initialized by the stated ideal logical overwrite of its actual joint Gibbs resource.
