# Independent audit of physical spin observables

## Verified physical join

The distinct-site dipolar join is correct for the specified open spin-2 AKLT state with identity on every dangling virtual qubit:

    rho = V I V† / Tr(V I V†).

This is a particular mixed ground-space state, not every choice of a pure boundary state. Equivalently one may purify its dangling qubits with external spin-1/2 singlet partners. Boundary spin-2 cores still use the same factor nine. If instead boundary physical spins are reduced to degree/2, the factor changes to (S_i+1)(S_j+1).

For normalized spin-S coherent states and normalized sphere measure, define A_a=(2S+1) integral n_a |n><n|. SU(2) covariance implies A_a=c S_a. Taking a trace with S_a gives (2S+1)S/3 on the left and c(2S+1)S(S+1)/3 on the right. Thus c=1/(S+1), proving the upper symbol of S_a is (S+1)n_a, not S n_a. Distinct sites factor independently. Consequently, for spin2,

    <S_i dot S_j> = 9 (-1)^(sublattice parity) G_ij, i != j,

where G_ij is the ferromagnetically staggered classical O(3) dot correlation. The same-axis zz correlator is one third of this in the SU(2)-invariant state. The on-site dot product is exactly six; substituting i=j into the factor-nine formula is wrong.

Direct independent contraction of the physical spin-2 tensors on an open2×2 square, tracing dangling virtual indices, gives nearest-neighbor dot correlation -45/14 and diagonal27/14. These agree with the loop/path calculation to less than9e-16. This contraction uses spin2 tensors at every site, independently of the worker's variable-degree VBS calculation. Script: `check_spin_symbol.py`.

## Open-path normalization

Adding a distinguished source edge carrying n_i dot n_j to the coherent norm expansion decomposes every routed source-containing configuration into one uniquely oriented i-to-j path and closed loops. The source loop's color factor cancels the extra endpoint moment factor, leaving

    a_p = 3^(-L(p)) (3/5)^r(p).

Here r includes degree-three path endpoints as well as degree-four internal path vertices. Paths can revisit either endpoint internally; forbidding that would lose terms. There is no 2L orientation correction, unlike the closed-loop birth measure. The closed loops acquire exactly the suppression product delta(p,gamma): zero for shared edges, and3/5 for each shared vertex.

Therefore G_ij=sum_p a_p E_pi[D_p]. The implemented `OpenTrailSampler` samples each physical oriented path with probability a_p/C and sends all leftover mass to a null output. The prefix/continuation/stop weights telescope correctly. We independently enumerated all physical paths and all routed closed configurations on2×2 and selected3×3 pairs and verified each implemented rational proposal probability, including endpoint revisits.

## Exact mean and variance

For one independent attempt, let X=C D_p when the path proposal is physical and zero otherwise; draw an independent exact closed gas only after a physical path proposal. Then

    E X = G,
    E X² = C sum_p a_p E_pi[D_p²],
    Var(9X) = 81[C sum_p a_p E_pi[D_p²] - G²].

If D_p is replaced by a Bernoulli coin with that success probability, its physical variance is exactly81(CG-G²). Evaluating D_p itself is Rao–Blackwellized and never has higher variance. The latter formula is an upper bound, not generally the exact variance of the product-delta implementation.

Independent exact values using the current C:

- 2×2 nearest neighbor: physical mean -45/14; variance7.0963136063.
- 3×3 center to neighboring edge: mean -22071/6395; product-delta variance6.4632731176 versus Bernoulli6.8015872992.
- 3×3 corner to center: mean2640/1279; product-delta variance3.7911041595.
- 3×3 opposite corners: mean804/1279; product-delta variance0.8937443115.

All exact rational expressions and enumerations are in `open_path_moments_results.json` and `check_open_path_moments.py`.

For n fixed independent attempts, |9X|<=9C. A valid two-sided additive Hoeffding half-width is9C sqrt(log(2/alpha)/(2n)). The implementation counts null attempts in n, includes their zeros in both moments, and uses a separately generated gas for every accepted path; this is correct. Reusing one gas for many paths would create dependence and require block-level or otherwise justified error accounting. Binary64 evaluation of the printed confidence radius is not itself an outward-rounded interval certificate.

One small reporting defect was identified and sent to the worker: `(-1)**sum(target)` produces a floating sign for negative displacement sum, causing the nominal `estimate_exact` to lose Fraction exactness. Use an integer parity branch. The worker corrected this to an integer parity branch before finalizing. This did not change the sampled law.

