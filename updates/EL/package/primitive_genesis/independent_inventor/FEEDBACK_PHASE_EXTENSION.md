# Feedback, reused factors, and a cubic-root response operation

Internal construction and proof, 2026-10-12. Historical novelty **UNKNOWN**. This is a changed mathematical route after Boolean support cancellation blocked generic feedback. It provides a nontrivial response operation, not a universal stationary sampler.

## 1. The local scientific model and its acquired observable algebra

Let P be any stochastic matrix on a finite directed network V. The network can have arbitrary feedback and arbitrarily slow mixing; the algorithm has a local row sampler for P and coordinate access to an input vector x with |x_v|<=1. The probabilistic model initially takes |x_v|=1. There is one circular phase y=exp(i theta), where theta evolves by Brownian motion on the circle with generator gamma*d^2/dtheta^2, gamma>0. At rate one, each active phase x_v independently chooses w~P(v,.) and is replaced by

    x_v <- y x_w.

This is a compact-state Feller jump-diffusion. Multiplication is nonlinear in the joint state. The same single phase can be reused on every edge and every feedback cycle. No large moment closure is supplied or acquired.

For phi_vk=x_v y^k, k>=0, direct local generator calculation gives

    L phi_vk = -(1+gamma k^2) phi_vk + sum_w P_vw phi_w,k+1.      (1.1)

Brownian motion contributes -gamma k^2, the active refresh contributes -phi_vk, and the replacement contributes y^(k+1)x_w. Other active-site updates do not affect phi_vk. Positive Fourier charge strictly increases even when the same phase is reused; unlike Boolean parity, y^2 does not erase it.

Put d_k=1+gamma k^2 and

    w_n = product_{k=0}^n d_k^{-1}.

Then the explicit response operator is

    h_v(x,y) = sum_{n>=0} w_n y^n (P^n x)_v.                    (1.2)

Only one walk on P is needed to evaluate a random term. This is an exact symbolic interface acquired from (1.1), independent of the number of possible joint phase configurations.

## 2. Domain, stationary centering, and the time-integral meaning

The series in (1.2) converges uniformly: w_n has at least factorial tails for any fixed gamma>0. Its first two theta derivatives also converge uniformly because multiplication by n or n^2 does not defeat these tails. The active jump part is a bounded operator on continuous functions. Thus h belongs to the generator's domain; alternatively one can use closedness of the Feller generator and the partial-sum identity

    L h^(N)_v = -x_v+w_N y^(N+1)(P^(N+1)x)_v.

The remainder tends uniformly to zero. Therefore

    -L h_v = x_v.                                               (2.1)

Every stationary law has pi(x_v)=0. The same argument starting at each k proves pi(phi_vk)=0, hence pi(h_v)=0. This centering is proved by the local algebra and does not rely on unique ergodicity of the full phase process.

The absolute first-moment evolution is dominated by the positive dual on (v,k): it makes a P-step and increments k at rate one, and is killed at rate gamma k^2. This dual has no explosion because its birth rate is one. Duhamel iteration of (1.1), with the remainder bounded by a Poisson birth-count tail on every finite time interval, proves the domination. Its mean lifetime from k=0 is

    S_gamma = sum_{n>=0} w_n < infinity.

Consequently integral_0^infinity |E_(x,y)[x_v(t)]|dt <= S_gamma, and (2.1) is the actual integrated transient response

    h_v(x,y) = integral_0^infinity E_(x,y)[x_v(t)]dt.             (2.2)

It measures how long a coherent local phase persists while it is transported through an arbitrary directed feedback network under a slowly wandering common modulation. The Brownian phase itself has relaxation time 1/gamma, but this source response has a shorter, explicitly certified scale.

## 3. Cubic-root scale and exact rational evaluation

Assume 0<gamma<=1, and let L0 be the smallest positive integer with gamma L0^3>=1. (The name L0 here denotes a block length, not the generator.) Since

    product_{k=1}^{L0}(1+gamma k^2)
      >= 1+gamma sum_{k=1}^{L0}k^2 >= 4/3,

and later factors are larger, every block of L0 factors contracts by at least 3/4. Therefore

    w_n <= (3/4)^floor(n/L0),       S_gamma<=4 L0.               (3.1)

Sample a block M with Pr(M=m)=(1/8)(7/8)^m, independently sample J uniformly in {0,...,L0-1}, and set N=L0*M+J. Follow N steps of P from v, reaching W_N, and output

    Y = w_N y^N x_(W_N) / [ (1/(8 L0))(7/8)^M ].                (3.2)

Then E Y=h_v and, pointwise,

    |Y| <= 8 L0 (6/7)^M <= 8 L0,
    E |Y|^2 <=64 L0^2,
    E N = 7 L0+(L0-1)/2 < 8 L0.                                (3.3)

Thus local network work is O(gamma^(-1/3)) per sample, with second moment O(gamma^(-2/3)), independently of the mixing time of P and the network size. Absolute-error eta evaluation by averages and median of means costs O(L0^3 eta^(-2) log(1/delta)) P-steps using this simple independent-replicate construction. A dimension-free per-sample claim is not the same as a dimension-free relative-error answer for a response that is close to zero.

