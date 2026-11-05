# Certified finite-box AKLT spin-correlation operation

## Result and honest scope

The exact closed-loop sampler has been joined to a physical, experimentally meaningful output: a bounded unbiased estimate of a specified spin-2 AKLT equal-time correlation, with a finite-sample confidence statement that does not assume Markov-chain equilibration. This is classical computation of observables in one explicitly specified finite quantum state. It is not quantum-state preparation, an infinite-volume theorem, a gap theorem, a static-response calculation, or a demonstrated runtime advantage over established loop/worm Monte Carlo.

The decisive join is independently checked in three different ways: exact sphere-moment expansion, exact routed-loop/open-path enumeration, and direct quantum VBS amplitudes. The complete implemented path distribution has also been checked by an independent worker on small boxes, including paths revisiting their endpoints.

## 1. Accessible input and specified quantum state

Input: an open rectangular square-lattice region R, two distinct core vertices i,j, a fixed number M of independent attempts, and a requested failure probability alpha. Each core is physical spin 2. The boundary virtual qubits are assigned the identity operator before applying the AKLT PEPS map V_R:

    sigma_R = V_R I_boundary V_R† / Tr(V_R I_boundary V_R†).

This is a particular mixture of open-boundary AKLT ground states, not an arbitrary boundary condition. An equivalent purification completes every boundary core to degree four with auxiliary spin-1/2 leaves, forms that decorated graph's VBS state, and traces the leaves. Tracing a leaf removes its classical coherent-state edge factor because the sphere integral of (1 - n·m) equals 1.

Preparation cost here means computation of this classical prediction. No physical device is assumed to have prepared sigma_R.

## 2. Exact physical-to-path identity

Let parity(i,j) be the square-lattice bipartite parity difference. The coherent-state upper symbol of S^a for a spin-S site is (S+1)n^a. Therefore, for distinct spin-2 sites,

    <S_i · S_j>_sigma = 9 (-1)^parity(i,j) G_ij.

The factor is 9 for the dot product. SU(2) invariance gives <S_i^z S_j^z> = <S_i·S_j>/3, so the analogous factor for zz against the classical dot product is 3. On site, <S_i²> = 6; the distinct-site factor 9 must not be reused.

After staggering the sphere variables on one sublattice, the classical integral has positive edge factors (1+n_u·n_v). Insert a single distinguished auxiliary factor (1+t n_i·n_j). In the coefficient of t, the source edge belongs to a unique routed component. Removing it produces one oriented edge-simple path p from i to j. The auxiliary edge is distinct even if i,j are physical neighbors, so the path of physical length one is included.

At degree two the normalized sphere moment is delta_ab/3. At degree four it is the sum of three pairings divided by 15. Every closed routed component has three possible colors. Thus a closed loop gamma of length L and r self-contact vertices has activity

    w_gamma = 3^(1-L) (3/5)^r.

For the component containing the source edge, removing that edge leaves

    a_p = 3^(-L_p) (3/5)^r_p.

Here r_p counts internal degree-four vertices and endpoints of physical degree three. Revisited endpoints are allowed. There is no 1/(2L), extra factor 3, or division by 3 for this distinguished oriented path.

The interaction between two components is zero if they share a physical edge, and otherwise contributes 3/5 for every shared vertex. Write delta(p,Gamma) for the product of these factors between p and a closed-loop configuration Gamma. Removing the source component leaves exactly the original normalized closed-loop Gibbs law mu_R, so

    G_ij = sum_{p:i→j} a_p E_{Gamma~mu_R}[delta(p,Gamma)].

There is no estimated denominator and no ratio-of-means bias. At a vertex where one component already uses all physical edges, a second touching component necessarily shares an edge and is rejected; this also enforces the maximum local degree.

## 3. Acquired operation: an exact unbounded path proposal

`open_trail_sampler.py` reuses the previously acquired rational finite-memory trail supersolution and, for a specified endpoint, the shifted 16-by-16 torus Green supersolution. The torus is only an auxiliary proposal majorant: the physical graph remains an open rectangle.

The proposal has an exactly known rational total mass C_ij and outputs any oriented physical path p with probability a_p/C_ij. All remaining probability produces a null output. It enumerates lengths one through five, then uses the certified six-step-memory continuation and exact rational stopping probabilities. It rejects out-of-box steps, repeated physical edges, incorrect physical endpoints, and memory-overcount mass. There is no imposed length cutoff. For every accepted path, prefix weights, continuation factors and the stopping factor telescope to the intended activity. The memory bound counts at most the actual four-line vertices; thinning by (3/5)^(r_true-r_memory) restores the exact activity.

