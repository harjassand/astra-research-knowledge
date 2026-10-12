# Information cost of imaginary-time-to-real-time prediction

## Status and access contract

This is a self-contained research proof candidate developed in this conversation. It has not been independently reviewed or formally verified. Priority for the combined result is unresolved. General ill-posedness of analytic continuation, optimal recovery, binomial moment cancellation, and the inverse spectral construction of Jacobi matrices are prior mathematics, not newly invented here.

An unknown probability measure mu is supported on [0,1]. Write

    G_mu(s) = integral exp(-s x) dmu(x),
    A_mu(t) = integral exp(-i t x) dmu(x),
    p_mu(t) = |A_mu(t)|^2.

A query chooses s in [0,B]. Two separate observation models are considered:

1. G_mu(s) + Z;
2. log G_mu(s) + Z;

where Z is independent standard Gaussian noise on every call. Query locations may depend on all previous data. Count a fixed worst-case number of calls, not an unproved expected-stopping-time budget. No state-preparation oracle, individual spectral-weight measurement, matrix entries, or coherent real-time evolution is supplied.

Let N_*(T,B) be the smallest call budget giving, uniformly over mu, a finite description of p_mu(t) on 0<=t<=T with uniform error at most 1/16 and probability at least 2/3. The analogous statement holds for A_mu with any fixed sufficiently small accuracy.

## Main theorem

There are universal c,C,T0>0 such that, for T>=T0 and every B>0, in either observation model,

    c T log(2+T/B) <= log(1+N_*(T,B)) <= C T log(2+T/B).

Constants in the exponent are not identified optimally. This is a constant-accuracy theorem, not a sharp joint accuracy/confidence asymptotic.

The lower bound is realized by one-particle real symmetric nearest-neighbour chains plus one known isolated reference level. The nominal pair has the same complete spectrum; all nonzero energies lie in [3/8,5/8]; the unique ground energy is zero with gap 3/8 and preparation overlap 1/4; every remaining spectral weight is at least inverse-polynomial in the number of levels. Known eigenvalues, all partition functions, and linearly many exact local moments may be supplied for free.

## 1. Positive, isospectral counterexamples

Let m be positive and odd, n=m+1, x_j=3/8+j/(4m), 0<=j<=m. On this grid let u be uniform on all nodes, u_even uniform on even-indexed nodes, and b_+, b_- the binomial(m,1/2) law conditioned on even/odd index. Define

    nu_+ = (1/4)u + (1/4)u_even + (1/2)b_+,
    nu_- = (1/4)u + (1/4)u_even + (1/2)b_-,
    mu_+ = (1/4)delta_0 + (3/4)nu_+,
    mu_- = (1/4)delta_0 + (3/4)nu_-.

All nu weights are at least 1/(4n), and all nonzero-energy mu weights are at least 3/(16n). Their signed bulk difference at node j is (-1)^j binom(m,j)/2^m. Finite differences therefore give equal moments of degrees 0,...,m-1, including after the common reference is added.

For all s>=0,

    G_+(s)-G_-(s)
      = (3/4) exp(-3s/8) [(1-exp(-s/(4m)))/2]^m.

Consequently, with a=min(B/(8m),1/2),

    sup_[0,B] |G_+-G_-| <= (3/4) a^m.

Both signals lie in [1/4,1]. Hence

    sup_[0,B] |log G_+-log G_-| <= 3 a^m.

At t_m=4 pi m, let xi=exp(-3 pi i m/2), which is +i or -i. Then

    A_+(t_m)=1/4+(9/16)xi,
    A_-(t_m)=1/4-(3/16)xi,
    p_+(t_m)=97/256,
    p_-(t_m)=25/256.

The return-probability gap is 9/32. Thus error <=1/16 suffices to test the hypotheses.

## 2. Adaptive statistical lower bound

For Gaussian observations whose conditional means differ by at most D, the chain rule gives transcript KL <= N D^2/2, even for adaptive query locations and randomized algorithms. Pinsker gives TV <= sqrt(N) D/2. Equal-prior success >=2/3 needs TV>=1/3.

For the more permissive logarithmic observation model, D<=3 a^m. Thus

    N >= (4/81) [max(2,8m/B)]^(2m).

The additive model has a stronger constant. Choosing the largest odd m with 4 pi m<=T gives m=Theta(T) for large T and proves the claimed lower exponential order. The statement applies to a whole predicted trajectory because t_m lies in the requested horizon.

Exact noiseless functions are not ambiguous: analytic uniqueness remains intact. The lower bound concerns finite noisy information. It does not lower-bound the number of noiseless infinite-precision queries.

