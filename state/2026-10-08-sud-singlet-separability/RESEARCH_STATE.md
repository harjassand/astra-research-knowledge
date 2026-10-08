# SU(d) invariant singlet marginal separability threshold — research candidate

Date: 2026-10-08 (Brisbane). Astra evidence base pinned to `b5824d0fcbfe0688980788da2722270a2f068fb0`; this draft branch starts from `95fc24535e1fa37c882c34f4f65882879fb18df7`. **Single-agent proof candidate, finite independently coded diagnostics, no independent specialist review or exhaustive priority check. DO NOT market as a certified breakthrough.**

## Precise theorem

Fix d>=2 and N divisible by d. Let P_N be the projector onto the global SU(d)-invariant subspace of (C^d)^{tensor N}, and let Omega_N=P_N/Tr(P_N). Write Omega_(N,k)=Tr_(N-k)(Omega_N) and SEP_k for fully separable k-qudit states. For k=k_N increasing to infinity with k/N->alpha,

1. If alpha<=1/(d+1), inf_(sigma in SEP_k) 1/2||Omega_(N,k)-sigma||_1 -> 0.
2. If alpha>1/(d+1), liminf of this distance is bounded below by
   Delta_d(alpha)=sup_(t>0){[1+2t(1-alpha)/d]^(-(d²-1)/2) - (1+t)^(-(d-1))}>0.
   At alpha=1 the distance tends to 1.
3. Omega_N is exactly d-producible: average uniformly over permutations of the tensor product of N/d antisymmetric d-qudit determinant singlets. This is a distance-to-FULL-separability result, NOT a claim about large entanglement depth.

Exact thresholds for d=2,3,4 are 1/3,1/4,1/5. All statements concern the ASYMPTOTIC ratio and a maximally-mixed SU(d)-invariant projector, not arbitrary singlet states or exact finite-N separability.

## Exact representation-theoretic formulas

Schur-Weyl: (C^d)^tensor k = direct sum_(lambda partitions k, len<=d) V_lambda tensor S_lambda. Put r=N/d. For a partition lambda padded to d entries with lambda_1<=r let mu_i=r-lambda_(d+1-i). Then the exact Young-diagram probability of the k-qudit marginal is

    p_(N,k)(lambda)= f^lambda f^mu / f^(r^d),

where f^lambda=k! Prod_(i<j)(lambda_i-lambda_j+j-i)/Prod_i(lambda_i+d-i)!. It vanishes if lambda_1>r. In the orthonormal traceless Hermitian generator normalization tr(T_a T_b)=delta_ab, m=d²-1, C_k=sum_a(sum_(i<=k)T_a^(i))², the SU(d) Casimir eigenvalue on lambda is

    c_lambda = sum_i(lambda_i-k/d)^2 + sum_i(d+1-2i)lambda_i.

The second sum equals sum_(i<j)(lambda_i-lambda_j)>=0. Total-singlet and permutation invariance give the exact Casimir expectation

    Tr Omega_(N,k) C_k = (m/d)*k*(N-k)/(N-1).

## Separable upper construction from a finite projective 2-design

For each fixed d, Caratheodory gives a finite positive weighted projective 2-design {(w_s,P_s)} satisfying Sum_s w_s P_s=I/d and Sum_s w_s(tr P_s H)^2=tr(H²)/[d(d+1)] for every traceless Hermitian H.

Set v=min(1,sqrt[(d+1)k/N]). Make a product of n_s=floor(k*w_s) local states rho_s=(1-v)I/d+v P_s, and O_d(1) maximally mixed remainder sites; call it tau_k. Twirl over collective SU(d) and S_k permutations to obtain a fully separable sigma_(N,k). Both sigma and Omega commute with SU(d) and S_k, hence are scalar on each Schur-Weyl sector; their trace norm difference equals total variation of the respective partition weights.