Endpoint displacement and exact proposal majorant:

| Displacement | C_ij |
|---|---:|
| (1,0) | 301805115576299/500964985405440 = 0.6024475250142336 |
| (1,1) | 220740793048349/500964985405440 = 0.4406311807794301 |
| (2,0) | 1391369939803831/4007719883243520 = 0.3471724522517702 |
| (3,0) | 147561699243599/667953313873920 = 0.2209161870726973 |
| all distinct endpoints | 6665794116561932/101174068823835 = 65.88441281499175 |

The fixed torus proposal has a long-distance alias floor. C_ij does not decay indefinitely with physical separation: C_(16,0) and C_(32,0) are approximately 0.16655. Consequently, the current proposal does not remove the rare-event cost of relative accuracy for small distant correlations.

## 4. Independent estimator and rigorous confidence

For each of M attempts, fixed before seeing data:

1. Generate the path proposal. If null, output zero without drawing a loop configuration.
2. Otherwise generate a fresh independent exact closed-loop configuration Gamma.
3. Return X = 9 (-1)^parity C_ij delta(p,Gamma).

This path-first order avoids unnecessary full-box sampling. The algorithm uses the exact rational suppression product rather than an additional acceptance coin. This is a Rao–Blackwell improvement over Bernoulli thinning.

The estimator is unbiased, lies in an interval of width 9 C_ij, and independent attempts give

    P(|mean(X)-<S_i·S_j>| > epsilon)
        <= 2 exp(-2 M epsilon² / (9 C_ij)²).

Thus M >= ceil((9 C_ij)² log(2/alpha)/(2 epsilon²)) suffices. A separately requested zz correlation divides the physical estimate and its error bound by three. Reusing one loop configuration for several path proposals would introduce dependence; the current implementation does not do that.

For the optional Bernoulli-thinned version, with G=G_ij,

    Var(X) = 81 (C_ij G - G²) <= 81 C_ij²/4.

The implemented product-suppression version has no larger variance. Its empirical standard error is reported only as a diagnostic, not substituted for the finite-sample bound.

The code uses Python PRNG streams for reproducible numerical runs. Mathematical exactness and confidence refer to ideal independent fair-bit inputs. Sampling decisions and output sums use integers/Fractions; only displayed numerical summaries and the confidence formula use binary64. The displayed floating confidence radius is not an outward-rounded interval certificate.

## 5. Full observed cost, not just sample counts

Nearest-neighbor range width: 9C = 5.422027725128102.

On the shared execution host:

| Run | Attempts | Valid paths / full independent loop samples | Result | 95% Hoeffding halfwidth | Elapsed excluding setup |
|---|---:|---:|---:|---:|---:|
| open 3×3, center→edge | 10,000 | 7,108 | -3.4601429 | 0.0736366 | 0.440 s |
| open 32×32, center→right neighbor | 512 | 439 | -3.5462603 | 0.3254310 | 42.210 s |

Setup was 0.118 s and 0.145 s respectively. In the 32×32 run, path proposals took 0.039 s and exact full-loop draws took 42.097 s. The expensive-sample fraction was 439/512 = 0.857421875. The exact 3×3 answer is -22071/6395 = approximately -3.4512901, within the reported confidence interval. The code's empirical variance 6.4368 agrees with independent exact variance 6.4632731 for that small case.

Projected 32×32 cost at 95% confidence, linearly extrapolated from this one run:

| Absolute error epsilon | Required attempts | Projected full loop samples | Projected wall time |
|---|---:|---:|---:|
| 0.5 | 217 | 186 | 17.9 s |
| 0.1 | 5,423 | 4,650 | 7.45 min |
| 0.05 | 21,690 | 18,597 | 29.8 min |
| 0.01 | 542,236 | 464,925 | 12.4 h |

These are workload projections, not measured long runs or runtime guarantees. Shared-host load varies; other runs measured faster full-box samples. The formal ancestor proof supplies almost-sure termination and finite expected work, not a small deterministic wall-clock bound. Costs grow with the full physical box. Query-local perfect sampling has not been implemented and is not assumed.

## 6. Equal-time summed observable