## 3. Local Hamiltonian realization and parameter conditioning

For either positive n-point bulk measure, orthonormalize 1,x,...,x^(n-1) in L2(nu). Multiplication by x has a symmetric tridiagonal matrix H in this basis. Orthogonality makes entries beyond the first off-diagonal zero; positive leading coefficients make the neighbouring couplings nonzero. A diagonal sign gauge makes them negative. The first basis vector is the constant function, so

    <e0, exp(-sH)e0> = G_nu(s),
    <e0, exp(-itH)e0> = A_nu(t).

This proves the realization without importing a counting or quantum-simulation algorithm. The two matrices are isospectral because their supports coincide. Their diagonal coefficients through index (m-3)/2 and bonds through distance (m-1)/2 coincide: those recurrence coefficients depend only on moments of degree <=m-1. The known part of the near boundary is therefore the same.

Every coupling has an inverse-polynomial lower bound. More generally, let a Jacobi matrix have n simple eigenvalues separated by Delta and endpoint weights >=alpha. Split the chain at any coupling b. The left principal block has fewer than n eigenvalues. Since intervals of radius Delta/3 can cover at most one full eigenvalue each, some full eigenvalue lambda is at distance >=Delta/3 from that block's spectrum. For its normalized eigenvector v,

    ||v_left|| <= 3 |b|/Delta,
    alpha <= |v_0|^2 <= 9 b^2/Delta^2.

Thus |b|>=Delta sqrt(alpha)/3. Here Delta=1/(4m), alpha=1/(4n), so every bulk coupling is at least 1/(24m sqrt(n)). No exponentially small hopping or endpoint spectral weight is necessary. The excited-state spacings are O(1/m); they are not claimed uniformly separated. The gap above the separately added ground state IS uniform.

The total Hamiltonian is 0 direct-sum H. Prepare psi=(1/2)e_ref+(sqrt(3)/2)e0. This is a fixed two-site superposition; it does not require preparing an unknown eigenstate. The graph is a path plus a known isolated reference. The ground level is unique and gapped. Entries of H are diagonals rational and square roots of positive rational couplings-squared. Exact monic recurrence constructs them in polynomial bit complexity in m. Explicit matrix access would make these small systems easy to simulate: the lower bound is about the specified measurement interface.

## 4. Robustness beyond exact binomial identities

Perturb the two bulk matrices by real symmetric tridiagonal E_+, E_-, with norms <=1/(64 t_m). Require their previously common near-boundary coefficients to remain common; a common perturbation E is sufficient. Keep the isolated reference unchanged.

The perturbed bulk spectra lie in [1/3,2/3]. Closed-walk expansion still makes moments 0,...,m-1 identical. This needs only spatial locality and the common prefix, not exact values of the coefficients.

For spectra in [0,1], the scalar Taylor remainder at the origin bounds the bulk response difference by 2 B^m/m!. For a uniform-in-s bound, Taylor-expand about x=1/2. On [1/3,2/3],

    remainder <= exp(-s/3) (s/6)^m/m!.

Its supremum over s>=0 is <=2^-m, since m! >= (m/e)^m. Therefore

    sup_[0,B] |G_+^pert-G_-^pert|
      <= (3/2) min(B^m/m!, 2^-m).

The reference still keeps G>=1/4, so the logarithmic difference is at most four times this. The same adaptive argument gives

    N >= (1/81) [max(2,m/(eB))]^(2m).

On the other hand, Duhamel's formula gives a real-time amplitude change <=t_m||E||<=1/64. Return probabilities change by at most 1/32 under each hypothesis. Their gap remains at least 7/32. Thus the same exponential order survives these inverse-polynomial, prefix-preserving perturbations in both noise models.

This perturbation theorem does NOT preserve the nominal exact common spectrum or the nominal eigenvector-weight floor. Free complete-spectrum side information is asserted for the unperturbed isospectral family, not for arbitrary perturbed pairs. It also does NOT assert a full unrestricted perturbation neighbourhood: errors at the near boundary can introduce much shorter detectable differences.

## 5. Matching constructive upper bound

Given target T>=1 and amplitude accuracy eps, set

    M=ceil(max(16T,log2(4/eps))),
    a=min(B/M,1/16),
    s_l=l a, 0<=l<=M.

For 0<=t<=T and 0<=x<=1 put z=1-exp(-a x), so 0<=z<=a. Then

    exp(-itx)=(1-z)^(it/a).

Truncate its binomial series after degree M:

    P_t(x)=sum_(j=0)^M c_j(t) [1-exp(-a x)]^j,
    c_j(t)=(-1)^j binom(it/a,j).