Their central class-character transforms F(g)=Tr rho g^tensor k satisfy the **same** local Gaussian limit for H traceless Hermitian and k/N->alpha<=1/(d+1):

    F_tar(exp(iH/sqrt(k))) -> exp[-(1-alpha)tr(H²)/(2d)],
    F_sep(exp(iH/sqrt(k))) -> exp[-(1-alpha)tr(H²)/(2d)].

For target, use the exact group-integral ratio

    F_tar(g)=Integral_G [tr(g u)]^k [tr u]^(N-k) du
                 / Integral_G [tr u]^N du.

Denominator equals the positive rectangular tableau dimension f^(r^d)=Theta_d(d^N N^(-(d²-1)/2)). The integral is dominated by u near the d center elements; write u=z exp(iX/sqrt N), note z^N=1, and expand numerator logarithms. The exponent is -[tr H²+2sqrt(k/N)tr(HX)+tr X²]/(2d). Completing the Gaussian square proves the target local limit, uniformly on compact H. The product local limit follows from the exact 2-design first/second cumulants; it remains valid at v->1.

Both transforms obey **global** Gaussian group-center envelopes. With Z the SU(d) center and delta(g)=dist(g,Z), the fundamental inequality |tr g|/d<=exp[-c delta(g)^2] follows by compactness and negative Hessian at center. For k<=N/2, delta(g)<=delta(gu)+delta(u) implies

    k delta(gu)^2+(N-k)delta(u)^2
       >=(k/4)delta(g)^2+((N-k)/2)delta(u)^2.

