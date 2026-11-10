ROOT WRIGHT-FISHER OBSERVATION COMPILER: SHORT-TIME BOUND AND A PAID FINITE-POPULATION INTERFACE
10 November 2026 Brisbane. These are mathematical preparation and scoped constructions. No full transient compiler, uniform-time approximation, historical novelty, physical realization or source-only reuse result is asserted.

MODEL. K>=2; alpha_i>0, alpha0=sum alpha_i; shifted genic selection 0<=sigma_i<=S; x0 is any simplex point, including a boundary point. The WF generator is
 Lf=1/2 sum_(i,j) x_i(delta_ij-x_j) partial_ij f
     +1/2 sum_i[alpha_i-alpha0*x_i+x_i(sigma_i-sigma.dot x)] partial_i f.
The requested discrete target at t>=0 is ONE X_t from this diffusion, followed by an ENTIRE ordered r-row of conditionally independent Cat(X_t) labels. Different labels share the same latent frequency. This is not an independent latent draw per position or a continuous-point TV target.

1. A UNIFORM SHORT-TIME OBSERVATION CERTIFICATE.
Write X_t-x0=int_0^t b(X_s)ds+M_t. The drift has
 ||b(x)||1<=alpha0+S,
and the martingale covariance has trace 1-sum_i x_i^2<=1. Thus
 E||X_t-x0||1 <=(alpha0+S)t+sqrt(Kt).                 (1)
Indeed the expected norm of the drift integral is bounded by the first term, and Cauchy-Schwarz plus the martingale isometry gives E||M_t||1<=sqrt(K)*sqrt(E||M_t||2^2)<=sqrt(Kt). Bounded coefficients justify the isometry; no interior-distance assumption is used.
Maximally couple each categorical pair conditionally on X_t,x0 and independently across positions. The two entire row laws have their required marginals and differ with probability at most
 (r/2)E||X_t-x0||1.
Consequently
 TV(observation_at_t, Cat(x0)^r)
 <=(r/2)[(alpha0+S)t+sqrt(Kt)].                      (2)
For r>=1 and rational epsilon>0, set
 theta=min{1,epsilon/[2r*max(1,alpha0+S)],
                 epsilon^2/(4Kr^2)}.
If t<=theta, r ordinary exact rational categorical draws from x0 give whole-row TV<=epsilon/2. This is computably checkable using rational arithmetic and costs polynomial expected bits in complete input length,K,r; NO numerical t^-1 is paid. For r=0 return the empty row exactly. At t=0 the categorical row is exact. The same proof works at all boundary points; it does not invoke a Gaussian or discard a rounding-boundary event. The earlier deterministic-grid counterexample concerns a DIFFERENT observation kernel and is not contradicted.

2. AN EXPLICIT RATIONAL MORAN-TYPE GRID GENERATOR.
For any integer N>=1, use states n in N^K, |n|=N, x=n/N. For i!=j take n->n-e_i+e_j at ordinary rational rate
 q_ij(n)=1/2[n_i*n_j+alpha_j*n_i
                   +(n_i*n_j/N)*(sigma_j-sigma_i)_+]. (3)
An empty source coordinate gives rate0, so the simplex lattice is preserved. Both mutation and selection drift are exact:
 sum q_ij*(e_j-e_i)/N
 =1/2[alpha-alpha0*x+x*(sigma-sigma.dot x)].
For selection, the identity (a-b)_+-(b-a)_+=a-b supplies each coordinate. Neutral pair rates have cancelling first order and second order exactly
 1/2 sum_(i,j) x_i(delta_ij-x_j) partial_ij f.
For a C^3 function extended to a neighbourhood of the simplex, Taylor expansion along e_j-e_i gives, with an absolute constant C and Euclidean derivative operator norms,
 ||L_N f-L f||_(grid)
 <=C/N*[||D^3 f||infty+(alpha0+S)||D^2 f||infty
                    +(alpha0+S)||D^3 f||infty/N].   (4)
All segments lie in the simplex. The sum of neutral rates is<=N^2/2; the mutation and selection rate sums are<=N(alpha0+S)/2. Those sums, jump length<=sqrt(2)/N and Taylor's remainder prove (4) directly. One may weaken its right side to C(1+alpha0+S)(||D^2f||+||D^3f||)/N.
A known rational uniformisation rate such as
 Lambda=N^2+N(alpha0+S)+1
dominates the actual total. At each tick sample one rational jump or a self-loop by finite integer arithmetic. The expected number of ticks up to t is Lambda*t; known-rational Poisson selection can be realised with charged fair bits or certified finite truncation. This is a paid finite process, NOT a population-independent oracle or an identity with the target diffusion. No state-space table of size N^(K-1) is required for trajectory simulation.

