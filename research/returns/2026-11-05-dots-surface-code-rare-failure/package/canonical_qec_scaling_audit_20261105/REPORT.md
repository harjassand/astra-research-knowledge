# Canonical-witness acceptance: useful finite regime, exponential worst case

Independent scaling audit, 2026-11-05. The target implementation is ../canonical_qec_witness_20261105/sampler.py. This report does not change its sampling law or decoder.

## Verdict

The implemented ordinary-square-code estimator is genuinely effective in its demonstrated low-p finite-distance regime. It is not a distance-uniform rare-event algorithm. An exact planar IID counterexample has exponentially declining acceptance even with perfect enumeration of simple shortest paths, so nonbacktracking walk waste is not the essential limitation. The ordinary square-code diagnostics also show a strong acceptance decline at fixed p, but they do not prove its asymptotic rate.

## Exact acceptance identity

Let F_L be decoder failure with the selected canonical residual path of length at most L, and let Z be the proposal normalizer, including any walks rejected before noise sampling. The algorithm's acceptance probability is exactly

alpha=P(F_L)/Z.

Thus the relative variance of its N-trial Bernoulli estimator is (1-alpha)/(N alpha). Independence removes an MCMC mixing assumption, but does not remove witness-overlap cost.

If M(E) counts all simple majority paths in the proposal family and the noise pattern E is retained, averaging over the conditional uniform choice of witness gives the Rao–Blackwell estimator Z 1_(F_L)(E)/M(E). It has no larger variance. Computing M(E) is an additional counting operation that the canonical method avoids; it is not available for free. Invalid non-simple proposals remain null outputs.

## An exact exponential counterexample

Construct m square diamonds in series. Each block has two two-edge routes between its articulation endpoints. All 4m physical edges fail independently with probability p. Only the two extreme endpoints are rough boundaries; all other vertices have ideal parity checks. The Z-error logical-path distance is2m. A CSS realization has dual X-distance2, so this is not a balanced distance2m surface-code family.

Every simple left-to-right path selects one route per diamond and has length2m. There are2^m such paths. Even the ideal simple-path envelope therefore has normalizer

Z_m=2^m P(Binomial(2m,p)>=m).

For actual error counts A,B on the two routes of one block, the minimum weight in the same local cycle class is

c0=min(A+B,4-A-B),

and in the opposite crossing class it is

c1=min(2-A+B,2-B+A).

The articulation checks force the same homology change through every block. Consequently the global class-cost difference is the sum of c1-c0. The independent increments D=(c1-c0)/2 take values+1,-1,0 with probabilities

a=(1-p)^4+p^4, b=2p²(1-p)², c=1-a-b.

Every minimum-weight decoder can fail only if sum D<=0. Chernoff's bound gives

P_fail <= (c+2sqrt(ab))^m.

Using binomial(2m,m)>=4^m/(2m+1),

alpha <= (2m+1) R(p)^m,

where R(p)=(c+2sqrt(ab))/(8p(1-p)). If q=p(1-p),

R(p)=(1-q)/2 + sqrt(2-8q+4q²)/4 <= (2+sqrt(2))/4 <0.853554

for0<p<=1/2. This proves exponential acceptance loss even as physical noise becomes arbitrarily small. No non-simple walk is involved.

The failure probability can actually be evaluated exactly in O(m²) arithmetic by the three-term convolution for sum D. Ties contribute exactly half their total probability for any deterministic minimum-weight tie convention: conditioned on each block's two midpoint syndromes, only the(0,0) block distinguishes the two crossing classes, with likelihoods a and b and minimum costs0 and2. The other midpoint-syndrome classes have equal likelihoods and equal costs. A global cost tie has equally many a/b exchanges, so the two global tied cosets have identical likelihood. This also gives a strong exact baseline on this constructed family, not a proposed new use for the estimator.

At p=.001, R(p)<.852347137366. Exact convolution gives acceptance approximately:

- Z-distance20:0.112014.
- Z-distance40:0.0226055.
- Z-distance100:0.000187080.
- Z-distance200:6.34793e-8.
- Z-distance400:7.31433e-15.