## Resource and precision limits

The nearest-neighbor proposal majorant is C=0.6024475250, giving physical range width5.422027725. The all-endpoint majorant is B=65.884412815, giving range width592.9597153 for the off-diagonal equal-time staggered sum. The latter is a mathematically volume-independent bounded estimator but has a large variance constant.

The observed32×32 nearest-neighbor run used512 attempts and439 independent full-gas samples, took42.21 seconds excluding0.145-second setup, and returned -3.5463 with a95% Hoeffding half-width0.3254. It establishes executable physical estimation, not high-precision or incumbent-superior performance. At the same bound, additive error0.01 with95% confidence requires about542,236 attempts, before considering faster variance-aware guarantees. Costs of gas generation dominate the path oracle.

The fixed16×16 auxiliary torus is not a uniformly sharp long-distance endpoint guide. For displacement(d,0), C_8=0.0657547, C_12=0.1376985, C_16=0.1665464 and C_32=0.1665464. Torus aliases produce a nondecaying envelope while the true distant correlation decays. Thus additive guarantees remain valid, but efficient fixed-relative-error long-distance estimation is not established. The proposal has no path-length cutoff, but absence of bias does not prevent rare-event variance.

Finite open boxes retain boundary and finite-size effects. These CIs refer to their specified state, not an infinite-volume state unless an independent finite-size error is supplied.

## Quadrupole cross-check and stronger consequence

For Qzz=S_z²-2, the spin2 upper symbol is (21/2)(n_z²-1/3)=7P2(n_z). The worker's distinct-site closed-loop estimator is

    H_ij = 98 sum_loop m_i(loop)m_j(loop) / [(d_i+3)(d_j+3)],

where m counts visits and d_i=2 sum_loop m_i(loop). It lies in[0,8]. Independent physical tensor contraction gives <Qzz_i Qzz_j>=7/50 for all distinct2×2 pairs, agreeing with that estimator. The on-site value is14/5 and must be inserted separately.

All nonzero H_ij values are integer multiples of1/25, so exact integer accumulation is available. The current float implementation is adequate for diagnostics but needs a rounding allowance or exact accumulation for literal certified numerical endpoints. A sample mean and estimated standard error of zero at a rarely connected distant pair do not certify that the expectation is zero.

This is stronger operationally than merely producing an abstract loop configuration: the same exact samples give unbiased bounded physical quadrupole correlations, including spatial averages without an extra open-path draw. There is also a deterministic physical consequence. Since occupation probability of a loop is at most its activity, the existing certified length moments imply the conservative uniform bound

    sum_j <Qzz_i Qzz_j>
      <=14/5 +(98/25)(S2+T2+2M4) <11.845.

It bounds an equal-time quadrupolar fluctuation/structure-factor sum for the specified state. The other auditor is sharpening this by subtracting the self term and using degree-four denominators. It is not a bound on quantum static susceptibility: a Kubo response involves imaginary-time evolution or excitation-energy denominators. Likewise6+9 sum_j G_ij is an equal-time staggered correlation sum, not a dynamical response.

## Strongest comparator and conclusion

Silva–Schakel–Vasconcelos2013 already formulate exactly this closed gas at N=3,K=1 and include an open-endpoint worm sector whose partition-function ratio is the classical spin dot correlation. Their Eq.2 and discussion following it cover crossing routings and site weights at source endpoints. Multiplying by the coherent-symbol factor is a known mapping, not a new physical input interface. Source: https://arxiv.org/pdf/1306.4996 . The2016 valence-bond-loop AKLT observable method is another direct comparator: https://arxiv.org/abs/1603.03444 .

The added rigorous capability is finite-time exact sampling plus fixed-budget nonasymptotic additive confidence for specified physical equal-time observables, and a quantitative uniform quadrupolar fluctuation bound. This closes the classical-to-observable interpretation, but it does not by itself demonstrate a speed or accuracy-per-cost advantage over established worm/valence-bond-loop methods. There is still no quantum state preparation, gap, finite-temperature dynamics, arbitrary boundary-state solution, or new experimental control operation.

Prior-art update: Kennedy–Lieb–Tasaki1988 already prove exponential spin two-point decay for the square-lattice spin2 model with periodic boundary conditions, https://doi.org/10.1007/BF01011563 . Thus an explicit weighted-trail decay estimate is not a first proof of dipolar clustering. Any new quadrupolar or constant-level consequence still needs a precise comparison.