3. THE RELEVANT TEST FUNCTIONS AVOID AN EXPONENTIAL OUTPUT ENUMERATION.
For ANY g:[K]^r->[-1,1], let G_g(x)=E[g(Z_1,...,Z_r)] for IID Cat(x) labels. It is a degree-r polynomial. For tangent increments h_1,...,h_l with coordinate sums0,
 |D^lG_g(x)[h_1,...,h_l]|
 <=(r)_l product_j||h_j||1, l<=r.                  (5)
Expand the derivative by replacing l distinct categorical factors by the signed measures h_j. Each of the (r)_l terms is bounded by the product of their total variations. This is uniform over ALL bounded row tests g and independent of the K^r number of rows. In particular derivative budgets for the observation kernel itself are polynomial in r and K for fixed derivative order. This does NOT automatically bound derivatives of P_s G_g uniformly in time and parameters. That intervening semigroup operation, or a suitable direct coupling, must be constructed before (4) becomes a polynomial whole-row TV approximation theorem.

4. EXACT EXISTING STATIONARY CAPITAL.
At positive alpha the known stationary frequency law is proportional to exp(sigma.dot x)Dir_alpha(dx). Existing N1795 already supplies a full rational finite-observation compiler by a positive total-degree truncation O(S+log epsilon^-1), integer prefix convolution/backtracking and an exact rational Polya urn. Its polynomial expected bit cost pays numeric S, K,r and complete input bits, with no continuous gamma/Dirichlet sample primitive. This is not a transient mixing certificate. An independently proved all-parameter mixing time plus the stationary compiler would permit a long-time branch, but no such bound is assumed here. Finite-time evolution, polynomial parameter dependence and the uniform time cutover remain open.

5. GOVERNING PRIMARY CONTRACTS AND LIMITS ACTUALLY READ.
Sant-Jenkins-Ruggiero arXiv2611.08623v1 (sole current version checked):
 https://arxiv.org/pdf/2611.08623v1
Section2.1 gives the model; Definition3.1 supplies explicit linear-birth/quadratic-death dual rates, Proposition3.6 its entrance law and Theorem4.1 its standard Dirichlet-mixture transition. Section4.2/Algorithm1 uses large finite initialisation or a small-time Gaussian approximation. That is not a supplied finite-bit, whole-row-TV, parameter-uniform cost theorem. The representation is existing mathematics, not ROOT's discovery.
Sant-Jenkins-Koskela-Spano arXiv2301.05459v1 (sole current arXiv version checked):
 https://arxiv.org/pdf/2301.05459v1
Its model/Section2 is TWO alleles, with exact diffusion/bridge constructions at that scope. The supplement Section6 uses a small-time Gaussian cutoff0.08 and an additional bridge approximation threshold0.008. These implementation approximations are not a uniform all-parameter finite-bit TV/cost certificate. Exact theoretical real-arithmetic simulation is not rejected or silently renamed approximate.
Earlier Jenkins-Spano1506.06998v4 neutral real-arithmetic retrospective methods retain their true scope; no new read of an unavailable original is asserted. The displayed (1)-(5) are ROOT's direct derivations from the specified generator and categorical kernel, not borrowed additional source theorems.

PORTABLE ASTRA BINDING. N1795 at main7d5a2683d668ee710d2ddd8f6e9ba121f8e0dc9a, unit U1795-complete-tilted-dirichlet-stationary-observation-finite-bit-compiler/v0001.json, whole governing
 research/returns/2026-11-10-root-tilted-dirichlet-observation-compiler/ROOT_TILTED_DIRICHLET_FINITE_OBSERVATION_COMPILER_20261110_PUBLIC_PATHS.md
SHA25633b72b15f1823245ae15472085ab10647e43da25d977b391baa4596e09a5056f. The full governing proof was fetched/read, not only a card or abstract. Earlier ROOT_DIRICHLET_FIBRE_COUPLING_AND_OBSERVATION_CONTRACT_20261110.txt7670/SHA c1dac0b17638bd6f97c5ec1318486319137330e78191ec863fde5940f885b639 supplies finite-observation smoothing and the separate grid counterexample. Existing P3 nominal/robust conditional-Poisson kinetics is not imported as a theorem about this different invariant family or a free physical simulator. No source-only unknown-law access from the former P1 question is assumed.
All known/unknown source/access/transfer/resource holds remain. No denied-source recovery, new worker/model/resource, software install, physical experiment, native retrieval probe or model-performance conclusion is part of this construction.