For j>M,

    |c_j(t)| z^j <= [eT/j+ea]^j <= (e/8)^j < 2^-j.

The uniform bias is at most 2^-M<=eps/4. Expanding powers gives

    P_t(x)=sum_(l=0)^M w_l(t) exp(-l a x).

The coefficient norm, uniformly for 0<=t<=T, is bounded by

    S = 2 [2e (1+T/(a M))]^M
      <= 2 [2e (2+T/B)]^M.

Proof: |binom(it/a,j)| <= (T/a)_j/j!. Since T/a>=1, the sequence 2^j(T/a)_j/j! grows by at least a factor two. Its finite sum is at most twice the last term; j! >=(j/e)^j gives the displayed expression.

If all sampled G(s_l) have deterministic error at most delta, then

    sup_(0<=t<=T) |sum w_l(t) Ghat(s_l)-A_mu(t)|
      <= 2^-M+S delta.

Choose delta=eps/(4S). Repeating each query O(S^2 eps^-2 log((M+1)/zeta)) times makes every mean accurate simultaneously with probability >=1-zeta. The output is a polynomial in t of degree M. The return probability obtained from it, clipped to [0,1], has error <=2e_A+e_A^2 when the amplitude error is e_A. A fixed small eps gives the desired 1/16 return-probability accuracy.

For the logarithmic observation model, estimate log G at the same grid, clip each estimated logarithm above at zero, and exponentiate. The map exp(min(z,0)) is 1-Lipschitz; the same raw accuracy suffices.

For constant eps,zeta, M=O(T), log S=O(T log(2+T/B)), and the total count has the stated upper exponential order. This reconstructs the requested response, not the microscopic Hamiltonian or a positive spectral density.

## 6. Precision, runtime, and implications

For rational T,B, a is rational and the binomial coefficients are complex rational polynomials in t. Generating and evaluating them to the required accuracy has polynomial bit cost in M, the input bit lengths, log S, and log(1/eps). The statistical count, not the arithmetic bit precision, is exponential. Quantization and independent systematic query errors must fit delta; an uncalibrated bias larger than delta invalidates the upper confidence statement. Since both G and log G are 1-Lipschitz in s on this spectral class, absolute setting errors <=delta suffice. This may demand extremely fine instrumental accuracy, despite only polynomially many precision bits. The oracle upper bound is not a demonstration that an instrument provides those settings. It uses times <=min(B,M/16); preparation, decorrelation, and per-query physical costs are separate from the stated sample count.

A deterministic oracle returning arbitrary-precision G with cost polynomial in requested precision bits is a stronger access model. This theorem does not rule out efficient deterministic continuation using it. Nor does it apply to algorithms that know the complete Hamiltonian, can measure individual spectral weights, implement energy filters, or evolve coherently in real time.

For fixed B, the recoverable horizon at constant accuracy from N noisy samples has order log N/log log N. Even when B is unlimited, the worst-case order is only log N. These are minimax orders, not guarantees that every individual spectrum is difficult.

## 7. Evidence and prior mathematics

verify.py uses exact Fraction arithmetic for moment matching, the positive background, Jacobi coefficients, local prefix matching, and polynomial coupling bounds. It independently compares local matrix moments to the prescribed spectral measure. Floating and multiprecision propagator and extrapolator tests are separately labelled. No physical experiment or acquisition of the enormous theoretical sample counts was performed. The first fixed-precision reconstruction diagnostic failed its requested 140-digit agreement test because of cancellation; this was not a failure at the theorem's constant-error target. The final verifier chooses working precision from the proven coefficient amplification bound.

Selective primary comparisons:
- Silver, Sivia and Gubernatis, Phys. Rev. B 41, 2380 (1990), DOI 10.1103/PhysRevB.41.2380: analytic continuation of imaginary-time Monte Carlo data and its ill-posedness.
- Ohzeki, APS Open Science 1, 000145 (21 September 2026), DOI 10.1103/8yw5-dhd4: singular-value structure and compression, explicitly distinguished from reliable spectral inversion.
- Polyanskiy and Wu, arXiv:1902.05616: convex duality between two-point lower bounds and functional estimators; the lower-bound/estimator paradigm is not a new principle here.
- Foucart and Paouris, arXiv:2301.07228: optimal recovery of linear functionals with noisy data, continuing Donoho's 1994 work.
- Christandl et al., Phys. Rev. Lett. 92, 187902 (2004), DOI 10.1103/PhysRevLett.92.187902: engineered nearest-neighbour coherent-transfer chains are prior art.

No new theorem asserted by Astra or openai/math is used as a premise. Their task-first entry / README and a selective analytic-continuation search were read. A missing search result would not establish priority.
