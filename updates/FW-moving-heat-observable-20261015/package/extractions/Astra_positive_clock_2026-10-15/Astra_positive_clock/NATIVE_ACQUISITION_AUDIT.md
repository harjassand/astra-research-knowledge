# Independent native spectral and finite-bit audit

## Verdict

The native rational-generator spectral acquisition is mathematically valid. I found no hidden inverse eigengap, inverse residue, or algebraic-compositum dependence. The displayed finite-bit compression budgets are conservative and consistent. Its exposition still delegates the exponential and Poisson implementations to N592; the elementary replacements below close those dependencies without assuming that source correct. Handle L=0 separately by returning 0.

This establishes a mathematical algorithm, not validation of the floating-point implementation, physical assumptions, or historical novelty.

## Exact acquisition and complexity

Multiply every local generator by its common entry denominator to obtain integer matrices of polynomial bit height. Determinant/minor coefficients have degree at most d_i and polynomial bit height by the determinant expansion. Rational gcd cancellation can be performed by fraction-free/subresultant arithmetic. Reduced numerator and denominator heights remain polynomial (integer-factor coefficient bounds suffice).

For D=diag(pi), D^(1/2)(-Q)D^(-1/2) is symmetric positive semidefinite. Its diagonal spectral measure is positive. Consequently the reduced diagonal resolvent has one simple pole for each distinct visible eigenvalue, including zero; repeated eigenvalues aggregate their projector weights, and invisible modes cancel. At alpha=-lambda the residue is A(alpha)/B'(alpha), with no minus sign.

The squarefree part P of the product of all local denominators has degree at most d and polynomial coefficient height. One never needs a field containing all roots. Module membership is identified by rational polynomial gcds with P. A primitive integer squarefree polynomial has nonzero integer discriminant. Combined with the Cauchy upper bound on all roots, the discriminant product gives a crude but sufficient minimum separation 2^(-poly(d,height(P))). Zero is one union root, so this also bounds nonzero rates away from zero. Sturm counting followed by dyadic bisection retains only intervals containing roots; its tree contains O(d times required precision) nodes, with polynomial exact arithmetic. This supplies a constructive polynomial root-isolation argument.