Drawing an endpoint along with the path gives an unbiased estimator of

    T_i = sum_j (-1)^parity(i,j) <S_i·S_j>
        = 6 + 9 sum_{j != i} G_ij.

This is an equal-time staggered correlation sum. Averaging T_i over sites gives a conventionally normalized equal-time staggered structure factor. It is NOT the static/Kubo susceptibility, which requires imaginary-time or excitation-energy information unavailable here.

The all-endpoint proposal has B=65.8844 and estimator range width 9B=592.9597. Although this bound is independent of volume, its constant is poor. A 10,000-attempt 3×3 test used 432 full-loop samples, took 0.065 s excluding setup and yielded 29.1065; the exact answer is 179454/6395 = 28.0616, and the conservative 95% Hoeffding halfwidth was 8.053. This is a checked operation, not a practical high-precision summed-observable breakthrough.

## 7. Independent verification and direct closed-loop alternative

`verify_observable_identity.py` verifies:

- All 36 distinct pairs in a 3×3 variable-degree pure VBS by independent quantum amplitudes against exact sphere moments. The upper-symbol coefficient is adapted to each site's actual S=degree/2 for this test.
- The exact 3×3 sphere partition function 2558/2187 against all 20 routed-loop configurations.
- All eight center-source routed-path decompositions using exact Fractions, including 184 paths with an endpoint revisited.
- All six physical spin-2 core correlations of a decorated 2×2 VBS purification, with 160,000-dimensional quantum Hilbert space. Nearest-neighbor dot product is -45/14 and diagonal dot product is 27/14.
- The independently derived closed-loop quadrupole estimator for Q_i=(S_i^z)²-2. For distinct sites it is

      Y_ij = 98 sum_gamma m_i,gamma m_j,gamma / ((d_i+3)(d_j+3)),

  where m counts visits and d is occupied degree. All six decorated 2×2 quantum pairs equal 7/50 and agree with that formula. This alternative avoids open-path noise; its separate benchmark belongs to `square_aklt_quantum_observable_audit_20261105`.

Independent exact implementation audit: `/workspace/shared/aklt_independent_full_audit/check_open_path_moments.py` and `open_path_moments_results.json`. They verify actual proposal probabilities rather than only a nominal distribution.

## 8. Strongest matched baseline and capability assessment

The coherent-state/loop representation is established AKLT technology. Generalized O(N) square-lattice worm methods already handle crossings, and AKLT loop/boundary Monte Carlo already exists. These are serious incumbents, not single-spin Glauber or exact dense tensor contraction. Relevant primary literature includes [Martyn–Kato–Lucia, Physical Review B 102, 035121 (2020)](https://arxiv.org/abs/1912.10327), which samples crossing-loop configurations to evaluate square-AKLT boundary states; [Wierschem–Beach, Physical Review B 93, 245141 (2016)](https://arxiv.org/abs/1603.03444), which evaluates AKLT correlators in a valence-bond loop gas; and [Silva–Schakel–Vasconcelos, Physical Review E 88, 021301 (2013)](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.88.021301), which gives an O(N) square-lattice worm algorithm handling crossings and loop counts.

The constructor's same-proposal empirical loop-count comparison finds ordinary birth/death MCMC roughly 3–4 times faster per estimated effective sample on 32×32. That is an empirical comparison for loop count, not a validated physical-correlation confidence guarantee, and this report does not turn it into either a positive or negative asymptotic speed theorem.

The acquired feature is independent stationary draws plus bounded unbiased physical readout, hence an explicit finite-confidence interval with no unquantified mixing bias. The current constants and full-box cost do not establish a practical speed advantage over established worm/loop Monte Carlo. This is a substantive correctness capability and a reusable verified interface, not yet a civilization-scale computational advance.

## Reproduce

    OPENBLAS_NUM_THREADS=1 python square_aklt_observable_join_20261105/verify_observable_identity.py
    python square_aklt_observable_join_20261105/estimate_spin_correlation.py --size 3 --attempts 10000
    python square_aklt_observable_join_20261105/estimate_spin_correlation.py --size 32 --attempts 512
    python square_aklt_observable_join_20261105/estimate_spin_correlation.py --size 3 --attempts 10000 --staggered-sum

Machine-readable results are `identity_checks.json`, `benchmark_3x3_pair.json`, `benchmark_32x32_pair.json`, `benchmark_3x3_staggered_sum.json`, and `confidence_costs.json`.
