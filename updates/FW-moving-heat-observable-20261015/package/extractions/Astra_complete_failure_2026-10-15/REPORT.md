# Fast bounded-error complete-failure estimator

## Scope and assumptions

This is an auditable numerical certificate under an explicit arithmetic/randomness model, not a machine-checked proof and not evidence about an actual material. The fixture has n=400 independent exponential failure times, threshold T=1/5, and statistic tau=sum_j (799-2j)t_(j)/160000. The preferred fixture has exact distinct rates lambda_i=(399+2i)/798 for i=0,...,399. All rates differ, so a two-type lumping does not apply. The two-type fixture is retained as a benchmark.

Assume correctly rounded binary64 +,-,*,/ and integer-to-double conversions, exact frexp/ldexp where the results are normal, and round-to-nearest ties-to-even. The compiler must preserve separate operations; build with g++ -O3 -std=c++17 -ffp-contract=off, without fast-math. The program rejects __FAST_MATH__, statically checks IEC559/radix2/53 significant bits and FLT_EVAL_METHOD==0, and checks FE_TONEAREST. Sorting/comparison and integer operations have their usual exact semantics. No system log, exp, or random exponential implementation enters sampling. A statistical confidence claim additionally assumes independent fair random bits. The reproducible mt19937_64 seed is not a proof of this assumption.

## Exact setup and estimator

All setup parameters are exact decimals converted to rational numbers. K=128. For each rate lambda, use categorical weights proportional to (m+1)p^m lambda/(lambda+a m), m=0,...,K, followed by Exp(lambda+a m). Define

F=1-(K+2)p^(K+1)+(K+1)p^(K+2),
Z_lambda=(1-p)^2 sum_m (m+1)p^m lambda/(lambda+a m),
C=2n sqrt(T a [1/(1-p)-1+log(1-p)]),
M=exp(sum_i log Z_i+C-n log F).

The exact finite-mixture normalized likelihood W_K on tau<=T is at most one by the survival-profile Cauchy–Schwarz argument. We instead compute

W0=1_{tau<=T} exp(n log F-C-2n log(1-p)+2 sum_i log(1-p exp(-a t_i))).

The omitted correction satisfies 0<=W_K-W0<=1-F^n pointwise. Thus the absolute bias in normalized probability from this simplification is at most 1-F^n. This is charged explicitly, not estimated from sample agreement. The copied integer-interval setup computes enclosing M endpoints and the constant base. Categorical CDF boundaries are exact rational values rounded downward to multiples of 2^-64; coupling each of K boundaries charges at most nK/2^64. The exact maximum single-coordinate proposal density is qmax=max_i(F lambda_i/Z_i), since every exponential-mixture density decreases. No maximum component-rate substitution is needed.

## Uniform elementary-kernel bounds

Write u=2^-53 and gamma_k=ku/(1-ku). Constants in coefficients.h are binary64 nearest approximations; verify_constants.py checks their relative errors exactly against rational coefficients, and checks ln2 against the integer-interval series.

### Log

For 2^-40 <= x <= 1 (also covering the weight-log arguments), frexp gives x=2^e m with 1<=m<2 and -40<=e<=0. Set z=(m-1)/(m+1), y=z^2 and evaluate by Horner

L(x)=z sum_{j=0}^{19} [2/(2j+1)] y^j + e ln2.

The exact series remainder is at most 2(1/3)^41/[41(1-1/9)] < 2e-21. The numerator m-1 is exact by Sterbenz. The computed z has relative error at most gamma_2; hence its induced logarithm error is below 2.25 gamma_2/3 < 2e-16. Including y rounding, all positive Horner operations, and coefficient errors gives a conservative gamma_100*1 < 1.2e-14 contribution. The ln2 constant error is below u, multiplied by at most 40; exponent multiplication and final addition add below 8e-15. Their sum is less than 3e-14; we charge the weaker uniform bound 1e-13. At x=1 the result is zero exactly. The smallest nonzero z is of order 2^-53, so no internal nonzero product is subnormal.

### Exp

For x<=0, return zero below -64; the omitted value is below 2e-28. Otherwise let v=x/128 in [-1/2,0] and Horner-evaluate degree-32 Taylor polynomial with nearest binary64 coefficients 1/j!, then square seven times. Scaling is exact. Taylor remainder is at most exp(1/2)(1/2)^33/33! < 3e-47. The polynomial Horner forward error, including coefficient rounding, is bounded by gamma_66 exp(1/2) < 1.3e-14. Let e_k be an absolute error after k squarings; the exact intermediates lie in [0,1], so

e_(k+1) <= (2+e_k)e_k + u(1+e_k)^2.

Starting at 1.3e-14, seven iterations are below 2e-12; we charge 1e-11 uniformly. All nonzero intermediate values are normal for the sampler’s attained arguments, including exp(-64); if extending this kernel to arbitrary subnormal arguments, add negligible absolute underflow slack instead of relying on the relative-error model. These are analytic whole-domain bounds; empirical checks are not used as substitutes.

## Random uniform, times, and classification

Each time draw uses 96 independent random bits R=2^32 H+L and the midpoint U=(R+1/2)/2^96. Construct its binary64 value as ldexp(double(H),-64)+ldexp(double(L)+0.5,-96). L+0.5 is exact and the resulting relative error is at most gamma_2. Couple this midpoint to a continuous uniform in the same cell: absolute error <=2^-97. Reject a whole path whenever H<2^24; the probability is at most n*2^-40. Outside this event, log-input perturbation is below 4u+2^-56, and true times are at most 40 log(2)/0.5 <56.

