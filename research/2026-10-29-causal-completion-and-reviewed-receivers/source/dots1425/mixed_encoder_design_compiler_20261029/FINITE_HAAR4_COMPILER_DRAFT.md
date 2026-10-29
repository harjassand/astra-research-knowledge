# Explicit finite Haar-two-qubit sampling and a uniform design compiler
2026-10-29. Author mathematical construction, not independently accepted or a practical implementation. This resolves a finite-controller existence obligation; it is not a new unitary-design theorem.

## Finite local sampler
For rational0<nu<=1/2, set R=16/nu, a=nu/16. Choose K=ceil(2R/h0) with h0=min(nu*a/64,nu/(8192R)), and h=2R/K. Use the K midpoint coordinates c_j=-R+(j+1/2)h.

Let N be a power of two at least max(1,R²). Choose an O(log(N/nu)) integer q such that3*2^(-q)<=nu/(8192N). For every midpoint, x=c_j²/N lies in[0,1]. An odd-degree alternating Taylor lower sum T_q(x) for exp(-x) is positive and differs relatively from exp(-x) by at most3/(q+1)!<=3*2^(-q). If necessary increase q by one to make it odd. Define the rational weight w_j=T_q(c_j²/N)^N. It obeys
 (1-nu/8192) exp(-c_j²)<=w_j<=exp(-c_j²).
All weights have a common explicitly computable integer denominator, since every c_j has a common denominator and q,N are common. Sample their integer numerators exactly using bounded uniform-integer rejection. Use at least ceil(log2(4096/nu)) attempts for each draw; on any cap failure return the identity gate. Draw32 independent real coordinates, assemble a4×4 complex matrix G_grid, and output its unitary polar factor. For singular matrices choose a unitary polar completion, or identity (the singular event is charged below). Known-control synthesis of this fixed-size algebraic unitary has a separately allocated operator error at mostnu/4.

This is a fully finite algorithm, not a real-valued Gaussian oracle. K=poly(1/nu); the Taylor degree is O(log(1/nu)); N=O(1/nu²); all integer numerator bit lengths are polynomial in1/nu. There are only K weights, reused for all32 draws, not K^32 weights. Fixed4×4 rational-matrix singularity, algebraic polar factors and Givens gate synthesis can be evaluated with certified polynomial bit cost in their input bit length and requested precision, by fixed-degree polynomial root isolation; no unbounded numerical stopping rule is intended. A straightforward exhaustive implementation is extraordinarily expensive. The full sampler has NOT been executed here.

## Coupling proof
Let G have independent circular complex Gaussian entries with density pi^-1 exp(-|z|²). Its unitary polar factor is exactly Haar U(4), by left/right unitary invariance. E||G||F²=16. Thus the chance G leaves the real-coordinate cube[-R,R]^32 is at most16/R².

If sigma_min(G)<=a, take a unit singular vector and one coordinate of magnitude at least1/2. The corresponding column has distance at most2a to the span of the other three columns. Conditional on those columns, its orthogonal one-complex-dimensional Gaussian residual has probability at most(2a)² of this event. Union over four columns gives probability at most16a². The sum16/R²+16a²<=nu²/8.

Condition on G lying in the cube. Its coordinates remain independent truncated one-dimensional Gaussians. For a coordinate x and its midpoint c, |x²-c²|<=Rh+h²/4. Therefore exact cell-integral weights and midpoint-density weights differ by a multiplicative factor exp(±(Rh+h²/4)); their normalized distributions differ in total variation by O(Rh). With h<=nu/(8192R), the32-coordinate coupling failure is less thannu/64. The Taylor-weight replacement contributes less thannu/128, and all32 bounded samplers together contribute at mostnu/128. These bounds are deliberately loose.

On the coupled good event, ||G_grid-G||F<=sqrt(32)h/2<3h. If G=QH, sigma_min(G)>=a, Procrustes optimality gives
 ReTr(Q†G)-ReTr(U†G)>=a||U-Q||F²/2
for every unitary U. Applying optimality of the polar factor Q' of G+E yields
 ||Q'-Q||F<=2||E||F/a.
Thus polar rounding error is at most6h/a<nu/4. Including known synthesis, the sampled implemented unitary is withinnu/2 in operator norm of Haar except on an event of probability less thannu/4. Consequently its t-copy conjugation channel differs from the Haar t-copy local gate average in diamond norm by at most4t*nu (conservatively), for every positive integer t. Discrete and continuous measures are NOT asserted close in total variation as measures on unitaries; only this coupling/channel statement is used.

## Explicit common-design circuit
Primary source: Brandao–Harrow–Horodecki, arXiv1208.0692v4, Corollary6 and Lemma3, https://arxiv.org/pdf/1208.0692v4 . Corollary6 supplies an explicit local-random-circuit length for Haar two-qubit gates; Lemma3 converts its approximate-design criterion into diamond twirl error. No unspecified algebraic-gate-set spectral-gap constant is used.

Take q_system>=2 qubits, t copies, and target diamond error0<epsilon<1. Let ell=ceil(log2(4t)), b=ceil(log2(8/epsilon)), computed by integer comparisons. A safe public length is
 L=170000*q_system*ell²*t^10*(2*q_system*t+b).
It upper-bounds Corollary6 at design error epsilon/8 (local dimension2), hence ideal common twirl diamond error<=epsilon/4. At every local gate, use the finite sampler above with nu<=epsilon/(64Lt). The SAME sampled gate acts on all t copies. Hybridization adds at most4Lt nu<=epsilon/16. Uniformly choosing the neighboring gate location uses exact integer rejection with a public cap giving total location-abort probability<=epsilon/16; identity fallback is charged as at mostepsilon/8 diamond error. The unused slack covers declared Schur and known-control synthesis errors. Independent random gates on different copies would be wrong.

## Compression application and scope
Following multiplicity extraction, prepare ONE known highest-weight vector in the small U(d)_lambda irrep, inverse small-d Schur, then apply the common design circuit. Haar twirling makes the irrep maximally mixed while preserving multiplicity, including arbitrary reference correlations. Replacing Haar by the certified design changes that entire channel by the declared error. This avoids enumerating all GT patterns to prepare a uniform irrep state.

Pad the target small dimension to a power of two at least4 and at least the supplied support bound, with factor at most4. If physical output D is too small for this isometric padding, D is itself O(d) and the direct small-dimensional branch applies. All quantum and classical costs are polynomial in t,d,1/epsilon,logD using the existing corrected Schur compiler, but constants/exponents are enormous. This is a theoretical finite construction, not polylog(1/epsilon) classical time, not an executed full sampler, not a hardware clock claim, and not practical superiority. Original fixed-d GT enumeration remains a separately valid fallback.