Using the normalization asymptotics gives |F_tar(g)|<=C exp[-c' k delta(g)^2]. For the product, the 2-design moment identity for all unitary g,

    Sum_s w_s |tr rho_s g|²
     = |tr g/d|²+[v²/(d+1)]*(1-|tr g/d|²),

and n_s>=k w_s/2 for k large imply |F_sep(g)|<=C exp[-c'' k delta(g)^2]. At each central element z, F(zg)=z^k F(g). Gaussian rescaling of Haar measure therefore yields

    k^((d²-1)/2) ||F_tar-F_sep||²_(L²(SU(d))) -> 0.

Here is the **local-to-trace-norm interface**: irreducible character orthogonality gives ||F_tar-F_sep||²_2=Sum_lambda |p_lambda-q_lambda|²/(dim V_lambda)². For c_lambda<=R² k, Weyl dimension formula bounds Sum_(typ) (dim V_lambda)²=O_(d,R)(k^((d²-1)/2)). Hence Cauchy-Schwarz makes the sum of |p-q| on typical partitions o(1). The tails are O_d(R^-2) by the exact O(k) Casimir moments of both states. Send k->infty then R->infty. This proves trace-distance→0, not merely weak collective-observable convergence.

## Lower bound: bounded heat-kernel/Casimir witness

For any t>0 set A_(k,t)=exp[-t C_k/k], 0<=A<=I. The standard SU(d) heat kernel p_{t/k} has representation Fourier transform e^{-t c_lambda/k} and small-time Lie-algebra limit H~N(0,2t I_m) under g=exp(iH/sqrt k). Consequently, from the target Gaussian characteristic limit,

    Tr Omega_(N,k) A_(k,t) -> [1+2t(1-alpha)/d]^(-m/2).

For an arbitrary k-dependent pure product tau_k=Tensor_i |psi_i><psi_i|, put r_i,a=tr(P_i T_a), b=k^-1/2 Sum_i r_i, and Sigma=k^-1 Sum_i Gamma_i, with Gamma_i,ab=1/2 tr P_i{T_a,T_b}-r_i,a r_i,b. Taylor expansion of the product characteristic function near identity is UNIFORM over all product arrays, including unbounded b (its phase has unit modulus):

    Tr tau exp(iH·X/sqrt k)
       =exp[i b·H-(1/2)H^T Sigma H+O_(d,R)(k^-1/2)]

for ||H||<=R. Integrating against the small-time heat kernel gives, uniformly over all product arrays,

    Tr tau A_(k,t)
       =det(I+2t Sigma)^(-1/2)
         *exp[-t b^T(I+2t Sigma)^(-1)b]+o_d(1).

For any pure single qudit, Gamma_i has exactly 2(d-1) eigenvalues 1/2 and (d-1)^2 zeros: rotate |psi_i> to |1> and inspect matrix generators coupling |1> to |j>. Since logdet(I+2t M) is concave on positive matrices,

    logdet(I+2t Sigma)
      >= (1/k)Sum_i logdet(I+2t Gamma_i)
      = 2(d-1)log(1+t).

Therefore sup_(sigma in SEP_k)Tr sigma A_(k,t) <=(1+t)^(-(d-1))+o(1). Variational trace distance and optimizing t yield Delta_d(alpha). The derivative at zero is [(d²-1)/d]*(alpha-1/(d+1)); positive for every alpha above the stated threshold. Taking alpha=1 and t->infty gives distance→1.

**Heat kernel convention:** the SU(d) Laplacian is Sum_a L_(iT_a)^2 (not half this); representation eigenvalue is -c_lambda, and tangent heat Gaussian covariance is 2t I. For d=2, C_k=2J_k² and the formula matches the independently derived qubit one-third result after rescaling t.

## d-producibility and adversarial boundaries

Take N/d disjoint d-qudit fully antisymmetric determinant singlets and uniformly permute their sites. The invariant SU(d) sector is the irreducible rectangular S_N module, so Schur's lemma makes this average equal the normalized invariant projector Omega_N. Thus Omega_N is d-producible EXACTLY.

Potential failure modes checked: (i) matching low moments alone cannot prove trace norm: the L² character estimate and Schur scalarity are essential; (ii) a non-bounded Casimir witness cannot imply a constant trace distance because of rare tails: e^(-t C/k) fixes this; (iii) SU(d) invariance ALONE is insufficient for equality of Young-label TV and full trace norm: also require S_k permutation invariance; (iv) this is fixed-d, not uniform d growing with N; (v) a finite k/N above threshold can still have exactly separable marginals (qubit N=10,k=4 counterexample in previous checkpoint). No large entanglement-depth or experimental noise-robustness claim.

## Finite tests, status and historical comparison

Reconstructed and executed: 810 exact rational SU(d) rectangle-complement branching/Casimir identities for d=2..5; direct full 3^6-dimensional six-qutrit projector computation reproducing k=3 SU(3) Casimir distribution {c=0:1/5,c=6:4/5}; pure covariance spectrum for d=2..5; random-array logdet bounds; explicit twelve-state qutrit projective 2-design with moment residual 1.4e-16 and local-character convergence to exp(-.125). Optimized lower bound at alpha=.4: Delta_2≈.010951655, Delta_3≈.043808425, Delta_4≈.069419719, Delta_5≈.087931009. All tests are INTERNAL finite checks, not external validation.

Prior relevant established works: Vitagliano, Gühne & Tóth, Quantum 9,1844 (2025), arXiv:2406.13338, on su(d) squeezing, Werner-singlet two-body marginals and a **white-noise** tolerance with factor 1/(d+1); that white-noise parameter is NOT this k/N sampling fraction. Mathé et al., Quantum 10,2078 (2026), arXiv:2504.07814, on separable approximations of spin-squeezed states. The precise extensive-marginal trace-distance transition was not found in a TARGETED literature scan, but priority is UNKNOWN; no field-breaking comparison has been certified.

**Highest-value continuation:** independent specialist check of saddle/center and heat-kernel normalizations; comprehensive prior-theorem search; exact asymptotic distance above threshold rather than lower bound; finite-N computable error rates; physical preparation/readout cost; formal mechanization; general compact-group representation extension. No external review, experiments, or formal proof checker have occurred.