The exact rational rates and a are rounded once to binary64; rate construction has relative error at most gamma_3. Combining the 1e-13 log bound, input perturbation, rate rounding, and the final division gives a time error less than 3e-13, uniformly for the admitted fixtures (lambda>=0.5, 0<a<1). Sorting is nonexpansive in the maximum coordinate norm. Positive weighted order-statistic coefficients sum to one, so tau changes by at most 3e-13. Computing the integer-weighted sum by 400 products/additions and one division has relative error at most gamma_802. Near T this is below 2e-14; the threshold representation error is below u. Thus any classification disagreement implies |tau-T|<=4e-13 (the relative-error inequality itself forces proximity to T).

Condition on all but one time. As that time increases, tau is continuous, piecewise linear, and its slope is at least 1/n^2. Therefore any tau interval of length h has conditional probability at most h n^2 qmax. Classification disagreement is bounded by 8e-13 n^2 qmax. This is a uniform law bound, not a sampled margin check.

## Uniform weight error and clipping

Both fixtures satisfy p<0.8 and a<1. The exact r_i=1-p exp(-a t_i) is at least 0.2. Time and multiplication perturbations change -a t_i by less than 3.2e-13. The exp kernel, p multiplication, and subtraction therefore change r_i by less than 8.3e-12. The logarithm sensitivity is at most 5.0001, so including its kernel error each log differs by less than 4.2e-11. Twice the sum over 400 coordinates contributes less than 3.36e-8. Sequential summation error, with absolute sum bounded by 2600, is below 1.2e-10; the exact prepared base is checked to be within 1e-12 of its binary64 representative. The map x -> exp(min(0,x)) is 1-Lipschitz, and the final exp kernel contributes <=1e-11. Hence 1e-7 safely bounds normalized weight error whenever classification agrees. Clipping into [0,1] is nonexpansive. Classification disagreements and rejected paths cost at most one, so they are charged separately.

Finally quantize weights downward to multiples of 2^-24, adding at most 2^-24 bias. The complete bound is

b=(1-F^n)+nK/2^64+n/2^40+(8e-13)n^2 qmax+1e-7+2^-24.

For the distinct-rate fixture b <= 7.2437543e-7, compared with normalized mean around 0.017. For the two-type fixture b <= 7.5428060e-7. The saved exact bias is rounded upward to a 160-bit dyadic rational.

## Exact empirical-Bernstein confidence calculation

The sampler emits 5000-path batch sums of integers v in [0,2^24] and v^2. Batch squared sums cannot overflow uint64 because 5000*2^48 <2^64. Python accumulates batches in unbounded integers, so the empirical mean and unbiased sample variance are exact rational numbers. The fixed-N empirical-Bernstein two-sided bound with failure probability 0.05 uses

r=sqrt(2 s^2 log(80)/N)+7 log(80)/(3(N-1)).

We replace log(80) by the rational 4.383, verified by a positive Taylor lower bound exp(4.383)>80. The square root is enclosed by integer arithmetic. The resulting exact confidence endpoints are M_lo max(0,mean-r-b) and M_hi min(1,mean+r+b). Conditional on the arithmetic and iid-bit model, these cover the desired complete-failure probability with at least 95% probability. The production N=3,000,000 was fixed before its independent-seed run and is not a stopping-time selection. Pilot runs are excluded.

## Reproduction

python verify_constants.py
g++ -O3 -std=c++17 -ffp-contract=off sampler.cpp -o sampler
python run.py two 20000 187492
python run.py distinct 20000 187492
python run.py distinct 3000000 90273041

Exact rational preparation takes about 0.6 seconds for two types and 31 seconds for 400 distinct rates. Both pilot runs take about one second per 20,000 paths. The sampler has no runtime dependency on the optimizer. JSON includes exact interval endpoints and sufficient integer statistics to recompute confidence bounds without rerunning random sampling.

## Fixed production result

The independent-seed production run used N=3,000,000 and seed 90273041. Sampling and exact final aggregation took 147.04 seconds, in addition to 30.66 seconds of exact preparation. It produced 1,530,186 candidate events and no exceptional uniforms. The exact 2^-24-unit totals are sum=860050578960 and sumsq=4834274523118736908.

Normalized mean: 0.01708766974925995.
Unbiased sample variance: 0.005432944428641937.
Empirical-Bernstein radius upper bound: 0.00012940528528984256.
Numerical and distributional bias upper bound: 0.0000007243754207462122.
M: approximately 5.41306281638298e-49.
Conditional 95% probability interval: [9.179222971065028e-51, 9.320102976605232e-51].
Relative halfwidth (radius plus bias divided by mean): 0.7615413%.

The exact rational endpoints and sufficient statistics are in distinct_3000000_90273041.json. Run python verify_results.py distinct_3000000_90273041.json to independently recompute the rational endpoints from those statistics. This checks endpoint arithmetic, not the randomness model or theorem assumptions. Pilot and production samples are not pooled.

## Independent audit and build provenance

A separate scientific and numerical audit agrees the numerical budgets are conservative; its tighter derivation gives log error <=3e-14 and exp error <=3e-12 on the relevant domain. Supplemental sampled kernel tests are diagnostic only. A requested FLT_EVAL_METHOD==0 compile-time guard was added after the run. Rebuilding produced a byte-identical executable to sampler_production, preserved from the actual production run: SHA256 9d60e35f9caf8fb192a50ee7a5fdd005a9882b974072f1c96e653f6d924d1d44. Compiler/runtime information is recorded in BUILD.txt.
