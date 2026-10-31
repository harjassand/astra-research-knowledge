# Acquired immigration-death bridges and the bosonic first-event compiler

Root central construction, 31 October 2026. Whole review pending. Receive only the separately checked domain/thermal limit at its stated scope; the finite-word and circuit joins below must be checked independently.

## 1. Normalize physical time and select the cutoff
Work on x=t/T in[0,1]. For each retained vacuum mode let u_i=lambda_i T>0, f_i be the charged physical coupling normalization, v_i=f_i T, G_i=v_i^2/u_i, G=sum_i G_i, and w_i=Omega_i T. The system drift normalization is H=alpha0 T. Thermal physical modes are first doubled into the received vacuum representation; the resulting G includes the factor2nbar+1.

Exactly zero-coupling modes initialized in vacuum are omitted. A positive-coupling mode with zero damping is not covered by this parameterization. Retained G_i,u_i are strictly positive finite-description inputs or certified upper normalizations; unknown operator entries are accessed through the paid blocks.

Choose local Fock cutoff L by the explicit accepted inequality

2 sqrt[(L+1)sum_i v_i^2] exp(G/8) 2^(-L/2) <= epsilon_cut.

This gives L polynomial in G and logarithmic in switching rate and inverse error. The finite-cutoff target keeps all physical mode registers between controls and jump events. The infinite-process approximation and the finite compiler errors receive separate budgets.

## 2. Positive full kernel, not a prepared Perron state
Ignoring known free number phases, the one-mode majorant is
M_i=-2u_i n+v_i(a+a^dagger).
Its positive kernel is

E_i(x)=exp(c_i) exp(alpha_i a^dagger) exp(-2u_i x n) exp(alpha_i a),
alpha_i=v_i(1-exp(-2u_i x))/(2u_i),
c_i=G_i x/2-G_i(1-exp(-2u_i x))/(4u_i).

For endpoints m,n<=L, entries are the finite positive sum

E_i(m,n)=exp(c_i)sqrt(m!n!) sum_(k=0)^min(m,n)
 alpha_i^(m+n-2k) exp(-2u_i x k)/[(m-k)!(n-k)!k!].

Compute these entries to absolute error using log factorials/positive sums, stable expm1 and the small-argument series for x-1+exp(-x). Do not form exp(+u_i x) or normalize the infinite Perron vector. Its stationary Poisson mean G_i/(4u_i) can be huge and is irrelevant to finite-time source acquisition.

The Perron transform of this kernel is the immigration-death chain with birth rate nu_i=G_i/2 and per-particle death delta_i=2u_i. Conditioning its endpoints gives the normalized scalar Dyson-path law. Known w_i phases and the chronological system blocks remain in SELECT. A path exceeding L selects ZERO as soon as a truncated creation operator would vanish; it is not rejected and resampled.

## 3. Exact conditioned particle construction
Fix a mode, duration x>0 and endpoints n,m<=L. Put p=exp(-delta x), beta=nu(1-p)/delta. The initial n independent particles survive with binomial law, while endpoint-surviving immigrants form an independent Poisson(beta) population. Sample k initial survivors with weights

binom(n,k)p^k(1-p)^(n-k) exp(-beta) beta^(m-k)/(m-k)!,
0<=k<=min(n,m).

The following relative weights avoid a rare-endpoint denominator:

r_k=binom(n,k)(m)_k [p/((1-p)beta)]^k, r_0=1.

Evaluate log r_k, subtract their maximum and normalize the finite list. A uniform log-weight error eta changes the normalized probabilities by O(eta), not eta divided by the endpoint probability. Zero counts are handled directly. The log parameter is evaluated as -delta*x+log(delta)-log(nu)-2log(1-exp(-delta*x)), with stable elementary functions.

Conditional on k, draw n-k independent truncated Exp(delta) times for initial deaths. Draw m-k independent truncated Exp(delta) AGES and place their surviving immigrant births at x-age. These are independent groups.

For immigrants born and dead before the endpoint, use a FRESH independent Poisson(nu*x) candidate process: candidate birth times are uniform on[0,x] and lifetimes are independent Exp(delta). Retain a candidate's birth and death only if death<=x. Marked Poisson thinning gives exactly the endpoint-independent dead-immigrant process. Discarded candidates do not add an endpoint survivor; that population was sampled separately. No particle-label register is needed for the occupation path.

Sort all retained births/deaths and the initial/survivor events. This is the exact conditioned occupation bridge. Its total virtual event count is at most

n+m+2Poisson(nu*x).

Across all modes the cap is therefore 2rL+O(G*x+log(1/eta)), with no division by tiny endpoint probabilities. Candidate counts can be sampled by a finite Poisson CDF scan through the declared cap, with overflow selecting zero. On the short windows below the total candidate mean is bounded; no large-mean or rare-endpoint oracle is hidden.

An equivalent retained-dead construction samples Poisson(nu*x-beta) dead pairs directly, using lifetime density proportional (x-ell)delta exp(-delta ell). A truncated exponential proposal accepted with probability1-ell/x has mean acceptance>=1/2. This alternative is valid, but the candidate-thinning route avoids its normalization and is the intended compiler source.