For rational gamma and P rows, and Gaussian-rational initial x_v,y (rational real and imaginary parts), the entire estimator is exact rational complex arithmetic. It never simulates Brownian motion or uses time discretization. The scalar product w_N has O(N(B+log N)) bits for B-bit gamma. Coordinate powers have O(NB) bits. The block-geometric N has all moments of order r bounded by O_r(L0^r), so standard exact arithmetic gives polynomial expected bit work in B and L0, in addition to the declared row-sampler and coordinate costs. General initial phases can be evaluated to controlled error; exact rational output is only claimed for the stated rational interface.

The scale is sharp even for P=[1] and x=y=1. Writing h=gamma^(1/3), for n=floor(t/h),

    log w_n = -sum_{k=1}^n log(1+h^3 k^2) -> -t^3/3.

The Taylor error is O(h) for t in a compact interval. The block bound (3.1) supplies an integrable exponential envelope for the Riemann sums. Hence

    gamma^(1/3) S_gamma
      -> integral_0^infinity exp(-t^3/3)dt
       = 3^(-2/3) Gamma(1/3).                                  (3.4)

The cubic-root exponent is closely related to familiar integrated-Brownian-phase dephasing and is **not claimed novel**. The exact network operator, rational estimator, and constants above are the scoped internal construction.

## 4. A local-query lower bound matching the per-sample scale

Set gamma=L0^(-3) for an integer L0>=4. Give an algorithm exact deterministic row queries on a line of states 0,...,L0 and a distinguished absorbing state star. Let x_star=1 and x_j=0 on all line states. In the base P, the line advances and ends at the zero-reward state L0. In alternative P_j, one unknown row j from {0,...,floor(L0/2)-1} instead jumps to star. The initial y is 1 and the requested response is at state 0.

The base response is zero. Every alternative response is sum_{n>=j+1} w_n, which is at least L0/(2e): for n<=L0,

    w_n >= exp(-gamma sum_{k=1}^n k^2) >= exp(-1).

Couple the base and a uniformly random alternative using the same internal randomness. Their transcripts are identical until a query of the changed row. If C is the expected base query count and J0=floor(L0/2), the probability D of such a hit is at most C/J0. If both base and all alternatives have output second moment at most M L0^2, Cauchy-Schwarz gives

    L0/(2e) <= 2 sqrt(M L0^2 Pr(D)),
    C >= J0/(16 e^2 M) = Omega(L0) for fixed M.                  (4.1)

This rules out a generic constant-work, constant-relative-second-moment evaluator under local P access. The O(L0)-work, O(L0^2)-second-moment estimator (3.2) matches this scaling. The lower bound is for this explicitly defined response functional; it is not a lower bound for every special P.

## 5. A natural dual estimator with worse variance

The killed pure-birth dual can also estimate the inverse by returning y^K x_(W_K)/(gamma K^2) when killed at charge K. Its expectation is (1.2). Its expected number of network steps is S_gamma=Theta(gamma^(-1/3)). However it is killed at K=1 with probability gamma/(1+gamma). At x=y=1, this event alone contributes

    E |Y_absorb|^2 >= 1/[gamma(1+gamma)].                        (5.1)

Thus its second moment is at least order gamma^(-1), worse than the O(gamma^(-2/3)) block estimator. The difference is a real variance issue caused by rare early killing. The comparison assumes equally informed scalar coefficients and row access for both methods. It does not establish a new historical Monte Carlo method.

## 6. The counterexample that prevents a false universal extension

Allow one edge to use the inverse phase. Take two active coordinates with updates

    x_0 <- y x_1,       x_1 <- y^(-1) x_0,

each at rate one, and the same Brownian y. Let phi_0=x_0 and phi_1=y x_1. Now

    L phi_0=-phi_0+phi_1,
    L phi_1=phi_0-(1+gamma)phi_1.

Positive charge is erased on the return edge. The exact response is

    h_0=[(1+gamma)phi_0+phi_1]/gamma,

whose value at x_0=x_1=y=1 is (2+gamma)/gamma. The cubic-root result fails: the full inverse-slow-rate scale returns in a two-coordinate feedback system. Real phase interactions commonly introduce conjugates; they cannot be included without a new argument.

## 7. Current scientific and originality gates

The operation is now proved for a nonlinear feedback family with arbitrary network feedback and a reused continuous phase; the observable closure is generated on demand, with one integer charge and one network vertex. It genuinely extends the fresh-Boolean-factor example.

The scope is nevertheless narrow. One-sided Fourier charge is a strong algebraic assumption. The model was constructed to expose that mechanism; no claim is made that generic real oscillator networks, interacting equilibrium systems, quantum channels, or arbitrary MCMC admit it. A consequential next gate is to handle conjugate returns using a verifiable nonzero cycle-charge condition, with complete occupation/variance costs. The exact two-cycle above shows why mere noise or local feedback is insufficient.

Prior art on stochastic duality, Monte Carlo inverse evaluation, stochastic phase response, and one-sided complex periodic potentials must be treated as collisions until a detailed theorem comparison establishes otherwise. Historical novelty remains UNKNOWN.