The JSON retains exact-rational-derived values and rigorous upper bounds; displayed decimals are summaries. check_diamonds.py independently enumerates every error pattern through m=4 (65,536 patterns at m4), builds global syndrome/logical-class minimum weights without using the local reduction, and verifies all cost differences. It also checks equality of the complete tied-coset weight enumerators. The conceptual reduction was independently checked by the estimator's builder.

## Ordinary square-code fixed-grid diagnostic

PRECOMMIT.md fixed this grid before execution. Each entry uses2000 trials of the unchanged implementation, L=max(55,3d), and a separate fixed seed. Values are acceptance fractions, not confidence claims about rare failure probabilities.

- p=.0001, d13/25/41/61: .341, .338, .3145, .274.
- p=.001, d13/25/41/61: .2845, .2035, .1135, .0585.
- p=.005, d13/25/41/61: .158, .053, .0175, .0025.

At p=.001,d61, the2000 outputs are117 accepted,2 non-simple,1017 not failures,864 other witnesses. Thus replacing nonbacktracking paths by a perfect self-avoiding-path oracle would barely address the observed loss. At p=.005,d61, only5 successes were observed, so its displayed fraction is especially imprecise. At p=.0001 the acceptance remains useful over this grid. None of these finite observations proves exponential behavior of the ordinary square family.

Full counters, normalizers, exact-tail-derived decimal ratios and timings are in square_grid_results.json. Largest run: d61,p=.005, setup1.401s and sampling7.185s for2000 trials on this shared host. Runtime is diagnostic, not a controlled cross-machine benchmark. Python Random remains an implementation PRNG, not certified iid randomness.

## Previously published IID and rare-event baselines

1. Karp–Luby(1983), summarized and analyzed by Owen, Maximov and Chertkov, 'Importance sampling the union of rare events', arXiv:1710.06965, https://arxiv.org/abs/1710.06965. Their ALOE method chooses a rare event with probability proportional to its mass, samples conditionally, and corrects by inverse witness multiplicity. This is the direct IID conceptual baseline. The canonical decoder certificate replaces a potentially difficult multiplicity count by one computable indicator. Neither IID conditional importance sampling nor rigorous IID intervals originate here.

2. Fault-weight/subset stratification is an established IID QEC technique. For example, Haruna and Murakami, arXiv:2610.35498, https://arxiv.org/abs/2610.35498, use uniform sampling/enumeration at each error weight as their MCMC-independent reference. Majorana/Floquet and other QEC simulations also use malignant-set or subset sampling. These methods can attach ordinary independent-sample confidence bounds when tail strata are bounded; it would be incorrect to claim that all existing rare-event QEC estimators require MCMC mixing assumptions.

3. Weight stratification is not automatically a competitive baseline on this particular low-p square instance. At d13,n313,p=.001, the exact binomial mass of all patterns of weight>=7 is4.17787383748e-8. Dividing the builder's diagnostic failure estimate3.8146e-16 by this mass gives conditional failure about9.13e-9. Merely sampling noise conditioned on at least the minimum failing weight would therefore still require roughly1.1e10 samples for100 failures. This comparison is diagnostic and does not benchmark every possible optimized IID proposal.

4. Bravyi and Vargo(2013), https://arxiv.org/abs/1308.6270, already use splitting and Bennett ratios for rare surface-code failures. A stronger current MCMC comparison is Haruna–Murakami(2026), arXiv:2610.35498: locally balanced flips plus cluster exchange, specifically tested against one-bit-chain trapping. Circuit-level rare-event splitting is also implemented in https://arxiv.org/abs/2509.13678. No matched-runtime experiment against those implementations has been completed here.

The resulting scope is a computable, exact-normalization canonical-witness implementation with finite-sample IID confidence under stated ideal-randomness/decoder assumptions, useful at the demonstrated parameters. It is not a new general IID rare-event principle, a general FPRAS, a hardware-noise acquisition, or an established speed record over the strongest existing method.