## 4. Source precision without conditional-kernel recursion
The posterior's log parameter has derivative in x of magnitude delta+2delta p/(1-p)<=delta+2/x. Truncated exponential quantile
D(z;x)=-log(1-z(1-exp(-delta*x)))/delta
has derivative in x between zero and one; its reversed age x-D is also1-Lipschitz. Candidate Poisson means change by at most nu|Delta x| in total variation. Uniform candidate arrivals move by at most |Delta x|; their untruncated lifetimes can be shared exactly in a coupling.

The initial-death/survivor-arrival densities are bounded by delta+1/x. Candidate birth densities are1/x, and candidate death densities are at most1/x by convolution. A retained candidate's birth-death gap has near-zero probability at most delta*zeta. Conditional on capped counts, different particles' draws are independent. Therefore boundary, retention-threshold and cross-event near-ties can be removed at cost polynomial in K, delta and1/x times zeta, without an endpoint-probability divisor. The same-particle birth/death pair has its separate lifetime strip bound.

Use a priced positive duration floor from the outer instrument, then a much finer event-time mesh. Exclude finite source-uniform tails and probability-comparison strips, allocate all capped draws an error budget, and choose arithmetic precision logarithmically in the resulting polynomial sensitivity bounds. For a candidate lifetime, compare -log U with delta*(x-birth) before dividing; a rejected candidate needs no unbounded real-valued lifetime output. Accepted lifetimes lie inside the finite window. No recursive inverse-CDF or repeated conditional-duration denominator is required by this construction.

Outside bad/tie sets the noncommuting word order is unchanged. Known bath phases have timing sensitivity bounded by a polynomial in L,sum|w_i|,K. H0 contributes its own H timing term. Damping is already in the positive weights and is not a free unitary phase. Uniform mean-word operator errors are then bounded by the coupling/sorting/time/gate errors, not by TV between continuous and discrete timestamp measures.

## 5. Factorized matrix-of-operators access
For endpoints<=L, the row/column sum of E_i(x) is at most exp(G_i x/2+sqrt(2G_i Lx)). Hence windows

tau<=min(1,1/[16rG(L+1)])

give product row/column bound below two. Local row/column preparations have only L+1 entries, obtained from the explicit positive formula. Their absolute amplitude errors telescope over r factors. Attach identical endpoint-conditioned source words on BOTH preparation sides, keep left/right failure sectors orthogonal, and SELECT the chronological normalized system operators and number phases. The overlap is the exact finite-cutoff no-jump operator divided by a constant, up to priced source errors. Paths that ever exceed L select zero in both preparations' shared source law.

This does not enumerate (L+1)^r endpoints. The weighted Schur argument aggregates uniform per-endpoint source errors without an exponential dimension factor. Fresh block-success work is used for products and projected only at the final good block.

## 6. Actual jump rows and complete isometry
For the positive kernel, a E_i=exp(-2u_i x)E_i a+alpha_i E_i. On finite endpoint blocks, both row and column sums of the jump majorant are bounded by the product row factor times

2sqrt(u_i L)exp(-2u_i x)+sqrt(G_i).

Thus a safe squared envelope has the form C[u_i(L+1)exp(-4u_i x)+G_i]. Summing its integrals over a window gives O(r(L+1)+G*tau). Its time law is a mixture of a truncated exponential and uniform. The complete first-event normalizer is O(sqrt(r(L+1))), with a known larger padded power of two.

The actual pre-jump occupation is one above the output occupation; its lowering coefficient is already in the positive matrix weight. Do not condition a bridge on the post-jump occupation or reset the physical modes to vacuum. Retain outer type/time uniforms as Kraus records, unprepare INNER bridge sources, and amplify the entire first-event isometry. Its exact Kraus completeness, not a normalization of a lone no-jump map, is the receiving guarantee.

The previous Chebyshev isometry amplification proof pays a polynomial normalizer and source-error budget. The outer timestamp approximation is in a common uniform-coordinate L2 space. It is not TV closeness to a continuous physical timestamp distribution. The private count-capped future and representative-time drift must receive their full generator-norm error budgets.

## 7. Intended full resource scope, still pending
The sharp cutoff supplies L=poly(G,log rate,log1/epsilon). The actual vacuum-emission cap is O(G+log1/epsilon), while no-event windows number O(rG(L+1)+p+1). Virtual source counts, row preparation, source arithmetic and amplification are polynomial in r,L and input precision. Known number phases can be compiled by binary arithmetic with logarithmic frequency dependence; generic H0 and every coupling encoding cost is paid.

If all finite-bit/clock interfaces close, overhead is polynomial in r,1+H+G+p, input/register sizes, log(2+sum u_i+sum|w_i|), and log(1/epsilon), plus the supplied encoding and external-instrument costs. Thermal nbar enters through the doubled G and mode count. This is not a heat-record simulator, an unknown-bath fitting method, a practical crossover claim or a completed theorem until the whole receiver is reviewed.