After jointly clearing denominators of A and B, Res_s(B(s),uB'(s)-A(s)) is an integer polynomial in u of degree at most deg B and polynomial coefficient bit height. Its constant term is nonzero because gcd(A,B)=1, and each residue is a root. The reciprocal Cauchy bound yields w >= 2^(-poly(B,d)). The same separation bound lower-bounds |B'(alpha)|, so rational interval evaluation of A/B' attains relative eta accuracy with polynomial(B,d,log(1/eta)) precision and work. Rational stationary probabilities and their product q have polynomial bit lengths, hence log(1/q) is polynomial too.

Independent exact symbolic checks:
- Complete graph and central path target both reduce to (s+1)/(s(s+3)); residue resultant is -(3u-2)(3u-1).
- Nonsymmetric example has integer A=2s^2+41s+114 and B=2s^3+47s^2+209s. Residue resultant is -722(11u-6)(5907u^2-2685u+64). This reproduces 6/11 and 5/22 +/- 103sqrt(537)/11814 exactly.

## Compression proof and independent finite primitives

For a stratum, a <= Lambda <= na and mu a >= 1/n. Its k-th mark moment obeys E[V^k] <= k! mu/a^(k-1). Therefore the centered mark and compound-Poisson cumulant bounds stated in CONSTRUCTION.md hold. Chernoff optimization gives the displayed 2 exp(-h^2 min(r,M)/(6n)) bound for 0<h<1. The stratum union bound and relative-error combination are valid.

With the section-4 constants, J<=16LR, local categorical coupling failures total at most J eta/16<=delta/4096, and small-count mismatch totals at most LR eta<=delta/4096. The approximate-intensity branch at 2R indeed implies true large intensity >=R and true small intensity <=4R. Poisson tail at K=12R+ell+1, for approximate mean <=2R, is far smaller than the stated budget. Concentration has slack since exp(-ell)<=2^(-ell).

To remove reliance on N592's finite exponential primitive: for at most J exponentials couple independent continuous U to a dyadic midpoint v, exclude U within rho=delta/(128J) of either endpoint, and choose grid spacing g <= t rho^2/8 for t a small multiple of eta. Off these endpoints, relative error in -log U from midpoint rounding is at most 2g/rho^2. Approximate -log v to absolute accuracy t rho/4. Compute logs using v=2^(-k)z, 1<=z<2, and the atanh expansion whose argument (z-1)/(z+1)<=1/3; likewise compute log 2. This costs polynomial(log J, log(1/delta), log(1/eta)) bits and work. Do not use an unreduced log series near v=0, which could introduce inverse-delta work.

For small Poisson tables with rational mean m<=2R, approximate exp(-m) by reciprocal of a positive exp(m) Taylor sum, then use p_k=exp(-m)m^k/k!, k<=K. Work and precision polynomial in R,K,log(1/zeta) suffice; allowance O(R+log(1/zeta)) precision handles amplification by exp(m). Round each probability downward within zeta/(K+1); assign omitted mass to an explicit failure outcome. Tail plus rounding mass bounds the coupling failure. Exact sampling from the resulting rational categorical vector takes expected fewer than two common-denominator power-of-two rejection attempts. These primitives suffice to close the stated expected polynomial bit theorem.

## Stronger convolution/interlacing alternative

The separate worker's compressed-spectrum route is sound and removes concentration/Poisson dependencies altogether. For a rational positive spectral law with zero atom q, sequentially convolve local laws, rounding every positive partial rate down to a binary-significand grid with ratio at most 1+theta. Keep zero exactly zero. On each underlying tuple,

  Lambda_hat <= Lambda <= (1+theta)^n Lambda_hat.

A grid spanning lambda_min/(1+theta)^n through n lambda_max has polynomially many bins for theta=O(epsilon/n). Fixed common integer denominators per local probability vector, and their prefix products, bound all DP weight heights polynomially. Use that representation rather than unreduced nested rational expressions.

For resulting distinct positive rates lambda_j and weights w_j, define D(s)=q+s sum_j w_j/(s+lambda_j). D'(s)=sum_j w_j lambda_j/(s+lambda_j)^2. F(r)=D(-r) is strictly decreasing between its poles and has exactly one root in each (0,lambda_1),(lambda_1,lambda_2),...,(lambda_(K-1),lambda_K), none above lambda_K. Each root r_j produces positive mixture mass

  a_j = q/[r_j sum_k w_k lambda_k/(lambda_k-r_j)^2].

The rational Laplace transform q/D(s) has atom q because its limit at infinity is q, and sum_j a_j=1-q because its value at zero is 1. No pole cancels. Rational polynomial root isolation and residue acquisition have polynomial complexity in K and the DP coefficient bit heights; no inverse-gap oracle is needed.

Coupling the same geometric count and Exp(1) marks proves the rate-rounding bound for the full hitting time. For native algebraic weights, acquire normalized local categorical vectors to TV at most c delta q/n, keeping local zero weights exact. The expected number of local choices in the geometric coupling is n(1-q)/q, so total mismatch probability is O(delta). This high precision is polynomial-bit, since it requires log(1/q), not 1/q. Approximate local rates, final mixture rates/weights, and final exponential draws with the remaining multiplicative/error budgets. The deterministic sandwich applies before these finite/native approximation failure events, not unconditionally to the final rational output.

Exact example: q=1/10, lambda=(1,3,8), w=(1/5,3/10,2/5) gives Laplace transform

  (s+1)(s+3)(s+8)/(10s^3+77s^2+119s+24).

Rates approximately (.236868075779197,1.78416712577579,5.67896479844501) have masses (.820712714786372,.0551172002381098,.0241700849755186), summing to .9.

## Correct theorem wording

For explicitly supplied finite irreducible reversible rational generators, designated product target, stationary product initialization, and rational 0<epsilon,delta<1/2, there exists a finite-random-bit algorithm returning a nonnegative rational Hhat that admits a coupling to H with P(|Hhat-H|>epsilon H)<=delta. Expected preprocessing and sampling bit costs are polynomial in total input length, total local dimension, epsilon^(-1), and log(delta^(-1)). The polynomial does not separately depend on inverse target mass, inverse visible residues, or inverse spectral gaps. The empty/nonmoving product returns zero. The compressed-spectrum route can preprocess a reusable positive exponential mixture; O(log K) per draw describes categorical search comparisons, not total bit complexity including exponential precision and rational output size.
